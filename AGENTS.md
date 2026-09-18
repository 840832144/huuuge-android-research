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

## Portability of deliverables

Anything committed here must work for another person on another machine. Do not make a
deliverable depend on the maintainer's local files, captures, instance serial or absolute
paths.

- Reference tools and documents by **repository-relative** path (`tools/analysis/...`),
  never by an absolute path on someone's disk.
- Take machine-specific values (device serial, forwarded port, output directory, capture
  folder, CA directory) from CLI arguments or environment variables, and auto-detect when
  exactly one candidate exists. Fail with a clear message instead of guessing or silently
  using a default that only works on one machine.
- Do **not** require the owner's private material (screen recordings, requirement
  documents, local captures) as an input to a committed procedure. Material used as
  evidence may be recorded as a fact with its hash, but any follow-up that needs it stays
  **out of scope** for the deliverable rather than a dependency or a blocker.
- Raw/value-bearing captures stay local. Committed artifacts are records, not inputs.

## Evidence discipline

Separate:

- **Confirmed** — directly observed from APKs, runtime output, tool results, or generated files.
- **Hypothesis** — not yet verified.

Do not promote a hypothesis into `CURRENT_STATUS.md` as fact without evidence.

### Negative claims need the authoritative method

A **negative** conclusion ("does not exist", "is not installed", "is unavailable",
"is not a repo", "cannot be read") is a claim like any other: verify it with the
**authoritative method for that domain** and state both the method and its output.
Indirect indicators — a cache or icon listing, a PATH/`which` probe, a proxy signal,
an old clone — are **not sufficient** to support a negative.

| Negative claim | Not sufficient | Authoritative method |
|---|---|---|
| a package is not installed on a running instance | BlueStacks `AppCache.json` icon list | `adb shell pm list packages` |
| a file was added/moved in this commit | `--diff-filter=A` on a **shallow** clone | `git fetch --unshallow`, then `git log --follow --diff-filter=R -- <path>` |
| root is unavailable on an instance | absence of a `su` binary | `adb root` then `adb shell id` (root may come from adbd, not `su`) |
| a directory is not a repository | tool not on PATH | `git -C <dir> rev-parse --is-inside-work-tree` |

If the authoritative method cannot be run here, record the item as **pending** —
do not state the negative. When a negative claim later turns out to be wrong,
correct it in the same record rather than silently dropping it.

## Safety / scope

The research workflow is passive. Do not implement or perform:

- balance/coin/reward modification;
- request forgery or replay for gameplay advantage;
- server-state modification;
- bypasses intended to cheat or obtain paid goods.

Dynamic instrumentation should copy already-decoded/serialized client data for analysis.

### Automated interaction (auto-click / auto-play)

The repository owner has **authorized automated tapping and spinning**, so an agent may drive
the game UI to produce the traffic a capture needs. This does **not** relax any item above: the
automation performs only the same UI actions a human would, and still must not modify values,
forge or replay requests, or change server state.

Conditions:

- Only on the **isolated research instance** and the owner's **own test account**. Never on the
  owner's normal/daily instance.
- Respect the limits given for the session (number of actions, time, or resource ceiling) and
  stop when they are reached.
- Record every automated session in `COLLAB_LOG.md`: what was automated, how many actions, and
  the in-game resource consumed, so the owner can audit the spend.
- If a step would cross into the prohibited list above, stop and report instead.

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
