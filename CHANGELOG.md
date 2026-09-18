# Changelog

All notable project/tooling changes are recorded here. Operator-specific investigative details belong in `COLLAB_LOG.md`.

## 2026-09-17

### Fixed

- `tools/analysis/popslots/pop_common.py`: adb output is decoded as UTF-8 with
  `errors="replace"` instead of through the console code page. Reported from another machine,
  where a localised adb message crashed subprocess' reader thread and left `stdout` as `None`,
  so the real cause surfaced as the misleading `can only concatenate str (not "NoneType") to
  str`. Both adb entry points also guard with `or ""`, and `test_pop_common.py` asserts the
  behaviour (None stdout tolerated, real error preserved, UTF-8 decoding requested).
- All CLI entry points now reconfigure stdout/stderr at **import** time. The reported
  `pop_capture.py --help` crash was an ordering bug rather than a missing call: the reconfigure
  ran inside `main()` after `argparse.parse_args()`, but `--help` exits during parsing.
  Verified by running `--help` for seven scripts under `PYTHONIOENCODING=cp1252`.
- `artifacts/bigfish_probe/bigfish_capture.py`: same decoding fix.
- `tools/analysis/toytycoon/try_bind_cacert.py`: rewritten to be portable — it had a hardcoded
  adb path, a hardcoded instance serial and a hardcoded certificate hash, and only supported
  the `su` root channel. It now takes the serial and certificate as arguments, computes the
  Android CA file name from the certificate itself, and works over either root channel.

### Added

- `tools/capture/ca_util.py`: shared helper computing the Android CA file name
  (`subject_hash_old`, e.g. `b69ec367.0`) from a PEM certificate.
- `tools/analysis/popslots/test_pop_common.py`: regression guard for the adb plumbing.
- **Slot-machine capture now works end to end** (measured on a live instance): attaching to
  the game and hooking libcurl captures `GET gamesfe.pscapi.com/slots2/startgame` and
  `GET gamesfe.pscapi.com/slots2/spin?lines=20&bet=2500&BIsi=N` with **plaintext JSON
  responses** carrying the numbers (totalWin, winType, coinsBalance, matrix, reelStopPoint,
  wins[], level/xp, machineName, spinTimestamp).
- `tools/analysis/popslots/pop_net_capture.py`: attaches via Frida and hooks the curl
  boundary — `CURLOPT_URL`, `CURLOPT_POSTFIELDS`, `CURLOPT_CUSTOMREQUEST` plus the write/read
  callbacks — emitting the same JSONL shape as `tools/capture/mitm_addon.py` so the module
  tools keep working. Response bytes travel over Frida's data channel (this runtime has no
  `base64encode`); request bodies arrive as text. Attribution deliberately avoids curl handle
  identity, because one callback address is shared by many handles: the newest URL context is
  used and flushed after 800 ms of quiet.
- `tools/analysis/popslots/pop_spin_export.py`: turns a capture into `slots_values.csv`
  (machine, bet/lines, spin index, totalWin/winType, win lines, coinsBalance, level/xp,
  matrix, reel stop points), tolerating several JSON documents concatenated into one body.
- `tools/analysis/popslots/pop_capture.py`: menu wizard (1 check / 2 start / 3 stop /
  4 export) plus `setup-frida <file>`, which pushes, runs and port-forwards frida-server over
  either root channel. Verified end to end on the instance.
- `tools/analysis/popslots/modules.popslots.json`: module presets (slots, lobby, social,
  finance, events, analytics, assets) so an operator needs no endpoint regexes.
- `artifacts/popslots/SLOT_CAPTURE.md`: step-by-step operating manual that states what the
  operator should see at each step. It supersedes the earlier proxy-based plan for this game:
  the engine ignores Android's global HTTP proxy (zero connections to the proxy while holding
  five live :443 sessions) and its exported TLS functions only yield TLS records.
- `tools/analysis/popslots/pop_doctor.py`: preflight check that answers "can this machine
  collect Pop! Slots right now?" — it walks adb → device → game installed/running → root
  channel → frida-server reachability → attach and engine-module load, printing what is
  ready and what is missing with the command to fix it (exit code 0 = the hook-based tools
  can run). Verified both ways on a real instance: it correctly reports the missing
  frida-server, then READY once the server is running and the port is forwarded.
- `tools/verify/test_mp4_facts.py`: fixture-free self-check for the MP4 fact checker. It
  synthesises minimal multi-track, audio-first, single-track and unparsable containers at
  runtime and asserts the parser's report, so the multi-track regression cannot return
  unnoticed without committing any media file. Verified to fail on the pre-fix code with
  the same symptom (`track[0] audio`, video missing) and to pass on the fix.
- `AGENTS.md`: new `Pushing, credentials, and cross-machine handoff` section — never use
  another machine's credentials or ask for tokens; when a push is impossible, land the work
  on a branch (and export a patch with its base commit if the branch cannot be pushed
  either); an author-name change does not fix a push failure; rebase after checking
  `git rev-list --left-right --count origin/main...<branch>`; keep correction commits
  narrow; never infer history from a `--depth 1` clone.
- `AGENTS.md`: the `Actor names` section now states that the actor name belongs in the
  `COLLAB_LOG.md` entry, while the Git author should remain the repository account
  identity rather than an invented `*-agent@localhost` identity.
- `tools/analysis/popslots/`: portable toolkit (public `pop_common.py` layer plus 12
  scripts) — symbols resolved by name at attach time, PID/adb/serial/package/frida
  port/output dir all configurable, APK paths resolved with `pm path`.
- `artifacts/popslots/REVIEW_RESPONSE_2026-09.md`: response to the TASK-0030 review,
  including the empirical refutation of the disputed "device-side pipe" defect, the
  9-script hardcoded-value inventory, and the `041f014` vs `759669b` rename correction.
- `AGENTS.md`: `Evidence discipline` now carries a **negative claims need the authoritative
  method** rule with a table of four concrete cases (package presence, commit history,
  root availability, repository detection) — indirect indicators such as a cache/icon
  listing, a shallow clone, a PATH probe or a `su`-binary check cannot support a negative
  conclusion, and an unverifiable item must be recorded as pending instead of asserted.
- `tools/verify/mp4_facts.py`: dependency-free MP4 fact checker (no ffprobe needed).
- `tools/capture/`: game-agnostic capture layer split into "capture everything" and "you
  choose the module". `mitm_addon.py` records all decrypted flows (host/path/method plus
  base64 bodies) with optional `MITM_FILTER`/`MITM_HOSTS` narrowing; `endpoints.py` lists
  what a capture contains with a body-shape guess (json / protobuf? / gzip / text /
  binary); `select_module.py` filters a capture down to one module defined in a
  `modules.json` mapping; `modules.example.json` is the template. Nothing about a game or
  module is hardcoded — the module choice belongs to the operator.
- `tools/capture/test_capture_tools.py`: fixture-free self-check for the above (synthetic
  capture; endpoint summary; module listing and selection; BOM-prefixed mapping/capture).
- `artifacts/popslots/SLOT_CAPTURE.md`: how to collect the slot-machine module of Pop!
  Slots through the network layer **without Frida**, including how to decide whether the
  engine's embedded TLS can be decrypted at all, and the fallback if it cannot.

### Fixed

- `tools/capture/select_module.py` and `endpoints.py` read JSON with `utf-8-sig`, so a
  mapping or capture re-saved by a Windows editor (PowerShell 5.1 / Notepad write UTF-8 with
  a BOM) parses instead of raising `Unexpected UTF-8 BOM`. Found by exercising the tools,
  not by reading them.
- `tools/analysis/toytycoon/`: the last hardcoded maintainer paths are gone — nine scripts
  now take `MITM_IN` / `MITM_OUT` / `PROTO_DICT` / `SAVE_OUT` / `CA_LOCAL` / `HOTFIX_DLL`
  from the environment with CWD-relative defaults. The duplicate Toy Tycoon `mitm_addon.py`
  was removed in favour of the canonical `tools/capture/mitm_addon.py`, and the references
  in the Toy Tycoon onboarding doc and AI prompt were repointed.

- `tools/analysis/popslots/pop_common.py`: root access is no longer assumed to come from a
  `su` binary. `root_mode()` detects `adbd` (already uid 0) versus `su`, and `adb_su()`
  picks the working channel; when neither exists it returns an explanatory message
  (suggesting `adb root`) instead of an empty result. A research instance rooted through
  adbd has no `su`, where the previous implementation failed silently.
- `tools/verify/mp4_facts.py`: frame rate is now computed per track with that track's own
  `mdhd` timescale (the first `mdhd` was previously reused for every `stts`, which
  mislabelled an audio track as a video frame rate); tracks are numbered in order of
  appearance; stdout is reconfigured to UTF-8 so non-ASCII paths do not break on Windows
  consoles; an unparsable container now reports what was found (e.g. a fragmented MP4)
  instead of printing `None`. Cross-checked against ffprobe (duration, resolution and fps
  agree).
- `tools/verify/mp4_facts.py`: **regression fix**. Giving each track a display index
  required a unique identity in the walker's path, but a plain `trak` token made every
  track produce the same path prefix, so all tracks collapsed into one slot and the audio
  track silently overwrote the video track (`demo.MP4` reported only
  `track[0] audio`, losing a 1188x682 video track). `walk()` now tags a `trak` with its
  byte offset (`trak@<off>`) and `slot()` matches that prefix, which also removes the
  need to infer a track's kind from whichever `hdlr` happens to be read first. Verified:
  multi-track files now list video and audio separately while single-track output is
  unchanged.
- Delivered documentation no longer points at the maintainer's machine: the Toy Tycoon
  runbook/iOS/MITM docs referenced an absolute local tool directory and now use
  repository-relative `tools/analysis/toytycoon/` paths plus a `<mitm-dir>` placeholder for
  the generated CA directory; the Big Fish probe docs and capture script used an absolute
  local capture folder and now use `<capture-dir>`.
- `tools/analysis/popslots/pop_common.py`: no instance serial is baked in. `resolve_serial()`
  takes `--serial`/`POP_SERIAL`, otherwise auto-detects the only connected device and fails
  with a clear message when none or several are attached; the `--frida` default is now
  frida-server's standard `127.0.0.1:27042` rather than a locally chosen port.
- `artifacts/bigfish_probe/bigfish_capture.py`: the same machine-specific defaults are gone —
  `--serial` resolves from `BIGFISH_SERIAL` or auto-detection via the script's own
  `_adb_path()` (which finds adb on PATH or in the usual platform-tools locations), and
  `--host` defaults to frida's standard 27042.
- Usage examples in `artifacts/live_probe/README.md` and the reproduce steps in
  `artifacts/popslots/ENVIRONMENT_LOCK.md` use `<serial>` instead of a concrete instance
  serial (the environment tables themselves are kept as records of the machine the
  analysis ran on).

### Changed

- `AGENTS.md`: new `Portability of deliverables` section — committed work must run for
  another person on another machine; use repository-relative paths and CLI/env values,
  auto-detect or fail loudly, never require the owner's private material as an input to a
  committed procedure, and keep follow-ups that would need it out of scope rather than
  recorded as blockers.
- `artifacts/popslots/POP_SLOTS_LOBBY_FORENSICS.md`: added a `方法学限制` section
  (fuzzy byte-window dump is not a field mapping; sampling window limited; three
  behaviours uncovered; script-availability timeline).
- Toy Tycoon documentation marked the in-process Frida route as closed and local-only so
  dangling script references are not chased.

### Verified

- TASK-0030 evidence (recorded, not a dependency): the delivery's screen recording hash
  matches the reported value and independently parses to 72.167 s / 996x558 / 30.0 fps;
  the two requirement DOCX files contain 11 + 5 = 16 embedded images. These files are not
  part of the repository and are not redistributable, so no committed procedure relies on
  them.
- A rooted research instance lists `com.playstudios.popslots` in `pm list packages`,
  settling the review's pending instance check.

## 2026-09-08

### Added

- **TASK-0022 Top Tycoon capture (network layer).** Recovered the static protocol
  dictionary from the hot-update `Game.Hotfix.dll` (422 messages / 48 services /
  1264 field slots) and committed it as
  `tools/analysis/toytycoon/toytycoon_protocol_dict.json` — it was referenced by the
  docs but had not been uploaded.
- Committed the Toy Tycoon toolchain under `tools/analysis/toytycoon/`:
  `README.md`, `bootstrap_gadget_tt.py`, `try_bind_cacert.py`, `analyze_play.py`,
  `decode_steal_amount.py`, `find_spin.py` and
  `gadget-listen.config.template.json`.
- Added the Toy Tycoon documents: `TT_CAPTURE_RUNBOOK.md` (verified mitmproxy
  deployment, replaces the Frida-hook approach), `DEPLOY_AND_ONBOARD.md`,
  `PLANNER_AI_REPLY.md`, `MITM_CAPTURE.md`, `GENERIC_CAPTURE.md`,
  `RUNTIME_CAPTURE_MINIMAL.md`, `PROTOCOL_RECOVERY.md`, `ENVIRONMENT_LOCK.md`,
  `TT_IOS_CAPTURE.md` and the one-click AI prompt `TT_CAPTURE_PROMPT.txt`.
- **TASK-0023 Pop! Slots lobby bot forensics.** Added
  `artifacts/popslots/POP_SLOTS_LOBBY_FORENSICS.md` and
  `artifacts/popslots/ENVIRONMENT_LOCK.md`, plus the toolkit
  `tools/analysis/popslots/` (symbol enumeration, `parseUserData` user sampler for
  bot detection, behaviour hooks, APK native-library extraction) with its README.

### Changed

- Moved `POP_SLOTS_LOBBY_FORENSICS.md` out of `artifacts/toptycoon/` into its own
  `artifacts/popslots/` directory, since it belongs to a different game.
- Documented the proxy toggle prominently in the Toy Tycoon runbook/onboarding: the
  device proxy must be **on** while capturing and **cleared** (`settings put global
  http_proxy :0`) otherwise, otherwise the game reports "connection interrupted" and
  cannot log in.
- `TASKS.md` and `CURRENT_STATUS.md` now track TASK-0022 and TASK-0023 so the new
  projects are discoverable from the entry documents.

### Fixed

- Closed the Toy Tycoon in-process Frida route with evidence (ARM64 Houdini
  translation + stripped `libil2cpp.so` + statically linked xLua +
  `UnitySendMessage` not carrying business logic) so the same dead end is not
  re-attempted.

### Added (repo hygiene)

- `.gitignore` now excludes raw capture artifact types (`*.jsonl`, `*.mitm`,
  `*.b64`, `*.png`, `*.jpg`, `*.jpeg`) so account-bearing captures stay local.

## 2026-09-01

### Added

- Published the CR Lottery activity-migration product package to design SVN revision `6637`: three planner-facing documents, an eight-sheet WBS/Gantt/RACI/real-package-test workbook, and six newly named `QuestLottery*` configuration-candidate workbooks.
- Added a CR-side candidate/release validator for the six Lottery workbooks. Candidate mode passes with four warnings; release mode blocks the four paid bundles until product IDs and prices are confirmed.
- Added TASK-0021 coordination state for the product-manager handoff, professional frontend/backend implementation, and `王坤` actual-package acceptance workflow.
- Published ten company-editable Feishu documents for TASK-0021 and a project navigation document linking the full product/configuration package; all formal documents passed readback and Documentation Hub registration/readback.
- Created the company-editable `CR Lottery 活动移植｜项目管理` Base with eight tables / 117 records, including the 38-task WBS, milestones, configuration list, product test matrix, risks, RACI and collaboration cadence.
- Extended the approved company Document Assistant provider with generic Bitable table/field/record/view and verified `tenant_editable` permission support; provider commit `e80fd8a` passed 44 tests and Secret Scan.

- Big Fish passive HTTP-JSON capture now reaches READY: the JS collector is verified through the logcat `Cobra Log` tag (`collector-already-installed` receipts observed) instead of the `cocos2d::log` export, which is a no-op under Cocos `DebugMode.NONE`.
- `bigfish_capture.py` now supports `--mode logcat` (default): streams ADB logcat and parses tagged `__CODEX_BIGFISH_HTTP_V1__` events locally (events.jsonl + one JSON per HTTP event). `--mode frida` optionally re-injects agent.js to guarantee collector installation and emit the receipt.
- Static confirmation of the same-room shared-win feature strings in `SALocalizationService.js`: `youHitScatter`, `otherPlayerHitScatter`, `foundTreasureForYou`, `EveryoneElseGets`, `YouFoundTreasure`, `bigBooty`.

### Fixed

- Big Fish transport: the collector previously hooked `cocos2d::log`, which never received events; the events flow through `cc.log`/`console.log` into logcat tags `Cobra Log` and `cocos2d-x debug info`.

### Changed

- TASK-0020 status updated from "not READY" to READY with an ordinary request/response pair validated (mission/characters/vip/alerts/booster/inbox/sparkle_lobby). Next step is normal play to capture the shared-win endpoint.
- Big Fish F4 spin + same-room shared-win confirmed: `slots.spin` endpoint recovered; its response `messages` include `jackpot.win` (targeted to same-room players, `data.otherPlayerWonAmount` = per-player room payout), `player.win`, `player.winningstoday`, `jackpot.update`, `spin.result`, and more. Same-room play is a broadcast room across multiple stake tiers.

### Added

- `artifacts/bigfish_probe/F4_SPIN_ANALYSIS.md` — full F4 protocol analysis of the spin endpoint and the same-room shared-win (`jackpot.win`) mechanism.
- `artifacts/bigfish_probe/agent_filesink.js` and `agent_reinject.js` — scene-scoped collectors. File sink writes events to `files/bf_capture.jsonl` (UTF-16LE), avoiding logcat truncation of large spin responses.

### Fixed

- Controller startup now tolerates the expected ADB `device not found` state long enough to launch only `Pie64_1 / HuuugeResearch` instead of aborting before its auto-start branch.
- Added a bounded `frida-ps` Gadget handshake before the lossless collector connects, preventing the transient `connection closed` race during Houdini `on_load=wait` startup.
- Bootstrap and controller now require both the ARM64 Gadget binary and `libhuuuge-gadget.config.so`; an app update can no longer leave a false-ready Gadget state with the configured `27043` endpoint missing.
- Collector state counters now refresh after READY instead of remaining frozen at the first decoded RPC while capture files continue to grow.

### Changed

- Validated the passive collector on research-instance Huuuge `12.08.27100` after a rollback-backed Google Play update; the normal BlueStacks instance remains untouched.
- Finalized capture `20260901_160002` into a 92-row sanitized RPC inventory, 1313 observed field paths and an updated 37-module catalog (21 live-confirmed, 16 schema-only). The Shared Jackpot endpoint remains schema-only with zero observed samples.
- Inventory summaries now derive manifest/lifecycle-marker facts from each Session, label undecoded rows accurately and avoid stale hard-coded claims about missing systems or manual markers.

## 2026-08-27

### Fixed

- Addressed TASK-0018 Review Round 1 with a planner-first Chinese report structure, Chinese evidence labels, ordinary chip-bet terminology and a technical-only description of the 117.516 output/cost ratio.
- Replaced the original Feishu document in place, removed the duplicate body title, repaired section ordering and verified complete readback plus company-editable permission.

### Added

- Added sanitized `PURCHASES.csv` output and local purchase-chain extraction for four successful real-money purchases, including amount, currency, ticket grant, other bundle rewards and caveated apparent per-ticket cost without exposing request, product, store or order identifiers.
- Added regression tests for purchase extraction, incomplete-chain fail-closed behavior, ordinary-spin public naming and bundle other-reward caveats; the suite now contains seven tests.

### Added

- TASK-0018 Chinese Lottery numerical report with playflow, evidence matrix, data dictionary, CR candidates and six sanitized CSV outputs under `reports/lottery/20260827_lottery-ticket-puzzle/`.
- Reproducible `tools/analysis/lottery/extract_lottery_facts.py` for Finalize validation, Lottery/Spin pairing, B0 normalization, ticket-ledger reconciliation, reward aggregation and upgrade-linked state-transition detection.
- Focused unit tests for reward classification, unsigned big-number decoding, percentile interpolation and Wilson confidence intervals.

### Changed

- Regenerated the 37-module catalog from finalized capture alias `LOT-20260827-A`; real Session identifiers and value-bearing analysis remain local.
- Lottery now has 692 primary live samples and a 90/100 structure/numerical baseline. The report explicitly separates direct Toss rewards from upgrade-linked ticket outcomes.
- Updated status, tasks and Codex handoff for ChatGPT Review. No collector runtime, CR repository, SVN package, game or server state was changed.

## 2026-08-26

### Added

- TASK-0006 architecture baseline under `docs/collector/`: status-qualified capability inventory, end-to-end data flow, software module relationship map and review-gated TODO Roadmap.
- Product release `1.0.0` with `HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md`, a planner-only install/update/capture/data/AI/FAQ manual.
- Reproducible `scripts/build_installer_package.ps1` outputting `HuuugeCollector_Installer.zip` with a machine-readable version/source/safety/file-hash manifest.
- Connector-verified Feishu edition of the deployment manual at `https://gfok27asqq.feishu.cn/docx/DSx8doLpIoI7SXxHCIoc4DQTnSb`.
- Native Windows planner GUI and controller with six actions: Start, Stop/Finalize, Recent Results, Environment Check/Repair, optional AI Handoff and Open Guide.
- `HUUUGE_COLLECTOR.cmd` daily launcher and SVN-first `HUUUGE_BOOTSTRAP.cmd` install/update flow.
- Session `manifest.json`, machine-readable collector state, clean stop control and automatic lifecycle `markers.jsonl` events.
- Deterministic Stop/Finalize pipeline that regenerates RPC inventory/field paths and the 37-module catalog while keeping raw values local.
- `scripts/sync_svn_package.ps1` with a safe planner-package allowlist and internal schema-only descriptor distribution.
- `AGENT_DATA_USAGE_GUIDE.md` for Codex, Trae + DeepSeek and other Agents to consume outputs with evidence/privacy discipline.

### Changed

- Replaced the obsolete pre-root Codex handoff with the current release `1.0.1` architecture, confirmed gaps, review state and exact next action; no collector behavior changed.
- Deployment manual `1.0.1` now opens with a plain-language product summary, calls `HuuugeResearch` a dedicated BlueStacks emulator created through Multi-instance Manager, removes reverse-engineering terminology from planner instructions, and places the official SVN package download link directly under “1. 你会拿到什么”.
- GUI “Open Guide” now opens the product-facing deployment manual; the SVN publisher builds the ready-to-distribute installer ZIP under `release/`.
- Bootstrap now adds read-only pinned Frida/server/Gadget checks and writes `.local/bootstrap/latest.json` with `ready_for_gui_validation` or actionable missing items.
- Collaboration rules now allow Chinese SVN messages only through an UTF-8 message file/Python submit workflow with XML readback; direct Chinese `svn commit -m` remains forbidden. Batch launchers stay ASCII-only and Chinese Windows PowerShell files use UTF-8 BOM.
- Bootstrap now supports Git, SVN or no-source preflight modes, clean/dirty working-copy preservation, optional Codex/Trae selection and non-interactive validation.
- Houdini bootstrap reports `gadget-load-started` before the Gadget's `on_load=wait` connection point, avoiding a launcher/collector deadlock.
- `live_decode.py` publishes READY only after hooks plus a real decoded RPC and explicitly records that console filters are display-only.
- Manual module/action marker controls were removed from the planner workflow; module classification is automatic after unrestricted capture.
- Planner distribution is mirrored to company SVN `trunk/HuuugeCollector`; Git remains the canonical engineering collaboration history.

## 2026-08-25

### Added

- Initial Huuuge Android research repository structure.
- Full technical handoff from the ChatGPT investigation.
- Recovered protobuf descriptor set and 36 recovered `.proto` schemas.
- Service/method RPC mapping and Battle Pass schema notes.
- Initial Frida live probe (`agent.js`) and protobuf decoder (`live_decode.py`).
- Collaboration protocol (`AGENTS.md`), canonical status (`CURRENT_STATUS.md`), and shared operator log (`COLLAB_LOG.md`).
- `CONTRIBUTING.md` with mandatory modification, validation, commit, push, conflict-resolution, and handoff rules for ChatGPT/Codex collaboration.
- Read-only `scripts/discover_bluestacks.ps1` for registry-derived install/data/config discovery and sanitized instance inventory.
- `RESEARCH_DATA_ARCHITECTURE.md` defining lossless broad capture, normalized interpretation, system-specific extractors and on-demand presentation for slots, lottery, missions, passes/events, offers/economy and future systems.
- Audited BlueStacks root scope/rollback evidence for the exact China `5.22.170.6509` environment.
- `bootstrap_houdini_gadget.py` to cold-spawn the ARM-translated client, reuse its real native-bridge namespace, and load an already-staged ARM64 Gadget before startup RPC traffic.
- `scripts/build_rpc_inventory.py` to reproducibly convert a local `live_decode.py` session into a value-free service/method/message inventory, heuristic system classification, aggregate coverage summary, and protobuf field-path/type inventory.
- Sanitized discovery artifacts for the unrestricted `20260825_182300` session under `artifacts/analysis/20260825_182300/`; the 741 raw wrappers and decoded values remain local and excluded from Git.
- `MODULE_STRUCTURE_CATALOG.md` as the structure-first dossier contract and catalog maintenance priority.
- `scripts/build_module_catalog.py` plus `artifacts/module_catalog/module_specs.json` to reproducibly combine descriptor, sanitized live, local-only variability and APK ZPK evidence.
- A 37-dossier module catalog covering 36/36 proto files, 1028/1028 descriptor messages, 356/356 service methods, 741 live samples and sanitized module/endpoint/field tables.
- `HUUUGE_DATA_COLLECTION_OVERVIEW.md`, a concise Chinese overview of the experiment environment, deployment architecture, capture workflow, capabilities, validation results and limitations.
- A connector-verified Feishu cloud-document edition of the concise overview, including a sanitized 29-spin live-data example without account identifiers, per-spin balances or full reel-stop values.
- `HUUUGE_DATA_COLLECTION_GUIDE.md`, the complete planner-oriented deployment/capture/capability guide with easy-deployment and low-operation use as explicit project requirements.
- `AI_DEPLOYMENT_PLAYBOOK.md`, a state-machine handoff for a computer-local AI to deploy/verify/repair the collector without asking planners to operate low-level ADB/Frida steps.
- `HUUUGE_BOOTSTRAP.cmd`, the intended Windows one-click entry for locating/cloning the private repo and launching safe bootstrap/preflight.
- `scripts/huuuge_bootstrap.ps1`, which safely updates a clean repo, creates an isolated Python venv, installs requirements, syncs/builds descriptors, runs BlueStacks/ADB discovery, writes `.local/bootstrap/` reports, and invokes a documentation-aware Codex preflight when available.

### Changed

- `AGENTS.md` now requires every agent to read and follow `CONTRIBUTING.md`, preserve unrelated work, update all applicable coordination files, push before handoff, and avoid destructive/shared-history rewrites.
- `check_device.ps1` now targets an explicit ADB serial, reports native-bridge/root evidence, and no longer runs the state-changing `adb root` test implicitly.
- `start_frida_server.ps1` now targets an explicit serial, enforces matching host/server Frida versions, requires a verified UID-0 launcher, and supports an explicitly labeled unprivileged diagnostic mode.
- `live_decode.py` now accepts `--device-id` so the research clone can be selected deterministically when multiple ADB devices exist.
- `live_decode.py` now accepts a Frida `--remote-endpoint` and explicit `--process`, enabling the decoder to attach to an ARM64 Gadget inside the x86_64 Houdini process.
- Live-probe documentation now distinguishes process enumeration from successful attach and documents BlueStacks whitelist-gated `su` behavior.
- Project scope is explicitly broader than Battle Pass: Battle Pass is only the first end-to-end validation target. The base collector must retain unrelated and unknown RPC traffic so later slot/lottery/mission/event/economy analysis can reuse the same raw sessions.
- `README.md`, `CURRENT_STATUS.md`, and `TASKS.md` now reflect the capture → normalize → system-specific export architecture.
- Live-probe documentation now covers the split x86_64 root-server / ARM64 Gadget workflow required by BlueStacks native translation.
- Project priority now favors broad module-structure coverage and incremental dossier enrichment before deep RTP, EV, purchase-value or other single-system modeling.
- `README.md` now makes the complete planner guide and one-click bootstrap the primary entry rather than requiring the operator to understand the technical handoff first.
- Easy deployment / low-operation use is now a first-class architecture goal. Safe steps should be automated; GitHub/Codex first login and BlueStacks machine-level root/host changes remain explicit one-time approvals.

### Current architecture direction

- Prefer passive high-level `Casino::Connection` / `Casino::RpcMessage` instrumentation over video OCR and TLS MITM.
- Prefer an isolated BlueStacks research clone for root/Frida experiments.
- Capture broadly and losslessly; use filters only for console/readability, not data retention.
- Preserve raw bytes and version/session metadata so interpretations and schemas can be corrected later.
- Build system-specific numerical views downstream rather than hard-coding the collector around one feature.
- Hide ADB/Frida/Proto complexity behind a planner-facing bootstrap and local-AI operator wherever practical.
