# Active Tasks

## Next milestone — Codex

Goal: capture and decode the first live Battle Pass `Casino.RpcMessage` from the Huuuge Casino client.

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
- [ ] Capture at least one `Casino.RpcMessage`.
- [ ] Decode a Battle Pass message through the recovered descriptor set.
- [ ] Save raw + JSON/CSV outputs and document the capture location.
- [ ] If this bounded root attempt fails, restore/verify backups as needed and record why before switching to the next environment/Gadget decision.
- [ ] Append results to `COLLAB_LOG.md` and update `CURRENT_STATUS.md` / `CHANGELOG.md` as applicable.

## Repository cleanup — after live capture works

- [ ] Version the full recovered 36-file `.proto` source set in Git.
- [ ] Verify `scripts/build_descriptors.py` regenerates a descriptor set equivalent to the locally recovered binary.
- [ ] Add a repeatable Battle Pass table exporter once real live payloads are available.
