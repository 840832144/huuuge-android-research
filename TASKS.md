# Active Tasks

## Next milestone — Codex

Goal: move from the now-working generic RPC instrumentation into a marked, broad discovery session that maps multiple Huuuge systems without letting the currently locked Battle Pass block progress.

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

### Broad discovery session — current priority

- [ ] Add a session manifest containing game/version code, descriptor fingerprint, Frida/Gadget version, device/research-instance id and capture start/end times.
- [ ] Add lightweight timestamped action/context markers that can be inserted while browsing/playing without relying on long video OCR.
- [x] Run a preliminary unmarked, unrestricted broad capture: 741/741 decoded RPCs across 42 unique endpoints.
- [x] Add a reproducible sanitized inventory builder and version aggregate/message/schema coverage outputs without raw values or account identifiers.
- [ ] Run one broad marked capture while visiting every currently accessible major system.
- [ ] Browse the slots lobby and play several representative machines; mark machine entry, bet changes, spins, feature/free-spin/jackpot-related states where naturally encountered.
- [ ] Browse lottery/draw/ticket systems and mark ticket/view/draw-related actions.
- [ ] Browse missions/quests and mark view/progress/claim actions where available.
- [ ] Browse live events/milestones/collections that are currently unlocked.
- [ ] Browse store/offers/bundles and mark offer-detail views.
- [ ] Browse VIP/clubs/progression/balance/reward screens where available.
- [x] Build an initial observed `service/method/message-type` inventory with counts, direction and decode status; marker correlation remains pending.
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
