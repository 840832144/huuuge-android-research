# Big Fish Casino passive HTTP JSON probe

This probe targets the isolated BlueStacks research app
`com.selfawaregames.acecasino`. It does not reuse Huuuge protobuf descriptors.

Confirmed client stack for version `21.3.8` (`versionCode 1293`):

- ARM64 `libgame.so` running through BlueStacks Houdini;
- Cocos2d JavaScript client resources;
- `SANetworkInterface.serverRequest` builds HTTP requests and parses successful
  response bodies as JSON.

`agent.js` injects a read-only wrapper around `SANetworkInterface.serverRequest`
on the game thread. It preserves the original function, arguments, returned
Promise, and request flow. Requests and already-parsed results are copied to the
host collector through a tagged Cocos log call intercepted before Android log
truncation.

Raw output may contain account/session/value-bearing data. Keep capture folders
outside Git (for example under `C:\bigfish_research\captures`).

The current research binding uses a dedicated Gadget listener on host port
`27044`; Huuuge retains `27043`.
