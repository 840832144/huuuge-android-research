# Agent Collaboration Rules

This repository is shared by ChatGPT and Codex. Treat the Git repository as the source of truth for cross-agent coordination.

## Before doing work

1. `git pull` the latest default branch.
2. Read `CURRENT_STATUS.md`.
3. Read the newest section of `COLLAB_LOG.md`.
4. Check `CHANGELOG.md` for recent tool/schema changes.
5. Reuse existing scripts and recovered artifacts before rebuilding anything.

## After doing work

Every meaningful work session must update all applicable records before the final commit:

1. **`COLLAB_LOG.md`** — append one entry containing actor, date/time, objective, actions, results, files changed, blockers, and next recommended action.
2. **`CURRENT_STATUS.md`** — update only confirmed current facts, current blocker, and next action.
3. **`CHANGELOG.md`** — append an entry when code, tooling, schemas, outputs, or workflow behavior changed.
4. Commit code + records together whenever practical.

## Actor names

Use exactly one of:

- `ChatGPT`
- `Codex`
- `User`

## Evidence discipline

Separate:

- **Confirmed** — directly observed from APKs, runtime output, tool results, or generated files.
- **Hypothesis** — not yet verified.

Do not promote a hypothesis into `CURRENT_STATUS.md` as fact without evidence.

## Safety / scope

The research workflow is passive. Do not implement or perform:

- balance/coin/reward modification;
- request forgery or replay for gameplay advantage;
- server-state modification;
- bypasses intended to cheat or obtain paid goods.

Dynamic instrumentation should copy already-decoded/serialized client data for analysis.

## BlueStacks rule

Do not modify the user's normal BlueStacks instance for root/instrumentation experiments. Use a clone/research instance and back up configuration before changing it.

## Commit style

Prefer concise prefixes:

- `docs:` documentation / handoff / logs
- `probe:` live capture tooling
- `proto:` protobuf recovery / mapping
- `env:` emulator / Frida environment helpers
- `analysis:` derived system/activity analysis

## Handoff rule

Never finish a session with only an informal chat summary. The next agent must be able to continue by reading the repository alone.
