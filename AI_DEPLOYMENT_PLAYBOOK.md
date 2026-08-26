# Local AI Deployment Playbook

This file is the handoff contract for a computer-local AI agent (Codex, Trae + DeepSeek, or another approved local operator) that is asked to deploy, verify, repair, or operate the Huuuge data-collection environment. AI is optional for deterministic capture/finalization.

## Goal

Make the workflow easy for a game designer / analyst. The human should not be asked to manually shuttle terminal commands or interpret low-level Frida/ADB output when the local AI can inspect and act directly.

## Mandatory reading order

Before changing anything, read:

1. `AGENTS.md`
2. `CONTRIBUTING.md`
3. `HUUUGE_DATA_COLLECTION_GUIDE.md`
4. `AGENT_DATA_USAGE_GUIDE.md`
5. `CURRENT_STATUS.md`
6. latest `COLLAB_LOG.md`
7. `TASKS.md`
8. `CHANGELOG.md`
9. relevant files under `artifacts/live_probe/`

## Safety boundary

- Never instrument or root the user's normal `Pie64 / BlueStacks 5` instance.
- Use only the isolated research instance (`Pie64_1 / HuuugeResearch`) unless the current machine uses a newly documented research instance.
- Do not modify balances, rewards, gameplay outcomes, requests, or server state.
- Do not forge/replay requests for advantage.
- Do not commit account IDs, session identifiers, APKs, proprietary `.so` files, Frida binaries, secrets or raw value-bearing captures.
- Before any BlueStacks host binary / VHDX / root modification, show the exact scope, backup path and rollback plan and obtain explicit user approval.

## Deployment state machine

Treat deployment as a state machine. Determine the highest completed state; do not repeat lower-level changes unnecessarily.

### S0 — Project package available

Verify:

- planner deployment is updated from company SVN `trunk/HuuugeCollector`;
- engineering/cross-agent changes remain mirrored in GitHub `840832144/huuuge-android-research` `main`;
- local changes in either working copy are preserved rather than overwritten.

### S1 — Host prerequisites

Verify/detect:

- Windows;
- Git;
- Python / `py`;
- ADB;
- BlueStacks install/data/config paths;
- Huuuge package/APK availability;
- local recovered descriptor or recoverable Proto source;
- optional Codex installation/auth state.

Prefer existing scripts:

```powershell
.\scripts\discover_bluestacks.ps1
.\scripts\sync_local_runtime.ps1
```

Do not hard-code paths when discovery can resolve them.

### S2 — Isolated research instance

Verify a dedicated research instance exists and is distinct from the normal instance.

Expected proven environment:

```text
normal:   Pie64   / BlueStacks 5     / ADB 5555 / root flag 0
research: Pie64_1 / HuuugeResearch   / ADB 5565
```

If a research instance does not exist, create/clone one through the safest available supported BlueStacks mechanism. Preserve the normal instance.

### S3 — Research root

Root success means an actual command returns:

```text
uid=0(root)
```

Flags, properties, existence of `su`, or process enumeration do not count.

For BlueStacks China `5.22.170.6509`, the previously audited approach is documented in:

```text
artifacts/recovered/BlueStacks_Root_GUI_audit.md
```

Do not blindly rerun patch logic. First compare version/signatures/scope against the current machine.

Before writes:

- power off research instance;
- verify virtual disk state is stable;
- back up every host/config/disk target;
- record SHA-256 source/backup equality;
- baseline normal-instance relevant hashes.

After writes:

- verify research `su -c id` -> UID 0;
- verify normal-instance root flag/data hashes remain unchanged where applicable;
- record rollback path.

### S4 — x86_64 root Frida server

Use Frida host/server versions that match exactly.

In the proven x86_64 BlueStacks guest, the root server architecture is x86_64 even though the Huuuge APK contains ARM64 native code.

Reuse:

```text
artifacts/live_probe/start_frida_server.ps1
```

Prove real attach/detach, not just process enumeration.

### S5 — ARM64 Houdini Gadget

Because Huuuge native code is ARM64 under Houdini, x86_64 Frida module enumeration is insufficient.

Use the matching ARM64 Frida Gadget staged only in the research environment and reuse:

```text
artifacts/live_probe/bootstrap_houdini_gadget.py
```

The correct path is:

1. cold-spawn Huuuge;
2. intercept the real native-bridge namespace used to load `libClawApp.so`;
3. load ARM64 Gadget through that namespace;
4. Gadget must report `Process.arch=arm64`;
5. Gadget must enumerate `libClawApp.so`.

Do not retry guessed namespaces after the real namespace can be observed.

### S6 — Collector

Use:

```text
artifacts/live_probe/live_decode.py
artifacts/live_probe/agent.js
```

The ARM64 Gadget connection is logically distinct from the x86_64 root-server connection.

Expected Gadget collector form:

```powershell
py artifacts\live_probe\live_decode.py `
  --remote-endpoint 127.0.0.1:27043 `
  --process Gadget
```

Console filters may be added for readability but must not narrow the saved dataset.

### S7 — Proof capture

Before telling the human that the environment is READY, prove:

- hooks installed (`WriteMessage`, `HandleRequest`, `HandleResponse`);
- at least one real `Casino.RpcMessage` saved;
- raw file exists;
- decoded JSON exists;
- service/method resolution works;
- descriptor loading works;
- no capture writes are directed at Git-tracked sensitive paths.

### S8 — Research-ready

Only after S7 say:

```text
READY — 可以开始正常玩，采集已启动。
```

Keep the wording simple for the planner.

## Normal capture workflow

When asked to start a session:

1. update the planner package from SVN safely (engineering agents also pull latest Git);
2. verify existing deployed states instead of rerooting/reinstalling;
3. start/verify research instance;
4. start/verify root Frida server if required;
5. cold-spawn through Houdini bootstrap;
6. connect ARM64 Gadget collector;
7. verify files are incrementally written;
8. report exactly `READY，可以开始玩了`;
9. let user play normally.

When asked to stop:

1. stop collector cleanly;
2. ensure buffers/files are flushed;
3. record session path;
4. generate inventory with `scripts/build_rpc_inventory.py`;
5. regenerate module catalog with `scripts/build_module_catalog.py`;
6. keep raw/value-bearing data local;
7. commit only sanitized tooling/structure/results;
8. tell the human where the deterministic inventory/catalog outputs are; use AI only when an interpretation is requested.

## Human interaction policy

Ask the human only for things the local AI cannot safely resolve itself, such as:

- first GitHub authentication;
- first Codex/AI login;
- explicit approval before machine-level BlueStacks root/host patch;
- game UI actions that cannot be automated safely;
- choosing which module to deeply model after broad capture.

Do not ask the human to paste long PowerShell/ADB output when you can run/read it locally.

## Reporting style for planners

Prefer:

```text
环境：READY
采集：运行中
本次 Session：2026xxxx_xxxxxx
已捕获：xxx 条 RPC
新增模块证据：Slots / Lottery / Missions
需要补充：Conquest / Battle Pass
```

Avoid dumping raw stack traces unless there is a blocker.

## Repository coordination

Follow `CONTRIBUTING.md` exactly. Git is the cross-agent source of truth; planner-facing package changes must also be mirrored to `trunk/HuuugeCollector` in SVN.

Every meaningful deployment/repair/capture session must leave enough evidence in Git for ChatGPT/Codex to continue without chat history.
