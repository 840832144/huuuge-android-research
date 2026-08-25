# BlueStacks-Root-GUI audit and applied scope

Audited source: `RobThePCGuy/BlueStacks-Root-GUI` at commit
`7002d185522c41a15ea9b184eff24393c5a62a11` (`master`, clean worktree).
The audited source reports application version `3.9.0` and explicitly detects
the China registry key `SOFTWARE\BlueStacks_nxt_cn`. Its compatibility matrix
lists China `5.22.170.6509`, including Android 9, in patch mode.

## Confirmed write scope

The patch-mode workflow has one shared host step and one per-instance step.

Shared host step:

- `HD-Player.exe`: replace the three-byte prologue of
  `_isDiskVerificationRequired()` with `31 C0 C3`, and replace the five-byte
  `plrCheckDiskIntegrity` call with `B0 01 90 90 90`.
- `HD-MultiInstanceManager.exe`: replace the five-byte call that resets
  `.enable_root_access` with NOPs.
- Create adjacent `.prepatch.bak` and patched-hash sidecars for rollback.
- Stop all known BlueStacks processes before writing. This is install-wide,
  even when only one Android instance is subsequently rooted.

Per-instance step:

- Set `bst.instance.<instance>.enable_root_access="1"` and the shared
  `bst.feature.rooting="1"` in `bluestacks.conf`.
- Scan only the selected instance directory. Prefer that instance's
  `Data.vhdx`; fall back to its `Root.vhd` only when `Data.vhdx` is absent.
- Change the three-byte entry of each signed-whitelist-gated guest `su` from
  its original prologue to `B0 01 C3`, recording every original offset/byte
  sequence in `<disk>.suroot.json` for exact reversal.

The GUI selection passes the selected instance's `data_path` directly to the
offline patcher; the code does not enumerate other instances on this path.
The CLI's separate `--all` path was not used.

## Local signature proof and applied result

Before writes, this machine's binaries produced exactly one match for every
required locator and the expected original bytes:

- `HD-Player.exe` unlock prologue at file offset `0x1BEB00`.
- `HD-Player.exe` integrity call at file offset `0xB4B51`.
- `HD-MultiInstanceManager.exe` root-reset call at file offset `0x550E3`.

Only `Pie64_1 / HuuugeResearch` was selected for the disk patch. Its clean,
powered-off `Data.vhdx` produced two gated `su` entries at virtual disk offsets
`0x1E08CB7860` and `0x1E08EC6860`, both with original bytes `53 48 8D`.
Both were changed to `B0 01 C3` and recorded in the sidecar.

The normal `Pie64` root flag remains `0`. Post-change SHA-256 checks for its
`Data.vhdx`, `Root.vhd`, `fastboot.vdi`, and `Pie64.bstk` all exactly matched
their pre-change baselines.

## Backup and rollback

The complete local backup is outside Git at:

`D:\BlueStacks_nxt_cn\backups\huuuge-research\plan1_20260825_181500`

`manifest.sha256.txt` records source/backup SHA-256 pairs, the normal-instance
baselines, and the pinned third-party commit. It contains full copies of both
patched host executables, `bluestacks.conf`, `Pie64_1.Data.vhdx`, and both
`Pie64_1` instance descriptors. Every source/backup pair matched before writes.

Rollback procedure: power off BlueStacks, restore the external host binaries,
shared config, research VHDX, and research instance descriptors to their exact
source paths, then verify the manifest hashes. The full VHDX copy is the final
recovery path even if the three-byte `su` sidecar reversal cannot be used.

## Runtime proof and residual risk

`su -c id` on ADB serial `127.0.0.1:5565` returned real `uid=0(root)` after
reboot. The research instance remained stable. The shared executable patches
invalidate the original Microsoft/BlueStacks Authenticode signatures and put
the installation into developer/integrity-bypass mode; those are accepted
host-wide effects of this bounded plan. The normal Android instance was not
started, rooted, or instrumented.
