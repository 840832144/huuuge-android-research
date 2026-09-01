# Current Status

_Last updated: 2026-09-01 by Codex_

## Goal

Build a reusable Huuuge Casino numerical-research workbench that is easy for a game designer/analyst to deploy and operate:

```text
one planner-facing entry
  -> broad passive capture
  -> protobuf decode
  -> module catalog enrichment
  -> deep analysis/export only when requested
```

The scope is not limited to Battle Pass. It includes Slots, Lottery, Missions, passes/events, offers/economy, rewards, progression/VIP/clubs and any additional systems discovered through RPCs, static config, Lua/native state or ZPK resources.

## TASK-0019 Shared Jackpot live investigation

- Finalized local capture: `20260901_160002`; manifest is `stopped`, all four lifecycle markers are present, and 8372/8398 RPCs decoded. Value-bearing files remain local and uncommitted.
- The user placed the account in the Buffalo slot room and enabled normal Auto Spin. A user-provided screenshot at the observation baseline shows three peer players in the same machine room; names, IDs and balances are not recorded in Git.
- Target RPC: `SlotsGameClient.HitSharedJackpot` (`service_index=5`, `method_index=3`, payload `Casino.SlotsProto.JackpotList`). The recovered schema contains per-jackpot `eligible_users`, `user_payouts`, `last_contributor`, `hits`, jackpot value and win fields.
- Final evidence boundary: across 645 Spin request/response pairs, 107 FreeSpin request/response pairs, 1493 `RoomUsers` updates and 5 `UpdateJackpot` messages, neither `HitSharedJackpot` nor ordinary `HitJackpot` appeared. The target hit flow remains `schema-only / live sample pending`; this session does not establish trigger probability, payout ratio or recipient rules.
- The five-minute current-thread monitor was deleted after the user requested stop. Collector clean stop, flush, sanitized inventory and module-catalog regeneration all completed.
- Huuuge was updated in the research instance only to `12.08.27100` (`versionCode=1786533240`) after the prior build became update-blocked. The pre-update four-split APK backup is local at `C:\huuuge_research\backups\apk_before_update\20260901_155449`.
- The update replaced the app directory, so both the verified ARM64 Gadget and `libhuuuge-gadget.config.so` were restaged with matching SHA-256. Bootstrap/controller checks now require both files.
- Collector hardening was pushed to Git in `cf44814` and mirrored to planner SVN as revision `6622`; the Chinese SVN log was read back from XML without mojibake.
- BlueStacks startup was repaired by removing only the leading UTF-8 BOM from `D:\BlueStacks_nxt_cn\bluestacks.conf`. The exact pre-change backup is `C:\huuuge_research\backups\bluestacks_config\20260901_155108\bluestacks.conf.FD2149898D313528ACDC42B2A720B955DEC63D2E3BBDFB5B1201D7B741F5069E.bak`; backup hash equals the recorded filename hash.

## TASK-0018 Lottery numerical baseline

- Capture alias `LOT-20260827-A` is confirmed Finalized: manifest `stopped`, all four lifecycle markers present, 8712/8712 RPCs decoded, 131 inventory rows and 2152 field-path rows.
- Primary Lottery evidence is now L3 Runtime Observed: 346/346 `LotteryToss` request/response pairs, 933 ticket units consumed, 588/588 ordinary chip-bet Spin pairs and 45/45 FreeSpin pairs.
- The exact in-Session free-ticket rule is `initial progress 1 + every 7 consumed ticket units -> 1 Bronze`: 133 grants and final progress 3.
- Spin/FreeSpin payloads expose no direct Lottery ticket grant. Six post-level state transitions add 16 Bronze tickets after source reconciliation; the state changes are Confirmed L3, while level-up causation remains Estimate L3 supported by repeated timing and User Manual evidence.
- Four successful real-money purchases total 54.43 SGD and grant 763 Lottery tickets plus 235 loyalty points; apparent per-ticket costs are descriptive bundle ratios, not standalone ticket prices.
- The planner-first sanitized report, purchase table and reproducible extractor are under `reports/lottery/20260827_lottery-ticket-puzzle/` and `tools/analysis/lottery/`.
- The original Feishu document was replaced in place and verified: `https://gfok27asqq.feishu.cn/docx/IK5adiJyWoHVJzxlovEcjxiWnO3`, one title, complete section order and company-editable permission.
- Raw/decoded capture values, real Session/account/request/product/order identifiers, absolute chip balances and full balance trajectories remain local and uncommitted.
- Current state: **Waiting for ChatGPT Review Round 2** after addressing Review Round 1. No collector, game, server, CR repository or SVN behavior was changed.

**Easy deployment and low-operation use are now first-class project requirements.** A planner should not need to manually manage ADB, Frida, Houdini or Protobuf details when scripts/local AI can do so.

Primary human documentation:

- `HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md` — product-facing installation, update, capture, data, AI and FAQ manual;

- `HUUUGE_DATA_COLLECTION_GUIDE.md` — complete planner-oriented guide;
- `HUUUGE_DATA_COLLECTION_OVERVIEW.md` — concise overview;
- `AI_DEPLOYMENT_PLAYBOOK.md` — local-AI operator contract.

A connector-verified Feishu brief is available at `https://gfok27asqq.feishu.cn/docx/ElvWduAAPoIGlVx9HdwcB5N7nye`.

The connector-verified Feishu deployment manual is available at `https://gfok27asqq.feishu.cn/docx/DSx8doLpIoI7SXxHCIoc4DQTnSb`.

## Confirmed research environment

- Windows ADB: `C:\platform-tools\adb.exe`
- BlueStacks: BlueStacks 5 China `5.22.170.6509`
- Install: `C:\Program Files\BlueStacks_nxt_cn\`
- Data root: `D:\BlueStacks_nxt_cn`
- Config: `D:\BlueStacks_nxt_cn\bluestacks.conf`
- Normal instance: `Pie64 / BlueStacks 5 / ADB 5555 / root flag 0`
- Research instance: `Pie64_1 / HuuugeResearch / ADB 127.0.0.1:5565`
- Android: 9
- BlueStacks primary ABI: `x86_64`
- Native bridge: `libnb.so` / Houdini
- Huuuge package: `com.huuuge.casino.slots`
- Huuuge ABI: `arm64-v8a`
- Current proven Huuuge version: `12.08.27100` (`versionCode=1786533240`)
- Host/Python Frida: `17.17.0`
- Matching x86_64 server: `C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64`
- Matching ARM64 Gadget: `C:\huuuge_research\tools\frida-17.17.0\frida-gadget-17.17.0-android-arm64.so`

Audited Plan-1 backup + SHA-256 manifest:

`D:\BlueStacks_nxt_cn\backups\huuuge-research\plan1_20260825_181500`

The research instance has proven real UID 0 through the audited guest-`su` patch. The normal `Pie64` root flag remains 0 and its baseline disk/config hashes were verified unchanged after the root/Frida experiments.

## Confirmed static / protocol recovery

- Primary native target: `libClawApp.so`
- Lua integration present
- Custom `.zpk` resources present
- 36 recovered Proto descriptor files
- 1028 message types assigned in the catalog
- 34 services / 356 recovered service methods
- `Casino.RpcMessage` wrapper recovered
- service/method and request/response/update mapping recovered

Local runtime descriptor source/path used by the proven environment:

`C:\huuuge_live_probe\huuuge_descriptors.pb`

## Confirmed dynamic instrumentation

The difficult instrumentation chain is complete:

```text
rooted Pie64_1
  -> root x86_64 Frida server
  -> Houdini native-bridge namespace interception
  -> ARM64 Frida Gadget
  -> libClawApp.so
  -> WriteMessage / HandleRequest / HandleResponse
  -> Casino.RpcMessage raw copy
  -> descriptor-backed JSON decode
```

`bootstrap_houdini_gadget.py` cold-spawns Huuuge, observes the real namespace used to load `libClawApp.so`, then loads the matching ARM64 Gadget through that namespace. Gadget reports `Process.arch=arm64` and exposes the ARM module view required by the hooks.

The collector keeps unrelated traffic even when a console filter is used; filters are display-only.

## Proven captures

### Proof capture

`C:\huuuge_research\captures\20260825_180346`

- 84 real RPC wrappers
- 84/84 descriptor-decoded JSON

### Broad discovery capture

`C:\huuuge_research\captures\20260825_182300`

- 741 RPC wrappers
- 741/741 decoded
- 42 unique `service.method` endpoints
- 66 direction/type-specific inventory rows
- 511 sanitized observed field-path/type rows

Observed traffic includes Slots gameplay/lobby, MiniPass, Vault, Offers/shop/purchase/reward flows, Charms, Loyalty and Progression. Raw/value-bearing capture data remains local and uncommitted.

A sanitized Slots example derived from this session contains 29 `Spin` request/response pairs (58/58 decoded) without account IDs, per-spin balances or full reel-stop arrays.

## Module structure catalog baseline

`artifacts/module_catalog/` is the current structure-first source of truth before deep numerical modeling.

- 37 independent dossiers
- 36/36 descriptor files covered
- 1028/1028 descriptor message types covered
- 356/356 recovered service methods covered
- 15 modules with live evidence
- 22 schema-only/live-pending modules
- `modules.csv`: 37 rows
- `endpoints.csv`: 356 rows
- `fields.csv`: 5292 rows

Most complete primary-live structures currently include Slots, Offers, Rewards, Player/Lobby, Other LiveOps and MiniPass.

Lottery has cross-cutting/config-only live evidence but no dedicated interactive Lottery endpoint in the broad capture. Battle Pass, generic Missions, Conquest, Sweepstakes, Adventure, Tournaments, Race, Elites, Personal Awards, Vouchers, Non-Spin Bonus and several platform/game-runtime families remain primarily schema-only/live pending.

## Planner-first deployment and operation

Planner distribution is SVN-first at `trunk/HuuugeCollector`; local publishing path is `D:\cr_design\HuuugeCollector`. GitHub `main` remains the engineering/cross-agent fact source.

Chinese SVN commit messages are supported only through the verified UTF-8 file workflow: CR `svn_submit.py`, or `svn commit --encoding UTF-8 --file`. Direct Chinese `svn commit -m` is proven to become mojibake through this host's CP936/TortoiseSVN CLI path. Revisions 6423 and 6424 were read back from UTF-8 XML with exact Chinese Unicode text. Batch launchers stay ASCII-only; Chinese PowerShell files require UTF-8 BOM.

Planner entries:

```text
HUUUGE_BOOTSTRAP.cmd  -> install/update + automatic preflight + GUI
HUUUGE_COLLECTOR.cmd  -> daily GUI
```

The GUI exposes six actions only: Start Capture, Stop/Finalize, Recent Results, Environment Check/Repair, AI Handoff, and Open Guide. It does not ask the planner to select a module or add action markers. Capture is broad and module classification happens after collection.

`scripts/huuuge_controller.ps1` now performs the deterministic lifecycle:

- verifies only `Pie64_1 / HuuugeResearch` and refuses normal `Pie64` instrumentation;
- proves real UID 0 and reuses/starts the matching root x86_64 Frida 17.17.0 server without rerooting;
- cold-starts the Houdini ARM64 Gadget and connects the lossless collector;
- requires hooks installed plus a real raw and decoded RPC before printing exactly `READY，可以开始玩了`;
- clean-stops/flushed capture and regenerates RPC inventory plus the module catalog;
- keeps local raw/value-bearing outputs out of Git/SVN.

Each Session now has `manifest.json`, machine-readable collector state, and automatic `markers.jsonl` lifecycle events (`collector-start`, `hooks-installed`, `collector-ready`, `collector-stop`). Console filters remain display-only.

`AGENT_DATA_USAGE_GUIDE.md` defines how Codex, Trae + DeepSeek or another Agent should consume the deterministic outputs. AI is optional for capture and is primarily for repair, interpretation and requested exports.

## Confirmed bootstrap / lifecycle validation

- The original CMD/PowerShell prototype was run and repaired on the proven Windows host.
- Git dirty mode preserves changes and fetches only; clean fast-forward behavior is implemented (final clean-tree run is the remaining release check).
- `.venv`, requirements, descriptor sync, BlueStacks discovery, `127.0.0.1:5565` read-only checks and `.local/bootstrap` reports all completed successfully.
- GUI `-BootstrapOnLoad` completed a real preflight while the WinForms window remained responsive.
- A fresh `.venv` bootstrap completed from `D:\cr_design\HuuugeCollector`, including the packaged schema-only descriptor; no Git checkout or AI was required.
- Git clean-tree bootstrap completed `pull --ff-only` with CMD exit code 0 and left the working tree clean.
- Git functional release `7cf574c` is pushed. SVN `trunk/HuuugeCollector` was committed at revision 6417, then its real CMD update/preflight completed at revision 6417 with exit code 0 and a clean target working copy.
- Codex executable discovery reached the WindowsApps binary but it was not runnable from this shell (`Access denied`); bootstrap records this without blocking. Trae CN is detected at `C:\Users\admin\AppData\Local\Programs\Trae CN\Trae CN.exe` and capture does not depend on either AI.
- End-to-end smoke Session `20260826_110725` reached READY and clean-stopped with 91/91 decoded RPCs. Manifest transitioned `ready -> stopped`; all four automatic lifecycle events were verified. Validation outputs stayed under `.local/controller/`.
- Current planner release is `1.0.1`. The manual opens with a plain-language product summary, calls `HuuugeResearch` a dedicated emulator newly created in BlueStacks Multi-instance Manager, contains no reverse-engineering terminology in planner instructions, and puts the official SVN ZIP link directly in section 1.
- SVN release revision `6429` carries `release/HuuugeCollector_Installer.zip` with SHA-256 `9dd5d1f31b3b076075cea4652f63dd00e0b43b78d592fb9442ef82f3ce4d4910`; its manifest records clean Git source `b4b440f38f2dacbeeb393331bf969abd2daeff70`, version `1.0.1` and the same four-file safety allowlist.
- The unchanged Bootstrap/GUI behavior remains covered by the r6427 empty-directory end-to-end install: new `.venv`, requirements and Descriptor/BlueStacks/ADB/Frida/Gadget preflight completed with exit code 0, `ready_for_gui_validation` and zero action items; no Root/host patch was run.
- The Feishu deployment manual was replaced and read back with the new introduction, dedicated-emulator wording, version 1.0.1 and direct SVN download link. Browser attachment upload was not completed because the Feishu editor interaction consistently timed out; the user may manually drag the verified ZIP into section 1 if an inline attachment is desired.
- The current Git Bootstrap additionally confirms pinned host Frida `17.17.0`, the local x86_64 server file and the research-instance ARM64 Gadget, then writes `.local/bootstrap/latest.json`; this machine reported `ready_for_gui_validation` with zero action items.
- Earlier smoke Session `20260826_103704` clean-stopped with 109/109 decoded RPCs and proved inventory/catalog finalization (38 inventory rows, 725 field paths, 37 modules).

The bootstrap and daily operation path execute no BlueStacks Root/host patch. The already deployed research environment is recognized and reused.

## TASK-0006 architecture baseline

The collector's current state has been reorganized as a reviewable architecture baseline under `docs/collector/`:

- `CURRENT_CAPABILITIES.md` separates proven, implemented-but-not-fully-validated, artifact-only and planned capabilities;
- `DATA_FLOW.md` documents deployment, passive runtime capture, descriptor decode, clean finalize and data-security boundaries;
- `MODULE_MAP.md` maps launchers, bootstrap, GUI, controller, Frida/Houdini capture, decode, inventory, catalog and release modules;
- `ROADMAP.md` starts with a mandatory ChatGPT Review gate and does not authorize feature development.

Confirmed gaps are now explicit: the complete recovered `.proto` source set is not versioned in Git, the normalized fact/event layer and module-specific extractors do not exist, Codex CLI preflight is blocked on this host, and first setup on another Windows machine still needs explicit one-time approval. Some generated dossier recommendations still refer to manual action markers even though the current GUI intentionally removed manual module/action marking; this is a documentation-consistency TODO, not a current runtime feature.

## Current blockers / missing workflow pieces

No blocker remains in the underlying RPC instrumentation or planner daily workflow.

Remaining follow-up work:

- Codex CLI safe-preflight cannot be proven on this host until a callable Codex CLI is installed; Trae + DeepSeek is the available optional AI path;
- first deployment on another Windows machine still requires SVN authentication, BlueStacks/game login, creation of a distinct research instance and explicit approval for the one-time audited Root/host patch.

## Exact next action

Resume TASK-0018 Review Round 2 and TASK-0006 review. If Shared Jackpot is investigated again later, start a new unrestricted capture in a populated machine room and preserve the first `SlotsGameClient.HitSharedJackpot` sample; correlate it with adjacent `RoomUsers` balance updates without reusing this no-hit session as evidence of payout behavior.
