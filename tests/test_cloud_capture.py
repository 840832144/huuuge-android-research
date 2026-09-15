"""Synthetic fixtures only. No device access and no real cloud acceptance claims."""
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from google.protobuf import descriptor_pb2 as pb, descriptor_pool, message_factory

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cloud_capture', ROOT / 'scripts/cloud_capture.py')
cloud = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cloud)

FAKE_FRIDA = '''
import os
from pathlib import Path
__version__ = 'synthetic-test-double'
class Script:
    def on(self, event, callback): self.callback = callback
    def load(self):
        mode = os.environ['FIXTURE_MODE']
        if mode == 'load-failure': raise RuntimeError('synthetic load failure')
        if mode == 'hook-failure':
            self.callback({'payload': {'kind':'status','level':'error','message':'Missing symbols'}}, None)
            return
        self.callback({'payload': {'kind':'status','message':'Huuuge hooks installed'}}, None)
        for name in ('good.rpc.bin', 'bad.rpc.bin', 'good.rpc.bin'):
            self.callback({'payload': {'kind':'rpc','direction':'in','stage':'HandleResponse'}},
                          (Path(os.environ['FIXTURE_DIR']) / name).read_bytes())
        if mode == 'disconnect': SESSION.callback('connection-terminated', None)
        elif mode == 'signal':
            import signal
            os.kill(os.getpid(), signal.SIGTERM)
        elif mode == 'stream':
            import threading, time
            self.done = threading.Event()
            def stream():
                while not self.done.wait(0.1):
                    self.callback({'payload': {'kind':'rpc','direction':'in','stage':'HandleResponse'}},
                                  (Path(os.environ['FIXTURE_DIR']) / 'good.rpc.bin').read_bytes())
            threading.Thread(target=stream, daemon=True).start()
        elif mode != 'wait': Path(os.environ['STOP_FILE']).touch()
    def unload(self):
        if hasattr(self, 'done'): self.done.set()
class Session:
    def on(self, event, callback): self.callback = callback
    def create_script(self, source): return Script()
    def detach(self): self.callback('application-requested', None)
SESSION = Session()
class Device:
    name = 'synthetic'
    def get_process(self, name): return type('Process', (), {'pid': 999})()
    def attach(self, pid): return SESSION
class Manager:
    def add_remote_device(self, endpoint): return Device()
def get_device_manager(): return Manager()
'''


def make_fixture(directory):
    fd = pb.FileDescriptorProto(name='Services.proto', package='Casino', syntax='proto2')
    rpc = fd.message_type.add(name='RpcMessage')
    fields = [('service_index', 5), ('method_index', 5), ('type', 5), ('payload', 12),
              ('user_id', 4), ('seq_number', 4), ('method_hash', 4), ('uncompressed_payload_size', 5)]
    for number, (name, kind) in enumerate(fields, 1):
        rpc.field.add(name=name, number=number, type=kind, label=3 if name == 'payload' else 1)
    payload = fd.message_type.add(name='TestPayload')
    payload.field.add(name='ok', number=1, type=8, label=1)
    svc = fd.service.add(name='SlotsGame')
    svc.method.add(name='Spin', input_type='.Casino.TestPayload', output_type='.Casino.TestPayload')
    fds = pb.FileDescriptorSet()
    fds.file.add().CopyFrom(fd)
    (directory / 'test.pb').write_bytes(fds.SerializeToString())
    pool = descriptor_pool.DescriptorPool()
    pool.Add(fd)
    rpc_cls = message_factory.GetMessageClass(pool.FindMessageTypeByName('Casino.RpcMessage'))
    message = rpc_cls(service_index=0, method_index=0, type=2, payload=[b'\x08\x01'])
    (directory / 'good.rpc.bin').write_bytes(message.SerializeToString())
    (directory / 'bad.rpc.bin').write_bytes(b'\x80')
    (directory / 'frida.py').write_text(FAKE_FRIDA, encoding='utf-8')


class CloudTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        make_fixture(self.directory)

    def tearDown(self):
        self.temp.cleanup()

    def decoder(self, mode='normal', sid='unit'):
        stop = self.directory / 'stop'
        env = dict(os.environ, PYTHONPATH=str(self.directory), PYTHONIOENCODING='utf-8',
                   FIXTURE_DIR=str(self.directory), STOP_FILE=str(stop), FIXTURE_MODE=mode)
        args = [sys.executable, str(ROOT / 'artifacts/live_probe/live_decode.py'),
                '--descriptors', str(self.directory / 'test.pb'), '--out', str(self.directory / 'results'),
                '--session-id', sid, '--remote-endpoint', '127.0.0.1:12345', '--stop-file', str(stop)]
        return subprocess.run(args, env=env, capture_output=True, text=True, encoding='utf-8', timeout=15)

    @property
    def session(self):
        return self.directory / 'results/unit'

    def test_real_decoder_with_synthetic_bytes_preserves_failed_wrapper(self):
        proc = self.decoder()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        summary = cloud.summarize(self.session, proc.returncode)
        self.assertEqual((summary['capture_count'], summary['decoded_count'], summary['decode_failed_count']), (3, 2, 1))
        self.assertEqual(summary['state'], 'finalized')
        self.assertEqual(summary['cloud_acceptance'], 'pending')
        self.assertEqual((self.session / 'raw/00002_wrapper_error.rpc.bin').read_bytes(), b'\x80')

    def test_new_run_refuses_existing_session_without_truncation(self):
        self.decoder()
        before = (self.session / 'manifest.json').read_bytes()
        self.assertNotEqual(self.decoder().returncode, 0)
        self.assertEqual((self.session / 'manifest.json').read_bytes(), before)

    def test_session_traversal_rejected(self):
        self.assertNotEqual(self.decoder(sid='../outside').returncode, 0)
        self.assertFalse((self.directory / 'outside').exists())

    def test_disconnect_is_failed_not_clean_stop(self):
        proc = self.decoder('disconnect')
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(cloud.read(self.session / 'manifest.json')['status'], 'failed')
        self.assertEqual(cloud.summarize(self.session, proc.returncode)['cloud_acceptance'], 'pending')

    def test_hook_error_never_ready(self):
        proc = self.decoder('hook-failure')
        self.assertEqual(proc.returncode, 1)
        manifest = cloud.read(self.session / 'manifest.json')
        self.assertEqual(manifest['hook_status'], 'pending')
        self.assertEqual(manifest['decoded_count'], 0)

    def test_startup_failure_cannot_finalize(self):
        proc = self.decoder('load-failure')
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(cloud.summarize(self.session, proc.returncode)['state'], 'finalized')

    def test_removed_file_blocks_finalization(self):
        self.decoder()
        next((self.session / 'json').glob('*.json')).unlink()
        self.assertEqual(cloud.summarize(self.session, 0)['state'], 'incomplete')

    def test_unknown_exit_or_timeout_cannot_finalize(self):
        self.decoder()
        self.assertNotEqual(cloud.summarize(self.session, None)['state'], 'finalized')
        self.assertNotEqual(cloud.summarize(self.session, 0, 'ready-timeout')['state'], 'finalized')

    def test_only_new_manual_window_rows_count_and_summary_is_value_free(self):
        self.decoder()
        cloud.write(self.session / 'manual-play.json', {'start_seq': 2, 'end_seq': 3})
        summary = cloud.summarize(self.session, 0)
        self.assertEqual(summary['manual_play_decoded_responses'], 1)
        self.assertEqual(summary['cloud_acceptance'], 'ready-for-human-review')
        self.assertNotIn(str(self.directory), json.dumps(summary))
        self.assertNotIn('user_id', summary)
        cloud.write(self.session / 'manual-play.json', {'start_seq': 3, 'end_seq': 4})
        self.assertEqual(cloud.summarize(self.session, 0)['cloud_acceptance'], 'pending')

    def test_unconfigured_template_and_public_transports_blocked(self):
        with self.assertRaises(ValueError):
            cloud.load_config(ROOT / 'deploy/cloud/cloud.example.json')
        for endpoint in ('8.8.8.8:27043', '0.0.0.0:27043', '169.254.169.254:27043'):
            with self.assertRaises(ValueError):
                cloud.endpoint(endpoint)
        with self.assertRaises(ValueError):
            cloud.endpoint('10.0.0.10:27043', loopback=True)

    def test_windows_runtime_blocked_before_any_device_call(self):
        with patch.object(cloud.sys, 'platform', 'win32'):
            with self.assertRaises(ValueError):
                cloud.cloud_only({})

    @unittest.skipUnless(sys.platform == 'linux', 'Linux lock ownership test')
    def test_second_process_cannot_take_active_lock(self):
        with cloud.lock(self.directory, '.run.lock'):
            proc = subprocess.run([sys.executable, '-c',
                "import fcntl,sys; f=open(sys.argv[1],'a'); fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)",
                str(self.directory / '.run.lock')], capture_output=True)
            self.assertNotEqual(proc.returncode, 0)

    @unittest.skipUnless(sys.platform == 'linux', 'POSIX SIGTERM test')
    def test_sigterm_flushes_without_forced_kill(self):
        proc = self.decoder('signal')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(cloud.summarize(self.session, 0)['state'], 'finalized')

    @unittest.skipUnless(sys.platform == 'linux', 'Full synthetic Linux supervisor path')
    def test_linux_supervisor_probe_manual_window_stop_and_repeat_stop(self):
        adb = self.directory / 'adb'
        adb.write_text('#!' + sys.executable + '\n' + '''
import sys
args = sys.argv
if args[-1] == 'get-state': print('device')
elif 'dumpsys' in args: print('versionName=1.2.3 versionCode=123 primaryCpuAbi=arm64-v8a')
elif args[-1] == '-u': print('0')
elif args[-1] == 'ro.build.version.release': print('12')
elif args[-1] == 'ro.product.cpu.abi': print('arm64-v8a')
elif args[-1] == '--list': print('10.0.0.10:5555 tcp:27043 tcp:27042')
else: sys.exit(1)
''', encoding='utf-8')
        adb.chmod(0o700)
        # Optional compression is unused in fixtures; provide only import discovery.
        (self.directory / 'lz4').mkdir()
        (self.directory / 'lz4/__init__.py').touch()
        (self.directory / 'lz4/block.py').touch()
        cfg = cloud.read(ROOT / 'deploy/cloud/cloud.example.json')
        cfg.update(resource_authorized=True, result_root=str(self.directory / 'cloud-results'),
                   adb=str(adb), descriptors=str(self.directory / 'test.pb'), game_version='1.2.3', version_code='123')
        config = self.directory / 'config.json'
        cloud.write(config, cfg)
        env = dict(os.environ, PYTHONPATH=str(self.directory), PYTHONIOENCODING='utf-8',
                   FIXTURE_DIR=str(self.directory), FIXTURE_MODE='stream')
        command = [sys.executable, str(ROOT / 'scripts/cloud_capture.py'), '--config', str(config)]
        root = Path(cfg['result_root'])
        with (self.directory / 'supervisor.log').open('w') as log:
            proc = subprocess.Popen(command + ['run'], env=env, stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    if (root / 'active.json').exists():
                        _, session = cloud.active_session(root)
                        if (session / 'cloud-environment.json').exists(): break
                    if proc.poll() is not None: self.fail((self.directory / 'supervisor.log').read_text())
                    time.sleep(0.1)
                else: self.fail('Synthetic supervisor never reached READY')
                duplicate = subprocess.run(command + ['run'], env=env, capture_output=True, timeout=5)
                self.assertNotEqual(duplicate.returncode, 0)
                for action in ('play-start', 'play-end', 'stop'):
                    if action == 'play-end': time.sleep(0.4)
                    result = subprocess.run(command + [action], env=env, capture_output=True, timeout=5)
                    self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(proc.wait(timeout=10), 0, (self.directory / 'supervisor.log').read_text())
                summary = cloud.read(session / 'cloud-summary.json')
                self.assertEqual(summary['cloud_acceptance'], 'ready-for-human-review')
                self.assertGreater(summary['manual_play_decoded_responses'], 0)
                self.assertFalse((root / 'active.json').exists())
                again = subprocess.run(command + ['stop'], env=env, capture_output=True, timeout=5)
                self.assertEqual(again.returncode, 0)
                self.assertEqual(json.loads(again.stdout)['state'], 'finalized')
            finally:
                if proc.poll() is None:
                    if (root / 'active.json').exists():
                        state, _ = cloud.active_session(root)
                        (root / (state['session_id'] + '.stop')).touch()
                    proc.wait(timeout=10)


if __name__ == '__main__':
    unittest.main()
