# Huuuge Android Research

Private research workspace for reverse-engineering Huuuge Casino Android client data structures and building a passive, reusable numerical-system collector.

## Scope

The project focuses on observing the user's own test environment and extracting structured data for the broader Huuuge numerical ecosystem, including slot machines, lottery/draw systems, missions/quests, passes, milestones, live events, offers, rewards, progression and other systems discovered through runtime RPCs or client data.

**Battle Pass is only one validation target. It is not the final scope.**

The desired architecture is:

```text
capture broadly / preserve raw evidence
        ↓
decode + normalize by system
        ↓
build reusable numerical models
        ↓
export only the requested system/view on demand
```

The workflow does **not** modify balances, rewards, requests, or server state.

## Planner / analyst start here

The project now treats **easy deployment and low-operation use** as a core requirement.

On Windows, the intended planner-facing entry is:

```text
HUUUGE_BOOTSTRAP.cmd
```

The bootstrap safely creates/updates the local workspace, prepares the Python environment, syncs runtime artifacts, checks BlueStacks/ADB, and—when Codex CLI is available—hands the repository to the local AI for a documentation-aware deployment preflight.

It deliberately does **not** silently perform BlueStacks root/host patching. First GitHub/Codex authentication and the first machine-level root/host change remain explicit one-time approvals.

Read in this order:

1. `HUUUGE_DATA_COLLECTION_GUIDE.md` — complete planner-oriented deployment, capture and capability guide.
2. `HUUUGE_DATA_COLLECTION_OVERVIEW.md` — concise Chinese experiment/environment overview.
3. `AI_DEPLOYMENT_PLAYBOOK.md` — local-AI deployment/repair/operation contract.
4. `CURRENT_STATUS.md` — canonical live project state.
5. `artifacts/module_catalog/MODULE_INDEX.md` — current structure-first map of Huuuge systems.
6. `AGENTS.md` / `CONTRIBUTING.md` / latest `COLLAB_LOG.md` — collaboration rules for ChatGPT/Codex.

## Key artifacts

- `HUUUGE_BOOTSTRAP.cmd` — Windows one-click bootstrap entry; can clone the private repository when distributed as a standalone file and otherwise runs the in-repo bootstrap.
- `scripts/huuuge_bootstrap.ps1` — safe bootstrap/preflight logic; writes machine-local reports under `.local/bootstrap/`.
- `HUUUGE_DATA_COLLECTION_GUIDE.md` — complete deployment/use guide with planner-first operating model.
- `HUUUGE_DATA_COLLECTION_OVERVIEW.md` — concise Chinese overview of the experiment environment, deployment chain, capture workflow, capabilities and validation results.
- `AI_DEPLOYMENT_PLAYBOOK.md` — state-machine handoff for a local AI such as Codex CLI.
- `artifacts/recovered/` — recovered proto schemas, RPC mappings, and schema notes.
- `artifacts/live_probe/` — Frida hook and protobuf live decoder.
- `artifacts/module_catalog/` — 37 module dossiers plus sanitized module/endpoint/field tables spanning the full recovered schema and current live session.
- `MODULE_STRUCTURE_CATALOG.md` — structure-first dossier contract and maintenance priority.
- `RESEARCH_DATA_ARCHITECTURE.md` — lossless capture, normalization, system-model and on-demand presentation contract.
- `scripts/build_descriptors.py` — rebuilds `huuuge_descriptors.pb` from the recovered `.proto` files.
- `CHANGELOG.md` — project/tooling change history.
- `COLLAB_LOG.md` — operator-by-operator work log and handoff trail.
- `CURRENT_STATUS.md` — canonical current state and next action.
- `TASKS.md` — active milestone checklist.

## Local files not committed

Large APKs remain on the user's Windows machine and should not be committed:

- `C:\huuuge_apk\base.apk`
- `C:\huuuge_apk\split_config.arm64_v8a.apk`
- `C:\huuuge_apk\split_config.hdpi.apk`
- `C:\huuuge_apk\split_config.zh.apk`

The existing local probe path is expected at `C:\huuuge_live_probe` if it still exists.

Runtime captures, account/session identifiers, APKs, native binaries, Frida binaries and other sensitive/generated artifacts remain local per `.gitignore` and `CONTRIBUTING.md`.

## Rebuild descriptor set

After installing the live-probe requirements:

```powershell
py -m pip install -r artifacts\live_probe\requirements.txt
py scripts\build_descriptors.py
```

This generates `artifacts/live_probe/huuuge_descriptors.pb`, which is intentionally not committed because it is reproducible from the recovered schemas.
