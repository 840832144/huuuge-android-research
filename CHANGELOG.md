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

### Changed

- `AGENTS.md` now requires every agent to read and follow `CONTRIBUTING.md`, preserve unrelated work, update all applicable coordination files, push before handoff, and avoid destructive/shared-history rewrites.
- `check_device.ps1` now targets an explicit ADB serial, reports native-bridge/root evidence, and no longer runs the state-changing `adb root` test implicitly.
- `start_frida_server.ps1` now targets an explicit serial, enforces matching host/server Frida versions, requires a verified UID-0 launcher, and supports an explicitly labeled unprivileged diagnostic mode.
- `live_decode.py` now accepts `--device-id` so the research clone can be selected deterministically when multiple ADB devices exist.
- Live-probe documentation now distinguishes process enumeration from successful attach and documents BlueStacks whitelist-gated `su` behavior.

### Current architecture direction

- Prefer passive high-level `Casino::Connection` / `Casino::RpcMessage` instrumentation over video OCR and TLS MITM.
- Prefer an isolated BlueStacks research clone for root/Frida experiments.
