# Modification & Commit Standard

This repository is jointly maintained by `ChatGPT`, `Codex`, and the user. Git is the canonical coordination layer. Every agent must leave the repository in a state that another agent can continue from without chat history.

## 1. Before changing anything

1. Sync first: `git pull --rebase` (or equivalent safe fast-forward/rebase workflow).
2. Read, in this order:
   - `AGENTS.md`
   - `CURRENT_STATUS.md`
   - newest entry in `COLLAB_LOG.md`
   - `TASKS.md`
   - relevant section of `CHANGELOG.md`
3. Inspect existing scripts/artifacts before rebuilding or replacing them.
4. If the working tree already contains unrelated user/agent changes, preserve them. Do not overwrite, reset, or discard them.

## 2. Scope of modifications

- Make the smallest coherent change that advances the current task.
- Do not mix unrelated refactors, formatting sweeps, environment changes, and analysis results in one commit.
- Prefer extending existing scripts over creating near-duplicates.
- Keep confirmed runtime facts separate from hypotheses.
- Do not modify the user's normal BlueStacks instance for root/instrumentation experiments. Use an isolated research instance and back up configuration first.

## 3. Files that must stay out of Git

Never commit:

- APK files or extracted proprietary native binaries such as `.so`;
- Frida server binaries or other downloaded third-party executables;
- raw runtime captures containing account/session identifiers unless explicitly sanitized for version control;
- credentials, cookies, tokens, private keys, passwords, account IDs, or machine-specific secrets;
- large generated artifacts that can be reproduced locally.

Use `.gitignore` and local workspace paths for those files. If a generated binary is required at runtime, add a reproducible sync/build script and document its expected local path.

## 4. Validation before commit

Before committing, run the most relevant available checks for the files changed. Examples:

- Python: syntax/import check and a focused dry-run where possible;
- PowerShell: parse/syntax check and non-destructive discovery mode first;
- Frida agent: load/parse check before live attachment when possible;
- protobuf/schema changes: regenerate or validate descriptor/mapping outputs;
- documentation/status updates: verify they agree with observed evidence and current code.

If a check cannot be run, record that explicitly in `COLLAB_LOG.md` instead of implying validation succeeded.

## 5. Required coordination updates

Every meaningful work session must update the applicable coordination files before the final push:

### `COLLAB_LOG.md`
Append-only. Include:

- date/time;
- actor (`ChatGPT`, `Codex`, or `User`);
- objective;
- actions performed;
- confirmed results/evidence;
- files changed;
- validation performed;
- blockers/failed attempts;
- next recommended action.

### `CURRENT_STATUS.md`
Update the canonical current state only. It must contain:

- confirmed facts only;
- current blocker;
- exact next action/milestone;
- important local paths/environment facts needed by the next agent.

Remove or replace stale current-state information instead of accumulating history here.

### `CHANGELOG.md`
Update when code, tools, schemas, output formats, or workflow behavior changes. Investigation-only notes with no project/tooling change belong in `COLLAB_LOG.md` instead.

### `TASKS.md`
Check off completed tasks and add newly discovered actionable tasks when useful.

## 6. Commit granularity

A commit should represent one coherent unit of work and be independently understandable.

Good examples:

- add BlueStacks environment discovery helper;
- fix RPC response type selection;
- document confirmed native-bridge behavior;
- add Battle Pass milestone exporter.

Avoid commits such as `update stuff`, `misc fixes`, or a single commit mixing root changes, decoder refactors, documentation rewrites, and unrelated analysis.

When practical, include the related coordination/log updates in the same commit as the code or analysis they describe.

## 7. Commit message format

Use:

```text
<prefix>: <imperative concise summary>
```

Allowed/common prefixes:

- `docs:` handoff, status, logs, documentation
- `probe:` Frida/live-capture tooling
- `proto:` protobuf recovery, schema, mappings
- `env:` BlueStacks/ADB/Frida environment helpers
- `analysis:` derived system/activity analysis
- `export:` structured JSON/CSV/Excel extraction
- `fix:` focused bug fix spanning categories
- `chore:` repository-only maintenance

Examples:

```text
env: discover BlueStacks data directory
probe: decode BattlePass response payloads
proto: add recovered MiniPass schemas
analysis: document confirmed BattlePass milestone fields
docs: record Frida attach blocker
```

## 8. Push / history rules

- Push completed work to the shared repository before handing off.
- Do not force-push shared `main`.
- Do not rewrite or squash someone else's already-pushed commits unless the user explicitly asks.
- Do not use destructive commands such as `git reset --hard`, `git clean -fd`, or checkout-overwrite on another agent's/user's work.
- If remote advanced while working, fetch and reconcile cleanly; preserve both sides' valid changes.
- Resolve conflicts semantically. Never choose `ours`/`theirs` blindly for `CURRENT_STATUS.md`, `COLLAB_LOG.md`, `CHANGELOG.md`, or `TASKS.md`.

## 8.1 Planner SVN mirror

Planner-facing deployment is also published to company SVN at `trunk/HuuugeCollector` (local working copy `D:\cr_design\HuuugeCollector`). Git remains the canonical engineering/cross-agent history.

- After a planner-facing code, workflow, or guide change passes validation, run `scripts\sync_svn_package.ps1`.
- Review and commit only the `HuuugeCollector` SVN path; preserve unrelated SVN working-copy changes.
- Never mirror raw captures, account/session values, APK/`.so`, Frida executables, credentials, or secrets.
- The SVN package may carry the validated protobuf descriptor because it contains schema structure and is required for offline planner deployment; it must not contain captured values.
- Record both the Git commit and SVN revision in `COLLAB_LOG.md` when available.

## 9. Handoff completion rule

A work session is not complete until all of the following are true:

1. useful code/analysis changes are saved;
2. relevant validation was run or its absence documented;
3. `COLLAB_LOG.md` was appended;
4. `CURRENT_STATUS.md` reflects the actual current state;
5. `CHANGELOG.md`/`TASKS.md` were updated if applicable;
6. commits use meaningful messages;
7. changes are pushed;
8. the final chat response names the commit(s), result, blocker, and exact next step.

The next agent must be able to continue from Git alone.
