# Toy Tycoon (TT) Capture — Deployment & Onboarding Guide for a Huuuge-Experienced Engineer

> Target audience: an engineer who ALREADY has Huuuge capture working on this
> machine, and now wants their computer's AI agent to also capture **Toy Tycoon
> (Top Tycoon, `com.monopoly.dream.idle.king`)** — reusing the proven, module-
> agnostic **mitmproxy (Path A')** route.
>
> This doc gives (1) the exact environment facts, (2) the full runbook, and
> (3) a **copy-paste prompt** ("话术") to hand directly to that machine's AI.

---

## 0. Key insight: why a different approach than Huuuge

Huuuge was captured in-process (Frida + ARM64 Gadget via Houdini). Toy Tycoon
is also Unity + il2cpp under BlueStacks Houdini, but the **business API is
plain HTTPS + protobuf** (host `api-tycoon-101.behefun.com`). So the robust,
module-agnostic way is **network-layer MITM decryption**, not fragile in-process
hooking. It works for ANY module (slots/building/mail/friend/team/activity/…).

---

## 1. Confirmed environment (2026-09-07)

| Item | Value |
|---|---|
| BlueStacks instance | `topTycoon` = `Pie64_5`, adb `127.0.0.1:5605` |
| Emulator OS | Android 9, SM-G998B, x86_64 (game ARM64 via Houdini) |
| Root | ENABLED — `bst.instance.Pie64_5.enable_root_access="1"`; `su -c id` → uid 0 |
| Host binaries | already patched from Huuuge work (HD-Player.exe @0x1BEB00=`31 C0 C3`, HD-MultiInstanceManager.exe @0x550E3=NOP) |
| Game package | `com.monopoly.dream.idle.king` (Top Tycoon) |
| **Business API host** | `api-tycoon-101.behefun.com:443` (CDN `cdn-res-us2.behefun.com`) |
| Android CA hash-file | `b69ec367.0` (= `subject_hash_old` of mitmproxy CA) |
| Device IP / host | device `10.0.2.15/24`, host = `10.0.2.2` (BlueStacks NAT) |
| mitmproxy | `mitmdump` on host, port **8080**, confdir `C:\bigfish_research\toptycoon\mitm` |
| CA cert PEM | `C:\bigfish_research\toptycoon\mitm\mitmproxy-ca-cert.pem` |

**System CA mount trick (critical):** `/system` (`/dev/sda1`) is RO and remount
fails. `/system/xbin` (`/dev/block/sdb1`) is RW. So we **bind-mount** a writable
dir over `/system/etc/security/cacerts`:

```
su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/b69ec367.0 && chmod 644 /data/local/cacerts/b69ec367.0'
su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'
```

This is **not persistent** — it must be re-run after an emulator reboot.

---

## 2. Full runbook (runbook)

### 2.1 Fresh-start setup (only needed once)
1. Add a BlueStacks 5 instance `topTycoon` (Pie64_5), adb port 5605, Android 9,
   x86_64. Install TT (`com.monopoly.dream.idle.king`) into it.
2. Enable root: in `D:\BlueStacks_nxt_cn\bluestacks.conf` set
   `bst.instance.Pie64_5.enable_root_access="1"` (byte-level edit, NO BOM; backup
   the conf first). Reboot the instance. Verify `adb ... shell su -c id` → uid 0.
3. Host tools: install Python 3.12 + mitmproxy
   (`pip install mitmproxy` → `mitmdump.exe`). Generate the CA in
   `C:\bigfish_research\toptycoon\mitm` (first mitmproxy run creates `mitmproxy-ca-cert.pem`).
4. Compute the Android CA build of the subject:
   ```python
   from cryptography import x509; import hashlib, re, base64, struct
   pem=open(r'...\mitmproxy-ca-cert.pem','rb').read()
   b64=re.search(rb'-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----',pem,re.S)
   der=base64.b64decode(b64.group(1).strip())
   cert=x509.load_der_x509_certificate(der)
   h=hashlib.sha1(cert.subject.public_bytes()).digest()
   print("%08x.0"%struct.unpack('<I',h[:4])[0])   # -> b69ec367.0
   ```
5. Push the CA to the device: `adb push mitmproxy-ca-cert.pem /data/local/tmp/mitm-ca.pem`.

### 2.2 Per-session (after emulator reboot)
Repeat these every time the emulator restarts:
```powershell
# bind-mount the system CA dir
adb -s 127.0.0.1:5605 shell "su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/b69ec367.0 && chmod 644 /data/local/cacerts/b69ec367.0'"
adb -s 127.0.0.1:5605 shell "su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'"
# point device to host mitmproxy
adb -s 127.0.0.1:5605 shell "settings put global http_proxy 10.0.2.2:8080"
# start mitmproxy with the logging addon
Start-Process "$env:APPDATA\Python\Python312\Scripts\mitmdump.exe" `
  -ArgumentList "--listen-port","8080","--set","confdir=C:\bigfish_research\toptycoon\mitm","-s","C:\bigfish_research\toptycoon\mitm_addon.py" `
  -WindowStyle Hidden
```
Then launch the game (it re-reads certs + proxy). All HTTPS is now decrypted.

> After playing, unset proxy to avoid the game "网络中断":
> `adb -s 127.0.0.1:5605 shell "settings put global http_proxy :0"`

### 2.3 Analyze the traffic
- `mitm_addon.py` writes host/path/method + base64 req/resp to
  `C:\bigfish_research\toptycoon\mitm_b64.jsonl`.
- Decode protobuf to field#=value: `python full_decode.py`
- Extract full JSON player save: `python extract_save.py` (→ `save_blocks\*.json`).

---

## 3. Copy-paste prompt ("话术") to hand to that machine's AI

> Give the AI this as one block. It is written so the AI can act from scratch.
> It references the same paths and facts; change paths only if needed.

"""
你正在在这台 Windows 主机上，为 BlueStacks 5 里的《Top Tycoon》
(com.monopoly.dream.idle.king) 做**网络层采集**（模块无关）。目标：玩家在游戏里
玩任意模块，你都能从解密后的 HTTPS 里抓出具体的 protobuf 数值。

环境（已确认，不要改）：
- BlueStacks 实例 = topTycoon (Pie64_5)，adb = 127.0.0.1:5605，Android 9，x86_64
  （游戏是 ARM64 走 Houdini）。
- 已开 root：adb 127.0.0.1:5605 shell su -c id 返回 uid=0。
- 业务 API 域名 = api-tycoon-101.behefun.com（443）；CDN = cdn-res-us2.behefun.com。
- 设备 IP=10.0.2.15，宿主机=10.0.2.2（BlueStacks NAT）。
- mitmdump 可用；CA 已生成在 C:\bigfish_research\toptycoon\mitm\mitmproxy-ca-cert.pem。
- Android 系统 CA 的 hash 文件名 = b69ec367.0。

第一步：把 mitmproxy 的 CA 以“bind-mount”方式装进系统信任区，并让设备走代理。
  adb -s 127.0.0.1:5605 shell "su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/b69ec367.0 && chmod 644 /data/local/cacerts/b69ec367.0'"
  adb -s 127.0.0.1:5605 shell "su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'"
  adb -s 127.0.0.1:5605 shell "settings put global http_proxy 10.0.2.2:8080"
  校验：adb -s 127.0.0.1:5605 shell "su -c 'ls /system/etc/security/cacerts/b69ec367.0'"
        → 应看到文件。若实例刚重启，bind-mount 会丢失，需重做本步。

第二步：在宿主机后台启动 mitmproxy（记录 raw base64 到 mitm_b64.jsonl）。
  Start-Process "$env:APPDATA\Python\Python312\Scripts\mitmdump.exe" `
    -ArgumentList "--listen-port","8080","--set","confdir=C:\bigfish_research\toptycoon\mitm","-s","C:\bigfish_research\toptycoon\mitm_addon.py" `
    -WindowStyle Hidden
  校验：netstat -ano | findstr :8080 应有 LISTEN。

第三步：启动游戏并请玩家玩一会儿（老虎机/建造/好友/队伍/邮件/活动等任选）。
  注意：不要用 adb reboot（会卡死 adbd）。切换实例用 BlueStacks 多开管理器。

第四步：分析 mitm_b64.jsonl。写一个解码器：
  - 每个 flow: host/path/method + req_b64/resp_b64。
  - 用 protobuf wire 格式解出 “字段号=值”。示例：
    /tycoon/game/attribute/uploadcoin 请求 f1=金币余额（已见 101882/109682/…）。
    /tycoon/login/basic/login 响应 f4=玩家uid、f5=用户名、f12=JWT。
    /tycoon/data/basic/saveuserdata 请求体是 f1=数据块名 + f2=gzip(base64(json))
      —— 解 gzip 得到完整 JSON 存档（硬币/能量/建筑/活动全部数值）。
  - 协议的字段字典（422 消息）已有：C:\bigfish_research\toptycoon\toytycoon_protocol_dict.json。

第五步：输出给策划的结论。例如：
  - 金币余额变化链（uploadcoin 的 f1 序列）与差值（获取/消耗）。
  - spin 倍率×N 消耗 N 能量（玩家调 bet：默认×1，最高×5一次耗5能量）；
    spin 产出金币（不同 spin 的 f 字段）。
  - 建造：house_res_id（如 30001=StorageBuilding, 30004），houseOrder/houseLevel，
    金币消耗在基本/扩展存档块里。
  - 偷取/攻击：steal/targethouse 响应 f3 嵌套里有可偷数量、目标玩家uid。

特别提醒：
  - 不要用 adb reboot；实例重启后重新 bind-mount 证书 + 重新设置代理。
  - 玩完把代理清掉：settings put global http_proxy :0，否则游戏会“网络中断”。
  - 所有 raw/账号/数值数据只留在本地，不要提交 Git；Git 只记 schema/路径/类型。
"""

---

## 4. Reusable asset list (already on this machine)

- `C:\bigfish_research\toptycoon\mitm_addon.py` — mitmproxy logging addon (b64).
- `C:\bigfish_research\toptycoon\full_decode.py` — protobuf wire decoder.
- `C:\bigfish_research\toptycoon\extract_save.py` — gzip JSON save extractor.
- `C:\bigfish_research\toptycoon\mitm\` — mitmproxy CA (pem/cer/p12/dhparam).
- `C:\bigfish_research\toptycoon\toytycoon_protocol_dict.json` — 422-message schema.
- Repo docs: `artifacts/toptycoon/{ENVIRONMENT_LOCK,PROTOCOL_RECOVERY,RUNTIME_CAPTURE_MINIMAL,GENERIC_CAPTURE,MITM_CAPTURE}.md`.
