# Changelog

All notable project/tooling changes are recorded here. Operator-specific investigative details belong in `COLLAB_LOG.md`.

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
