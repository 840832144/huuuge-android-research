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
- [ ] Perform one bounded check whether BlueStacks 5 China exposes a supported Root Access control elsewhere in the research-instance UI/resources.
- [ ] If no supported control exists or it still cannot yield UID 0, stop repeating BlueStacks root attempts and choose the isolated fallback: ARM64 Frida Gadget research APK or a separate rootable research emulator/device.
- [ ] Establish a working Frida attach path in the research environment.
- [ ] Load `artifacts/live_probe/agent.js` successfully.
- [ ] Capture at least one `Casino.RpcMessage`.
- [ ] Decode a Battle Pass message through the recovered descriptor set.
- [ ] Save raw + JSON/CSV outputs and document the capture location.
- [x] Append discovery/permission results to `COLLAB_LOG.md` and update `CURRENT_STATUS.md`.

## Repository cleanup — after live capture works

- [ ] Version the full recovered 36-file `.proto` source set in Git.
- [ ] Verify `scripts/build_descriptors.py` regenerates a descriptor set equivalent to the locally recovered binary.
- [ ] Add a repeatable Battle Pass table exporter once real live payloads are available.
