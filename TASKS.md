# Active Tasks

## Next milestone — Codex

Goal: capture and decode the first live Battle Pass `Casino.RpcMessage` from the Huuuge Casino client.

- [ ] Pull latest `main`.
- [ ] Run `scripts\sync_local_runtime.ps1` and verify local descriptor/APK/ADB paths.
- [ ] Discover actual BlueStacks executable path, data directory, version, config path, and instance IDs.
- [ ] Preserve the normal instance; use/create an isolated research clone for root/Frida experiments.
- [ ] Verify `ro.dalvik.vm.native.bridge` and actual Huuuge runtime architecture.
- [ ] Establish a working Frida attach path in the research environment.
- [ ] Load `artifacts/live_probe/agent.js` successfully.
- [ ] Capture at least one `Casino.RpcMessage`.
- [ ] Decode a Battle Pass message through the recovered descriptor set.
- [ ] Save raw + JSON/CSV outputs and document the capture location.
- [ ] Append results to `COLLAB_LOG.md` and update `CURRENT_STATUS.md`.

## Repository cleanup — after live capture works

- [ ] Version the full recovered 36-file `.proto` source set in Git.
- [ ] Verify `scripts/build_descriptors.py` regenerates a descriptor set equivalent to the locally recovered binary.
- [ ] Add a repeatable Battle Pass table exporter once real live payloads are available.
