# Toy Tycoon MITM Decode — FULL SUCCESS (module-agnostic value capture)

> Path A' is fully working and now DECODES concrete values. Chain:
> root + bind-mount system CA → device proxy → mitmproxy decrypts all HTTPS →
> protobuf bodies + full JSON player save decode to numeric fields. This is the
> planner-facing value-capture tool for ANY module.

## Captured & decoded (verified 2026-09-07)

- **Business host**: `api-tycoon-101.behefun.com:443` (CDN `cdn-res-us2.behefun.com`).
- **126 flows** across all modules, 41 with responses (GC).
- **Player identity**: `/tycoon/login/basic/login` RESP → uid `f4=20044286775`,
  name `f5='tycoon775'`, JWT `f12`, `f10/f11` timestamps.
- **Currency**: `/tycoon/game/attribute/uploadcoin` REQ → `f1=101882` (coin),
  `f11=132`, `f12=79`. Dict maps `CGUploadCoin = {coin, energy, estate}`.
- **Full player save** `/tycoon/data/basic/saveuserdata`: body is
  `f1=<block>` + `f2=<gzip(base64(json))>` + `f3=<version>`. Blocks decoded to
  JSON: `ext2` (40KB), `basic` (7.9KB), `stage` (3.4KB), `ext` (1.8KB),
  `system` (1.9KB). Values read: `bonus_lua.energy=34`, `task_energy=24`,
  `energy_level=3`, `history_earn_energy=30`.
- **Activity**: `/tycoon/activity/ladder/myladderinfo` RESP → `f5=16176`,
  `f13=13218`, `f14=70`, `f23=100`.
- **Endpoints** (all modules): `/tycoon/data/basic/{saveuserdata,targetlistsocialattrs,
  clientversion,playerdataversion,playerpaytotal}`, `/tycoon/game/attribute/
  {uploadcoin,changefcmtoken}`, `/tycoon/game/{slots/randomsteal, house/myhouse,
  exchangerate/rate, gusd/mygusdinfo, reward/list, news/*, invite/info, bindemail/info}`,
  `/tycoon/{mail,friends,team,activity}/basic/*`, `/tycoon/friend/{recommend/recommendlist,
  waitlist/waitlist}`, `/tycoon/team/basic/{eachtargetteam,teamver}`,
  `/tycoon/{login/basic/login, guest/basic/login, server/basic/time}`.

## Decoding tools (local `C:\bigfish_research\toptycoon\`)

- `mitm_addon.py` — mitmproxy addon: logs host/path/method + base64 req/resp
  (raw protobuf) to `mitm_b64.jsonl`.
- `proto_dump.py` / `full_decode.py` — decode protobuf wire → `field#=value`.
- `extract_save.py` — pulls the gzip JSON player save blocks from saveuserdata
  into `save_blocks/*.json`.
- CA + hash helper `b69ec367.0` in `mitm\`.

## How to run

1. Root + bind-mount cacerts (see prior section), `settings put global http_proxy 10.0.2.2:8080`.
2. `mitmdump --listen-port 8080 -s mitm_addon.py` on host.
3. (Re)launch the game; it re-reads certs/proxy and all HTTPS is decrypted.
4. Play; `mitm_b64.jsonl` grows; decode with the tools above.

## Value for planner

Any module's request/response protobuf fields AND the full JSON player save are
available — coins, energy, rewards, activity values, building progress — module-
agnostic, re-runnable, no fragile in-process hooking.
