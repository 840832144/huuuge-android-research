# Toy Tycoon MITM Capture (root + mitmproxy) — Workflow

> Path A': use the now-enable root to install the mitmproxy CA as a system/user
> cert and decrypt the game's HTTPS (business = HTTP + protobuf). This is the
> most reliable, module-agnostic route for reading concrete request/response
> values, avoiding fragile Houdini in-process hooking.

## Status (2026-09-07)

- Root enabled: `su -c id` → uid 0 (Pie64_5.enable_root_access=1).
- Device `127.0.0.1:5605`, IP `10.0.2.15/24` (host = `10.0.2.2`, BlueStacks NAT).
- mitmdump runs on host, listens `8080` (dir `C:\bigfish_research\toptycoon\mitm`),
  writes `flows_all.mitm`.
- CA cert = `mitmproxy-ca-cert.cer` (1172 B).
- **Android cacerts hash-name**: `b69ec367.0` (subject_hash_old-style, computed
  via cryptography: SHA1 of canonical Subject DER, first 4 bytes LE).

## What was attempted / obstacles

- `/system/etc/security/cacerts/` is **read-only** in BlueStacks
  (`mount -o rw,remount /system` → I/O error / `Read-only file system`).
  System-cert install requires a writable system image — not available here.
- Installed user cert at `/data/misc/user/0/cacerts-added/b69ec367.0` (created
  dir as root, chmod 644). Whether the game trusts *user* certs (targetSdk
  dependent) is the open question.
- Set device global proxy `10.0.2.2:8080` (needs re-check after reboot).
- A `adb reboot` left the instance adbd **offline** (BlueStacks reboot is
  unreliable; adbd wedges). Recovery = stop/start instance in the BlueStacks
  Multi-Instance Manager.

## Next steps (after instance recovers)

1. Verify device online + proxy still set (`settings get global http_proxy`).
2. Launch game; confirm mitmproxy decrypts traffic (look for the business host
   `47.88.24.84` in flows_all.mitm).
3. If the game does NOT trust the user cert, options:
   - Re-launch the game so it re-checks user cert store, or
   - Use BlueStacks system-image write (if available), or
   - APK re-pack + let the app trust our CA (mitm alternatives).

## Reusable assets

- CA cert + mitmproxy config: `C:\bigfish_research\toptycoon\mitm\`
- Hash helper: subject_hash_old computed in Python (cryptography).
