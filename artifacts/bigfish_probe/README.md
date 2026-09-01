# Big Fish Casino passive HTTP JSON probe

This probe targets the isolated BlueStacks research app
`com.selfawaregames.acecasino`. It does not reuse Huuuge protobuf descriptors.

Confirmed client stack for version `21.3.8` (`versionCode 1293`):

- ARM64 `libgame.so` running through BlueStacks Houdini;
- Cocos2d JavaScript client resources (Cocos Creator 3.x jsb, SpiderMonkey engine);
- `SANetworkInterface.serverRequest` builds HTTP requests and parses successful
  response bodies as JSON. All traffic is HTTP JSON; no WebSocket/fetch in
  client JS.

## How capture works (READY, verified 2026-09-01)

`agent.js` injects a read-only wrapper around `SANetworkInterface.serverRequest`
on the game thread. Events are emitted as tagged `cc.log`/`console.log` lines,
which land in logcat under the tags **`Cobra Log`** and **`cocos2d-x debug
info`** with the marker prefix `__CODEX_BIGFISH_HTTP_V1__`.

Key diagnostic facts:

- `cc.log` is a no-op when Cocos `DebugMode.NONE`; the JS collector therefore
  must be verified through logcat, not through the `cocos2d::log` export.
- `ScriptingCore::evalString` runs on the game JS thread inside
  `MinXmlHttpRequest::update`; `global.SANetworkInterface` is visible from
  there (set by `GameClient.loadGameClient()` via `ccrequire`).
- `cc.FileUtils.writeStringToFile` works from the eval context (used in
  diagnostics).

`bigfish_capture.py` consumes the logcat stream (`--mode logcat`, default) and
writes parsed events locally (events.jsonl + one JSON per HTTP event).
`--mode frida` additionally (re)injects agent.js to guarantee the collector is
installed and to produce a `collector-installed` / `collector-already-installed`
receipt.

README-to-command mapping:

```text
python artifacts/bigfish_probe/bigfish_capture.py --output C:\bigfish_research\captures\<name> --mode logcat
python artifacts/bigfish_probe/bigfish_capture.py --output C:\bigfish_research\captures\<name> --mode frida
```

Verified on 2026-09-01: receipt `collector-already-installed` observed in
logcat; ordinary request/response pairs for mission/characters/vip/alerts/
booster/inbox/sparkle_lobby captured and JSON-valid.

Raw output may contain account/session/value-bearing data. Keep capture folders
outside Git (for example under `C:\bigfish_research\captures`).

The current research binding uses a dedicated Gadget listener on host port
`27044`; Huuuge retains `27043`.
