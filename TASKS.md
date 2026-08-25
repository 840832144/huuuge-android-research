# Active Tasks

## Next milestone — Codex

Goal: establish a lossless generic Huuuge RPC capture session, then use Battle Pass as the first named-schema validation while retaining unrelated traffic for later system analysis.

- [x] Pull latest `main`.
- [x] Run `scripts\sync_local_runtime.ps1` and verify local descriptor/APK/ADB paths.
- [x] Discover actual BlueStacks executable path, data directory, version, config path, and instance IDs.
- [x] Preserve the normal instance; use the existing `Pie64_1` / `HuuugeResearch` clone for root/Frida experiments.
- [x] Verify `ro.dalvik.vm.native.bridge=libnb.so`, x86_64 guest ABI, and ARM64 Huuuge package ABI.
- [x] Install matching host/server Frida `17.17.0` and prove process enumeration on `127.0.0.1:5565`.
- [x] Record the exact shell-server attach failure (`PermissionDeniedError`) and exclude version/ABI/ADB causes.
- [x] Verify from user screenshot that the visible BlueStacks Settings → Advanced page has no `Root Access` control in this China build; do not toggle unrelated input-debug options.
- [x] User selected Plan 1: make one audited BlueStacks-root attempt on the isolated research setup before switching emulator/Gadget routes.
- [ ] Audit `RobThePCGuy/BlueStacks-Root-GUI` source/release behavior for BlueStacks 5 China `5.22.170.6509`; identify exact files/disks/config it changes and rollback path before running/replicating it.
- [ ] Back up + hash all patch targets, including any shared BlueStacks host binary, `bluestacks.conf`, and `Pie64_1` research-instance disk/config data.
- [ ] Apply root for the `Pie64_1 / HuuugeResearch` research workflow while preserving normal `Pie64` Android instance/data/root state.
- [ ] Verify a real UID-0 command on ADB serial `127.0.0.1:5565`; flags/presence of `su` do not count.
- [ ] If UID 0 succeeds, run matching root-owned Frida `17.17.0` x86_64 server and establish a working attach path.
- [ ] Load `artifacts/live_probe/agent.js` successfully.
- [ ] Verify the base collector stores **all observable `Casino.RpcMessage` traffic**, not only messages matching console filters.
- [ ] For every observed message, retain raw wrapper/payload bytes, timestamp, direction, service/method IDs/names, decode result/error and session version metadata where available.
- [ ] Capture and decode at least one Battle Pass message as the first named-schema validation.
- [ ] During that same session, verify unrelated RPCs are also retained for later slot/lottery/mission/event/economy analysis.
- [ ] Save raw + JSON/CSV outputs plus a reproducible session manifest.
- [ ] If this bounded root attempt fails, restore/verify backups as needed and record why before switching to the next environment/Gadget decision.
- [ ] Append results to `COLLAB_LOG.md` and update `CURRENT_STATUS.md` / `CHANGELOG.md` as applicable.

## Full numerical-system program — after live capture works

- [ ] Build an observed `service/method` inventory from normal browsing and gameplay, preserving unknown traffic.
- [ ] Classify observed traffic into initial domains: slots, lottery, missions/quests, passes/events, offers/economy, clubs/VIP/progression, other/unknown.
- [ ] Add lightweight action/context markers such as opening a machine, spinning, entering lottery, claiming a mission, viewing an offer, etc., without relying on long video OCR.
- [ ] Add a normalized analytical fact/event layer while keeping raw bytes as the source evidence.
- [ ] Build a slots extractor for observable machine/game id, bet, win, feature/free-spin, jackpot and session fields.
- [ ] Build a lottery extractor for ticket cost, entries, draw timing, reward tiers, result/payout and odds/weights when observable.
- [ ] Build a mission/quest extractor for requirement, progress, action type, limitations, rewards, reset/expiry and skip mechanics.
- [ ] Build pass/event/milestone extractors for requirements, reward tracks, currencies, expiry and prestige/repeat loops.
- [ ] Build offer/economy extractors for product price, reward composition, quantity, eligibility/segment, limits and expiry.
- [ ] Add system-specific CSV/Excel/chart/report exporters only downstream of the generic capture/normalization layers.

## Repository cleanup — after live capture works

- [ ] Version the full recovered 36-file `.proto` source set in Git.
- [ ] Verify `scripts/build_descriptors.py` regenerates a descriptor set equivalent to the locally recovered binary.
- [ ] Add reusable report exporters once real live payloads are available.
