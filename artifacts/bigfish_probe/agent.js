'use strict';

const TARGET_MODULE = 'libgame.so';
const LOG_MARKER = '__CODEX_BIGFISH_HTTP_V1__';

const SYMBOLS = {
  cocosLog: '_ZN7cocos2d3logEPKcz',
  scriptingCoreGetInstance: '_ZN13ScriptingCore11getInstanceEv',
  scriptingCoreEvalString: '_ZN13ScriptingCore10evalStringEPKc',
  xhrUpdate: '_ZN17MinXmlHttpRequest6updateEf',
};

let installed = false;
let jsCollectorInstalled = false;

function emit(kind, extra) {
  send(Object.assign({ kind, timestamp_ms: Date.now() }, extra || {}));
}

function install(module) {
  if (installed) return;
  installed = true;

  const addresses = {};
  for (const [name, symbol] of Object.entries(SYMBOLS)) {
    addresses[name] = module.getExportByName(symbol);
  }

  Interceptor.attach(addresses.cocosLog, {
    onEnter(args) {
      let line;
      try {
        line = args[0].readUtf8String();
      } catch (_) {
        return;
      }
      if (!line.startsWith(LOG_MARKER)) return;

      const raw = line.slice(LOG_MARKER.length);
      try {
        const event = JSON.parse(raw);
        if (event.kind === 'collector-installed' ||
            event.kind === 'collector-already-installed') {
          jsCollectorInstalled = true;
        }
        emit('bigfish-http', { event });
      } catch (error) {
        emit('bigfish-http-parse-error', {
          error: String(error),
          raw,
        });
      }
    },
  });

  const getScriptingCore = new NativeFunction(
    addresses.scriptingCoreGetInstance,
    'pointer',
    []
  );
  const evalString = new NativeFunction(
    addresses.scriptingCoreEvalString,
    'bool',
    ['pointer', 'pointer']
  );

  const source = `
(function installCodexBigFishCollector() {
  'use strict';
  var MARKER = ${JSON.stringify(LOG_MARKER)};

  function emit(event) {
    try {
      cc.log(MARKER + JSON.stringify(event));
    } catch (_) {}
  }

  function safeValue(value) {
    if (typeof value === 'undefined') return null;
    try {
      JSON.stringify(value);
      return value;
    } catch (error) {
      return { _capture_error: String(error) };
    }
  }

  if (global.__codexBigFishHttpCollectorV1) {
    emit({ kind: 'collector-already-installed', timestamp_ms: Date.now() });
    return true;
  }

  var network = typeof SANetworkInterface !== 'undefined'
    ? SANetworkInterface
    : (typeof global !== 'undefined' ? global.SANetworkInterface : null);
  if (!network || typeof network.serverRequest !== 'function') {
    global.__codexBigFishHttpPendingV1 =
      (global.__codexBigFishHttpPendingV1 || 0) + 1;
    if (global.__codexBigFishHttpPendingV1 === 1 ||
        global.__codexBigFishHttpPendingV1 % 300 === 0) {
      emit({
        kind: 'collector-pending',
        timestamp_ms: Date.now(),
        attempts: global.__codexBigFishHttpPendingV1,
        sanetwork_type: typeof SANetworkInterface,
        game_type: typeof Game,
        game_client_type: typeof GameClient
      });
    }
    return false;
  }

  var original = network.serverRequest;
  var nextRequestId = 1;

  network.serverRequest = function codexPassiveServerRequest(params) {
    var requestId = nextRequestId++;
    var startedAt = Date.now();
    var request = params || {};
    emit({
      kind: 'request',
      request_id: requestId,
      timestamp_ms: startedAt,
      controller: request.controller || null,
      method: request.method || null,
      params: safeValue(request.params),
      url: request.url || null,
      encoding: request.encoding || null,
      post_object: safeValue(request.postObject)
    });

    var promise;
    try {
      promise = original.apply(this, arguments);
    } catch (error) {
      emit({
        kind: 'throw',
        request_id: requestId,
        timestamp_ms: Date.now(),
        duration_ms: Date.now() - startedAt,
        error: String(error)
      });
      throw error;
    }

    promise.then(function(result) {
      emit({
        kind: 'response',
        request_id: requestId,
        timestamp_ms: Date.now(),
        duration_ms: Date.now() - startedAt,
        controller: request.controller || null,
        method: request.method || null,
        url: request.url || null,
        result: safeValue(result)
      });
    }, function(error) {
      emit({
        kind: 'reject',
        request_id: requestId,
        timestamp_ms: Date.now(),
        duration_ms: Date.now() - startedAt,
        controller: request.controller || null,
        method: request.method || null,
        url: request.url || null,
        error: String(error)
      });
    });

    return promise;
  };

  global.__codexBigFishHttpCollectorV1 = {
    installed_at_ms: Date.now(),
    original_server_request: original
  };
  emit({ kind: 'collector-installed', timestamp_ms: Date.now() });
  return true;
})()
`;

  let attempts = 0;
  Interceptor.attach(addresses.xhrUpdate, {
    onEnter() {
      if (jsCollectorInstalled) return;
      attempts += 1;
      try {
        const core = getScriptingCore();
        if (core.isNull()) return;
        const ok = evalString(core, Memory.allocUtf8String(source));
        if (attempts === 1 || attempts % 300 === 0) {
          emit('js-hook-eval', { attempts, ok });
        }
      } catch (error) {
        if (attempts <= 3 || attempts % 300 === 0) {
          emit('js-hook-error', { attempts, error: String(error) });
        }
      }
    },
  });

  emit('native-hooks-installed', {
    module: TARGET_MODULE,
    base: module.base.toString(),
    symbols: Object.fromEntries(
      Object.entries(addresses).map(([name, address]) => [name, address.toString()])
    ),
  });
}

const existing = Process.findModuleByName(TARGET_MODULE);
if (existing !== null) install(existing);
Process.attachModuleObserver({
  onAdded(module) {
    if (module.name === TARGET_MODULE) install(module);
  },
  onRemoved() {},
});
