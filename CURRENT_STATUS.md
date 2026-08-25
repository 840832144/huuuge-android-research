# Current Status

_Last updated: 2026-08-25 by ChatGPT_

## Goal

Capture Huuuge Casino activity/system values as structured protobuf-derived data rather than relying on video OCR.

## Confirmed environment

- Windows ADB: `C:\platform-tools\adb.exe`
- Huuuge package: `com.huuuge.casino.slots`
- BlueStacks Android: 9
- BlueStacks ABI list: `x86_64,x86,arm64-v8a,armeabi-v7a,armeabi`
- Huuuge package ABI: `arm64-v8a`
- ADB connection has worked as `emulator-5554 device`
- Current normal instance has no usable root / `su`
- `run-as com.huuuge.casino.slots` is not usable

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
- `C:\huuuge_live_probe` (expected from prior extraction; verify before relying on it)

## Current blocker

No working Frida attach yet. The normal BlueStacks instance is not rooted, and the real BlueStacks install/data/config path has not yet been discovered on this Windows machine.

## Next action

Codex should:

1. Pull the latest repository.
2. Discover BlueStacks process path, version, data directory, config file, and instance IDs automatically.
3. Preserve the normal instance and use/create a research clone.
4. Determine `ro.dalvik.vm.native.bridge` and actual Huuuge runtime/native-bridge behavior.
5. Establish root/Frida on the research instance, or fall back to Gadget/alternate research emulator if needed.
6. Run `artifacts/live_probe/agent.js` + `live_decode.py`.
7. First target: capture and decode a real Battle Pass `Casino.RpcMessage`.

## Definition of next milestone

A successful first milestone is reached when a live Battle Pass RPC is captured from the running client and decoded to named protobuf fields using `huuuge_descriptors.pb`, with raw + JSON output saved under a reproducible capture directory.
