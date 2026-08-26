# Current Status

_Last updated: 2026-08-26 by ChatGPT_

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

**Easy deployment and low-operation use are now first-class project requirements.** A planner should not need to manually manage ADB, Frida, Houdini or Protobuf details when scripts/local AI can do so.

Primary human documentation:

- `HUUUGE_DATA_COLLECTION_GUIDE.md` — complete planner-oriented guide;
- `HUUUGE_DATA_COLLECTION_OVERVIEW.md` — concise overview;
- `AI_DEPLOYMENT_PLAYBOOK.md` — local-AI operator contract.

A connector-verified Feishu brief is available at `https://gfok27asqq.feishu.cn/docx/ElvWduAAPoIGlVx9HdwcB5N7nye`.

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
- Proven Huuuge version: `12.07.27012` (`versionCode=1784198526`)
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

## Planner-first deployment prototype

New intended Windows entry:

```text
HUUUGE_BOOTSTRAP.cmd
```

In-repo implementation:

```text
scripts/huuuge_bootstrap.ps1
```

The current bootstrap prototype safely:

- locates/creates the repo workspace when launched through the CMD entry;
- clones or fast-forward updates Git when safe;
- preserves a dirty working tree and fetches instead of overwriting it;
- creates `.venv` and installs live-probe requirements;
- syncs/builds the descriptor set when possible;
- runs BlueStacks discovery;
- performs a read-only check of the known research ADB target when available;
- writes machine-local reports under `.local/bootstrap/`;
- when `codex` exists, runs a non-interactive documentation-aware **safe preflight** using `AI_DEPLOYMENT_PLAYBOOK.md`.

The bootstrap deliberately does **not** silently perform BlueStacks root/host patching or other machine-level changes.

One-time explicit human actions remain:

1. private GitHub authentication on a new machine;
2. Codex/local-AI first login;
3. approval before first BlueStacks root/host patch with backup/rollback scope shown.

## Validation status of the new bootstrap

The documentation and bootstrap prototype are committed, but **the new CMD/PowerShell bootstrap has not yet been executed end-to-end on the proven Windows host by ChatGPT**. This environment does not provide Windows PowerShell runtime validation.

Therefore the bootstrap must currently be treated as **prototype / pending local Windows validation**, not yet as a production one-click installer.

Codex should validate it on the proven machine before the project claims full self-service deployment.

## Current blockers / missing workflow pieces

No blocker remains in the underlying RPC instrumentation chain.

The current productization gaps are:

- Windows end-to-end validation/fix of `HUUUGE_BOOTSTRAP.cmd` + `scripts/huuuge_bootstrap.ps1`;
- automatic session `manifest.json`;
- lightweight action/context markers;
- planner-facing daily `Start Capture` action that verifies hooks/files then prints `READY`;
- planner-facing `Stop / Finalize` action that flushes the session, rebuilds inventory and refreshes the module catalog.

## Exact next action

1. Codex pulls latest `main` on the proven Windows machine.
2. Codex reads `HUUUGE_DATA_COLLECTION_GUIDE.md` and `AI_DEPLOYMENT_PLAYBOOK.md`.
3. Run `HUUUGE_BOOTSTRAP.cmd` end-to-end against the already-working research environment.
4. Fix any CMD/PowerShell/path/Codex-preflight problems and record validation evidence.
5. Once bootstrap is stable, add the daily planner workflow: Start -> `READY` -> normal play -> Stop/Finalize -> inventory/catalog refresh.
6. Add manifest/markers before calling the daily flow fully self-service.
7. Continue enriching the same 37 module dossiers from future captures; do not force a single deep model until the user selects it.
