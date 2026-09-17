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
8. **Chinese SVN log messages are allowed only through a verified UTF-8 file workflow.** Never pass Chinese directly to `svn commit -m`. Use the CR `svn_submit.py` workflow or `svn commit --encoding UTF-8 --file <utf8-file>`, then read back `svn log --xml` and verify the exact Unicode text. Existing garbled logs are historical and should not be rewritten.

## Actor names

Use exactly one of:

- `ChatGPT`
- `Codex`
- `User`

The actor name above is what you record in your `COLLAB_LOG.md` entry. For the Git *author*
itself, use the repository account identity already present in history
(`840832144 <152851362+840832144@users.noreply.github.com>`) instead of inventing a bot
identity such as `*-agent@local`; amend with `git commit --amend --author=` if needed.

## Pushing, credentials, and cross-machine handoff

- **Never use credentials that belong to another machine or person, and never ask for a
  token, password, or SSH key in chat.** If this machine has no write credential for the
  remote, that is an environment limit — do not work around it (no credential pasting, no
  transport switching, no third-party upload service).
- When you cannot push, land the work in a form the repository owner can take:
  1. commit on a **branch** (never on shared `main`); and
  2. if that branch cannot be pushed either, export a patch (`git format-patch` or
     `git diff`) and report its path together with the exact base commit.
  A change that exists only in chat is not delivered.
- A push from a machine without a write credential fails **regardless of the commit author
  name**, so renaming the author is never a fix for a push failure.
- Before pushing a branch, check its relation to `main` and rebase:
  `git rev-list --left-right --count origin/main...<branch>`. A stale base silently reverts
  whatever landed in the meantime (for example entry-document updates).
- Keep a correction commit's scope minimal: fix the artifact under review and do not absorb
  unrelated coordination files that other commits have already changed.
- Shallow clones (`--depth 1`) truncate history and mislead "who added this?" queries: get
  full history (`git fetch --unshallow`) and ask for renames explicitly with
  `git log --follow --diff-filter=R -- <path>`.

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
