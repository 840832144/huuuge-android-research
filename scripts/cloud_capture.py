"""Single cloud-host controller. No provisioning, login, game input or daemon install."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
PACKAGE = 'com.huuuge.casino.slots'
LIFECYCLE = {'collector-start', 'hooks-installed', 'collector-ready', 'collector-stop'}


def now():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temporary.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def endpoint(value, loopback=False):
    host, port = value.rsplit(':', 1)
    address = ipaddress.IPv4Address(host)
    networks = ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '127.0.0.0/8')
    if not any(address in ipaddress.IPv4Network(n) for n in networks):
        raise ValueError('Only an approved private IPv4 or loopback transport is supported')
    if loopback and not address.is_loopback:
        raise ValueError('Frida must use a loopback forward on the cloud execution host')
    if not 1024 <= int(port) <= 65535:
        raise ValueError('Invalid transport port')


def load_config(path):
    cfg = read(path)
    required = {'execution_location', 'resource_authorized', 'result_root', 'adb',
                'adb_server_port', 'adb_serial', 'frida_endpoint', 'process',
                'game_version', 'version_code', 'abi', 'descriptors', 'ready_timeout_seconds'}
    if set(cfg) != required:
        raise ValueError('Config fields must exactly match cloud.example.json')
    if cfg['execution_location'] != 'cloud-linux' or cfg['resource_authorized'] is not True:
        raise ValueError('Cloud resources must be supplied and authorized before use')
    for name in ('result_root', 'adb', 'descriptors'):
        if not PurePosixPath(cfg[name]).is_absolute() or '..' in PurePosixPath(cfg[name]).parts:
            raise ValueError('Use explicit absolute cloud paths')
    if cfg['result_root'] == '/':
        raise ValueError('Use a dedicated result directory')
    endpoint(cfg['adb_serial'])
    endpoint(cfg['frida_endpoint'], loopback=True)
    if not isinstance(cfg['adb_server_port'], int) or not 1024 <= cfg['adb_server_port'] <= 65535 or cfg['adb_server_port'] == 5037:
        raise ValueError('Use a dedicated ADB server port, not the shared default 5037')
    if cfg['process'] not in (PACKAGE, 'Gadget'):
        raise ValueError('Attach only the verified Huuuge process or its dedicated Gadget')
    if cfg['abi'] != 'arm64-v8a':
        raise ValueError('This pilot requires a verified native ARM64 Huuuge build')
    if not re.fullmatch(r'\d+(\.\d+)+', cfg['game_version']) or not str(cfg['version_code']).isdigit():
        raise ValueError('Record the actual game version and versionCode before capture')
    if not isinstance(cfg['ready_timeout_seconds'], int) or not 10 <= cfg['ready_timeout_seconds'] <= 300:
        raise ValueError('READY timeout must be between 10 and 300 seconds')
    return cfg


def cloud_only(cfg):
    if sys.platform != 'linux':
        raise ValueError('Runtime commands are cloud Linux only; local check does not collect')
    root = Path(cfg['result_root']).resolve()
    if root == REPO or REPO in root.parents or root in REPO.parents:
        raise ValueError('Results must be outside the source checkout')
    os.umask(0o077)
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if root.stat().st_uid != os.getuid() or root.stat().st_mode & 0o077:
        raise ValueError('Result directory must be owned by this dedicated user and mode 0700')
    return root


@contextmanager
def lock(root, name):
    import fcntl
    with (root / name).open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('This single-instance operation is already running') from exc
        yield handle


def adb_read(cfg, *args):
    # The operator has already created the isolated server/connection. Never kill it.
    env = os.environ.copy()
    for key in ('ADB_SERVER_SOCKET', 'ANDROID_ADB_SERVER_PORT'):
        env.pop(key, None)
    proc = subprocess.run([cfg['adb'], '-H', '127.0.0.1', '-P', str(cfg['adb_server_port']),
                           '-s', cfg['adb_serial'], *args], env=env,
                          capture_output=True, text=True, timeout=20)
    if proc.returncode:
        raise ValueError('ADB read failed; inspect transport/authorization on the controlled host')
    return proc.stdout.strip()


def probe(cfg):
    if adb_read(cfg, 'get-state') != 'device':
        raise ValueError('Target device is not ready')
    info = adb_read(cfg, 'shell', 'dumpsys', 'package', PACKAGE)
    version = re.search(r'\bversionName=([^\s]+)', info)
    code = re.search(r'\bversionCode=(\d+)', info)
    abi = re.search(r'\bprimaryCpuAbi=([^\s]+)', info)
    if not version or not code or not abi:
        raise ValueError('Installed Huuuge identity could not be read')
    observed = {'game_version': version[1], 'version_code': code[1], 'abi': abi[1]}
    if any(str(cfg[k]) != v for k, v in observed.items()):
        raise ValueError('Huuuge version/ABI differs from reviewed config; verify build and schema')
    if adb_read(cfg, 'shell', 'id', '-u') != '0':
        raise ValueError('Root transport unavailable; do not change permissions automatically')
    observed['android_version'] = adb_read(cfg, 'shell', 'getprop', 'ro.build.version.release')
    observed['device_abi'] = adb_read(cfg, 'shell', 'getprop', 'ro.product.cpu.abi')
    if observed['device_abi'] != 'arm64-v8a':
        raise ValueError('Native ARM64 device required; translated/Houdini route is not assumed')
    # Ensure the loopback endpoint maps to this exact ADB device, not another game.
    forwards = adb_read(cfg, 'forward', '--list').splitlines()
    local_port = 'tcp:' + cfg['frida_endpoint'].rsplit(':', 1)[1]
    if not any(line.split()[:2] == [cfg['adb_serial'], local_port] for line in forwards):
        raise ValueError('Frida forward is not mapped to the configured cloud device')
    for module in ('frida', 'google.protobuf', 'lz4.block'):
        if importlib.util.find_spec(module) is None:
            raise ValueError('Missing dependency in the dedicated cloud virtual environment')
    if not Path(cfg['descriptors']).is_file():
        raise ValueError('Verified descriptor file is missing on the cloud host')
    return observed


def active_session(root, filename='active.json'):
    state = read(root / filename)
    sid = state['session_id']
    if not re.fullmatch(r'cloud-\d{8}T\d{6}-[0-9a-f]{12}', sid):
        raise ValueError('Invalid active session reference')
    session = root / sid
    if session.resolve().parent != root:
        raise ValueError('Session must stay inside this result root')
    return state, session


def summarize(session, exit_code, reason=None):
    """Read only this new session. Never export raw values, paths or device identifiers."""
    summary = {'schema_version': 1, 'state': 'incomplete', 'capture_count': None,
               'decoded_count': None, 'decode_failed_count': None,
               'manual_play_decoded_responses': 0, 'browser_play_confirmed': False,
               'process_exited': exit_code is not None, 'exit_code': exit_code,
               'capture_start': None, 'capture_end': None, 'reason': reason}
    try:
        manifest = read(session / 'manifest.json')
        with (session / 'index.csv').open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.DictReader(handle))
        with (session / 'markers.jsonl').open(encoding='utf-8') as handle:
            markers = {json.loads(line)['event'] for line in handle if line.strip()}
        count = manifest['message_count']
        decoded = manifest['decoded_count']
        summary.update(capture_count=count, decoded_count=decoded, decode_failed_count=count-decoded,
                       capture_start=manifest['capture_start'], capture_end=manifest['capture_end'])
        if [int(r['seq']) for r in rows] != list(range(1, count + 1)):
            raise ValueError('index-inconsistent')
        if sum(r['decoded'] == '1' for r in rows) != decoded:
            raise ValueError('decode-count-inconsistent')
        nonempty_responses = set()
        for row in rows:
            for key, directory in (('raw_file', 'raw'), ('json_file', 'json')):
                if key == 'json_file' and row['decoded'] != '1':
                    continue
                path = Path(row[key]).resolve()
                if path.parent != (session / directory).resolve() or not path.is_file() or path.stat().st_size == 0:
                    raise ValueError('result-file-missing-or-outside-session')
                if key == 'json_file':
                    record = read(path)
                    if record['seq'] != int(row['seq']) or record['decoded'] is not True:
                        raise ValueError('decoded-file-inconsistent')
                    if record.get('data'):
                        nonempty_responses.add(int(row['seq']))
        with (session / 'messages.jsonl').open(encoding='utf-8') as handle:
            if sum(1 for line in handle if line.strip()) != count:
                raise ValueError('message-count-inconsistent')
        if len(list((session / 'raw').glob('*.rpc.bin'))) != count or len(list((session / 'json').glob('*.json'))) != decoded:
            raise ValueError('artifact-count-inconsistent')
        play_path = session / 'manual-play.json'
        if play_path.exists():
            play = read(play_path)
            if 'end_seq' in play and 0 <= play['start_seq'] < play['end_seq'] <= count:
                summary['browser_play_confirmed'] = True
                summary['manual_play_decoded_responses'] = sum(
                    play['start_seq'] < int(r['seq']) <= play['end_seq']
                    and r['decoded'] == '1' and r['rpc_type'] == 'RESPONSE'
                    and int(r['seq']) in nonempty_responses
                    and r['service'].startswith('Slots') for r in rows)
        clean = (exit_code == 0 and not reason and manifest['status'] == 'stopped'
                 and LIFECYCLE <= markers and bool(manifest['capture_end']) and decoded > 0)
        if clean:
            summary['state'] = 'finalized'
        if exit_code not in (None, 0) or manifest['status'] == 'failed':
            summary['state'] = 'failed'
    except (OSError, ValueError, KeyError, TypeError):
        summary['reason'] = reason or 'missing-or-inconsistent-session-evidence'
    summary['cloud_acceptance'] = (
        'ready-for-human-review' if summary['state'] == 'finalized'
        and summary['browser_play_confirmed'] and summary['manual_play_decoded_responses'] > 0
        else 'pending')
    return summary


def finalize(root, state, session):
    summary = summarize(session, state.get('exit_code'), state.get('reason'))
    write(session / 'cloud-summary.json', summary)
    write(root / 'last.json', {'session_id': state['session_id'], **summary})
    # Uncertain/failed runs stay active for diagnosis; never discard their data.
    if summary['state'] == 'finalized':
        (root / 'active.json').unlink()
    return summary


def run(cfg, root):
    with lock(root, '.run.lock') as ownership:
        if (root / 'active.json').exists():
            raise ValueError('Previous session needs status/finalize review before a new run')
        observed = probe(cfg)
        sid = datetime.now(timezone.utc).strftime('cloud-%Y%m%dT%H%M%S-') + uuid.uuid4().hex[:12]
        session = root / sid
        control = root / (sid + '.stop')
        revision = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip()
        state = {'session_id': sid, 'created_at': now(), 'exit_code': None, 'reason': None}
        write(root / 'active.json', state)
        stop = lambda *_: control.touch(exist_ok=True)
        previous = {sig: signal.signal(sig, stop) for sig in (signal.SIGTERM, signal.SIGINT)}
        cmd = [sys.executable, '-u', str(REPO / 'artifacts/live_probe/live_decode.py'),
               '--out', str(root), '--session-id', sid, '--remote-endpoint', cfg['frida_endpoint'],
               '--process', cfg['process'], '--descriptors', cfg['descriptors'],
               '--stop-file', str(control), '--game-version', cfg['game_version'],
               '--version-code', str(cfg['version_code']), '--research-instance', 'cloud-single-instance',
               '--source-revision', revision]
        try:
            # Keep the single-run lock inherited by the child even if the supervisor dies.
            with (root / (sid + '.log')).open('x', encoding='utf-8') as log:
                child = subprocess.Popen(cmd, cwd=REPO, stdout=log, stderr=subprocess.STDOUT,
                                         start_new_session=True, pass_fds=(ownership.fileno(),))
                deadline = time.monotonic() + cfg['ready_timeout_seconds']
                ready = False
                while child.poll() is None:
                    manifest_path = session / 'manifest.json'
                    if manifest_path.exists() and not ready:
                        manifest = read(manifest_path)
                        ready = (manifest['status'] == 'ready' and manifest['decoded_count'] > 0
                                 and any((session / 'raw').glob('*.rpc.bin'))
                                 and any((session / 'json').glob('*.json')))
                        if ready:
                            write(session / 'cloud-environment.json', observed)
                            print(json.dumps({'state': 'ready', 'cloud_acceptance': 'pending'}), flush=True)
                    if not ready and time.monotonic() > deadline:
                        state['reason'] = 'ready-timeout'
                        stop()
                    time.sleep(0.25)
                state['exit_code'] = child.returncode
        except Exception:
            stop()
            state['reason'] = 'supervisor-error-process-state-unknown'
            raise
        finally:
            write(root / 'active.json', state)
            for sig, handler in previous.items():
                signal.signal(sig, handler)
        result = finalize(root, state, session)
        print(json.dumps(result))
        return 0 if result['state'] == 'finalized' else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('action', choices=('check', 'probe', 'run', 'status', 'stop', 'play-start', 'play-end', 'finalize'))
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.action == 'check':
        print(json.dumps({'state': 'config-valid', 'cloud_acceptance': 'pending'}))
        return 0
    root = cloud_only(cfg)
    if args.action == 'probe':
        print(json.dumps({'state': 'environment-readable', 'cloud_acceptance': 'pending', **probe(cfg)}))
        return 0
    if args.action == 'run':
        return run(cfg, root)
    with lock(root, '.control.lock'):
        if not (root / 'active.json').exists():
            if args.action in ('status', 'stop', 'finalize') and (root / 'last.json').exists():
                state, session = active_session(root, 'last.json')
                result = summarize(session, state.get('exit_code'), state.get('reason'))
                print(json.dumps(result))
                return 1 if args.action == 'finalize' and result['state'] != 'finalized' else 0
            raise ValueError('No active session')
        state, session = active_session(root)
        if args.action == 'stop':
            (root / (state['session_id'] + '.stop')).touch(exist_ok=True)
            print(json.dumps({'state': 'stop-requested', 'saved': False}))
        elif args.action in ('play-start', 'play-end'):
            manifest = read(session / 'manifest.json')
            if manifest['status'] != 'ready':
                raise ValueError('Mark ordinary browser play only during a READY capture')
            path = session / 'manual-play.json'
            if args.action == 'play-start':
                if path.exists():
                    raise ValueError('Manual play window already exists')
                write(path, {'start_at': now(), 'start_seq': manifest['message_count']})
            else:
                play = read(path)
                if 'end_seq' in play:
                    raise ValueError('Manual play window already closed')
                write(path, {**play, 'end_at': now(), 'end_seq': manifest['message_count']})
            print(json.dumps({'state': 'manual-observation-recorded'}))
        elif args.action == 'finalize':
            with lock(root, '.run.lock'):
                result = finalize(root, state, session)
                print(json.dumps(result))
                return 0 if result['state'] == 'finalized' else 1
        else:
            print(json.dumps(summarize(session, state.get('exit_code'), state.get('reason'))))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError, ImportError, subprocess.SubprocessError) as exc:
        # Never echo config, endpoint, full subprocess output or private payloads.
        print(json.dumps({'state': 'blocked', 'error_type': type(exc).__name__,
                          'next': 'Check cloud configuration, transport and private run files using the deployment guide'}))
        raise SystemExit(2)
