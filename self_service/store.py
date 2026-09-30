"""Durable auth and the single phone lease. All ownership decisions are transactions."""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import secrets
import sqlite3
import time


class Conflict(Exception):
    pass


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.is_symlink() or self.path.parent.is_symlink():
            raise ValueError('Private state cannot use a symlink')
        if os.name=='posix':
            parent=self.path.parent.stat()
            if parent.st_uid!=os.getuid() or parent.st_mode & 0o077:
                raise ValueError('State directory must be owned and mode 0700')
            try:
                fd=os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                os.close(fd)
            except FileExistsError:
                stat=self.path.stat()
                if stat.st_uid!=os.getuid() or stat.st_mode & 0o077:
                    raise ValueError('State file must be owned and mode 0600')
        with self.tx() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    name TEXT PRIMARY KEY, password_hash TEXT NOT NULL,
                    admin INTEGER NOT NULL DEFAULT 0, enabled INTEGER NOT NULL DEFAULT 1);
                CREATE TABLE IF NOT EXISTS auth (
                    token_hash TEXT PRIMARY KEY, user TEXT NOT NULL,
                    csrf TEXT NOT NULL, expires REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS attempts (bucket TEXT, at REAL);
                CREATE INDEX IF NOT EXISTS attempts_bucket ON attempts(bucket,at);
                CREATE TABLE IF NOT EXISTS research (
                    id TEXT PRIMARY KEY, owner TEXT NOT NULL, auth_hash TEXT NOT NULL,
                    page TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'start',
                    phase TEXT NOT NULL DEFAULT 'queued', desired INTEGER NOT NULL DEFAULT 1,
                    lease INTEGER NOT NULL DEFAULT 1, started REAL NOT NULL, ended REAL,
                    browser_seen REAL NOT NULL, worker_seen REAL NOT NULL DEFAULT 0,
                    capture INTEGER NOT NULL DEFAULT 0, decoded INTEGER NOT NULL DEFAULT 0,
                    failed INTEGER NOT NULL DEFAULT 0, error TEXT NOT NULL DEFAULT '',
                    complete INTEGER NOT NULL DEFAULT 0, export_state TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0, retry_requested INTEGER NOT NULL DEFAULT 0,
                    control_generation INTEGER NOT NULL DEFAULT 0,
                    pending_page TEXT, ticket TEXT, control_revoked INTEGER NOT NULL DEFAULT 0);
                CREATE UNIQUE INDEX IF NOT EXISTS one_phone ON research(lease) WHERE lease=1;
                CREATE TABLE IF NOT EXISTS segments (
                    id TEXT PRIMARY KEY, research TEXT NOT NULL, ordinal INTEGER NOT NULL,
                    state TEXT NOT NULL, started REAL NOT NULL, ended REAL,
                    capture INTEGER NOT NULL DEFAULT 0, decoded INTEGER NOT NULL DEFAULT 0,
                    failed INTEGER NOT NULL DEFAULT 0, reason TEXT NOT NULL DEFAULT '',
                    UNIQUE(research,ordinal));
                CREATE TABLE IF NOT EXISTS events (
                    research TEXT NOT NULL, at REAL NOT NULL, kind TEXT NOT NULL,
                    detail TEXT NOT NULL);
            ''')

    @contextmanager
    def tx(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def event(self, db, sid, kind, detail=''):
        db.execute('INSERT INTO events VALUES (?,?,?,?)', (sid, time.time(), kind, detail))

    def get(self, sid):
        with self.tx() as db:
            row = db.execute('SELECT * FROM research WHERE id=?', (sid,)).fetchone()
            return dict(row) if row else None

    def active(self):
        with self.tx() as db:
            row = db.execute('SELECT * FROM research WHERE lease=1').fetchone()
            return dict(row) if row else None

    def start(self, user, auth, page):
        now = time.time()
        with self.tx() as db:
            old = db.execute('SELECT * FROM research WHERE lease=1').fetchone()
            if old:
                if old['owner'] == user and old['auth_hash'] == auth and old['page'] == page:
                    return old['id']  # double click / same request is idempotent
                raise Conflict('手机正在使用或收尾中。')
            sid = 'research-' + secrets.token_hex(12)
            db.execute('''INSERT INTO research
                (id,owner,auth_hash,page,started,browser_seen) VALUES (?,?,?,?,?,?)''',
                (sid, user, auth, page, now, now))
            self.event(db, sid, 'start-requested')
            return sid

    def control(self, sid, user, auth, page, action, reclaim_after=10):
        now = time.time()
        with self.tx() as db:
            row = db.execute('SELECT * FROM research WHERE id=? AND owner=?', (sid,user)).fetchone()
            if not row:
                raise Conflict('本次会话不可用。')
            same = row['auth_hash'] == auth and row['page'] == page
            if action == 'claim':
                if not row['lease'] or not row['desired']:
                    raise Conflict('本次采集已在收尾。')
                if not same and now - row['browser_seen'] <= reclaim_after:
                    raise Conflict('原页面仍在线；刷新后请稍候恢复。')
                if row['pending_page'] and row['pending_page'] != page:
                    raise Conflict('正在恢复另一个页面。')
                if not same:
                    db.execute('''UPDATE research SET pending_page=?,auth_hash=?,
                        browser_seen=?,ticket=NULL WHERE id=?''', (page,auth,now,sid))
                    self.event(db,sid,'control-reclaim-requested')
                return
            if not same or row['pending_page']:
                raise Conflict('此页面没有操作权；请在当前控制页面操作。')
            if action == 'stop':
                # desired off is committed before any external stop command.
                db.execute('''UPDATE research SET desired=0,ticket=NULL,
                    phase=CASE WHEN lease=1 THEN 'stopping' ELSE phase END,
                    state=CASE WHEN lease=1 THEN 'start' ELSE state END WHERE id=?''',(sid,))
                self.event(db,sid,'stop-requested')
            elif action == 'heartbeat':
                if row['lease'] and row['desired']:
                    db.execute('UPDATE research SET browser_seen=? WHERE id=?',(now,sid))
            elif action == 'retry':
                if not row['lease'] or not row['desired'] or row['state'] != 'error':
                    raise Conflict('当前状态不能重连采集。')
                if row['attempts'] >= 3:
                    raise Conflict('已达到恢复上限，请结束并联系维护者。')
                db.execute('UPDATE research SET retry_requested=1 WHERE id=?',(sid,))
            else:
                raise ValueError('unknown action')

    def update(self, sid, **fields):
        allowed = {'state','phase','desired','lease','worker_seen','capture','decoded','failed',
                   'error','complete','export_state','ended','attempts','retry_requested',
                   'control_generation','pending_page','page','ticket','control_revoked'}
        if not fields or not set(fields) <= allowed:
            raise ValueError('invalid state update')
        with self.tx() as db:
            db.execute('UPDATE research SET '+','.join(k+'=?' for k in fields)+' WHERE id=?',
                       (*fields.values(),sid))
