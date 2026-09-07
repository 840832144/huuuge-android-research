# Toy Tycoon MITM Capture — SUCCESS (root + bind-mount system CA)

> Path A' is now WORKING: BlueStacks root + bind-mount of a writable cacerts
> dir over `/system/etc/security/cacerts`, plus device proxy → mitmproxy
> decrypts ALL HTTPS. This is the reliable, module-agnostic capture: every
> module's request/response (protobuf) is visible.

## How it was made to work (2026-09-07)

1. Root enabled (`Pie64_5.enable_root_access=1`), `su -c id` → uid 0.
2. `/system` (`/dev/sda1`) is ext4 **ro** and remount fails
   (`'/dev/sda1' is read-only`). `/dev/block/sdb1` (`/system/xbin`) is **rw**.
3. **Bind mount** a writable dir over the system CA dir:
   ```
   su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/b69ec367.0 && chmod 644 /data/local/cacerts/b69ec367.0'
   su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'
   ```
   → `ls /system/etc/security/cacerts/b69ec367.0` shows our cert (1172 B).
4. CA hash filename (Android system cacerts): **`b69ec367.0`** (subject_hash_old).
5. Device global proxy → host mitmproxy: `settings put global http_proxy 10.0.2.2:8080`.
6. mitmdump on host `:8080` with an addon that logs raw protobuf (base64) to
   JSONL. Restart the game (force-stop + start) so it re-reads certs + proxy.

## Result — decrypted, module-agnostic capture

- Business host: **`api-tycoon-101.behefun.com:443`** (CDN: `cdn-res-us2.behefun.com`).
- Endpoints are REST paths + protobuf body. Captured (all modules):
  `/tycoon/data/basic/{saveuserdata,targetlistsocialattrs,clientversion,playerdataversion,playerpaytotal}`,
  `/tycoon/game/attribute/{uploadcoin,changefcmtoken}`,
  `/tycoon/game/slots/randomsteal`, `/tycoon/game/house/myhouse`,
  `/tycoon/game/{exchangerate/rate,gusd/mygusdinfo,reward/list,news/*,invite/info,bindemail/info}`,
  `/tycoon/{mail,friends,team,activity}/basic/*`, `/tycoon/friend/recommend/recommendlist`,
  `/tycoon/team/basic/{eachtargetteam,teamver}`, `/tycoon/login/basic/login`,
  `/tycoon/guest/basic/login`, `/tycoon/server/basic/time`, CDN `PackageManifest_*.version`.
- 110+ flows captured in a single boot; protobuf bodies are readable (raw bytes
  in base64 in `mitm_b64.jsonl`).

## Files / assets

- Addon logger: `C:\bigfish_research\toptycoon\mitm_addon.py` (logs host/path/
  method + base64 req/resp to `mitm_b64.jsonl`).
- CA cert + hash helper: `C:\bigfish_research\toptycoon\mitm\` (mitmproxy-ca-*);
  hash `b69ec367.0` computed via python `cryptography` (X509 subject_hash_old).
- Static protobuf schema: `toytycoon_protocol_dict.json` (422 messages) → decode
  the captured bodies to concrete per-module field values.

## Decoding plan

Map REST path → protobuf message (via service/method), then decode body bytes
with the static dict's field numbers/types to read concrete values (coins,
energy, rewards, etc.). This yields the planner-facing numeric output.
