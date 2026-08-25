# Huuuge Android Research

Private research workspace for reverse-engineering Huuuge Casino Android client data structures and building a passive activity/system value collector.

## Scope

The project focuses on observing the user's own test environment and extracting structured activity/system data such as milestones, missions, rewards, passes, offers, and event configuration. It does **not** modify balances, rewards, requests, or server state.

## Start here

1. Read `CURRENT_STATUS.md` for the live project state.
2. Read `HUUUGE_CODEX_HANDOFF.md` for the technical handoff and prior findings.
3. Read `AGENTS.md` for collaboration rules between ChatGPT and Codex.
4. Read the newest entries in `COLLAB_LOG.md` before changing anything.

## Key artifacts

- `artifacts/recovered/` — recovered proto schemas, RPC mappings, and schema notes.
- `artifacts/live_probe/` — Frida hook and protobuf live decoder.
- `scripts/build_descriptors.py` — rebuilds `huuuge_descriptors.pb` from the recovered `.proto` files.
- `CHANGELOG.md` — user-facing/project change history.
- `COLLAB_LOG.md` — operator-by-operator work log and handoff trail.
- `CURRENT_STATUS.md` — canonical current state and next action.

## Local files not committed

Large APKs remain on the user's Windows machine and should not be committed:

- `C:\huuuge_apk\base.apk`
- `C:\huuuge_apk\split_config.arm64_v8a.apk`
- `C:\huuuge_apk\split_config.hdpi.apk`
- `C:\huuuge_apk\split_config.zh.apk`

The existing local probe path is expected at `C:\huuuge_live_probe` if it still exists.

## Rebuild descriptor set

After installing the live-probe requirements:

```powershell
py -m pip install -r artifacts\live_probe\requirements.txt
py scripts\build_descriptors.py
```

This generates `artifacts/live_probe/huuuge_descriptors.pb`, which is intentionally not committed because it is fully reproducible from the recovered schemas.
