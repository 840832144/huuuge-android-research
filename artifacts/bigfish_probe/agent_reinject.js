'use strict';
// Re-inject the Big Fish JS collector into the CURRENT (slots2) context and
// keep the logcat transport. Works for any scene: installs if absent.

const TARGET_MODULE = 'libgame.so';
const LOG_MARKER = '__CODEX_BIGFISH_HTTP_V1__';

const SYMBOLS = {
  scriptingCoreGetInstance: '_ZN13ScriptingCore11getInstanceEv',
  scriptingCoreEvalString: '_ZN13ScriptingCore10evalStringEPKc',
  xhrUpdate: '_ZN17MinXmlHttpRequest6updateEf',
};

const module = Process.findModuleByName(TARGET_MODULE);
const getInstance = new NativeFunction(module.getExportByName(SYMBOLS.scriptingCoreGetInstance), 'pointer', []);
const evalString = new NativeFunction(module.getExportByName(SYMBOLS.scriptingCoreEvalString), 'bool', ['pointer', 'pointer']);

// Same JS collector source as agent.js (module-scoped install).
const source = `
(function installCodexBigFishCollector() {
  'use strict';
  var MARKER = ${JSON.stringify(LOG_MARKER)};
  function emit(event) {
    try { cc.log(MARKER + JSON.stringify(event)); } catch (_) {}
  }
  function safeValue(value) {
    if (typeof value === 'undefined') return null;
    try { JSON.stringify(value); return value; }
    catch (error) { return { _capture_error: String(error) }; }
  }
  if (global.__codexBigFishHttpCollectorV1) {
    emit({ kind: 'collector-already-installed', timestamp_ms: Date.now() });
    return true;
  }
  var network = typeof SANetworkInterface !== 'undefined'
    ? SANetworkInterface
    : (typeof global !== 'undefined' ? global.SANetworkInterface : null);
  if (!network || typeof network.serverRequest !== 'function') {
    global.__codexBigFishHttpPendingV1 = (global.__codexBigFishHttpPendingV1 || 0) + 1;
    if (global.__codexBigFishHttpPendingV1 === 1 || global.__codexBigFishHttpPendingV1 % 300 === 0) {
      emit({ kind: 'collector-pending', timestamp_ms: Date.now(), attempts: global.__codexBigFishHttpPendingV1 });
    }
    return false;
  }
  var original = network.serverRequest;
  var nextRequestId = 1;
  network.serverRequest = function codexPassiveServerRequest(params) {
    var requestId = nextRequestId++;
    var startedAt = Date.now();
    var request = params || {};
    emit({ kind: 'request', request_id: requestId, timestamp_ms: startedAt,
      controller: request.controller || null, method: request.method || null,
      params: safeValue(request.params), url: request.url || null,
      encoding: request.encoding || null, post_object: safeValue(request.postObject) });
    var promise;
    try { promise = original.apply(this, arguments); }
    catch (error) {
      emit({ kind: 'throw', request_id: requestId, timestamp_ms: Date.now(), duration_ms: Date.now() - startedAt, error: String(error) });
      throw error;
    }
    promise.then(function(result) {
      emit({ kind: 'response', request_id: requestId, timestamp_ms: Date.now(), duration_ms: Date.now() - startedAt,
        controller: request.controller || null, method: request.method || null, url: request.url || null, result: safeValue(result) });
    }, function(error) {
      emit({ kind: 'reject', request_id: requestId, timestamp_ms: Date.now(), duration_ms: Date.now() - startedAt,
        controller: request.controller || null, method: request.method || null, url: request.url || null, error: String(error) });
    });
    return promise;
  };
  global.__codexBigFishHttpCollectorV1 = { installed_at_ms: Date.now(), original_server_request: original };
  emit({ kind: 'collector-installed', timestamp_ms: Date.now() });
  return true;
})()
`;

let attempts = 0;
let confirmed = false;

Interceptor.attach(module.getExportByName(SYMBOLS.xhrUpdate), {
  onEnter() {
    if (confirmed) return;
    attempts += 1;
    try {
      const core = getInstance();
      if (core.isNull()) return;
      const ok = evalString(core, Memory.allocUtf8String(source));
      if (attempts <= 3 || attempts % 50 === 0) {
        send({ kind: 'js-hook-eval', attempts, ok });
      }
    } catch (e) {
      if (attempts <= 3) send({ kind: 'js-hook-error', attempts, error: String(e) });
    }
  },
});

// Also probe once via file to confirm the wrapper is now active.
setTimeout(() => {
  const probe = `
(function() {
  var out = { collector: (typeof global !== 'undefined' && global.__codexBigFishHttpCollectorV1) ? 'present' : 'absent' };
  try {
    if (typeof cc !== 'undefined' && cc.FileUtils && cc.FileUtils.getInstance) {
      var fu = cc.FileUtils.getInstance();
      fu.writeStringToFile(JSON.stringify(out), fu.getWritablePath() + 'diag_reinstall.json');
    }
  } catch (e) {}
  return true;
})()`;
  try {
    const core = getInstance();
    if (!core.isNull()) evalString(core, Memory.allocUtf8String(probe));
  } catch (_) {}
}, 4000);

send({ kind: 'reinject-installed' });
