from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import frida
from google.protobuf import descriptor_pb2, descriptor_pool, json_format, message_factory

try:
    import lz4.block
except Exception:
    lz4 = None

PKG = 'com.huuuge.casino.slots'
HERE = Path(__file__).resolve().parent
DEFAULT_DESC = HERE / 'huuuge_descriptors.pb'
DEFAULT_AGENT = HERE / 'agent.js'


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='milliseconds')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def load_pool(path: Path):
    fds = descriptor_pb2.FileDescriptorSet()
    fds.ParseFromString(path.read_bytes())

    pool = descriptor_pool.DescriptorPool()
    pool.AddSerializedFile(descriptor_pb2.DESCRIPTOR.serialized_pb)

    pending = list(fds.file)
    errors = {}
    for _ in range(len(pending) + 5):
        if not pending:
            break
        progress = False
        next_pending = []
        for fd in pending:
            try:
                pool.Add(fd)
                progress = True
            except Exception as exc:
                errors[fd.name] = exc
                next_pending.append(fd)
        pending = next_pending
        if not progress:
            names = ', '.join(fd.name for fd in pending)
            raise RuntimeError(f'Could not load descriptor dependencies: {names}; errors={errors}')

    rpc_desc = pool.FindMessageTypeByName('Casino.RpcMessage')
    rpc_cls = message_factory.GetMessageClass(rpc_desc)
    services_file = pool.FindFileByName('Services.proto')
    services = list(services_file.services_by_name.values())
    return pool, rpc_cls, services


def safe_name(text: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', text)[:150]


def maybe_decompress_payload(rpc, parts: list[bytes]) -> tuple[bytes, str]:
    if not parts:
        return b'', 'empty'
    n = int(getattr(rpc, 'uncompressed_payload_size', 0) or 0)
    first = parts[0]
    if n > 0 and len(first) < n:
        if lz4 is None:
            return b''.join(parts), 'lz4-needed-but-module-missing'
        try:
            expanded = lz4.block.decompress(first, uncompressed_size=n)
            return expanded + b''.join(parts[1:]), 'lz4'
        except Exception as exc:
            return b''.join(parts), f'lz4-failed:{exc}'
    return b''.join(parts), 'raw'


def type_name_for_rpc(rpc, services):
    si = int(rpc.service_index)
    mi = int(rpc.method_index)
    if si < 0 or si >= len(services):
        return None, None, None
    service = services[si]
    methods = list(service.methods)
    if mi < 0 or mi >= len(methods):
        return service.name, None, None
    method = methods[mi]
    is_request = int(rpc.type) == 1
    desc = method.input_type if is_request else method.output_type
    return service.name, method.name, desc


def message_to_dict(msg):
    return json_format.MessageToDict(
        msg,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
        always_print_fields_with_no_presence=False,
    )


def main():
    ap = argparse.ArgumentParser(description='Live Huuuge Casino RpcMessage decoder')
    ap.add_argument('--package', default=PKG)
    ap.add_argument('--descriptors', type=Path, default=DEFAULT_DESC)
    ap.add_argument('--agent', type=Path, default=DEFAULT_AGENT)
    ap.add_argument('--out', type=Path, default=Path('captures'))
    ap.add_argument('--device-id', default='', help='Exact Frida device id, e.g. 127.0.0.1:5565')
    ap.add_argument('--remote-endpoint', default='',
                    help='Frida remote endpoint to add, e.g. 127.0.0.1:27043 for Gadget')
    ap.add_argument('--process', default='',
                    help='Process name or numeric PID to attach instead of --package')
    ap.add_argument('--filter', default='', help='Comma-separated case-insensitive service/method/type substrings')
    ap.add_argument('--spawn', action='store_true', help='Spawn app instead of attaching to an already-running process')
    ap.add_argument('--all-json', action='store_true', help='Print full decoded JSON for every matched message')
    ap.add_argument('--session-id', default='', help='Explicit session directory name; default is current time')
    ap.add_argument('--stop-file', type=Path, help='Exit cleanly when this local control file appears')
    ap.add_argument('--state-file', type=Path, help='Machine-readable collector state written atomically')
    ap.add_argument('--game-version', default='unknown')
    ap.add_argument('--version-code', default='unknown')
    ap.add_argument('--research-instance', default='unknown')
    ap.add_argument('--source-revision', default='unknown')
    args = ap.parse_args()

    pool, rpc_cls, services = load_pool(args.descriptors)
    filters = [x.strip().lower() for x in args.filter.split(',') if x.strip()]

    stamp = args.session_id or datetime.now().strftime('%Y%m%d_%H%M%S')
    session_dir = args.out / stamp
    raw_dir = session_dir / 'raw'
    json_dir = session_dir / 'json'
    raw_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = session_dir / 'messages.jsonl'
    csv_path = session_dir / 'index.csv'
    manifest_path = session_dir / 'manifest.json'
    markers_path = session_dir / 'markers.jsonl'
    state_path = args.state_file or (session_dir / 'collector_state.json')
    markers_path.touch(exist_ok=True)

    def append_marker(event: str, **details) -> None:
        marker = {
            'schema_version': 1,
            'time': iso_now(),
            'event': event,
            'source': 'collector-auto',
            **details,
        }
        with markers_path.open('a', encoding='utf-8') as marker_file:
            marker_file.write(json.dumps(marker, ensure_ascii=False) + '\n')

    manifest = {
        'schema_version': 1,
        'session_id': stamp,
        'status': 'starting',
        'capture_start': iso_now(),
        'capture_end': None,
        'package': args.package,
        'game_version': args.game_version,
        'version_code': args.version_code,
        'research_instance': args.research_instance,
        'device_id': args.device_id or None,
        'remote_endpoint': args.remote_endpoint or None,
        'process': args.process or args.package,
        'frida_version': frida.__version__,
        'python_version': platform.python_version(),
        'descriptor_sha256': sha256(args.descriptors),
        'agent_sha256': sha256(args.agent),
        'source_revision': args.source_revision,
        'console_filter': filters,
        'console_filter_scope': 'display-only; all observable RPC messages are persisted',
        'message_count': 0,
        'decoded_count': 0,
        'hook_status': 'pending',
    }
    write_json_atomic(manifest_path, manifest)
    append_marker('collector-start')
    state = {
        'schema_version': 1,
        'status': 'starting',
        'session_id': stamp,
        'session_dir': str(session_dir.resolve()),
        'hooks_installed': False,
        'message_count': 0,
        'decoded_count': 0,
        'last_update': iso_now(),
    }
    write_json_atomic(state_path, state)

    csv_f = csv_path.open('w', newline='', encoding='utf-8-sig')
    csv_w = csv.writer(csv_f)
    csv_w.writerow(['seq','time','direction','stage','rpc_type','service_index','service','method_index','method','payload_type','rpc_bytes','payload_bytes','compression','decoded','raw_file','json_file'])
    jsonl_f = jsonl_path.open('w', encoding='utf-8')

    manager = frida.get_device_manager()
    if args.remote_endpoint:
        device = manager.add_remote_device(args.remote_endpoint)
    elif args.device_id:
        device = manager.get_device(args.device_id, timeout=10)
    else:
        device = frida.get_usb_device(timeout=10)
    print(f'[+] Frida device: {device.name}')

    spawned_pid = None
    if args.spawn:
        if args.remote_endpoint:
            raise RuntimeError('--spawn is not supported with a Gadget remote endpoint')
        spawned_pid = device.spawn([args.package])
        session = device.attach(spawned_pid)
    else:
        target = args.process or args.package
        if target.isdecimal():
            session = device.attach(int(target))
        else:
            proc = device.get_process(target)
            session = device.attach(proc.pid)

    script = session.create_script(args.agent.read_text(encoding='utf-8'))
    seq = 0
    decoded_count = 0
    hooks_installed = False

    def publish_state(status: str | None = None) -> None:
        if status is not None:
            state['status'] = status
        state['hooks_installed'] = hooks_installed
        state['message_count'] = seq
        state['decoded_count'] = decoded_count
        state['last_update'] = iso_now()
        write_json_atomic(state_path, state)

    def maybe_publish_ready() -> None:
        if hooks_installed and seq > 0 and decoded_count > 0 and manifest['status'] != 'ready':
            manifest['status'] = 'ready'
            write_json_atomic(manifest_path, manifest)
            append_marker('collector-ready', message_count=seq, decoded_count=decoded_count)
            publish_state('ready')

    def on_message(message, data):
        nonlocal seq, decoded_count, hooks_installed
        if message.get('type') == 'error':
            print('[FRIDA ERROR]', message.get('stack') or message)
            return
        payload = message.get('payload') or {}
        if payload.get('kind') == 'status':
            level = payload.get('level', 'info').upper()
            status_message = payload.get('message', '')
            print(f'[{level}] {status_message}', flush=True)
            if status_message == 'Huuuge hooks installed':
                hooks_installed = True
                manifest['hook_status'] = 'installed'
                manifest['hook_details'] = {
                    key: payload.get(key)
                    for key in ('moduleBase', 'writeMessage', 'handleRequest', 'handleResponse')
                }
                write_json_atomic(manifest_path, manifest)
                append_marker('hooks-installed', **manifest['hook_details'])
                maybe_publish_ready()
            return
        if payload.get('kind') != 'rpc' or data is None:
            return

        seq += 1
        now = datetime.now().isoformat(timespec='milliseconds')
        rpc_bytes = bytes(data)
        rpc = rpc_cls()
        try:
            rpc.ParseFromString(rpc_bytes)
        except Exception as exc:
            print(f'[{seq:05d}] RPC wrapper decode failed: {exc}')
            return

        service, method, pdesc = type_name_for_rpc(rpc, services)
        rpc_type_name = 'REQUEST' if int(rpc.type) == 1 else 'RESPONSE' if int(rpc.type) == 2 else str(int(rpc.type))
        payload_type = pdesc.full_name if pdesc is not None else ''
        display = '.'.join(x for x in [service, method] if x) or f'svc{rpc.service_index}.method{rpc.method_index}'
        hay = f'{display} {payload_type}'.lower()
        matched = (not filters) or any(f in hay for f in filters)

        parts = [bytes(x) for x in rpc.payload]
        payload_bytes, compression = maybe_decompress_payload(rpc, parts)
        decoded_obj = None
        decoded_ok = False
        decode_error = None

        if pdesc is not None:
            cls = message_factory.GetMessageClass(pdesc)
            obj = cls()
            try:
                obj.ParseFromString(payload_bytes)
                decoded_obj = message_to_dict(obj)
                decoded_ok = True
                decoded_count += 1
            except Exception as exc:
                decode_error = str(exc)

        raw_name = f'{seq:05d}_{safe_name(payload.get("direction","?"))}_{safe_name(display)}.rpc.bin'
        raw_path = raw_dir / raw_name
        raw_path.write_bytes(rpc_bytes)

        json_path = ''
        record = {
            'seq': seq,
            'time': now,
            'direction': payload.get('direction'),
            'stage': payload.get('stage'),
            'rpc_type': rpc_type_name,
            'service_index': int(rpc.service_index),
            'service': service,
            'method_index': int(rpc.method_index),
            'method': method,
            'payload_type': payload_type,
            'user_id': str(rpc.user_id) if rpc.HasField('user_id') else None,
            'seq_number': int(rpc.seq_number) if rpc.HasField('seq_number') else None,
            'method_hash': int(rpc.method_hash) if rpc.HasField('method_hash') else None,
            'uncompressed_payload_size': int(rpc.uncompressed_payload_size) if rpc.HasField('uncompressed_payload_size') else None,
            'compression': compression,
            'payload_bytes': len(payload_bytes),
            'decoded': decoded_ok,
            'decode_error': decode_error,
            'data': decoded_obj,
        }
        jsonl_f.write(json.dumps(record, ensure_ascii=False) + '\n')
        jsonl_f.flush()

        if decoded_ok:
            jp = json_dir / f'{seq:05d}_{safe_name(display)}.json'
            jp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
            json_path = str(jp)

        csv_w.writerow([
            seq, now, payload.get('direction'), payload.get('stage'), rpc_type_name,
            int(rpc.service_index), service, int(rpc.method_index), method, payload_type,
            len(rpc_bytes), len(payload_bytes), compression, int(decoded_ok), str(raw_path), json_path
        ])
        csv_f.flush()
        manifest['message_count'] = seq
        manifest['decoded_count'] = decoded_count
        write_json_atomic(manifest_path, manifest)
        maybe_publish_ready()
        if manifest['status'] == 'ready':
            # Keep GUI/CLI Status counters current after the one-time READY
            # transition. The manifest was already current, but the lightweight
            # controller state previously stayed frozen at the first RPC.
            publish_state('ready')

        if matched:
            arrow = '→' if payload.get('direction') == 'out' else '←'
            state = 'OK' if decoded_ok else 'RAW'
            print(f'[{seq:05d}] {arrow} {rpc_type_name:<8} {display:<45} {len(payload_bytes):>7} B [{state}]', flush=True)
            if args.all_json and decoded_obj is not None:
                print(json.dumps(decoded_obj, ensure_ascii=False, indent=2), flush=True)

    script.on('message', on_message)
    script.load()
    if spawned_pid is not None:
        device.resume(spawned_pid)

    print(f'[+] Attached to {args.process or args.package}')
    print(f'[+] Output: {session_dir.resolve()}')
    publish_state('attached')
    if filters:
        print('[+] Console filter:', ', '.join(filters))
    print('[+] Keep this window open and browse the game. Ctrl+C to stop.\n')

    try:
        while True:
            if args.stop_file and args.stop_file.exists():
                print('\n[+] Stop control file received.')
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('\n[+] Stopping...')
    finally:
        publish_state('stopping')
        try: script.unload()
        except Exception: pass
        try: session.detach()
        except Exception: pass
        jsonl_f.close()
        csv_f.close()
        manifest['status'] = 'stopped'
        manifest['capture_end'] = iso_now()
        manifest['message_count'] = seq
        manifest['decoded_count'] = decoded_count
        write_json_atomic(manifest_path, manifest)
        append_marker('collector-stop', message_count=seq, decoded_count=decoded_count)
        publish_state('stopped')


if __name__ == '__main__':
    main()
