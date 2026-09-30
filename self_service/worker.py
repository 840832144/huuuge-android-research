"""Single capture worker. Official Web phone sessions are outside its lifecycle."""
import json
import os
from pathlib import Path
import signal
import threading
import time

from scripts import cloud_capture as cloud
from .collector import Collector
from .export import build
from .store import Store
from .capture_runtime import CaptureRuntime
from .capacity import check as capacity_check


class Worker:
    def __init__(self,config,runtime,collector_factory=Collector):
        self.config=config;self.root=Path(config['data_root']);self.store=Store(self.root/'state.sqlite3')
        self.runtime=runtime;self.collector_factory=collector_factory
        self.collector=None;self.segment=None;self.research=None;self.retry_at=0

    def segments(self,sid):
        with self.store.tx() as db:
            return [dict(r) for r in db.execute('SELECT * FROM segments WHERE research=? ORDER BY ordinal',(sid,))]

    def totals(self,sid):
        rows=self.segments(sid)
        return {key:sum(r[key] for r in rows) for key in ('capture','decoded','failed')}

    def start_segment(self,row):
        ordinal=len(self.segments(row['id']))+1;segment=f'segment-{ordinal:03d}'
        with self.store.tx() as db:
            current=db.execute('SELECT desired FROM research WHERE id=?',(row['id'],)).fetchone()
            if not current['desired']: return
            db.execute('INSERT INTO segments(id,research,ordinal,state,started) VALUES (?,?,?,?,?)',
                       (row['id']+'-'+segment,row['id'],ordinal,'starting',time.time()))
            db.execute('UPDATE research SET attempts=attempts+1,retry_requested=0 WHERE id=?',(row['id'],))
            self.store.event(db,row['id'],'segment-started',segment)
        self.segment=row['id']+'-'+segment
        self.collector=self.collector_factory(self.root,self.config,self.runtime)
        self.store.update(row['id'],state='start',phase='starting',error='')
        self.collector.start(row['id'],self.segment)

    def finish_segment(self,row,reason=''):
        if not self.segment: return
        sealed=self.collector.stop(row['id'],self.segment,reason)
        with self.store.tx() as db:
            db.execute('''UPDATE segments SET state=?,ended=?,capture=?,decoded=?,failed=?,reason=?
                WHERE id=?''',(sealed['state'],time.time(),sealed['capture'],sealed['decoded'],
                               sealed['failed'],reason,self.segment))
            self.store.event(db,row['id'],'segment-sealed',reason)
        self.segment=None;self.collector=None
        self.store.update(row['id'],**self.totals(row['id']))

    def adopt(self,row):
        pending=[r for r in self.segments(row['id']) if r['ended'] is None]
        if len(pending)>1: raise RuntimeError('多个未收尾片段，保持占用并人工核验。')
        if pending:
            self.segment=pending[0]['id']
            self.collector=self.collector_factory(self.root,self.config,self.runtime)
            self.finish_segment(row,'worker-restart-gap')
            self.store.update(row['id'],state='error',phase='recovery',error='服务重启，中断片段已保留。')
            self.retry_at=time.time()+5
        self.research=row['id']

    def close(self,row):
        self.store.update(row['id'],state='start',phase='stopping',ticket=None)
        # Stop/flush before runtime cleanup; unknown cleanup retains the capture lease.
        self.finish_segment(row)
        rows=self.segments(row['id'])
        if any(r['ended'] is None for r in rows): raise RuntimeError('采集仍在停止，保持占用。')
        self.store.update(row['id'],ended=row['ended'] or time.time(),**self.totals(row['id']))
        if rows:
            self.runtime.cleanup_capture()
        complete=bool(rows) and all(r['state']=='finalized' and not r['reason'] for r in rows)
        self.store.update(row['id'],lease=0,complete=int(complete),
                          state='ended' if complete else 'error',phase='packaging',
                          error='' if complete else '已停止并保存；本轮有中断或启动失败，数据不完整。')
        self.research=None

    def tick(self):
        row=self.store.active()
        if row:
            self.store.update(row['id'],worker_seen=time.time())
            try:
                if self.research!=row['id']: self.adopt(row)
                row=self.store.get(row['id'])
                capacity=capacity_check(self.config,row)
                if capacity and row['desired']:
                    self.store.update(row['id'],desired=0,error=capacity)
                    with self.store.tx() as db: self.store.event(db,row['id'],'capacity-stop',capacity)
                    row=self.store.get(row['id'])
                if time.time()-row['browser_seen']>self.config.get('reconnect_grace_seconds',180):
                    self.store.update(row['id'],desired=0,ticket=None)
                    row=self.store.get(row['id'])
                if not row['desired']:
                    self.close(row)
                else:
                    if row['desired']:
                        if not self.collector and row['attempts']<3 and (time.time()>=self.retry_at or row['retry_requested']):
                            self.runtime.cleanup_capture()
                            self.runtime.preflight()
                            self.start_segment(row)
                        if self.collector:
                            value=self.collector.read()
                            with self.store.tx() as db:
                                db.execute('UPDATE segments SET capture=?,decoded=?,failed=? WHERE id=?',
                                           (value['capture'],value['decoded'],value['failed'],self.segment))
                            self.store.update(row['id'],**self.totals(row['id']))
                            if value.get('exited'):
                                self.finish_segment(row,'collector-exited-gap')
                                self.retry_at=time.time()+min(30,5*2**row['attempts'])
                                self.store.update(row['id'],state='error',phase='recovery',
                                                  error='采集已中断；旧片段保留，有限重连中。')
                            elif value['ready'] and value['capture']>0 and value['decoded']>0:
                                self.store.update(row['id'],state='collecting',phase='active',error='')
                            elif row['state']=='collecting':
                                self.store.update(row['id'],state='error',phase='recovery',
                                                  error='探针心跳中断，本段覆盖不完整。')
                                self.finish_segment(row,'probe-heartbeat-gap')
                                self.retry_at=time.time()+5
            except Exception as exc:
                # Exception class only. Low-level output can contain private identifiers.
                with self.store.tx() as db:
                    self.store.event(db,row['id'],'worker-error',type(exc).__name__)
                self.store.update(row['id'],state='error',error='采集条件或清理尚未确认；保留采集锁和已有数据，请结束或联系维护者。')
                self.retry_at=time.time()+30
        # Export does not hold the capture lease; official Web sessions are untouched.
        with self.store.tx() as db:
            pending=[dict(r) for r in db.execute("SELECT * FROM research WHERE ended IS NOT NULL AND desired=0 AND lease=0 AND export_state='pending'")]
        for item in pending:
            if any(r['ended'] is None for r in self.segments(item['id'])): continue
            try:
                if capacity_check(self.config,item,export=True): raise RuntimeError('export-capacity')
                build(self.root,item,self.segments(item['id']),self.config['export_metadata'])
                self.store.update(item['id'],export_state='ready',phase='saved' if not item['lease'] else item['phase'])
            except Exception:
                self.store.update(item['id'],export_state='failed')


def main():
    os.umask(0o077)
    config=json.loads(Path(os.environ['HUUUGE_WORKBENCH_CONFIG']).read_text())
    root=Path(config['data_root']);root.mkdir(mode=0o700,parents=True,exist_ok=True)
    stop=threading.Event()
    for sig in (signal.SIGTERM,signal.SIGINT): signal.signal(sig,lambda *_:stop.set())
    with cloud.lock(root,'.worker.lock'):
        worker=Worker(config,CaptureRuntime(config))
        while not stop.is_set():
            worker.tick();stop.wait(1)
        row=worker.store.active()
        if row:
            worker.store.update(row['id'],desired=0,ticket=None)
            worker.close(worker.store.get(row['id']))


if __name__=='__main__': main()
