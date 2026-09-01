# Active Tasks

## TASK-0021 — CR Lottery activity migration planning package

Status: **Planning package complete — implementation handoff pending**

- [x] Freeze the Huuuge Lottery research/data baseline and separate confirmed observations from planning candidates.
- [x] Create Chinese product plan, requirements/configuration notes, and actual-package test/pre-launch plan.
- [x] Create six new `QuestLottery*` configuration-candidate workbooks following the CR naming and four-row header conventions.
- [x] Create the development schedule with WBS, Gantt, milestones, configuration list, test matrix, risks/dependencies, and RACI.
- [x] Assign planner/product acceptance ownership to `王坤`; keep frontend/backend implementation with the professional development owners.
- [x] Render and inspect all workbooks; pass formula/error scanning and CR repository validation.
- [x] Add candidate/release validation that blocks the four unconfirmed paid-bundle product IDs/prices.
- [x] Publish the complete planning package to CR design SVN revision `6637` and verify the Unicode log plus clean working copy.
- [ ] Product/numerical/frontend/backend/payment/operations owners review and confirm IDs, reward weights/values, paid product IDs/prices, and resource dates.
- [ ] Frontend/backend owners implement and produce an actual test package.
- [ ] `王坤` executes the actual-package acceptance matrix, records defects/retests, and completes the normal pre-launch check.
- [ ] If the company approves Bitable write capability, connect an approved Feishu provider and import the WBS with a real Feishu member field for `王坤`; this is optional and does not block the local/SVN handoff.

## TASK-0020 — Big Fish same-room shared-win investigation

Status: **F4 confirmed — spin + same-room shared-win sample captured**

- [x] Correct the target product to Big Fish Casino based on user confirmation.
- [x] Identify package/version/ABI and confirm Cocos2d JavaScript + ARM64 `libgame.so` under Houdini.
- [x] Preserve installed split APKs locally with SHA-256.
- [x] Load a dedicated Frida 17.17.0 ARM64 Gadget on port `27044` without touching normal `Pie64` or Huuge's `27043` listener.
- [x] Add a Big Fish-specific passive Agent and local-only collector under `artifacts/bigfish_probe/`.
- [x] Receive the business-side `collector-installed` acknowledgement; the JS collector confirms through the logcat `Cobra Log` tag, not the `cocos2d::log` export.
- [x] Capture and verify one ordinary request/response pair without modifying request, Promise or server state.
- [x] Observe normal play and identify the same-room shared-win endpoint/fields; capture a natural sample.
- [x] Recover the core machine endpoint `slots.spin` and its response message set (spin.result, player.win, jackpot.update, jackpot.win, player.cash2, player.winningstoday, prize.award.allPrizes, etc.).
- [x] Confirm the same-room shared-win mechanism: `jackpot.win.to` = same-room player list and `data.otherPlayerWonAmount` = payout to the other same-room online players.
- [ ] Collect additional `jackpot.win` samples across `jackpotType` tiers and same-room stake levels to map per-tier `otherPlayerWonAmount`.

## TASK-0019 — Same-room Shared Jackpot live investigation

Status: **Closed as wrong product / Huuge no-hit evidence retained only for Huuge**

- [x] Update only `Pie64_1 / HuuugeResearch` after the old client became update-blocked; preserve rollback APKs.
- [x] Restore and hash-verify ARM64 Gadget plus its `27043 / on_load=wait` configuration in the new app directory.
- [x] Reach collector READY on Huuuge `12.08.27100` and confirm decoded files grow during normal play.
- [x] Identify `SlotsGameClient.HitSharedJackpot` and its eligibility/payout fields from the recovered schema.
- [x] Establish a user-confirmed baseline with three peer players in the same Buffalo machine room without committing names, IDs or balances.
- [x] Start a five-minute passive monitor for the target RPC and collector health.
- [ ] Capture the first natural `HitSharedJackpot` sample.
- [ ] Correlate eligible-user/payout structure with adjacent `RoomUsers` balance changes and separate it from ordinary `HitJackpot`/`UpdateJackpot`.
- [x] After the user finished, clean-stop/finalize, publish only sanitized structural findings and update the Slots dossier; retain the target as schema-only/live-pending because it did not trigger.

## TASK-0018 — Huuuge Lottery numerical breakdown report

Status: **Waiting for ChatGPT Review Round 2**

- [x] Verify TASK-0015 Session Finalize and 100% decode completeness.
- [x] Build a reproducible sanitized Lottery extractor and regression tests.
- [x] Separate direct Toss rewards, threshold rebates and upgrade-linked ticket outcomes.
- [x] Analyze playflow, ticket consumption, progress, reward output, return limits and CR candidates.
- [x] Produce Chinese Git report, structured CSVs and a company-editable Feishu edition.
- [x] Update the module catalog and collaboration records without committing raw data.
- [x] Address Review Round 1: planner-first structure, real-money purchase extraction, ordinary-bet terminology, bundle caveats, Feishu layout and Extractor regression tests.
- [x] Replace and read back the original Feishu document without creating a duplicate.
- [ ] ChatGPT performs Review Round 2 on the revised report, Extractor and original Feishu document.

## TASK-0015 — Lottery live capture

Status: **Complete**

- [x] Start a dedicated Lottery capture and reach READY before gameplay.
- [x] Stop/Finalize after user gameplay.
- [x] Confirm manifest `stopped`, lifecycle completeness and 8712/8712 decoded RPCs.
- [x] Keep raw/value-bearing Session data local and provide sanitized alias `LOT-20260827-A` to TASK-0018.

## TASK-0006 — Collector architecture baseline

Status: **Waiting for ChatGPT Review**

- [x] Sync Git and audit current collector source, scripts, validated Sessions and release evidence.
- [x] Establish a status-qualified current capability inventory.
- [x] Document deployment, capture, decode, finalize and data-boundary flows.
- [x] Document software module responsibilities and Mermaid relationship maps.
- [x] Establish a review-gated TODO Roadmap without developing features.
- [x] Update CHANGELOG, CURRENT_STATUS, COLLAB_LOG and Codex handoff.
- [ ] ChatGPT reviews and accepts or requests changes to `docs/collector/`.

## Next milestone — Codex

Goal: maintain a broad structure-first catalog across Huuuge modules, then use unrestricted captures to enrich missing dossiers without asking planners to preselect modules.

### Instrumentation foundation

- [x] Preserve the normal `Pie64` instance and use `Pie64_1 / HuuugeResearch` as the isolated research environment.
- [x] Audit and apply the approved BlueStacks root route with backup/hash/rollback evidence.
- [x] Verify real UID 0 on `127.0.0.1:5565`.
- [x] Run matching root-owned x86_64 Frida `17.17.0` server.
- [x] Establish the Houdini ARM instrumentation path with ARM64 Gadget.
- [x] Load all three `agent.js` hooks in the ARM64 module view.
- [x] Capture real `Casino.RpcMessage` traffic.
- [x] Decode a full proof session: 84/84 RPCs to JSON.
- [x] Verify console filters do not discard unrelated/unknown RPCs.
- [x] Retain raw wrapper bytes, timestamps, direction, service/method IDs/names and decode results.
- [x] Retain and verify rollback backups; normal-instance disk/config hashes remain unchanged from baseline.

### Planner-first deployment / operation

- [x] Publish manual/package 1.0.1 with a plain-language product introduction, dedicated BlueStacks-emulator wording and a direct package entry in section 1; Feishu body/readback is complete. Native ZIP attachment was unavailable through browser control, so the verified SVN download link remains the automatic path and the user may drag the file manually.
- [x] Add a product-facing `HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md` covering install, update, Start, Stop, data paths, AI usage and FAQ without requiring reverse-engineering knowledge.
- [x] Add a reproducible versioned `HuuugeCollector_Installer.zip` builder and a package manifest with per-file SHA-256 values.
- [x] Validate the extracted installer through a genuinely new directory: SVN checkout, new `.venv`, requirements, descriptor sync and environment preflight completed without Root/host changes.
- [x] Publish and read back a dedicated Feishu deployment manual.
- [x] Publish release 1.0.0 to Git and SVN, re-run the committed r6427 ZIP from an empty directory and verify its manifest/source/hash and `ready_for_gui_validation` result.

- [x] Add complete planner-oriented guide in `HUUUGE_DATA_COLLECTION_GUIDE.md`.
- [x] Add local-AI state-machine handoff in `AI_DEPLOYMENT_PLAYBOOK.md`.
- [x] Add a provider-neutral `AGENT_GIT_QUICKSTART.md` and DSH opening prompt for safe Git engineering handoff.
- [x] Add `HUUUGE_BOOTSTRAP.cmd` as the intended Windows one-click entry.
- [x] Add `scripts/huuuge_bootstrap.ps1` for safe repo/Python/runtime/BlueStacks/ADB/Codex preflight.
- [x] Run the new bootstrap end-to-end on the proven Windows machine and fix PowerShell/CMD/runtime issues.
- [x] Switch planner deployment/update from Git clone to company SVN `trunk/HuuugeCollector`; retain Git as engineering/cross-agent truth.
- [x] Validate a fresh `.venv` bootstrap directly from the SVN package directory with packaged descriptor and no AI dependency.
- [x] Confirm committed `HUUUGE_BOOTSTRAP.cmd` can update `trunk/HuuugeCollector` and complete preflight with exit code 0; first checkout still needs a genuinely new machine/path.
- [ ] Confirm `codex exec` preflight reads the required docs and returns a useful Chinese deployment assessment without machine-level changes.
- [x] Add a planner-facing daily GUI: start environment → verify root/server/Gadget/hooks/files/real decoded RPC → print `READY，可以开始玩了`.
- [x] Add planner-facing stop/finalize: clean stop → flush → inventory → module-catalog refresh.
- [x] Add session `manifest.json` and automatic lifecycle markers; do not make planners choose modules or mark normal gameplay.
- [x] Add optional Codex or Trae + DeepSeek AI handoff while keeping capture fully AI-independent.
- [x] Add `AGENT_DATA_USAGE_GUIDE.md` for Agent-side consumption, privacy, evidence labels and reusable prompts.
- [ ] Keep SVN/game login and first BlueStacks root/host patch as explicit one-time steps/approvals; do not silently automate them.

### Module structure catalog — current priority

- [x] Add the structure-first catalog contract in `MODULE_STRUCTURE_CATALOG.md`.
- [x] Create 37 independent module dossiers covering required systems plus newly discovered casino, live-ops, platform and social families.
- [x] Cover all 36 descriptor files, 1028 descriptor message types and 356 recovered service methods.
- [x] Generate `modules.csv`, `endpoints.csv` and `fields.csv` with observed-live/schema-only/inferred separation.
- [x] Integrate all 741 current live samples and local-only populated/non-empty/distinct/variability statistics without committing values.
- [x] Attach module-specific base-APK ZPK filename evidence and preserve shared Lua/native evidence boundaries.
- [x] Record exact missing data and next user actions in every dossier.
- [x] Add concise experiment/environment/deployment documentation in `HUUUGE_DATA_COLLECTION_OVERVIEW.md`.
- [x] Publish the concise overview as a connector-verified Feishu cloud document with a sanitized live Slots `Spin` example.
- [ ] After each future capture, regenerate and enrich the existing dossiers before starting a one-off deep model.
- [ ] Split newly coherent endpoint/message families from `other_protocol.md` into dedicated dossiers.
- [ ] Defer RTP/EV/paid-value/final single-system conclusions until explicitly selected after broader catalog enrichment.

### Broad discovery capture follow-up

- [x] Add a session manifest containing game/version code, descriptor fingerprint, Frida/Gadget version, device/research-instance id and capture start/end times.
- [x] Add automatic timestamped collector lifecycle markers without planner module selection.
- [x] Run a preliminary unmarked, unrestricted broad capture: 741/741 decoded RPCs across 42 unique endpoints.
- [x] Add a reproducible sanitized inventory builder and version aggregate/message/schema coverage outputs without raw values or account identifiers.
- [ ] Run another unrestricted broad capture while visiting every currently accessible major system; no manual markers required.
- [ ] Browse the slots lobby and play several representative machines, including bet changes and naturally encountered feature/free-spin/jackpot states.
- [ ] Browse lottery/draw/ticket systems and trigger ticket/view/draw-related actions.
- [ ] Browse missions/quests and trigger view/progress/claim actions where available.
- [ ] Browse live events/milestones/collections that are currently unlocked.
- [ ] Browse store/offers/bundles and mark offer-detail views.
- [ ] Browse VIP/clubs/progression/balance/reward screens where available.
- [x] Build an initial observed `service/method/message-type` inventory with counts, direction and decode status.
- [x] Classify the initial observed traffic heuristically into slots, lottery, missions/quests, passes/events, offers/economy, clubs/VIP/progression and other/unknown.
- [ ] Preserve undecoded and unclassified messages as first-class evidence rather than dropping them.
- [ ] Identify at least two accessible systems with concrete field-level evidence suitable for normalized extractors.
- [ ] Build the first normalized extractor for the highest-value accessible gameplay system (prefer slots or lottery if traffic is sufficiently rich).
- [ ] Build one meta/economy extractor (missions or offers) if the discovery session exposes adequate fields.

### Battle Pass — non-blocking follow-up

- [ ] When an eligible account is available, capture and decode Battle Pass main/reward/mission traffic.
- [ ] Export milestone/mission JSON/CSV as a named-schema validation case.
- [ ] Do **not** block generic inventory, slots, lottery, missions, offers or other extractors on current Huuuge Pass requirement `35`.

### Repository / modeling follow-up

- [ ] Append each discovery/modeling session to `COLLAB_LOG.md` and update `CURRENT_STATUS.md` / `CHANGELOG.md` as applicable.
- [ ] Version the full recovered 36-file `.proto` source set in Git.
- [ ] Verify `scripts/build_descriptors.py` regenerates a descriptor set equivalent to the locally recovered binary.
- [ ] Add the normalized analytical fact/event layer while keeping raw bytes as source evidence.
- [ ] Add system-specific CSV/Excel/chart/report exporters only downstream of generic capture/normalization.
