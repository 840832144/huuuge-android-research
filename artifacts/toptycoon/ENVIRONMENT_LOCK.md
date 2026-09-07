# Toy Tycoon F4 Investigation — Environment & Stack Lock

> Target: `Top Tycoon` (a.k.a. Monopoly Dream / Idle King), a Unity idle / slot
> game. F4 goal: recover the protocol layer for module analysis (spin, albums,
> economy, hot-update), reusing the DSH F4 methodology.

## Environment (confirmed 2026-09-07)

- Emulator: **BlueStacks 5 (蓝叠多开)**, instance **`topTycoon`** (Pie64_5),
  adb **`127.0.0.1:5605`**.
- OS: Android 9, SM-G998B, `x86_64` (game runs ARM64 via Houdini).
- **Root: ENABLED (updated 2026-09-07)**. Set
  `bst.instance.Pie64_5.enable_root_access="1"` in `bluestacks.conf`
  (byte-level, no BOM, backup at `bluestacks.conf.toptycoon_root.bak`), then
  rebooted the instance. `su -c id` → `uid=0(root)`. Host patches
  (`HD-Player.exe` @0x1BEB00 = `31 C0 C3`, `HD-MultiInstanceManager.exe`
  @0x550E3 = `90 90 90 90 90`) were already applied by the earlier Huuuge
  root work and persist.
- Package: `com.monopoly.dream.idle.king`, version 1.0.12, main Activity
  `com.google.firebase.MessagingUnityPlayerActivity`.

## Runtime injection (confirmed 2026-09-07)

Reused the Huuuge pattern (root + x86_64 frida-server + ARM64 Gadget via
Houdini namespace):

- `frida-server-17.17.0-android-x86_64` pushed to `/data/local/tmp/frida-server`,
  run as root, listens `127.0.0.1:27042` (forwarded).
- `frida-gadget-17.17.0-android-arm64.so` copied to the app native dir
  `/data/app/.../lib/arm64/libfrida-gadget.so`, with a `libfrida-gadget.config.so`
  (`{"interaction":{"type":"listen","address":"127.0.0.1","port":27045,"on_load":"wait"}}`).
- `bootstrap_gadget_tt.py` (adapted from Huuuge
  `bootstrap_houdini_gadget.py`) hooks `NativeBridgeLoadLibraryExt`, targets
  `libmain.so`, and loads the ARM64 Gadget into the Houdini ARM64 namespace.
  Gadget listens on `127.0.0.1:27045` (forwarded). Verify:
  `frida -H 127.0.0.1:27045` → `Process.arch=arm64`, sees
  `libil2cpp.so`/`libunity.so`/`libmain.so`.

- x86_64 frida-server (27042) can attach the game pid (ARM64 process) and sees
  **x86_64** modules including `libcronet.121.0.6167.71.so` and
  `libcrypto.so`/`libssl.so`. ARM64 Gadget (27045) sees the ARM64 modules.
  Cross-arch: Cronet is x86_64 (in-process, host ABI), business il2cpp is ARM64.

- **Business traffic**: game holds an ESTABLISHED TLS connection to
  `47.88.24.84:443`. The TLS stack is **Cronet's built-in BoringSSL**
  (symbols are internal, not `libssl.so`'s exported `SSL_write`/`SSL_read`),
  so hooking `libssl.so` SSL_write/read does NOT capture it — verified 0 calls
  during a spin. Cronet is the business transport.

## Stack (confirmed)

Unity + **il2cpp** with a **HybridCLR / IL hot-update** + **xLua** + **YooAsset**
resource hot-update. Key native libs (`lib/arm64-v8a`):

- `libunity.so`, `libil2cpp.so`, `libmain.so`, `libc++_shared.so`
- **`libxlua.so`** (xLua), `_burst_generated.so`
- `libFirebaseCpp*` (App/Analytics/Crashlytics/DynamicLinks/Messaging)
- `libOni.so`, **`libpglarmor.so`** (packer/protection — may hinder hooking)
- `libapplovin*`, `libtapjoy.so` (ads), `libavcodec/avformat/avutil` (video),
  `liblofelt_sdk.so`
- `libnms.so`, `libsigner.so`, `libtobEmbedPagEncrypt.so`, `libtt_ugen_layout.so`
  (encryption / protection helpers)

## Network / protocol evidence

- **Firebase Realtime Database**: `google-services-desktop.json` →
  `https://top-tycoon-default-rtdb.firebaseio.com` (project "top-tycoon").
- Firebase Messaging + Analytics + Crashlytics confirmed in runtime logs.
- Runtime log shows **Cronet (org.chromium.net)** streams +
  `UnityEngine.WorkRequest` (UnityWebRequest) activity, and
  `TRuntime.CctTransportBackend` (Firebase logging).
- **Business API base URL NOT found as plaintext** in static assets — it is
  assembled in hot-update logic (Lua / HybridCLR assembly) and/or encrypted.
  Asset configs under `assets/yoo/Logic/*configs_hotfix_*.bundle` are YooAsset
  binary/encrypted bundles.
- C# symbols retained in logcat: `Game.Patch`, `Game.Hotfix.*`,
  `Game.PurchaseAgent`, `Game.AdSDKObj`, `Game.AdjustObj`,
  `Game.Runtime.MainState.*`, `Game.MainStateBridge`, etc.

## F4 implications / candidate routes

- Business traffic is TLS (443) and the API base is hidden in hot-update code —
  so static-only will not reveal the protocol. A **dynamic hook** is required.
- Protections present (`libpglarmor`, `libOni`) and **no root** → naive Gadget
  injection may be blocked; APK-repack Frida Gadget is the no-root route but
  must contend with the packer.
- Candidate interception points (once the transport is identified):
  - `UnityWebRequest` (C# / il2cpp) — if business API uses UnityWebRequest.
  - Native SSL write (`SSL_write`) if requests go through libssl/BoringSSL.
  - Cronet (`org.chromium.net`) if the game routes API via Cronet.
  - xLua / HybridCLR layer — locate the Lua/IL HTTP client to find the API base
    and request schema without hooking the socket.

## Next step (awaiting direction)

Confirm the transport before deploying a capture agent: (a) static analysis of
the xLua/HotUpdate scripts to find the HTTP client and API base, or (b) dynamic
interception (APK-repack Frida Gadget → hook UnityWebRequest/Cronet/SSL_write).
The presence of a packer and no root makes static analysis of the hot-update
logic the lower-risk first step.


## Confirmed business host (from live TCP connections)

During runtime, the game holds an ESTABLISHED TLS connection to:

- **`47.88.24.84:443`** (no PTR record; an independent/overseas node, not Google).
  This is the likely **business API host**. All other active peers are
  Google/Firebase (`*.googleusercontent.com`, `*.1e100.net`, `dns.google`,
  `8.8.8.8:853` DoT, `172.217.x.x:443` QUIC), plus
  `34.149.76.49` (Google) and `172.217.113.4`/`172.217.119.4` (QUIC HTTP/3).
- UDP 443 to Google = QUIC/HTTP3 (Firebase/Cronet). Business traffic is
  TLS/443 to `47.88.24.84`.

## Next step

The API base/protocol must be read dynamically (static scan found no business
URL; configs are encrypted YooAsset bundles). Candidate: intercept the request
to `47.88.24.84` at the transport layer (SSL_write / UnityWebRequest / Cronet)
or resolve the HTTP client in the xLua/HotUpdate logic.
