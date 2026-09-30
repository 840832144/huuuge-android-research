"""Synthetic runtime boundaries. These tests never access a phone/cloud target."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scripts import cloud_capture as cloud
from self_service.capture_runtime import CaptureRuntime, process_identity, listeners
from self_service.collector import Collector
from self_service.store import Store


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        c=json.loads((cloud.REPO/'deploy/cloud/cloud.example.json').read_text())
        c.update(resource_authorized=True,game_version='1.2.3',version_code='123',
                 adb_serial='127.0.0.1:15555',adb_server_port=15038,frida_endpoint='127.0.0.1:27044')
        c['transport']=dict(kind='ssh-adb-frida-tls',certificate='/private/cert.pem',token_file='/private/token',device_port=27042)
        self.config=dict(data_root=str(self.root),runtime=dict(controller=c,tunnel_uid=23456,
            phone_tools='/data/local/tmp/task0037/tools',phone_runs='/data/local/tmp/task0037/runs',
            frida_version='synthetic',adb_key='/private/adbkey',device_serial_sha256='0'*64))
        self.runtime=CaptureRuntime(self.config);self.runtime.root.mkdir()

    def test_transport_kind_is_explicit_and_public_mode_still_rejects_disguised_address(self):
        cfg=copy.deepcopy(self.config['runtime']['controller']);path=self.root/'controller.json'
        path.write_text(json.dumps(cfg));cloud.load_config(path)
        cfg['transport']['kind']='public-adb-frida-tls';path.write_text(json.dumps(cfg))
        with self.assertRaises(ValueError): cloud.load_config(path)
        cfg['transport']['kind']='ssh-adb-frida-tls';cfg['adb_serial']='192.168.1.4:5555'
        path.write_text(json.dumps(cfg))
        with self.assertRaises(ValueError): cloud.load_config(path)

    def test_tunnel_requires_exact_loopback_listener_and_dedicated_uid(self):
        for observed in ([],[('tcp','00000000',23456)],[('tcp','0100007F',99)]):
            with patch('self_service.capture_runtime.listeners',return_value=observed):
                with self.assertRaises(RuntimeError):self.runtime.tunnel_ready()
        with patch('self_service.capture_runtime.listeners',return_value=[('tcp','0100007F',23456)]):
            self.runtime.tunnel_ready()

    def test_changed_pid_identity_does_not_kill_or_disconnect(self):
        run='a'*32
        self.runtime.save(dict(run=run,remote=self.config['runtime']['phone_runs']+'/'+run,
                               adb_process=dict(pid=99,start='1',command='abc')))
        with patch('self_service.capture_runtime.process_identity',return_value=dict(pid=99,start='2',command='def')), \
             patch.object(self.runtime,'adb') as adb,patch('self_service.capture_runtime.os.kill') as kill:
            with self.assertRaises(RuntimeError):self.runtime.cleanup_capture()
            adb.assert_not_called();kill.assert_not_called()
        self.assertTrue(self.runtime.journal.exists())

    def test_new_segment_gets_new_secret_and_certificate_command_before_authentication(self):
        scripts=[];tokens=[]
        def adb(*args):
            if args[0]=='pull':Path(args[2]).write_text('synthetic-public-certificate')
            if args[0]=='push' and str(args[1]).endswith('frida.token'):
                tokens.append(Path(args[1]).read_text())
            return ''
        def authenticate(*a,**k):
            if k['token']=='task0037-negative-token':raise ValueError('incorrect token')
            return SimpleNamespace(query_system_parameters=lambda:{})
        manager=SimpleNamespace(add_remote_device=authenticate,
                                remove_remote_device=lambda *a:None)
        fake=SimpleNamespace(__version__='synthetic',get_device_manager=lambda:manager,InvalidArgumentError=ValueError)
        with patch.object(self.runtime,'preflight'),patch.object(self.runtime,'start_adb'), \
             patch.object(self.runtime,'adb',side_effect=adb),patch.object(self.runtime,'shell',side_effect=lambda s:scripts.append(s)), \
             patch('self_service.capture_runtime.listeners',return_value=[('tcp','0100007F',os.getuid() if os.name=='posix' else 123)]), \
             patch('self_service.capture_runtime.os.getuid',return_value=os.getuid() if os.name=='posix' else 123,create=True), \
             patch.object(cloud,'verify_tls') as tls,patch.object(cloud,'probe'),patch.dict(sys.modules,frida=fake):
            for n in range(2):
                directory=self.root/'research'/'synthetic'/str(n);directory.mkdir(parents=True)
                result=self.runtime.prepare_capture(directory)
                self.assertEqual(result['transport']['kind'],'ssh-adb-frida-tls')
                self.assertIn('subjectAltName=IP:127.0.0.1',scripts[-2])
                self.assertIn('req -config /dev/null',scripts[-2])
                self.assertNotIn(tokens[-1],''.join(scripts))
                self.runtime.journal.unlink() # Synthetic fixture reset; no real cleanup claim.
            self.assertEqual(tls.call_count,2)
        self.assertNotEqual(tokens[0],tokens[1])

    def test_controller_exit_before_active_is_reported(self):
        collector=Collector(self.root,self.config,self.runtime);collector.directory=self.root
        collector.child=SimpleNamespace(poll=lambda:2)
        self.assertTrue(collector.read()['exited'])

    def test_stop_during_tls_preparation_never_launches_decoder(self):
        store=Store(self.root/'state.sqlite3');sid=store.start('synthetic','hash','page')
        def prepare(directory):
            store.update(sid,desired=0)
            return dict(self.config['runtime']['controller'])
        collector=Collector(self.root,self.config,self.runtime)
        try:
            with patch.object(self.runtime,'prepare_capture',side_effect=prepare), \
                 patch.object(cloud,'load_config'),patch('self_service.collector.subprocess.Popen') as launch:
                with self.assertRaises(RuntimeError):collector.start(sid,'segment')
                launch.assert_not_called()
        finally:
            if collector.log:collector.log.close()

    def test_verified_cleanup_removes_only_current_token_and_journal(self):
        run='a'*32;directory=self.root/'research'/'synthetic'/'segment';directory.mkdir(parents=True)
        (directory/'frida.token').write_text('synthetic-secret')
        (directory/'frida.crt').write_text('synthetic-public-cert')
        identity=dict(pid=99,start='1',command='abc')
        self.runtime.save(dict(run=run,remote=self.config['runtime']['phone_runs']+'/'+run,
            adb_process=identity,directory=str(directory)))
        with patch('self_service.capture_runtime.process_identity',side_effect=[identity,identity,None]), \
             patch.object(self.runtime,'verify_device'),patch.object(self.runtime,'shell',return_value='cleaned'), \
             patch.object(self.runtime,'adb',return_value='') as adb, \
             patch('self_service.capture_runtime.os.kill') as kill, \
             patch('self_service.capture_runtime.listeners',return_value=[]):
            self.runtime.cleanup_capture()
            self.assertEqual(kill.call_count,1)
            self.assertIn(('disconnect','127.0.0.1:15555'),[c.args for c in adb.call_args_list])
        self.assertFalse(self.runtime.journal.exists());self.assertFalse((directory/'frida.token').exists())
        self.assertTrue((directory/'frida.crt').exists());self.assertTrue((directory/'cleanup.json').exists())

    @unittest.skipUnless(sys.platform=='linux','Linux process ownership and kernel listener check')
    def test_real_local_process_identity_and_loopback_listener(self):
        import socket
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));sock.listen()
            self.assertEqual(listeners(sock.getsockname()[1]),[('tcp','0100007F',os.getuid())])
        child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(10)'])
        try:
            identity=process_identity(child.pid)
            self.assertEqual(identity,process_identity(child.pid));self.assertTrue(identity['command'])
        finally:child.terminate();child.wait()
        self.assertIsNone(process_identity(child.pid))


if __name__=='__main__':unittest.main()
