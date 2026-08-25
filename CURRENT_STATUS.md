# Current Status

_Last updated: 2026-08-25 by ChatGPT_

## Goal

Build a reusable numerical-research pipeline for Huuuge Casino that captures broad client data once, preserves raw evidence, and later produces system-specific analyses on demand.

The intended scope is **not limited to Battle Pass**. It includes slot machines, lottery/draw systems, missions/quests, passes, live events, milestones, offers/economy, progression/VIP/clubs and other systems discovered through RPCs, static config, Lua/native data or ZPK resources.

Battle Pass is only one named-schema validation target. It must not block broader collection when the current research account cannot access it.

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
- The plain ADB shell remains UID 2000, but the audited research-only guest-`su` patch makes both `/system/xbin/bstk/su -c id` and `/system/xbin/su -c id` return real `uid=0(root)`.
- The normal `Pie64` instance was not launched or modified during the Codex root/Frida experiments.

## Confirmed static analysis

- Primary native target: `libClawApp.so`
- Lua integration present
- Custom `.zpk` resources present
- Protobuf-generated descriptors present in native binary
- 36 `.proto` schemas recovered
- `Casino.RpcMessage` wrapper recovered
- RPC service/method mapping recovered
- Battle Pass fields and key RPC methods recovered
- Recovered schema inventory includes broader domains such as `Slots.proto`, `Lottery.proto`, `Offers.proto`, `MiniPass.proto`, clubs/game services and other systems.

## Existing local Windows artifacts

- `C:\huuuge_apk\base.apk`
- `C:\huuuge_apk\split_config.arm64_v8a.apk`
- `C:\huuuge_apk\split_config.hdpi.apk`
- `C:\huuuge_apk\split_config.zh.apk`
- `C:\huuuge_live_probe\huuuge_descriptors.pb`
- Host Frida/Python packages: Frida `17.17.0`, Frida tools `14.10.4`
- Matching x86_64 server: `C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64`
- Matching ARM64 Gadget: `C:\huuuge_research\tools\frida-17.17.0\frida-gadget-17.17.0-android-arm64.so`

## Confirmed dynamic status

- Audited source: `RobThePCGuy/BlueStacks-Root-GUI` commit `7002d185522c41a15ea9b184eff24393c5a62a11`; exact patch scope/rollback is recorded in `artifacts/recovered/BlueStacks_Root_GUI_audit.md`.
- Shared host patches are active only as approved; only `Pie64_1\Data.vhdx` received the guest-`su` patch.
- Post-change SHA-256 values for normal `Pie64` `Data.vhdx`, `Root.vhd`, `fastboot.vdi`, and `Pie64.bstk` match their pre-change baselines; its root flag remains `0`.
- Root-owned x86_64 Frida server `17.17.0` can attach/detach Huuuge; the prior permission blocker is resolved.
- Because Huuuge ARM64 native code runs through Houdini, the x86_64 Frida view cannot expose `libClawApp.so` as an ARM module.
- `bootstrap_houdini_gadget.py` cold-spawns the client, intercepts the real native-bridge namespace, and loads matching ARM64 Gadget into the translated process.
- ARM64 Gadget reports `Process.arch=arm64`, enumerates `libClawApp.so`, and installs `WriteMessage`, `HandleRequest`, and `HandleResponse` hooks successfully.
- `huuuge_descriptors.pb` resolves `Casino.RpcMessage` plus 34 services.
- Reproducible local capture `C:\huuuge_research\captures\20260825_180346` contains 84 real RPC wrappers, 84 raw files, and 84 descriptor-decoded JSON files; 84/84 decoded successfully.
- Named observed methods include `AppServer.GetPlayerList`, `AppServer.GetJackpotValues`, `AppServer.DiscardPersonalOffer`, and `AppServer.ResetUserInactivity`.
- A `BattlePass` console filter did not discard unrelated messages; all observed traffic was retained, proving the generic lossless capture contract.
- The current research account shows Huuuge Pass locked at requirement `35`, so no Battle Pass RPC was observed. This is no longer considered a blocker for the broader project.

## Capture contract

The base collector captures and retains **all observable `Casino.RpcMessage` traffic**, including unrelated and unknown traffic. Console filters are display-only.

Raw wrapper bytes, timestamps, direction, service/method IDs/names, decode results/errors and decoded JSON are retained. System-specific exporters belong downstream and must not change the raw capture contract.

A session manifest with explicit app/schema/tool versions and lightweight user/action markers still needs to be added.

## Current project state

**The difficult instrumentation milestone is complete:** rooted isolated research environment, Houdini ARM64 Gadget path, native hooks, generic RPC copying, service/method mapping and protobuf JSON decoding are all working.

The project now moves from environment reverse-engineering into **system discovery and numerical modeling**.

## Next action — broad system exploration first

1. Add a reproducible session manifest: app/version code, descriptor fingerprint, Frida/Gadget version, research instance/device id, capture start/end.
2. Add lightweight timestamped action/context markers so a user action can be correlated with the RPC burst without relying on video OCR.
3. Run one broad exploratory capture on `HuuugeResearch` and visit/use every currently accessible system, prioritizing:
   - slots lobby and several representative slot machines;
   - normal spins plus any accessible feature/free-spin/jackpot flow;
   - lottery/draw/ticket screens;
   - daily/weekly/general missions or quests;
   - live events/milestones/collections;
   - offers/store/bundles;
   - VIP/clubs/progression screens;
   - balances/reward claims where naturally available.
4. Build an observed `service/method/message-type` inventory from that session, including unknown traffic, with counts and marker/time correlation.
5. Classify the observed traffic into initial domains: slots, lottery, missions, passes/events, offers/economy, clubs/VIP/progression, other/unknown.
6. Select the first high-value accessible system with sufficiently rich traffic (likely slots, missions, lottery, or offers) and build its normalized extractor before presentation/export.
7. Battle Pass should be captured later when an eligible account is available; do not block the generic inventory or other system extractors on it.

## Definition of next milestone

A broad discovery milestone is complete when one marked exploration session produces:

- lossless raw + decoded RPC data;
- session/version manifest;
- action/context markers;
- a service/method/message inventory with system classification;
- evidence mapping at least two accessible systems (preferably one gameplay system such as slots/lottery and one meta/economy system such as missions/offers) to concrete RPC/message fields.
