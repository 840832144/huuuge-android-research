from __future__ import annotations

import argparse
import json
import time

import frida


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Load an ARM64 Frida Gadget through BlueStacks Houdini using the app namespace.'
    )
    parser.add_argument('--device-id', required=True)
    parser.add_argument('--package', default='com.huuuge.casino.slots')
    parser.add_argument('--module', default='libClawApp.so')
    parser.add_argument('--gadget-path', required=True,
                        help='Absolute Android path to the ARM64 Gadget inside the app native-library directory')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()

    device = frida.get_device_manager().get_device(args.device_id, timeout=10)
    try:
        device.kill(device.get_process(args.package).pid)
        time.sleep(1)
    except frida.ProcessNotFoundError:
        pass

    pid = device.spawn([args.package])
    session = device.attach(pid)
    source = r'''
'use strict';
const targetModule = __TARGET_MODULE__;
const gadgetPath = __GADGET_PATH__;
let installed = false;
let scheduled = false;

function install(module) {
  if (installed) return;
  installed = true;
  const address = module.getExportByName(
    '_ZN7android26NativeBridgeLoadLibraryExtEPKciPNS_25native_bridge_namespace_tE'
  );
  const loadLibraryExt = new NativeFunction(
    address, 'pointer', ['pointer', 'int', 'pointer']
  );
  Interceptor.attach(address, {
    onEnter(args) {
      this.path = '';
      try { this.path = args[0].readCString(); } catch (_) {}
      this.flags = args[1].toInt32();
      this.namespace = args[2];
    },
    onLeave(result) {
      if (!this.path.endsWith('/' + targetModule)) return;
      send({
        kind: 'target-load',
        path: this.path,
        flags: this.flags,
        namespace: this.namespace.toString(),
        handle: result.toString()
      });
      if (scheduled) return;
      scheduled = true;
      const namespace = this.namespace;
      setImmediate(function () {
        try {
          const handle = loadLibraryExt(
            Memory.allocUtf8String(gadgetPath), 2, namespace
          );
          send({kind: 'gadget-load', handle: handle.toString(),
                namespace: namespace.toString()});
        } catch (error) {
          send({kind: 'gadget-error', error: error.stack,
                namespace: namespace.toString()});
        }
      });
    }
  });
  send({kind: 'bridge-hook-installed', base: module.base.toString()});
}

const existing = Process.findModuleByName('libnativebridge.so');
if (existing !== null) install(existing);
Process.attachModuleObserver({
  onAdded(module) {
    if (module.name === 'libnativebridge.so') install(module);
  },
  onRemoved(module) {}
});
'''.replace('__TARGET_MODULE__', json.dumps(args.module))
    source = source.replace('__GADGET_PATH__', json.dumps(args.gadget_path))

    messages: list[dict] = []

    def on_message(message, data) -> None:
        messages.append(message)
        print(json.dumps(message, ensure_ascii=False), flush=True)

    script = session.create_script(source)
    script.on('message', on_message)
    script.load()
    device.resume(pid)
    print(json.dumps({'kind': 'spawned', 'pid': pid}), flush=True)

    deadline = time.monotonic() + args.timeout
    try:
        while time.monotonic() < deadline:
            kinds = {
                item.get('payload', {}).get('kind')
                for item in messages if item.get('type') == 'send'
            }
            if 'gadget-load' in kinds or 'gadget-error' in kinds:
                break
            time.sleep(0.25)
        else:
            raise TimeoutError('Timed out waiting for Gadget load completion')
    finally:
        try:
            script.unload()
        except frida.InvalidOperationError:
            pass
        try:
            session.detach()
        except frida.InvalidOperationError:
            pass


if __name__ == '__main__':
    main()
