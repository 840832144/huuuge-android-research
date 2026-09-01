'use strict';
// Big Fish JS collector that writes responses to app files (no logcat
// truncation). Each matching event is appended to a rotating bounded JSONL
// file. Host polls it via adb. installs into the current (machine) context.

const module = Process.findModuleByName('libgame.so');
const LOG_MARKER = '__CODEX_BIGFISH_FILESINK__';
const getInstance = new NativeFunction(module.getExportByName('_ZN13ScriptingCore11getInstanceEv'), 'pointer', []);
const evalString = new NativeFunction(module.getExportByName('_ZN13ScriptingCore10evalStringEPKc'), 'bool', ['pointer', 'pointer']);

const source = `
(function installFileSinkCollector() {
  'use strict';
  var MARKER = ${JSON.stringify(LOG_MARKER)};
  if (global.__codexBigFishFileSinkV1) return true;
  function safe(v) { if (typeof v === 'undefined') return null; try { JSON.stringify(v); return v; } catch(e){ return {_err:String(e)}; } }

  function sink(event) {
    try {
      if (typeof cc === 'undefined' || !cc.FileUtils || !cc.FileUtils.getInstance) return;
      var fu = cc.FileUtils.getInstance();
      var p = fu.getWritablePath() + 'bf_capture.jsonl';
      // read existing, append, write (bounded to last 200 lines)
      var existing = '';
      try { existing = fu.getStringFromFile(p) || ''; } catch(e){}
      var line = JSON.stringify(event);
      existing = (existing + line + '\\n');
      var lines = existing.split('\\n');
      if (lines.length > 300) existing = lines.slice(-250).join('\\n') + '\\n';
      fu.writeStringToFile(existing, p);
    } catch(e){}
  }

  var network = (typeof SANetworkInterface !== 'undefined') ? SANetworkInterface : global.SANetworkInterface;
  if (!network || typeof network.serverRequest !== 'function') return false;
  var original = network.serverRequest;
  var rid = 1;
  network.serverRequest = function(params) {
    var id = rid++;
    var start = Date.now();
    var req = params || {};
    sink({ kind:'request', request_id:id, ts_ms:start, controller:req.controller||null, method:req.method||null, params:safe(req.params), url:req.url||null, encoding:req.encoding||null, post_object:safe(req.postObject) });
    var p;
    try { p = original.apply(this, arguments); }
    catch(e) { sink({ kind:'throw', request_id:id, ts_ms:Date.now(), error:String(e) }); throw e; }
    p.then(function(result) {
      sink({ kind:'response', request_id:id, ts_ms:Date.now(), duration_ms:Date.now()-start, controller:req.controller||null, method:req.method||null, url:req.url||null, result:safe(result) });
    }, function(err) {
      sink({ kind:'reject', request_id:id, ts_ms:Date.now(), controller:req.controller||null, method:req.method||null, error:String(err) });
    });
    return p;
  };
  global.__codexBigFishFileSinkV1 = { installed_at_ms: Date.now() };
  return true;
})()
`;

let attempts = 0, done = false;
Interceptor.attach(module.getExportByName('_ZN17MinXmlHttpRequest6updateEf'), {
  onEnter() {
    if (done) return;
    attempts += 1;
    try {
      const core = getInstance();
      if (core.isNull()) return;
      const ok = evalString(core, Memory.allocUtf8String(source));
      send({ kind: 'fsink-eval', attempts, ok });
      if (ok) done = true;
    } catch (e) { send({ kind: 'fsink-error', error: String(e) }); }
  },
});

send({ kind: 'fsink-installed' });
