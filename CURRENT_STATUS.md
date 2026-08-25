# Current Status

_Last updated: 2026-08-25 by Codex_

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
- Audited Plan 1 full backup + SHA-256 manifest: `D:\BlueStacks_nxt_cn\backups\huuuge-research\plan1_20260825_181500`
- Huuuge package: `com.huuuge.casino.slots`
- BlueStacks Android: 9
- BlueStacks primary ABI: `x86_64`
- BlueStacks ABI list: `x86_64,x86,arm64-v8a,armeabi-v7a,armeabi`
- Native bridge: `ro.dalvik.vm.native.bridge=libnb.so`
- Huuuge package ABI: `arm64-v8a`
- Research Huuuge version: `12.07.27012` (`versionCode=1784198526`)
- Research Huuuge PID observed as `4310`; PIDs are not stable
- The plain ADB shell remains UID 2000, but the audited research-only guest-`su` patch now makes both `/system/xbin/bstk/su -c id` and `/system/xbin/su -c id` return real `uid=0(root)`
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
- Matching local ARM64 Gadget: `C:\huuuge_research\tools\frida-17.17.0\frida-gadget-17.17.0-android-arm64.so`

## Confirmed dynamic status

- Audited source: `RobThePCGuy/BlueStacks-Root-GUI` commit `7002d185522c41a15ea9b184eff24393c5a62a11`; local signatures had one unambiguous match per required host patch. Exact scope/rollback is in `artifacts/recovered/BlueStacks_Root_GUI_audit.md`.
- Shared host patches are active only as approved: two `HD-Player.exe` checks and the `HD-MultiInstanceManager.exe` root-reset write. Only `Pie64_1\Data.vhdx` received the guest-`su` patch (two three-byte entries with a rollback sidecar).
- Post-change SHA-256 values for normal `Pie64` `Data.vhdx`, `Root.vhd`, `fastboot.vdi`, and `Pie64.bstk` exactly match the pre-change baselines. Its root flag remains `0`.
- Root-owned x86_64 Frida server `17.17.0` runs as Android user `root` and can attach/detach Huuuge; the prior `PermissionDeniedError` is resolved.
- The x86_64 server sees the outer Houdini process as `Process.arch=x64`; root-readable maps contain ARM64 `libClawApp.so`, but the x64 Frida Module API does not expose it. Loading `agent.js` directly through this view installs no hooks.
- A cold-spawn bridge hook captured the real Huuuge native-bridge namespace (`0x3`) and loaded the matching ARM64 Gadget into the same process. Gadget reports `Process.arch=arm64`, enumerates `libClawApp.so`, and installs all three existing hooks successfully.
- `huuuge_descriptors.pb` loads successfully with current protobuf and resolves `Casino.RpcMessage` plus 34 services.
- Reproducible local capture `C:\huuuge_research\captures\20260825_180346` contains 84 real RPC wrappers, 84 raw files, and 84 descriptor-decoded JSON files. Named methods include `AppServer.GetPlayerList`, `AppServer.GetJackpotValues`, `AppServer.DiscardPersonalOffer`, and `AppServer.ResetUserInactivity`.
- No Battle Pass RPC was present in that capture. The research account UI visibly shows Huuuge Pass locked at requirement `35`; tapping it generated no request.

## Capture contract

The base collector captures and retains **all observable `Casino.RpcMessage` traffic**, including traffic unrelated to the console filter. The 84-message proof session used a `BattlePass` console filter but still retained every observed non-Battle-Pass wrapper and decode.

Raw wrapper bytes (which contain payload bytes), timestamps, direction, service/method IDs/names, decode results/errors and decoded JSON are retained. A session manifest with explicit app/schema/tool versions remains to be added so later slot/lottery/mission/event/economy analysis can reproduce every interpretation.

System-specific exporters belong downstream. They must not change what the base collector records.

## Current blocker

The root/Frida/hook/RPC/descriptor chain is working. The remaining Battle Pass blocker is account/UI access: the current research account has Huuuge Pass locked at requirement `35`, so it cannot open the Battle Pass screen or trigger its RPCs. Continuing requires the user to complete any necessary account login/account selection in the visible `HuuugeResearch` instance using an account where Battle Pass is unlocked.

## Selected route — completed 2026-08-25 18:07 +08:00

Plan 1 succeeded and is stable. Backups are retained; rollback was not triggered. Root and the x86_64 host server are used only for `Pie64_1`. ARM64 Gadget is needed inside Houdini for the ARM module view; it is staged only in the research clone's app/data disk.

## Next action

1. User: in visible `HuuugeResearch`, complete any required login/account selection so Huuuge Pass is unlocked; do not use the normal `Pie64` instance for instrumentation.
2. Codex: re-run `bootstrap_houdini_gadget.py` with the staged ARM64 Gadget in `on_load: wait` mode, then connect `live_decode.py --remote-endpoint 127.0.0.1:27043 --process Gadget --filter BattlePass --all-json`.
3. Open Battle Pass main/reward/mission screens and confirm `BattlePassUpdate`, `BattlePassGetMilestones`, `BattlePassGetDailyMissions`, or `BattlePassGetWeeklyMissions` in the saved index.
4. Export milestone/mission JSON/CSV and add an explicit session/version manifest. Keep raw account/session-bearing capture files local and out of Git.
5. After the Battle Pass validation, build the observed service/method inventory and broader system classification defined in `RESEARCH_DATA_ARCHITECTURE.md` without narrowing the raw capture contract.

## Definition of next milestone

A generic lossless live milestone is complete: real RPCs are hooked, named, and decoded to JSON while unrelated traffic is retained. The first named-schema milestone remains a live Battle Pass RPC decoded to named fields, followed by milestone/mission JSON/CSV export and a reproducible session manifest.
