# Toy Tycoon (TT) Capture — 通用接入模板（部署 + 需要收集的信息）

> 适用对象：任何**在自己电脑上从头接入** Top Tycoon(Top Tycoon,
> `com.monopoly.dream.idle.king`) 网络层采集的工程师/团队。
> 这套方法**模块无关**：玩家玩任意模块（老虎机/建造/好友/队伍/邮件/活动…），
> 都能从解密后的 HTTPS 里拿到 protobuf 数值。

---

## 0. 原理（为什么用网络层采集）

Top Tycoon 是 Unity + il2cpp，跑在 BlueStacks 的 ARM64(Houdini) 下。业务 API
是**纯 HTTPS + protobuf**（域名 `api-tycoon-101.behefun.com`）。所以最稳、模块
无关的方式是**网络层 MITM 解密**（root + 系统 CA + mitmproxy），而不是脆弱的
进程内 hook。它对你机器上任何登录账号都成立，不限定特定实例。

---

## 1. 你需要先知道/收集这些信息（★ 对方提供，或对方电脑上自己测）

下面的值是**接入必需**的。有两个来源：**A. 原实现者可告知**（游戏/服务端属性），
**B. 对方在自己电脑上实测/探测**。

### 来源 A —— 原实现者/服务端侧告知（游戏属性，各机器一致）
| 项 | 值 | 说明 |
|---|---|---|
| 游戏包名 | `com.monopoly.dream.idle.king` | Top Tycoon |
| 业务 API 域名 | `api-tycoon-101.behefun.com`（443）| HTTPS 业务入口 |
| CDN 域名 | `cdn-res-us2.behefun.com` | 资源热更 |
| 分析 API 模板 | `/tycoon/{game,data,basic,login,…}/…` | REST 路径 + protobuf body |
| 关键字段示例 | `uploadcoin` f1=金币、`login` f4=uid/f5=用户名/f12=JWT、`saveuserdata` f2=gzip(JSON) | 解码参考 |
| 协议字典来源 | 反编译 `Game.Hotfix.dll` 可导出 422 消息/字段 | 可选，无则按字段号+已知值反推 |

### 来源 B —— 对方在自己电脑上实测/探测（每台机器不同）
| 项 | 占位符 | 如何测 |
|---|---|---|
| BlueStacks 实例名 | `<实例名>` | 多开管理器里实例的名字 |
| adb 端口 | `<adb端口>` | `adb devices` 显示，如 `127.0.0.1:5605` |
| 是否已 root | — | `adb -s <端口> shell su -c id` → uid=0(已root)/uid=2000(未root) |
| 设备 IP / 宿主 IP | `10.0.2.15` / `10.0.2.2` | BlueStacks NAT 通常如此，`ip addr` 实测 |
| mitm 目录 | `<你的mitm目录>` | 你存放 mitmproxy CA 的路径 |
| CA.pem 路径 | `<你的CA.pem>` | 你首次跑 mitmproxy 生成的 `mitmproxy-ca-cert.pem` |
| 系统CA是否只读 | — | `adb ... shell "su -c 'touch /system/etc/security/cacerts/t 2>&1'"` → 报 read-only 则需 bind-mount |
| mitm_addon.py 路径 | `<你的mitm_addon.py>` | 你使用的日志 addon（记录 base64）|

> ★ **发起接入前**：原实现者应让策划/对方确认来源 A 的值（域名/字段示例），
> 并让对方自己测来源 B（实例名/端口/root/路径）。**不要用某个人的特定实例名
> 或本机路径当默认值。**

---

## 2. 一次性初始化（每台机器第一次做）

1. BlueStacks 5 新建实例（Android 9，x86_64），adb 端口拿到，装 TT(`com.monopoly.dream.idle.king`)。
2. 开 root：编辑 `bluestacks.conf`，把该实例的 `enable_root_access` 设为 `"1"`
   （**字节级、无 BOM**，改前备份 conf）。重启实例。验证 `su -c id` → uid 0。
   > 若该 BlueStacks 版本开 root 需要额外补丁，参考已有 Huuuge 的 host 补丁流程；
   > 若实在拿不到 root，改用“APK 重打包 + 证书信任”或模拟器内抓包（见第 6 节）。
3. 装 Python3.12 + mitmproxy（`pip install mitmproxy` → `mitmdump.exe`）。
4. 首次运行 mitmproxy 生成 CA（`mitmproxy-ca-cert.pem`），放到 `<你的mitm目录>`。
5. 计算 CA 的 Android hash 文件名（**一次性**）：
   ```python
   # 换成你的 CA.pem 路径
   from cryptography import x509; import hashlib, re, base64, struct
   pem=open(r'<你的CA.pem>','rb').read()
   b64=re.search(rb'-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----',pem,re.S)
   der=base64.b64decode(b64.group(1).strip())
   cert=x509.load_der_x509_certificate(der)
   h=hashlib.sha1(cert.subject.public_bytes()).digest()
   print('%08x.0'%struct.unpack('<I',h[:4])[0])   # -> e.g. b69ec367.0（你的会不同）
   ```
6. 把 CA 推到设备：`adb -s <adb端口> push <你的CA.pem> /data/local/tmp/mitm-ca.pem`。

---

## 3. 每次会话（实例重启后必须重做，bind-mount 不持久）

```powershell
# (1) bind-mount 系统 CA 目录，放入你的 CA
adb -s <adb端口> shell "su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/<hash>.0 && chmod 644 /data/local/cacerts/<hash>.0'"
adb -s <adb端口> shell "su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'"
# 校验
adb -s <adb端口> shell "su -c 'ls /system/etc/security/cacerts/<hash>.0'"

# (2) 设备走宿主 mitmproxy
adb -s <adb端口> shell "settings put global http_proxy 10.0.2.2:8080"

# (3) 宿主机后台启动 mitmdump（记录 base64）
Start-Process "$env:APPDATA\Python\Python312\Scripts\mitmdump.exe" `
  -ArgumentList "--listen-port","8080","--set","confdir=<你的mitm目录>","-s","<你的mitm_addon.py>" `
  -WindowStyle Hidden
```

---

## 4. 采集与分析

- `mitm_addon.py` 写 `host/path/method + req_b64/resp_b64` 到 `mitm_b64.jsonl`。
- 解码（protobuf wire → 字段号=值）：
  - `/tycoon/game/attribute/uploadcoin` REQ `f1` = 金币余额。
  - `/tycoon/login/basic/login` RESP `f4`=uid、`f5`=用户名、`f12`=JWT。
  - `/tycoon/data/basic/saveuserdata` REQ `f1`=数据块名、`f2`=gzip(base64(json)) → 解 gzip 得完整 JSON 存档。
- 字段字典（可选，422 消息）可从 `Game.Hotfix.dll` 离线导出；否则按“字段号+已知 UI 值”反推。

---

## 5. 输出给策划的结论（示例）

- 金币余额变化链（uploadcoin f1 序列）与差值（获取/消耗）。
- spin 倍率 ×N 消耗 N 能量（bet 默认 ×1，最高 ×5 一次耗 5 能量）；spin 产出金币。
- 建造：`house_res_id`(30001=StorageBuilding/30004)、`houseOrder/houseLevel`、金币消耗在存档块。
- 偷取/攻击：`steal/targethouse` RESP f3 嵌套含可偷数量、目标玩家 uid。

---

## 6. 没有 root 时的替代方案

- **APK 重打包 + network_security_config 信任你的 CA**：改 APK 加 `trust-anchors`，
  重签重装。缺点：可能触发签名/加固检测。
- **模拟器内抓包**：若系统证书区可写则直接写；若不可写且无 root，考虑用
  支持证书导入的模拟器镜像。
- 原则上优先拿 root（BlueStacks 多数版本可开，参考 Huuuge 已验证流程）。

---

## 7. 特别注意（避坑）

- **不要用 `adb reboot`**（会卡死 adbd，实例需在 BlueStacks 多开管理器里重启）。
- 实例重启后 **重新 bind-mount 证书 + 重新设代理**。
- 玩完**清掉代理** `settings put global http_proxy :0`，否则游戏会“网络中断”。
- 所有 raw/账号/数值数据只留本地，**不提交 Git**；Git 只记 schema/路径/类型。
