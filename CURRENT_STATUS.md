# Current Status

_Last updated: 2026-08-25 by ChatGPT_

## Goal

Build a reusable numerical-research pipeline for Huuuge Casino that captures broad client data once, preserves raw evidence, and later produces system-specific analyses on demand.

The intended scope is **not limited to Battle Pass**. It includes slot machines, lottery/draw systems, missions/quests, passes, live events, milestones, offers/economy, progression/VIP/clubs and other systems discovered through RPCs, static config, Lua/native data or ZPK resources.

Battle Pass remains the **first end-to-end validation target only** because its schema/RPC mapping is already well understood. Once the pipeline works, the raw capture contract must remain generic and retain unrelated/unknown RPCs rather than filtering them out.

See `RESEARCH_DATA_ARCHITECTURE.md` for the canonical capture → interpretation → presentation design.

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
- User screenshot of the visible `HuuugeResearch` BlueStacks Settings → Advanced page at 2026-08-25 17:23 +08:00 shows ABI, Android Debug Bridge, and input-debug controls only; no visible `Root Access` control is present on that page. Do not ask the user to toggle unrelated input-debug options as a root step.

## Confirmed static analysis

- Primary native target: `libClawApp.so`
- Lua integration present
- Custom `.zpk` resources present
- Protobuf-generated descriptors present in native binary
- 36 `.proto` schemas recovered
- `Casino.RpcMessage` wrapper recovered
- RPC service/method mapping recovered
- Battle Pass fields and key RPC methods recovered
- Recovered schema inventory already includes broader domains such as `Slots.proto`, `Lottery.proto`, `Offers.proto`, `MiniPass.proto`, clubs/game services and other systems, supporting a generic collector rather than a Battle-Pass-only implementation.

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
- No live RPC capture has been produced yet.

## Capture contract after attach works

The base collector must capture and retain **all observable `Casino.RpcMessage` traffic**, including unknown/undecoded traffic. Filters are display-only and must not discard the underlying session data.

Raw wrapper bytes, payload bytes, timestamps, direction, service/method IDs/names, decode results/errors and version metadata should be retained so later slot/lottery/mission/event/economy analysis can reuse the same session evidence.

System-specific exporters belong downstream. They should not change what the base collector records.

## Current blocker

No working Frida attach yet. BlueStacks' built-in root flag/UI path has not produced a general UID-0 shell; the remaining blocker is privileged process access for Frida.

## Selected route — user approved 2026-08-25 17:32 +08:00

Proceed with **Plan 1: audited BlueStacks root on the isolated research environment** before changing emulators or using Frida Gadget.

Candidate implementation to audit first: `RobThePCGuy/BlueStacks-Root-GUI`.

This approval allows Codex to inspect and, if the source/patch scope is understood and recoverable, use the tool or reproduce its required patching on the research setup. Because some BlueStacks 5.22 root methods may patch shared host files such as `HD-Player.exe`, Codex must make backups and record hashes before any host-level modification. The normal `Pie64` Android instance/data must remain unrooted and unmodified.

## Next action

1. Pull latest `main` and inspect the candidate BlueStacks root project's source/release behavior before executing it. Do not blindly run an unreviewed binary.
2. Verify how it handles BlueStacks 5 China `5.22.170.6509`, especially host integrity checks, `su` whitelist behavior, instance targeting, and rollback.
3. Before any patch, back up and hash every file/disk/config that would be changed, including shared BlueStacks host binaries if applicable, `bluestacks.conf`, and `Pie64_1` research-instance disk/config data.
4. Apply root only for the `Pie64_1 / HuuugeResearch` research workflow. Preserve `Pie64` instance root flag/data unchanged.
5. Success criterion is an actual UID-0 command on `127.0.0.1:5565`; configuration flags alone do not count.
6. On UID 0, immediately start the matching Frida `17.17.0` x86_64 server as root, verify attach, load `agent.js`, and prove generic lossless `Casino.RpcMessage` capture.
7. Use Battle Pass only as the first named-schema validation. During that same capture, verify unrelated RPCs are also stored.
8. After the first successful session, build an observed service/method inventory and begin classification for slots, lottery, missions, passes/events, offers/economy and other systems without changing the raw capture contract.
9. If the audited BlueStacks root route fails or makes the research environment unstable after a bounded attempt, restore backups and stop this route; then evaluate LDPlayer/rootable research emulator or Frida Gadget as the next decision.

## Definition of next milestone

The first technical milestone is reached when a live `Casino.RpcMessage` session is captured losslessly and at least one Battle Pass RPC is decoded to named protobuf fields, while unrelated observed RPCs from the same session are also retained as raw/decoded evidence for later system analysis.
