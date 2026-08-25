# Current Status

_Last updated: 2026-08-25 by Codex_

## Goal

Capture Huuuge Casino activity/system values as structured protobuf-derived data rather than relying on video OCR.

## Confirmed environment

- Windows ADB: `C:\platform-tools\adb.exe`
- BlueStacks product/version: BlueStacks 5 China `5.22.170.6509`
- Install directory: `C:\Program Files\BlueStacks_nxt_cn\`
- Data root: `D:\BlueStacks_nxt_cn`
- Engine directory: `D:\BlueStacks_nxt_cn\Engine\`
- Config: `D:\BlueStacks_nxt_cn\bluestacks.conf`
- Normal instance: `Pie64` / display name `BlueStacks 5` / ADB port `5555` / root flag remains `0`
- Research clone: `Pie64_1` / display name `HuuugeResearch` / ADB `127.0.0.1:5565` / root flag `1`
- Config backup before the research-root change: `D:\BlueStacks_nxt_cn\backups\huuuge-research\bluestacks.conf.before_Pie64_1_root.20260825_164549.bak`
- Huuuge package: `com.huuuge.casino.slots`
- BlueStacks Android: 9
- BlueStacks primary ABI: `x86_64`
- BlueStacks ABI list: `x86_64,x86,arm64-v8a,armeabi-v7a,armeabi`
- Native bridge: `ro.dalvik.vm.native.bridge=libnb.so`
- Huuuge package ABI: `arm64-v8a`
- Research Huuuge version: `12.07.27012` (`versionCode=1784198526`)
- Research Huuuge PID observed as `4310`; PIDs are not stable
- `Pie64_1` reports `ro.debuggable=1`, `ro.secure=0`, `bst.enable_root_access=1`, and `bst.config.bindmount=1`, but the ADB shell remains UID 2000
- The bundled `su` is signature/command-whitelist-gated; both `/system/xbin/bstk/su -c id` and `/system/xbin/su -c id` return exit 1, not root
- The normal `Pie64` instance was not launched or modified during the Codex root/Frida experiments

## Confirmed static analysis

- Primary native target: `libClawApp.so`
- Lua integration present
- Custom `.zpk` resources present
- Protobuf-generated descriptors present in native binary
- 36 `.proto` schemas recovered
- `Casino.RpcMessage` wrapper recovered
- RPC service/method mapping recovered
- Battle Pass fields and key RPC methods recovered

## Existing local Windows artifacts

- `C:\huuuge_apk\base.apk`
- `C:\huuuge_apk\split_config.arm64_v8a.apk`
- `C:\huuuge_apk\split_config.hdpi.apk`
- `C:\huuuge_apk\split_config.zh.apk`
- `C:\huuuge_live_probe\huuuge_descriptors.pb` (verified and synced into the ignored runtime location)
- Host Frida/Python packages: Frida `17.17.0`, Frida tools `14.10.4`
- Matching local server: `C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64`

## Confirmed dynamic status

- The x86_64 Frida server is the required first server architecture for this x86_64 Android guest; server `17.17.0` matches host Frida `17.17.0`. Instrumenting the ARM-translated app remains unproven until a privileged attach succeeds.
- A shell-owned server on `Pie64_1` can enumerate processes, and `frida-ps`/the Python API sees `Huuuge Casino`.
- Attaching to the live Huuuge PID fails exactly with `frida.PermissionDeniedError: unable to access process with pid 4310`.
- This separates the current blocker from ADB connectivity, Frida version mismatch, and server ABI selection.
- `huuuge_descriptors.pb` loads successfully with current protobuf and resolves `Casino.RpcMessage` plus 34 services.
- No live RPC or Battle Pass capture has been produced yet.

## Current blocker

No working Frida attach yet. BlueStacks accepted the research instance root config flag and exposed its whitelist-gated `su`, but it has not granted a general UID-0 shell. A shell-owned Frida server can enumerate Huuuge but cannot ptrace/attach it.

## Next action

1. In the visible `HuuugeResearch` window only, open BlueStacks Settings (`Ctrl+Shift+I`) and use the product's **Root Access → Enabled → Save changes/restart** action. Computer-use capture could not automate this hardware-rendered window (`0x80004002`).
2. Re-run `artifacts\live_probe\check_device.ps1 -Serial 127.0.0.1:5565` and require an actual `uid=0(root)` result; flags or the presence of `su` alone do not count.
3. If UID 0 works, run `start_frida_server.ps1` with the matching local x86_64 server, attach by explicit device id, load `agent.js`, and capture Battle Pass.
4. If the UI-applied setting still leaves `su` whitelist-denied, stop repeating BlueStacks root attempts and move to the already-approved fallback evaluation: ARM64 Frida Gadget research APK or a separate rootable research emulator/device.

## Definition of next milestone

A successful first milestone is reached when a live Battle Pass RPC is captured from the running client and decoded to named protobuf fields using `huuuge_descriptors.pb`, with raw + JSON output saved under a reproducible capture directory.
