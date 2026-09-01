# Changelog

All notable project/tooling changes are recorded here. Operator-specific investigative details belong in `COLLAB_LOG.md`.

## 2026-09-01

### Added

- Big Fish passive HTTP-JSON capture now reaches READY: the JS collector is verified through the logcat `Cobra Log` tag (`collector-already-installed` receipts observed) instead of the `cocos2d::log` export, which is a no-op under Cocos `DebugMode.NONE`.
- `bigfish_capture.py` now supports `--mode logcat` (default): streams ADB logcat and parses tagged `__CODEX_BIGFISH_HTTP_V1__` events locally (events.jsonl + one JSON per HTTP event). `--mode frida` optionally re-injects agent.js to guarantee collector installation and emit the receipt.
- Static confirmation of the same-room shared-win feature strings in `SALocalizationService.js`: `youHitScatter`, `otherPlayerHitScatter`, `foundTreasureForYou`, `EveryoneElseGets`, `YouFoundTreasure`, `bigBooty`.

### Fixed

- Big Fish transport: the collector previously hooked `cocos2d::log`, which never received events; the events flow through `cc.log`/`console.log` into logcat tags `Cobra Log` and `cocos2d-x debug info`.

### Changed

- TASK-0020 status updated from "not READY" to READY with an ordinary request/response pair validated (mission/characters/vip/alerts/booster/inbox/sparkle_lobby). Next step is normal play to capture the shared-win endpoint.

### Fixed

- Controller startup now tolerates the expected ADB `device not found` state long enough to launch only `Pie64_1 / HuuugeResearch` instead of aborting before its auto-start branch.
- Added a bounded `frida-ps` Gadget handshake before the lossless collector connects, preventing the transient `connection closed` race during Houdini `on_load=wait` startup.
- Bootstrap and controller now require both the ARM64 Gadget binary and `libhuuuge-gadget.config.so`; an app update can no longer leave a false-ready Gadget state with the configured `27043` endpoint missing.
- Collector state counters now refresh after READY instead of remaining frozen at the first decoded RPC while capture files continue to grow.

### Changed

- Validated the passive collector on research-instance Huuuge `12.08.27100` after a rollback-backed Google Play update; the normal BlueStacks instance remains untouched.
- Finalized capture `20260901_160002` into a 92-row sanitized RPC inventory, 1313 observed field paths and an updated 37-module catalog (21 live-confirmed, 16 schema-only). The Shared Jackpot endpoint remains schema-only with zero observed samples.
- Inventory summaries now derive manifest/lifecycle-marker facts from each Session, label undecoded rows accurately and avoid stale hard-coded claims about missing systems or manual markers.

## 2026-08-27

### Fixed

- Addressed TASK-0018 Review Round 1 with a planner-first Chinese report structure, Chinese evidence labels, ordinary chip-bet terminology and a technical-only description of the 117.516 output/cost ratio.
- Replaced the original Feishu document in place, removed the duplicate body title, repaired section ordering and verified complete readback plus company-editable permission.

### Added

- Added sanitized `PURCHASES.csv` output and local purchase-chain extraction for four successful real-money purchases, including amount, currency, ticket grant, other bundle rewards and caveated apparent per-ticket cost without exposing request, product, store or order identifiers.
- Added regression tests for purchase extraction, incomplete-chain fail-closed behavior, ordinary-spin public naming and bundle other-reward caveats; the suite now contains seven tests.

### Added

- TASK-0018 Chinese Lottery numerical report with playflow, evidence matrix, data dictionary, CR candidates and six sanitized CSV outputs under `reports/lottery/20260827_lottery-ticket-puzzle/`.
- Reproducible `tools/analysis/lottery/extract_lottery_facts.py` for Finalize validation, Lottery/Spin pairing, B0 normalization, ticket-ledger reconciliation, reward aggregation and upgrade-linked state-transition detection.
- Focused unit tests for reward classification, unsigned big-number decoding, percentile interpolation and Wilson confidence intervals.

### Changed

- Regenerated the 37-module catalog from finalized capture alias `LOT-20260827-A`; real Session identifiers and value-bearing analysis remain local.
- Lottery now has 692 primary live samples and a 90/100 structure/numerical baseline. The report explicitly separates direct Toss rewards from upgrade-linked ticket outcomes.
- Updated status, tasks and Codex handoff for ChatGPT Review. No collector runtime, CR repository, SVN package, game or server state was changed.

## 2026-08-26

### Added

- TASK-0006 architecture baseline under `docs/collector/`: status-qualified capability inventory, end-to-end data flow, software module relationship map and review-gated TODO Roadmap.
- Product release `1.0.0` with `HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md`, a planner-only install/update/capture/data/AI/FAQ manual.
- Reproducible `scripts/build_installer_package.ps1` outputting `HuuugeCollector_Installer.zip` with a machine-readable version/source/safety/file-hash manifest.
- Connector-verified Feishu edition of the deployment manual at `https://gfok27asqq.feishu.cn/docx/DSx8doLpIoI7SXxHCIoc4DQTnSb`.
- Native Windows planner GUI and controller with six actions: Start, Stop/Finalize, Recent Results, Environment Check/Repair, optional AI Handoff and Open Guide.
- `HUUUGE_COLLECTOR.cmd` daily launcher and SVN-first `HUUUGE_BOOTSTRAP.cmd` install/update flow.
- Session `manifest.json`, machine-readable collector state, clean stop control and automatic lifecycle `markers.jsonl` events.
- Deterministic Stop/Finalize pipeline that regenerates RPC inventory/field paths and the 37-module catalog while keeping raw values local.
- `scripts/sync_svn_package.ps1` with a safe planner-package allowlist and internal schema-only descriptor distribution.
- `AGENT_DATA_USAGE_GUIDE.md` for Codex, Trae + DeepSeek and other Agents to consume outputs with evidence/privacy discipline.

### Changed

- Replaced the obsolete pre-root Codex handoff with the current release `1.0.1` architecture, confirmed gaps, review state and exact next action; no collector behavior changed.
- Deployment manual `1.0.1` now opens with a plain-language product summary, calls `HuuugeResearch` a dedicated BlueStacks emulator created through Multi-instance Manager, removes reverse-engineering terminology from planner instructions, and places the official SVN package download link directly under “1. 你会拿到什么”.
- GUI “Open Guide” now opens the product-facing deployment manual; the SVN publisher builds the ready-to-distribute installer ZIP under `release/`.
- Bootstrap now adds read-only pinned Frida/server/Gadget checks and writes `.local/bootstrap/latest.json` with `ready_for_gui_validation` or actionable missing items.
- Collaboration rules now allow Chinese SVN messages only through an UTF-8 message file/Python submit workflow with XML readback; direct Chinese `svn commit -m` remains forbidden. Batch launchers stay ASCII-only and Chinese Windows PowerShell files use UTF-8 BOM.
- Bootstrap now supports Git, SVN or no-source preflight modes, clean/dirty working-copy preservation, optional Codex/Trae selection and non-interactive validation.
- Houdini bootstrap reports `gadget-load-started` before the Gadget's `on_load=wait` connection point, avoiding a launcher/collector deadlock.
- `live_decode.py` publishes READY only after hooks plus a real decoded RPC and explicitly records that console filters are display-only.
- Manual module/action marker controls were removed from the planner workflow; module classification is automatic after unrestricted capture.
- Planner distribution is mirrored to company SVN `trunk/HuuugeCollector`; Git remains the canonical engineering collaboration history.

## 2026-08-25

### Added

- Initial Huuuge Android research repository structure.
- Full technical handoff from the ChatGPT investigation.
- Recovered protobuf descriptor set and 36 recovered `.proto` schemas.
- Service/method RPC mapping and Battle Pass schema notes.
- Initial Frida live probe (`agent.js`) and protobuf decoder (`live_decode.py`).
- Collaboration protocol (`AGENTS.md`), canonical status (`CURRENT_STATUS.md`), and shared operator log (`COLLAB_LOG.md`).
- `CONTRIBUTING.md` with mandatory modification, validation, commit, push, conflict-resolution, and handoff rules for ChatGPT/Codex collaboration.
- Read-only `scripts/discover_bluestacks.ps1` for registry-derived install/data/config discovery and sanitized instance inventory.
- `RESEARCH_DATA_ARCHITECTURE.md` defining lossless broad capture, normalized interpretation, system-specific extractors and on-demand presentation for slots, lottery, missions, passes/events, offers/economy and future systems.
- Audited BlueStacks root scope/rollback evidence for the exact China `5.22.170.6509` environment.
- `bootstrap_houdini_gadget.py` to cold-spawn the ARM-translated client, reuse its real native-bridge namespace, and load an already-staged ARM64 Gadget before startup RPC traffic.
- `scripts/build_rpc_inventory.py` to reproducibly convert a local `live_decode.py` session into a value-free service/method/message inventory, heuristic system classification, aggregate coverage summary, and protobuf field-path/type inventory.
- Sanitized discovery artifacts for the unrestricted `20260825_182300` session under `artifacts/analysis/20260825_182300/`; the 741 raw wrappers and decoded values remain local and excluded from Git.
- `MODULE_STRUCTURE_CATALOG.md` as the structure-first dossier contract and catalog maintenance priority.
- `scripts/build_module_catalog.py` plus `artifacts/module_catalog/module_specs.json` to reproducibly combine descriptor, sanitized live, local-only variability and APK ZPK evidence.
- A 37-dossier module catalog covering 36/36 proto files, 1028/1028 descriptor messages, 356/356 service methods, 741 live samples and sanitized module/endpoint/field tables.
- `HUUUGE_DATA_COLLECTION_OVERVIEW.md`, a concise Chinese overview of the experiment environment, deployment architecture, capture workflow, capabilities, validation results and limitations.
- A connector-verified Feishu cloud-document edition of the concise overview, including a sanitized 29-spin live-data example without account identifiers, per-spin balances or full reel-stop values.
- `HUUUGE_DATA_COLLECTION_GUIDE.md`, the complete planner-oriented deployment/capture/capability guide with easy-deployment and low-operation use as explicit project requirements.
- `AI_DEPLOYMENT_PLAYBOOK.md`, a state-machine handoff for a computer-local AI to deploy/verify/repair the collector without asking planners to operate low-level ADB/Frida steps.
- `HUUUGE_BOOTSTRAP.cmd`, the intended Windows one-click entry for locating/cloning the private repo and launching safe bootstrap/preflight.
- `scripts/huuuge_bootstrap.ps1`, which safely updates a clean repo, creates an isolated Python venv, installs requirements, syncs/builds descriptors, runs BlueStacks/ADB discovery, writes `.local/bootstrap/` reports, and invokes a documentation-aware Codex preflight when available.

### Changed

- `AGENTS.md` now requires every agent to read and follow `CONTRIBUTING.md`, preserve unrelated work, update all applicable coordination files, push before handoff, and avoid destructive/shared-history rewrites.
- `check_device.ps1` now targets an explicit ADB serial, reports native-bridge/root evidence, and no longer runs the state-changing `adb root` test implicitly.
- `start_frida_server.ps1` now targets an explicit serial, enforces matching host/server Frida versions, requires a verified UID-0 launcher, and supports an explicitly labeled unprivileged diagnostic mode.
- `live_decode.py` now accepts `--device-id` so the research clone can be selected deterministically when multiple ADB devices exist.
- `live_decode.py` now accepts a Frida `--remote-endpoint` and explicit `--process`, enabling the decoder to attach to an ARM64 Gadget inside the x86_64 Houdini process.
- Live-probe documentation now distinguishes process enumeration from successful attach and documents BlueStacks whitelist-gated `su` behavior.
- Project scope is explicitly broader than Battle Pass: Battle Pass is only the first end-to-end validation target. The base collector must retain unrelated and unknown RPC traffic so later slot/lottery/mission/event/economy analysis can reuse the same raw sessions.
- `README.md`, `CURRENT_STATUS.md`, and `TASKS.md` now reflect the capture → normalize → system-specific export architecture.
- Live-probe documentation now covers the split x86_64 root-server / ARM64 Gadget workflow required by BlueStacks native translation.
- Project priority now favors broad module-structure coverage and incremental dossier enrichment before deep RTP, EV, purchase-value or other single-system modeling.
- `README.md` now makes the complete planner guide and one-click bootstrap the primary entry rather than requiring the operator to understand the technical handoff first.
- Easy deployment / low-operation use is now a first-class architecture goal. Safe steps should be automated; GitHub/Codex first login and BlueStacks machine-level root/host changes remain explicit one-time approvals.

### Current architecture direction

- Prefer passive high-level `Casino::Connection` / `Casino::RpcMessage` instrumentation over video OCR and TLS MITM.
- Prefer an isolated BlueStacks research clone for root/Frida experiments.
- Capture broadly and losslessly; use filters only for console/readability, not data retention.
- Preserve raw bytes and version/session metadata so interpretations and schemas can be corrected later.
- Build system-specific numerical views downstream rather than hard-coding the collector around one feature.
- Hide ADB/Frida/Proto complexity behind a planner-facing bootstrap and local-AI operator wherever practical.
