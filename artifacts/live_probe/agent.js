'use strict';

const TARGET_MODULE = 'libClawApp.so';
const MAX_RPC_SIZE = 32 * 1024 * 1024;
let installed = false;

const SYMBOLS = {
  writeMessage: '_ZN6Casino10Connection12WriteMessageERKN6google8protobuf7MessageE',
  handleRequest: '_ZN6Casino10Connection13HandleRequestERKNS_10RpcMessageE',
  handleResponse: '_ZN6Casino10Connection14HandleResponseERKNS_10RpcMessageE',
  rpcByteSize: '_ZNK6Casino10RpcMessage8ByteSizeEv',
  rpcSerialize: '_ZNK6Casino10RpcMessage31SerializeWithCachedSizesToArrayEPh',
  rpcVtable: '_ZTVN6Casino10RpcMessageE'
};

function findSymbol(module, exactName) {
  const symbols = module.enumerateSymbols();
  for (const s of symbols) {
    if (s.name === exactName) return s.address;
  }
  return null;
}

function install(module) {
  if (installed) return;
  installed = true;

  const addrWrite = findSymbol(module, SYMBOLS.writeMessage);
  const addrReq = findSymbol(module, SYMBOLS.handleRequest);
  const addrResp = findSymbol(module, SYMBOLS.handleResponse);
  const addrSize = findSymbol(module, SYMBOLS.rpcByteSize);
  const addrSer = findSymbol(module, SYMBOLS.rpcSerialize);
  const addrVtable = findSymbol(module, SYMBOLS.rpcVtable);

  const missing = [];
  for (const [k, v] of Object.entries({addrWrite, addrReq, addrResp, addrSize, addrSer, addrVtable})) {
    if (v === null) missing.push(k);
  }
  if (missing.length) {
    send({kind: 'status', level: 'error', message: 'Missing symbols: ' + missing.join(', ')});
    return;
  }

  const rpcByteSize = new NativeFunction(addrSize, 'int', ['pointer']);
  const rpcSerialize = new NativeFunction(addrSer, 'pointer', ['pointer', 'pointer']);
  const rpcVptr = addrVtable.add(Process.pointerSize * 2);

  function isRpcMessage(obj) {
    if (obj.isNull()) return false;
    try {
      return obj.readPointer().equals(rpcVptr);
    } catch (_) {
      return false;
    }
  }

  function emitRpc(direction, stage, obj) {
    try {
      if (!isRpcMessage(obj)) {
        send({kind: 'status', level: 'debug', message: stage + ': protobuf object is not Casino::RpcMessage'});
        return;
      }
      const n = rpcByteSize(obj);
      if (n <= 0 || n > MAX_RPC_SIZE) {
        send({kind: 'status', level: 'warn', message: stage + ': suspicious RpcMessage size=' + n});
        return;
      }
      const buf = Memory.alloc(n);
      const end = rpcSerialize(obj, buf);
      let actual = end.sub(buf).toInt32();
      if (actual <= 0 || actual > n) actual = n;
      const bytes = buf.readByteArray(actual);
      send({kind: 'rpc', direction: direction, stage: stage, size: actual}, bytes);
    } catch (e) {
      send({kind: 'status', level: 'error', message: stage + ': ' + e.stack});
    }
  }

  Interceptor.attach(addrWrite, {
    onEnter(args) {
      emitRpc('out', 'WriteMessage', args[1]);
    }
  });

  Interceptor.attach(addrReq, {
    onEnter(args) {
      emitRpc('in', 'HandleRequest', args[1]);
    }
  });

  Interceptor.attach(addrResp, {
    onEnter(args) {
      emitRpc('in', 'HandleResponse', args[1]);
    }
  });

  send({
    kind: 'status',
    level: 'info',
    message: 'Huuuge hooks installed',
    moduleBase: module.base.toString(),
    writeMessage: addrWrite.toString(),
    handleRequest: addrReq.toString(),
    handleResponse: addrResp.toString()
  });
}

const existing = Process.findModuleByName(TARGET_MODULE);
if (existing !== null) install(existing);

Process.attachModuleObserver({
  onAdded(module) {
    if (module.name === TARGET_MODULE) install(module);
  },
  onRemoved(module) {}
});
