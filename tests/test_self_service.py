"""Synthetic component evidence only. No real users, phone, capture or cloud acceptance."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

from werkzeug.security import generate_password_hash
from self_service.app import create_app
from self_service.export import build
from self_service.store import Store, Conflict
from self_service.worker import Worker
from self_service.capture_runtime import CaptureRuntime

ORIGIN='https://workbench.example.test'
PAGE_A='a'*32
PAGE_B='b'*32


class Setup(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.config=dict(origin=ORIGIN,data_root=str(self.root),admission_enabled=True,
                         min_free_bytes=0,
                         reconnect_grace_seconds=180,export_metadata=dict(game_version='synthetic',
                         collector_revision='synthetic-test',schema_version='synthetic',timezone='UTC',evidence_kind='synthetic'))
        self.app=create_app(self.config);self.app.testing=True
        self.store=self.app.extensions['store']
        with self.store.tx() as db:
            for name in ('planner-a','planner-b'):
                db.execute('INSERT INTO users(name,password_hash) VALUES (?,?)',
                           (name,generate_password_hash('synthetic-only-password')))
        self.a,self.ca=self.login('planner-a');self.b,self.cb=self.login('planner-b')

    def login(self,user):
        client=self.app.test_client()
        response=client.post('/api/login',base_url=ORIGIN,headers={'Origin':ORIGIN},
                             json=dict(username=user,password='synthetic-only-password',remember=True))
        self.assertEqual(response.status_code,200)
        self.assertIn('Secure; HttpOnly',response.headers['Set-Cookie'])
        return client,response.json['csrf']

    def post(self,client,csrf,path,data=None):
        return client.post(path,json=data or {},base_url=ORIGIN,
                           headers={'Origin':ORIGIN,'X-CSRF-Token':csrf})

    def start(self):
        response=self.post(self.a,self.ca,'/api/start',{'page':PAGE_A})
        self.assertEqual(response.status_code,202);return response.json['id']


class AuthCaptureLockTests(Setup):
    def test_auth_csrf_origin_and_unknown_target(self):
        outsider=self.app.test_client()
        self.assertEqual(outsider.get('/api/status',base_url=ORIGIN).status_code,401)
        self.assertEqual(self.a.post('/api/start',base_url=ORIGIN,json={'page':PAGE_A}).status_code,403)
        self.assertEqual(self.post(self.a,'wrong','/api/start',{'page':PAGE_A}).status_code,403)
        self.assertEqual(self.post(self.a,self.ca,'/api/start',{'page':PAGE_A,'instance':'other'}).status_code,400)

    def test_double_click_two_users_and_tabs(self):
        sid=self.start()
        self.assertEqual(self.post(self.a,self.ca,'/api/start',{'page':PAGE_A}).json['id'],sid)
        self.assertEqual(self.post(self.a,self.ca,'/api/start',{'page':PAGE_B}).status_code,409)
        self.assertEqual(self.post(self.b,self.cb,'/api/start',{'page':PAGE_B}).status_code,409)
        self.assertEqual(self.post(self.b,self.cb,f'/api/session/{sid}/stop',{'page':PAGE_B}).status_code,404)
        self.assertEqual(self.b.get('/api/download/'+sid,base_url=ORIGIN).status_code,404)
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/ticket',{'page':PAGE_B}).status_code,404)

    def test_atomic_claim_race(self):
        def claim(n):
            try: return self.store.start(str(n),str(n),str(n))
            except Conflict:return None
        with ThreadPoolExecutor(8) as pool: rows=list(pool.map(claim,range(8)))
        self.assertEqual(sum(r is not None for r in rows),1)

    def test_refresh_reclaims_without_second_capture(self):
        sid=self.start()
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/claim',{'page':PAGE_B}).status_code,409)
        with self.store.tx() as db: db.execute('UPDATE research SET browser_seen=? WHERE id=?',(time.time()-15,sid))
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/claim',{'page':PAGE_B}).status_code,202)
        self.assertEqual(self.store.get(sid)['page'],PAGE_B)
        self.assertIsNone(self.store.get(sid)['pending_page'])
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/ticket',{'page':PAGE_A}).status_code,404)
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/stop',{'page':PAGE_A}).status_code,409)
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/heartbeat',{'page':PAGE_B}).status_code,202)
        with self.store.tx() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM research').fetchone()[0],1)

    def test_panel_has_no_embedded_phone_or_vendor_credentials_route(self):
        sid=self.start()
        page=self.a.get('/',base_url=ORIGIN)
        self.assertNotIn('<iframe',page.get_data(as_text=True))
        self.assertIn('不锁定手机',page.get_data(as_text=True))
        self.assertIn("frame-src 'none'",page.headers['Content-Security-Policy'])
        self.assertEqual(self.a.get('/vendor/WuyingWebSDK.js',base_url=ORIGIN).status_code,404)
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/ticket',{'page':PAGE_A}).status_code,404)

    def test_stop_is_idempotent_and_revokes_desired_state(self):
        sid=self.start();self.store.update(sid,ticket='{"secret":"synthetic"}')
        for _ in range(2):
            self.assertEqual(self.post(self.a,self.ca,f'/api/session/{sid}/stop',{'page':PAGE_A}).status_code,202)
        row=self.store.get(sid);self.assertFalse(row['desired']);self.assertIsNone(row['ticket'])
        self.assertTrue(row['lease'])

    def test_status_stale_cancels_green_and_hides_secrets(self):
        sid=self.start()
        with self.store.tx() as db: db.execute('UPDATE research SET started=? WHERE id=?',(time.time()-20,sid))
        self.store.update(sid,state='collecting',ticket='synthetic-secret',worker_seen=time.time()-15)
        response=self.a.get('/api/status',base_url=ORIGIN)
        self.assertEqual(response.json['sessions'][0]['state'],'error')
        self.assertNotIn('synthetic-secret',response.get_data(as_text=True))

    def test_login_rate_limit_revocation_and_expiry(self):
        client=self.app.test_client()
        for _ in range(11):
            response=client.post('/api/login',base_url=ORIGIN,headers={'Origin':ORIGIN},
                                 json={'username':'absent','password':'wrong'})
        self.assertEqual(response.status_code,429)
        self.post(self.a,self.ca,'/api/logout')
        self.assertEqual(self.a.get('/api/status',base_url=ORIGIN).status_code,401)
        with self.store.tx() as db: db.execute('UPDATE auth SET expires=0')
        self.assertEqual(self.b.get('/api/status',base_url=ORIGIN).status_code,401)

    def test_result_owner_and_immutable_repeat_download(self):
        sid=self.start();directory=self.root/'exports';directory.mkdir();(directory/(sid+'.zip')).write_bytes(b'synthetic-zip')
        self.store.update(sid,desired=0,lease=0,ended=time.time(),export_state='ready',state='ended')
        for _ in range(2):
            response=self.a.get('/api/download/'+sid,base_url=ORIGIN)
            self.assertEqual(response.data,b'synthetic-zip');response.close()
        self.assertEqual(self.b.get('/api/download/'+sid,base_url=ORIGIN).status_code,404)
        self.assertEqual(self.a.get('/api/download/../state.sqlite3',base_url=ORIGIN).status_code,404)


def sealed_fixture(root,sid,segment=None):
    segment=segment or sid+'-segment-001';directory=root/'research'/sid/segment
    capture='cloud-20260930T000000-0123456789ab'
    (directory/capture).mkdir(parents=True)
    common=dict(time='2026-09-30T00:00:00+00:00',service='SlotsGameServer',method='Spin',
                decoded=True,seq_number=17,payload_bytes=100,user_id='DO_NOT_EXPORT_ACCOUNT')
    rows=[dict(common,seq=1,rpc_type='REQUEST',direction='out',payload_type='Casino.SlotsProto.SpinRequest',
               data={'bet':'900719925474099312345','auto':False,'max_bet_btn':False,
                     'password':'DO_NOT_EXPORT_PASSWORD','future':{'free_text':'DO_NOT_EXPORT_TEXT'}}),
          dict(common,seq=2,rpc_type='RESPONSE',direction='in',payload_type='Casino.SlotsProto.SpinResponse',
               data={'stop':[1,2,3,4,5],'jackpot':False,'cash':{'value':'40000000000000001'},
                     'free_spins':{'spin_count':5},'balance':'DO_NOT_EXPORT_BALANCE'})]
    (directory/capture/'messages.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    (directory/'sealed.json').write_text(json.dumps(dict(research_id=sid,segment_id=segment,state='finalized',
                                capture=2,decoded=2,failed=0,capture_directory=capture)))
    return dict(id=segment,started=1,ended=2,reason='',state='finalized',capture=2,decoded=2,failed=0)


class ExportTests(Setup):
    def test_allowlist_counts_exact_integer_pair_and_retry(self):
        sid=self.start();segment=sealed_fixture(self.root,sid)
        self.store.update(sid,desired=0,lease=0,ended=2,capture=2,decoded=2,complete=1)
        path=build(self.root,self.store.get(sid),[segment],self.config['export_metadata'])
        first=path.read_bytes()
        with zipfile.ZipFile(path) as z:
            self.assertEqual(len(z.namelist()),8)
            self.assertFalse(any('raw' in name or '..' in name for name in z.namelist()))
            all_text='\n'.join(z.read(n).decode() for n in z.namelist())
            self.assertNotIn('DO_NOT_EXPORT',all_text)
            self.assertNotIn(str(self.root),all_text)
            data=[json.loads(s) for s in z.read('decoded/messages.jsonl').decode().splitlines()]
            self.assertEqual(data[0]['data']['bet'],'900719925474099312345')
            self.assertEqual(data[0]['pair_alias'],data[1]['pair_alias'])
            manifest=json.loads(z.read('manifest.json'))
            self.assertEqual((manifest['capture_count'],manifest['decoded_count']),(2,2))
            self.assertTrue(manifest['shared_game_account'])
        self.assertEqual(build(self.root,self.store.get(sid),[segment],self.config['export_metadata']).read_bytes(),first)

    def test_unfinished_or_inconsistent_result_cannot_publish(self):
        sid=self.start();segment=sealed_fixture(self.root,sid)
        with self.assertRaises(ValueError): build(self.root,self.store.get(sid),[segment],self.config['export_metadata'])
        self.store.update(sid,desired=0,lease=0,ended=2,capture=9,decoded=9)
        with self.assertRaises(ValueError): build(self.root,self.store.get(sid),[segment],self.config['export_metadata'])
        self.assertFalse((self.root/'exports'/(sid+'.zip')).exists())


class FakeRuntime:
    """Synthetic test double, never loaded by service entry points."""
    fail_cleanup=False
    phone_calls=0
    def preflight(self):pass
    def issue(self):
        self.phone_calls+=1
        raise AssertionError('panel must not issue phone credentials')
    def revoke(self):
        self.phone_calls+=1
        raise AssertionError('panel must not revoke official Web sessions')
    def cleanup_capture(self):
        if self.fail_cleanup: raise RuntimeError('synthetic uncertain capture cleanup')


class FakeCollector:
    ready=True
    exited=False
    starts=0
    count=2
    def __init__(self,root,config,runtime): self.root=root
    def start(self,sid,segment):
        type(self).starts+=1;self.sid=sid;self.segment=segment
        sealed_fixture(self.root,sid,segment)
    def read(self):return dict(ready=self.ready,capture=self.count,decoded=self.count,failed=0,exited=self.exited)
    def stop(self,sid,segment,reason=''):
        directory=self.root/'research'/sid/segment;directory.mkdir(parents=True,exist_ok=True)
        result=json.loads((directory/'sealed.json').read_text())
        result['state']='incomplete' if reason else 'finalized'
        (directory/'sealed.json').write_text(json.dumps(result));return result


class WorkerTests(Setup):
    def setUp(self):
        super().setUp();FakeCollector.starts=0;FakeCollector.ready=True;FakeCollector.exited=False;FakeCollector.count=2
        self.runtime=FakeRuntime();self.worker=Worker(self.config,self.runtime,FakeCollector)

    def test_capture_cleanup_failure_holds_capture_lock_but_saves_results(self):
        sid=self.start();self.worker.tick();self.runtime.fail_cleanup=True
        self.post(self.a,self.ca,f'/api/session/{sid}/stop',{'page':PAGE_A});self.worker.tick()
        row=self.store.get(sid);self.assertTrue(row['lease']);self.assertFalse(row['desired'])
        self.assertEqual(row['state'],'error');self.assertIsNotNone(row['ended'])
        self.assertEqual(row['export_state'],'ready')
        self.assertEqual(self.post(self.b,self.cb,'/api/start',{'page':PAGE_B}).status_code,409)
        self.assertEqual(FakeCollector.starts,1)
        self.assertEqual(self.runtime.phone_calls,0)

    def test_stop_cannot_restart_and_next_user_has_new_research(self):
        sid=self.start();self.worker.tick()
        self.post(self.a,self.ca,f'/api/session/{sid}/stop',{'page':PAGE_A})
        self.worker.tick();self.worker.tick()
        self.assertFalse(self.store.get(sid)['lease']);self.assertEqual(FakeCollector.starts,1)
        self.assertEqual(self.store.get(sid)['state'],'ended')
        self.assertEqual(self.runtime.phone_calls,0)
        other=self.post(self.b,self.cb,'/api/start',{'page':PAGE_B}).json['id']
        self.assertNotEqual(sid,other)
        self.assertEqual(self.post(self.a,self.ca,f'/api/session/{other}/stop',{'page':PAGE_A}).status_code,404)

    def test_heartbeat_loss_is_red_and_recovery_has_new_segment(self):
        sid=self.start();self.worker.tick();self.assertEqual(self.store.get(sid)['state'],'collecting')
        FakeCollector.ready=False;self.worker.tick()
        self.assertEqual(self.store.get(sid)['state'],'error')
        FakeCollector.ready=True;self.worker.retry_at=0;self.worker.tick()
        rows=self.worker.segments(sid);self.assertEqual(len(rows),2)
        self.assertEqual(rows[0]['reason'],'probe-heartbeat-gap')
        self.assertNotEqual(rows[0]['id'],rows[1]['id'])

    def test_closed_browser_grace_then_save(self):
        sid=self.start();self.worker.tick()
        with self.store.tx() as db:db.execute('UPDATE research SET browser_seen=? WHERE id=?',(time.time()-181,sid))
        self.worker.tick();row=self.store.get(sid)
        self.assertFalse(row['desired']);self.assertFalse(row['lease']);self.assertEqual(row['export_state'],'ready')

    def test_hook_connection_without_real_data_cannot_turn_green(self):
        sid=self.start();FakeCollector.count=0;self.worker.tick()
        self.assertNotEqual(self.store.get(sid)['state'],'collecting')

    def test_unconfigured_protected_runtime_never_starts_capture(self):
        sid=self.start()
        worker=Worker(self.config,CaptureRuntime(self.config),FakeCollector)
        worker.tick()
        self.assertEqual(FakeCollector.starts,0)
        self.assertEqual(self.store.get(sid)['state'],'error')
        self.assertTrue(self.store.get(sid)['lease'])
        self.post(self.a,self.ca,f'/api/session/{sid}/stop',{'page':PAGE_A})
        worker.tick()
        self.assertFalse(self.store.get(sid)['lease'])


if __name__=='__main__':unittest.main()
