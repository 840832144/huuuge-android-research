"""One immutable controller root per segment; never invoke retry-start for recovery."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from scripts import cloud_capture as cloud


class Collector:
    def __init__(self, root, config, runtime):
        self.root=Path(root)
        self.config=config
        self.runtime=runtime
        self.child=None
        self.log=None
        self.directory=None

    def start(self,sid,segment):
        self.directory=self.root/'research'/sid/segment
        self.directory.mkdir(parents=True,mode=0o700,exist_ok=False)
        config=self.runtime.prepare_capture(self.directory)
        # The provider must return a protected, target-verified cloud controller config.
        if not isinstance(config,dict): raise ValueError('protected capture config required')
        config['result_root']=str(self.directory)
        cloud.write(self.directory/'controller.json',config)
        cloud.load_config(self.directory/'controller.json')
        self.log=(self.directory/'controller.log').open('x',encoding='utf-8')
        self.child=subprocess.Popen([sys.executable,str(cloud.REPO/'scripts/cloud_capture.py'),
                    '--config',str(self.directory/'controller.json'),'run'],cwd=cloud.REPO,
                    stdout=self.log,stderr=subprocess.STDOUT,start_new_session=True)

    def read(self):
        if not self.directory: return dict(ready=False,capture=0,decoded=0,failed=0)
        active=self.directory/'active.json'
        if not active.exists(): active=self.directory/'last.json'
        if not active.exists(): return dict(ready=False,capture=0,decoded=0,failed=0)
        state,session=cloud.active_session(self.directory,active.name)
        path=session/'collector_state.json'
        value=cloud.read(path) if path.exists() else {}
        count=value.get('message_count',0); decoded=value.get('decoded_count',0)
        heartbeat=value.get('last_probe_heartbeat')
        fresh=False
        if heartbeat:
            parsed=datetime.fromisoformat(heartbeat)
            if parsed.tzinfo is None: parsed=parsed.replace(tzinfo=timezone.utc)
            fresh=0 <= time.time()-parsed.timestamp()<=10
        ready=(value.get('status')=='ready' and value.get('hooks_installed') is True
               and count>0 and decoded>0 and fresh and self.child and self.child.poll() is None)
        return dict(ready=bool(ready),capture=count,decoded=decoded,failed=count-decoded,
                    exited=self.child is not None and self.child.poll() is not None,
                    heartbeat_fresh=fresh)

    def stop(self,sid,segment,reason=''):
        directory=self.directory or self.root/'research'/sid/segment
        directory.mkdir(parents=True,mode=0o700,exist_ok=True)
        active=directory/'active.json'
        if active.exists():
            state,session=cloud.active_session(directory)
            (directory/(state['session_id']+'.stop')).touch(exist_ok=True)
        if self.child:
            try: self.child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                # No unsafe PID kill or seal while the collector may still be writing.
                raise RuntimeError('采集进程停止未确认，保留占用与已有数据。')
        # This is the controller's inherited lock, including after a supervisor restart.
        with cloud.lock(directory,'.run.lock'):
            ref=directory/'last.json'
            if not ref.exists(): ref=active
            if ref.exists():
                state,session=cloud.active_session(directory,ref.name)
                summary=cloud.summarize(session,state.get('exit_code'),reason or state.get('reason'))
                count=summary.get('capture_count')
                if count is None:
                    # Startup failed before the decoder made any files. Never invent data.
                    if session.exists(): raise RuntimeError('结果计数无法回读。')
                    count=0
                decoded=summary.get('decoded_count') or 0
                capturedir=session.name if session.exists() else None
            else:
                if list(directory.glob('cloud-*/messages.jsonl')):
                    raise RuntimeError('缺少采集控制记录，不能封存。')
                summary={'state':'incomplete'};count=decoded=0;capturedir=None
            sealed=dict(research_id=sid,segment_id=segment,state=summary['state'],capture=count,
                        decoded=decoded,failed=count-decoded,capture_directory=capturedir)
            path=directory/'sealed.json'
            if path.exists():
                if cloud.read(path)!=sealed: raise RuntimeError('封存结果不可覆盖。')
            else: cloud.write(path,sealed)
        if self.log: self.log.close();self.log=None
        self.child=None
        return sealed
