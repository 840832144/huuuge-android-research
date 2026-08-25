# Collaboration Log

Append-only work log for ChatGPT, Codex, and user-driven environment changes.

---

## 2026-08-25 — ChatGPT — Initial reverse-engineering handoff

**Objective**

Replace unreliable video/OCR-based Huuuge Casino activity research with structured client data collection.

**Actions**

- Connected to BlueStacks through ADB and identified package `com.huuuge.casino.slots`.
- Pulled base and split APKs from the user's BlueStacks installation.
- Analyzed `base.apk` and `split_config.arm64_v8a.apk`.
- Identified `libClawApp.so` as the main native analysis target.
- Confirmed Lua integration and a custom `.zpk` resource ecosystem.
- Recovered serialized protobuf descriptors from the native binary.
- Reconstructed 36 `.proto` schemas and generated a descriptor set.
- Reconstructed RPC service/method mappings.
- Recovered Battle Pass milestone/mission/update field structures.
- Designed a passive Frida hook around `Casino::Connection::WriteMessage`, `HandleRequest`, and `HandleResponse`.
- Created `agent.js` and `live_decode.py` to serialize/copy `Casino::RpcMessage` and decode payloads through the recovered descriptors.
- Tested BlueStacks root/debug state: current instance has working ADB but no usable root or `su`; `run-as` is unavailable.

**Confirmed results**

- Android: 9.
- Emulator ABI list: `x86_64,x86,arm64-v8a,armeabi-v7a,armeabi`.
- Huuuge `primaryCpuAbi=arm64-v8a`.
- Current normal instance: ADB-accessible but not rootable through the tested `adb root` path.
- `libClawApp.so` contains protobuf-generated symbols/descriptors and Lua integration.
- 36 protobuf schema descriptors recovered successfully.

**Current blocker**

Dynamic Frida attach has not yet been established because the existing BlueStacks instance lacks usable root. BlueStacks installation/data paths also differ from assumed defaults and must be discovered automatically.

**Files produced**

- `HUUUGE_CODEX_HANDOFF.md`
- `CODEX_KICKOFF_PROMPT.md`
- `artifacts/recovered/*`
- `artifacts/live_probe/*`

**Next recommended action**

Codex should automatically discover the real BlueStacks install/data/config paths, identify or create an isolated research clone, validate the native bridge/runtime architecture, and establish Frida attach without modifying the user's normal instance.

---

## 2026-08-25 — ChatGPT — GitHub workspace bootstrap

**Objective**

Make GitHub the shared source of truth so ChatGPT and Codex can see each other's work without relying on chat history.

**Actions**

- Confirmed private repository `840832144/huuuge-android-research`.
- Added `README.md`, `AGENTS.md`, `CHANGELOG.md`, `CURRENT_STATUS.md`, this `COLLAB_LOG.md`, the full Codex handoff, and Codex kickoff instructions.
- Added the passive live probe implementation: `agent.js`, `live_decode.py`, device/root check helper, Frida-server starter, and requirements.
- Added recovered Battle Pass and `Casino.RpcMessage` schema notes.
- Added `scripts/sync_local_runtime.ps1` so Codex can automatically reuse the existing local `C:\huuuge_live_probe\huuuge_descriptors.pb` and APK directory without asking the user to repeat prior setup.
- Added `.gitignore` rules preventing APKs, native `.so` binaries, runtime captures, Frida binaries, and generated descriptor binaries from being committed accidentally.

**Repository coordination rule**

- Before work: pull, read `CURRENT_STATUS.md` and latest `COLLAB_LOG.md`.
- After work: append `COLLAB_LOG.md`, update `CURRENT_STATUS.md`, and update `CHANGELOG.md` when tooling/schema/workflow changes.
- Commit the code and its handoff record together whenever practical.

**Known repository gap**

The full recovered 36-file `.proto` source set and generated `huuuge_descriptors.pb` are not yet fully versioned as individual Git files. The descriptor already exists locally at `C:\huuuge_live_probe\huuuge_descriptors.pb` and is enough for the current live decoder; Codex should sync/use that local file immediately and may later version the recovered proto source set in a dedicated commit.

**Next recommended action**

Codex should clone/pull this repository, run `scripts\sync_local_runtime.ps1`, then continue from the BlueStacks discovery/root/Frida milestone recorded in `CURRENT_STATUS.md`.

---

## 2026-08-25 — ChatGPT — Modification and commit governance

**Objective**

Make ChatGPT/Codex changes auditable and prevent one agent from silently overwriting, rebasing away, or obscuring the other agent's work.

**Actions**

- Added `CONTRIBUTING.md` as the mandatory modification and commit standard.
- Updated `AGENTS.md` to require reading/following `CONTRIBUTING.md` before work.
- Defined safe sync, minimal-scope modification, validation, logging, commit-message, push, conflict-resolution, and handoff requirements.
- Explicitly prohibited force-pushing shared `main`, rewriting another agent's pushed history, destructive reset/clean operations on shared work, and blind conflict resolution.
- Defined files that must remain local/untracked, including APKs, proprietary native binaries, Frida binaries, secrets, and unsanitized account/session captures.

**Confirmed results**

- Repository now has an explicit cross-agent modification/submission contract rather than relying only on informal chat instructions.
- Every meaningful session must leave evidence in `COLLAB_LOG.md` and current facts in `CURRENT_STATUS.md`, with `CHANGELOG.md`/`TASKS.md` updated when applicable.

**Files changed**

- `CONTRIBUTING.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `COLLAB_LOG.md`

**Validation**

- Verified the repository files exist on `main` and the coordination rules are mutually consistent.

**Next recommended action**

Codex should pull `main`, read `AGENTS.md` and `CONTRIBUTING.md` first, then continue from `CURRENT_STATUS.md`/`TASKS.md` and record/push its own work under the same protocol.
