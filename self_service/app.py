"""Small HTTPS application; external resources are never selected by browser input."""
from functools import wraps
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import time
from urllib.parse import urlsplit

from flask import Flask, abort, g, jsonify, render_template, request, send_file, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash

from .store import Conflict, Store, digest

COOKIE = '__Host-huuuge'
PAGE = re.compile(r'[a-zA-Z0-9-]{32,64}')


def create_app(config):
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=8192, TRUSTED_HOSTS=[urlsplit(config['origin']).hostname])
    origin = config['origin'].rstrip('/')
    if not origin.startswith('https://'):
        raise ValueError('HTTPS origin required; tests use Flask test_client with https base_url')
    root = Path(config['data_root'])
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    store = Store(root / 'state.sqlite3')
    app.extensions.update(store=store, workbench_config=config)
    dummy = generate_password_hash(secrets.token_urlsafe(32))

    def body(allowed):
        data = request.get_json(silent=True)
        if not isinstance(data,dict) or set(data) - set(allowed):
            abort(400)
        return data

    def identity():
        if not hasattr(g,'identity'):
            token = request.cookies.get(COOKIE,'')
            with store.tx() as db:
                row = db.execute('''SELECT a.*,u.admin FROM auth a JOIN users u ON a.user=u.name
                    WHERE token_hash=? AND expires>? AND u.enabled=1''',
                    (digest(token),time.time())).fetchone()
            g.identity = dict(row) if row else None
        return g.identity

    def auth(fn):
        @wraps(fn)
        def wrapped(*args,**kwargs):
            who = identity()
            if not who:
                abort(401)
            if request.method != 'GET' and not hmac.compare_digest(
                    request.headers.get('X-CSRF-Token',''), who['csrf']):
                abort(403)
            return fn(*args,**kwargs)
        return wrapped

    def owned(sid, control=False):
        row = store.get(sid)
        who = identity()
        if not row or (row['owner'] != who['user'] and (control or not who['admin'])):
            abort(404)
        return row

    def page_id(data):
        page = data.get('page','')
        if not isinstance(page,str) or not PAGE.fullmatch(page): abort(400)
        return page

    def public(row):
        fields = ('id','started','ended','capture','decoded','failed','state','phase','error',
                  'complete','export_state','lease','worker_seen','control_generation')
        result = {k:row[k] for k in fields}
        if row['lease'] and time.time()-max(row['worker_seen'],row['started'])>10:
            result.update(state='error',error='采集状态中断，是否继续待确认。')
        result['downloadable'] = row['export_state']=='ready'
        return result

    @app.before_request
    def security():
        # Only the task proxy may reach the loopback listener. No forwarded host trust.
        if request.method not in ('GET','HEAD','OPTIONS'):
            if request.headers.get('Origin') != origin: abort(403)
        if request.query_string and not request.path.startswith('/vendor/'):
            abort(400)  # application auth/paths/commands never come from a query

    @app.after_request
    def headers(response):
        response.headers.update({
            'Cache-Control':'no-store','Referrer-Policy':'no-referrer',
            'X-Content-Type-Options':'nosniff','X-Frame-Options':'SAMEORIGIN',
            'Permissions-Policy':'camera=(), microphone=(), clipboard-read=(), clipboard-write=()',
            'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; frame-src 'self'; object-src 'none'; base-uri 'none'; "
                "form-action 'self'; frame-ancestors 'self'",
            'Strict-Transport-Security':'max-age=31536000'})
        # Vendor iframe needs vendor streaming endpoints, WASM and its inline bootstrap;
        # isolate it from the app with its own URL scope and upstream vendor policy.
        if request.path.startswith('/vendor/'):
            response.headers.pop('Content-Security-Policy',None)
        return response

    @app.errorhandler(Conflict)
    def conflict(error): return jsonify(error=str(error)),409

    for code in (400,401,403,404,413,429,500,503):
        app.register_error_handler(code,lambda error: (jsonify(error={
            401:'请先登录。',403:'请求未获授权，请刷新页面。',404:'结果不存在或不可访问。',
            429:'尝试过于频繁，请稍后再试。',503:'服务准备未完成，请联系维护者。'
        }.get(error.code,'请求失败，已有数据会保留。')),error.code))

    @app.get('/')
    def index(): return render_template('index.html')

    @app.post('/api/login')
    def login():
        data=body({'username','password','remember'})
        name=data.get('username',''); password=data.get('password','')
        if not isinstance(name,str) or not isinstance(password,str) or len(name)>64 or len(password)>256:
            abort(400)
        now=time.time()
        buckets=[digest('user:'+name),digest('ip:'+str(request.remote_addr))]
        with store.tx() as db:
            db.execute('DELETE FROM attempts WHERE at<?',(now-900,))
            for bucket in buckets:
                if db.execute('SELECT COUNT(*) FROM attempts WHERE bucket=? AND at>?',
                              (bucket,now-300)).fetchone()[0]>=10:
                    abort(429)
            db.executemany('INSERT INTO attempts VALUES (?,?)',[(b,now) for b in buckets])
            user=db.execute('SELECT * FROM users WHERE name=? AND enabled=1',(name,)).fetchone()
        okay=check_password_hash(user['password_hash'] if user else dummy,password)
        if not okay or not user: abort(401)
        token=secrets.token_urlsafe(32); csrf=secrets.token_urlsafe(32)
        ttl=604800 if data.get('remember') is True else 28800
        with store.tx() as db:
            db.execute('INSERT INTO auth VALUES (?,?,?,?)',(digest(token),name,csrf,now+ttl))
            db.execute('DELETE FROM auth WHERE expires<=?',(now,))
            db.executemany('DELETE FROM attempts WHERE bucket=? AND at=?',[(b,now) for b in buckets])
        response=jsonify(csrf=csrf)
        response.set_cookie(COOKIE,token,secure=True,httponly=True,samesite='Strict',
                            path='/',max_age=ttl if data.get('remember') is True else None)
        return response

    @app.get('/api/me')
    @auth
    def me(): return jsonify(csrf=identity()['csrf'],username=identity()['user'])

    @app.post('/api/logout')
    @auth
    def logout():
        with store.tx() as db:
            db.execute('DELETE FROM auth WHERE token_hash=?',(identity()['token_hash'],))
            db.execute('''UPDATE research SET desired=0,ticket=NULL,phase='stopping',state='start'
                WHERE auth_hash=? AND lease=1''',(identity()['token_hash'],))
        response=jsonify(ok=True); response.delete_cookie(COOKIE,secure=True,path='/')
        return response

    @app.get('/api/status')
    @auth
    def status():
        with store.tx() as db:
            rows=db.execute('SELECT * FROM research WHERE owner=? ORDER BY started DESC LIMIT 50',
                            (identity()['user'],)).fetchall()
        active=store.active()
        return jsonify(sessions=[public(dict(r)) for r in rows],busy=bool(active),
                       mine=bool(active and active['owner']==identity()['user']),
                       enabled=config.get('admission_enabled',False),server_time=time.time())

    @app.post('/api/start')
    @auth
    def start():
        page=page_id(body({'page'}))
        if not config.get('admission_enabled',False): abort(503)
        if shutil.disk_usage(root).free < config.get('min_free_bytes',5*1024**3):
            raise Conflict('存储空间不足，已有结果保留；请联系维护者。')
        sid=store.start(identity()['user'],identity()['token_hash'],page)
        return jsonify(id=sid),202

    @app.post('/api/session/<sid>/<action>')
    @auth
    def control(sid,action):
        if action not in {'stop','heartbeat','retry','claim','ticket','export'}: abort(404)
        data=body({'page'}); row=owned(sid,control=True)
        if action=='export':
            if not row['ended'] or row['export_state'] not in ('failed','ready'): abort(409)
            if row['export_state']=='failed': store.update(sid,export_state='pending')
            return jsonify(ok=True),202
        page=page_id(data)
        if action=='ticket':
            if (row['auth_hash']!=identity()['token_hash'] or row['page']!=page
                or row['pending_page'] or not row['desired'] or not row['lease']): abort(403)
            if not row['ticket']: return jsonify(pending=True),202
            return jsonify(json.loads(row['ticket']))
        store.control(sid,identity()['user'],identity()['token_hash'],page,action)
        return jsonify(ok=True),202

    @app.get('/api/download/<sid>')
    @auth
    def download(sid):
        row=owned(sid)
        if row['export_state']!='ready' or not row['ended']: abort(409)
        path=root/'exports'/(sid+'.zip')
        if path.is_symlink() or not path.is_file(): abort(404)
        return send_file(path,as_attachment=True,download_name='Huuuge_'+sid+'.zip',conditional=True)

    @app.get('/vendor/<path:name>')
    @auth
    def vendor(name):
        active=store.active()
        if not active or active['owner']!=identity()['user'] or not active['desired']: abort(403)
        return send_from_directory(config['vendor_root'],name)

    return app


if __name__=='__main__':
    from waitress import serve
    os.umask(0o077)
    configuration=json.loads(Path(os.environ['HUUUGE_WORKBENCH_CONFIG']).read_text())
    serve(create_app(configuration),host='127.0.0.1',port=configuration['listen_port'],threads=8,
          clear_untrusted_proxy_headers=True)
