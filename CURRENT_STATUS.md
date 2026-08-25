# Current Status

_Last updated: 2026-08-25 by ChatGPT_

## Goal

Build a reusable numerical-research pipeline for Huuuge Casino that captures broad client data once, preserves raw evidence, and later produces system-specific analyses on demand.

The intended scope is **not limited to Battle Pass**. It includes slot machines, lottery/draw systems, missions/quests, passes, live events, milestones, offers/economy, progression/VIP/clubs and other systems discovered through RPCs, static config, Lua/native data or ZPK resources.

Battle Pass is only one named-schema validation target. It must not block broader collection when the current research account cannot access it.

See `RESEARCH_DATA_ARCHITECTURE.md` for the canonical capture → interpretation → presentation design. A concise Chinese environment/deployment/capability overview is available in `HUUUGE_DATA_COLLECTION_OVERVIEW.md`.

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

## Latest broad discovery capture

- Local session `C:\huuuge_research\captures\20260825_182300` ran from `2026-08-25T18:23:06.234` through `2026-08-25T18:29:29.701` with no capture filter.
- It retained 741 RPC wrappers and decoded 741/741 payloads successfully; 42 unique `service.method` endpoints were observed.
- The sanitized direction/message-type inventory has 66 rows, and the sanitized schema-coverage inventory has 511 field-path/type rows with zero missing decoded JSON files.
- Heuristic coverage by message count: slots 384 across 10 endpoints; other/unknown 217 across 11; clubs/VIP/progression 70 across 4; offers/economy 55 across 12; passes/events 15 across 5.
- Observed pass/event traffic was MiniPass/Vault. No Lottery, Battle Pass, Collection Event, or Conquest endpoint was observed.
- Sanitized, value-free results are versioned under `artifacts/analysis/20260825_182300/`; raw wrappers and decoded values remain local and uncommitted.
- `scripts/build_rpc_inventory.py` reproduces the service/method/message inventory, heuristic classification, aggregate coverage summary, and value-free protobuf field-path inventory from a local capture.
- This was an unmarked exploratory session. It does not satisfy the marked-session milestone because first-class manifest generation and action markers were not yet available.

## Current project state

**The difficult instrumentation milestone is complete:** rooted isolated research environment, Houdini ARM64 Gadget path, native hooks, generic RPC copying, service/method mapping and protobuf JSON decoding are all working.

**The first broad module-catalog milestone is also complete:** `artifacts/module_catalog/` now provides a reusable structure-first map before deep numerical modeling.

`HUUUGE_DATA_COLLECTION_OVERVIEW.md` is the concise human-readable introduction for the experiment environment, deployment chain, capture workflow, capabilities and current validation level.

## Module structure catalog baseline

- `scripts/build_module_catalog.py` combines the recovered descriptor set, the sanitized `20260825_182300` inventories, optional local decoded values (counts/fingerprints only), and base-APK ZPK filenames.
- The catalog covers 37 independent dossiers, 36/36 descriptor files, 1028/1028 message types and 356/356 `Services.proto` methods.
- Machine-readable outputs: `modules.csv` (37 rows), `endpoints.csv` (356 rows) and `fields.csv` (5292 rows: 4303 schema-field rows plus 989 live-path rows).
- 15 modules have live evidence; 22 are schema-only/live pending. The 15 include 11 primary-endpoint-confirmed modules plus Lottery, Collection, Clubs and Economy with cross-cutting/config-only live evidence.
- Primary module endpoint counts sum to all 741 captured messages. All 741 remain decoded; 412 catalog live-path rows were labeled varying (cross-cutting rows may duplicate an underlying path across dossiers).
- Most structurally complete primary-live dossiers are Slots, Offers, Rewards, Player/Lobby, Other LiveOps and MiniPass. This is structural coverage, not RTP/EV/purchase-value analysis.
- No dedicated Lottery toss/draw endpoint appeared, but populated Lottery fields were observed inside shared `AddDciEvent` configuration; Lottery is therefore labeled `live-confirmed (cross-cutting/config only)`, not fully interactive-live.
- Battle Pass, generic Missions, Conquest, Sweepstakes, Adventure, Tournaments, Race, Elites, Personal Awards, Vouchers, Non-Spin Bonus, table games, Game Runtime, Authentication, Social and Contact Point remain schema-only/live pending.
- Raw value-bearing session data remains only under the local capture directory and is not versioned.

## Next action — enrich the catalog, not one deep model

1. Add a reproducible session manifest: app/version code, descriptor fingerprint, Frida/Gadget version, research instance/device id, capture start/end.
2. Add lightweight timestamped action/context markers so a user action can be correlated with the RPC burst without relying on video OCR.
3. During ordinary play, prioritize currently schema-only or config-only gaps: generic Missions, Conquest, interactive Lottery/Sweepstakes, Collection/Clubs dedicated screens, Non-Spin Bonus, Tournaments/Race/Adventure/Elites and Battle Pass when eligible.
4. After each capture, regenerate `rpc_inventory.csv`/`field_paths.csv` and `artifacts/module_catalog/`, preserving evidence labels and extending the same dossiers.
5. Split new coherent endpoint families out of `other_protocol.md` when markers/static evidence justify it.
6. Defer deep RTP, EV, paid-value or single-system normalized extractors until the user selects a module after the broad catalog has accumulated enough live samples.

## Definition of next milestone

A marked catalog-enrichment milestone is complete when one follow-up session produces:

- lossless raw + decoded RPC data;
- session/version manifest;
- action/context markers;
- a service/method/message inventory with system classification;
- updates to at least three currently schema-only/config-only dossiers with dedicated live endpoint/field evidence;
- regenerated module/endpoint/field tables without committing captured values.
