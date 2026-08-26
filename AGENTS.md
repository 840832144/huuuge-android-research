# Agent Collaboration Rules

This repository is shared by ChatGPT and Codex. Treat the Git repository as the source of truth for cross-agent coordination.

The detailed modification/commit standard is in `CONTRIBUTING.md` and is mandatory for every agent.

## Before doing work

1. Sync the repository safely (`git pull --rebase` or equivalent).
2. Read `AGENTS.md` and `CONTRIBUTING.md`.
3. Read `CURRENT_STATUS.md`.
4. Read the newest section of `COLLAB_LOG.md`.
5. Check `TASKS.md` and `CHANGELOG.md` for recent work/tool/schema changes.
6. Reuse existing scripts and recovered artifacts before rebuilding anything.
7. Preserve unrelated existing user/agent changes; never reset or overwrite them.

## After doing work

Every meaningful work session must update all applicable records before the final push:

1. **`COLLAB_LOG.md`** — append one entry containing actor, date/time, objective, actions, confirmed results/evidence, files changed, validation, blockers/failed attempts, and next recommended action.
2. **`CURRENT_STATUS.md`** — update only confirmed current facts, current blocker, environment facts needed by the next agent, and exact next action.
3. **`CHANGELOG.md`** — append an entry when code, tooling, schemas, outputs, or workflow behavior changed.
4. **`TASKS.md`** — check off completed work and add useful newly discovered tasks.
5. Commit code + records together whenever practical, using the commit format in `CONTRIBUTING.md`.
6. Push completed work before handing off.
7. For planner-facing tooling/workflow/docs, mirror the validated safe allowlist to `trunk/HuuugeCollector` with `scripts\sync_svn_package.ps1`, review only that SVN path, and commit it without including unrelated SVN changes.
8. **SVN log messages must be ASCII-only English.** Do not use Chinese or other non-ASCII characters in `svn commit -m`; the installed Windows/TortoiseSVN command-line encoding path corrupts them in repository history. Existing garbled logs are historical and should not be rewritten.

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

Use the full standard in `CONTRIBUTING.md`. Common prefixes include:

- `docs:` documentation / handoff / logs
- `probe:` live capture tooling
- `proto:` protobuf recovery / mapping
- `env:` emulator / Frida environment helpers
- `analysis:` derived system/activity analysis
- `export:` structured output tooling
- `fix:` focused bug fix
- `chore:` repository maintenance

Do not force-push shared `main`, rewrite another agent's pushed history, or use destructive Git commands on existing work.

## Handoff rule

Never finish a session with only an informal chat summary. The next agent must be able to continue by reading the repository alone.
