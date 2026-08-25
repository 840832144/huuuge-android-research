# Huuuge Android Research

Private research workspace for reverse-engineering Huuuge Casino Android client data structures and building a passive, reusable numerical-system collector.

## Scope

The project focuses on observing the user's own test environment and extracting structured data for the broader Huuuge numerical ecosystem, including slot machines, lottery/draw systems, missions/quests, passes, milestones, live events, offers, rewards, progression and other systems discovered through runtime RPCs or client data.

**Battle Pass is only the first end-to-end validation target. It is not the final scope.**

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

Console filters may reduce noise, but the underlying capture should retain all observable RPCs, including unknown/undecoded messages, so later analysis does not require repeating the same gameplay session unnecessarily.

See `RESEARCH_DATA_ARCHITECTURE.md` for the full capture/model/presentation design.

The current structure-first map is in `artifacts/module_catalog/MODULE_INDEX.md`. It should be enriched after each new capture before any one module is treated as the global priority.

The workflow does **not** modify balances, rewards, requests, or server state.

## Start here

1. Read `CURRENT_STATUS.md` for the live project state.
2. Read `HUUUGE_CODEX_HANDOFF.md` for the technical handoff and prior findings.
3. Read `RESEARCH_DATA_ARCHITECTURE.md` for the full-system data strategy.
4. Read `AGENTS.md` and `CONTRIBUTING.md` for collaboration rules between ChatGPT and Codex.
5. Read the newest entries in `COLLAB_LOG.md` before changing anything.

## Key artifacts

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

This generates `artifacts/live_probe/huuuge_descriptors.pb`, which is intentionally not committed because it is fully reproducible from the recovered schemas.
