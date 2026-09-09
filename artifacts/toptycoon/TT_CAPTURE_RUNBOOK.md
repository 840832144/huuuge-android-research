# Top Tycoon 采集器 —— 正确部署指引（已验证跑通）

> 目标：采集 Top Tycoon（com.monopoly.dream.idle.king）逐把 Spin 的
> bet / 结果 / 余额，供策划拆值。
>
> **重要**：不要走 Frida 进程内 hook（那是死路，见文末"为什么不用 Frida"）。
> **用已经验证跑通的 mitmproxy 网络层方案** —— 业务是 HTTPS+protobuf，
> 数值就在请求/响应里，**已实测拿到金币/能量/完整存档**。

---

## 一、为什么不用 Frida 进程内 hook（先别踩坑）

Top Tycoon 是 **ARM64 Houdini 翻译 + il2cpp 符号剥离 + xLua 静态链接**，三重叠加导致
Frida Gadget 钩业务函数基本走不通：
- ARM64 Gadget 只枚举 ARM64 命名空间，看不到 x86-64 侧的 `libil2cpp.so`（Houdini 架构隔离）
- `libil2cpp.so` 被 strip，无标准 `il2cpp_*` 导出（要从 global-metadata.dat 重建，复杂脆弱）
- `libxlua.so` 的 Lua API 静态链接不导出，hook 不到
- `UnitySendMessage` 不走业务逻辑，hook 它 0 消息

**→ 已实证业务流量是 HTTPS（`api-tycoon-101.behefun.com`），用网络层抓包即可拿到所有数值，无需碰这些。**

---

## 二、方案原理（一句话）

```
root + bind-mount 系统证书(mimproxy CA)
  → 设备代理 → 宿主 mitmproxy
  → 游戏信任系统CA → 所有 HTTPS 明文
  → protobuf 解码 + gzip 玩家存档解 JSON
  → 拿到每次 spin/建造/活动的具体数值
```

---

## 三、环境（已确认）

| 项 | 值 |
|---|---|
| 蓝叠实例 | `topTycoon` = Pie64_5，adb `127.0.0.1:5605` |
| 系统 | Android 9, x86_64（游戏 ARM64 走 Houdini）|
| root | 已开（`Pie64_5.enable_root_access="1"`；`su -c id` → uid 0）|
| 游戏包 | `com.monopoly.dream.idle.king` |
| 业务 host | `api-tycoon-101.behefun.com:443` |
| 系统 CA hash | `b69ec367.0` |
| 设备/宿主 | `10.0.2.15` / `10.0.2.2`（蓝叠 NAT）|
| mitmproxy | 宿主机 8080 |

---

## 四、部署步骤

### 第 0 步：一次性（生成 CA + 算 hash）
```powershell
# 1. 安装 mitmproxy
pip install mitmproxy

# 2. 首次跑一次生成 CA（在安装目录出 mitmproxy-ca-cert.pem）
# 3. 算 Android 系统证书 hash 文件名
python -c "
from cryptography import x509; import hashlib, re, base64, struct
pem=open('mitmproxy-ca-cert.pem','rb').read()
b64=re.search(rb'-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----',pem,re.S)
der=base64.b64decode(b64.group(1).strip())
c=x509.load_der_x509_certificate(der)
h=hashlib.sha1(c.subject.public_bytes()).digest()
print('%08x.0'%struct.unpack('<I',h[:4])[0])"
# 输出如 b69ec367.0
```

### 第 1 步：装系统证书 + 设备代理（每次实例重启后要做）
```powershell
$adb="C:\platform-tools\adb.exe"
# 把 CA 推到设备
$adb -s 127.0.0.1:5605 push mitmproxy-ca-cert.pem /data/local/tmp/mitm-ca.pem
# bind-mount：/system 只读 → 把可写目录挂到系统证书区
$adb -s 127.0.0.1:5605 shell "su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/b69ec367.0 && chmod 644 /data/local/cacerts/b69ec367.0'"
$adb -s 127.0.0.1:5605 shell "su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'"
# 校验（应看到文件）
$adb -s 127.0.0.1:5605 shell "su -c 'ls /system/etc/security/cacerts/b69ec367.0'"
# 设备代理指向宿主 mitmproxy
$adb -s 127.0.0.1:5605 shell "settings put global http_proxy 10.0.2.2:8080"
```

### 第 2 步：宿主机跑 mitmproxy（带记录 addon，后台）
```powershell
Start-Process "$env:APPDATA\Python\Python312\Scripts\mitmdump.exe" `
  -ArgumentList "--listen-port","8080","--set","confdir=C:\bigfish_research\toptycoon\mitm","-s","C:\bigfish_research\toptycoon\mitm_addon.py" `
  -WindowStyle Hidden
# 校验
netstat -ano | findstr :8080
```

### 第 3 步：启动游戏 + 玩家玩
```powershell
$adb -s 127.0.0.1:5605 shell "am start -n com.monopoly.dream.idle.king/com.google.firebase.MessagingUnityPlayerActivity"
```
玩家玩任意模块（spin/建造/活动…），`mitm_b64.jsonl` 自动记录。

### 第 4 步：分析数值
```powershell
# protobuf wire 解码 → 字段#=值
python C:\bigfish_research\toptycoon\full_decode.py
# 解完整玩家存档（gzip→JSON）
python C:\bigfish_research\toptycoon\extract_save.py
```

---

## 五、已知能拿到的数值（实证）

| 数据 | 字段 |
|---|---|
| 金币余额 | `/tycoon/game/attribute/uploadcoin` REQ `f1`（实测 101882 / 109682 / …）|
| 玩家 uid / 用户名 | `/tycoon/login/basic/login` RESP `f4` / `f5` |
| 完整玩家存档 | `/tycoon/data/basic/saveuserdata` f2=gzip(JSON)：`bonus_lua.energy` 等 |
| 活动数值 | `/tycoon/activity/ladder/myladderinfo` RESP（f5/f13/f14 等）|
| 各模块接口 | `slots/house/mail/friend/team/activity/reward/news` 等 |

---

## ★★★ 六、代理开关（必看，否则游戏登不进）★★★

**这个坑最容易踩，务必记住**：

- **采集时**：必须**开着代理**（`10.0.2.2:8080`），否则 mitmproxy 抓不到数据。
- **不采集/要正常玩时**：必须**清掉代理**，否则游戏**直接"链接中断"登不进**（实测踩坑）。

```powershell
# 开代理（采集时）
adb -s 127.0.0.1:5605 shell "settings put global http_proxy 10.0.2.2:8080"

# 清代理（不采集时，游戏才能连上服务器——否则报"链接中断"）
adb -s 127.0.0.1:5605 shell "settings put global http_proxy :0"
```

**判断方法**：
- 想看当前代理：`adb -s 127.0.0.1:5605 shell "settings get global http_proxy"`
  - 返回 `10.0.2.2:8080` = 代理开着（采集模式）
  - 返回 `:0` = 直连（正常模式）
- 游戏报**"链接中断 / 请检查网络"** = **100% 代理没清**，不要怀疑别的地方，直接 `:0` 清掉重开游戏。

---

## 七、注意（避坑）

- **不要 `adb reboot`**（会卡死 adbd，实例要在蓝叠多开管理器重启）
- 实例重启后要**重做第 1 步**（bind-mount + 代理会丢）
- **raw/账号/数值只留本地**，不提交 Git（Git 只放 schema/脚本/文档）

---

## 八、可用工具（已跑通）

| 文件 | 用途 |
|---|---|
| `mitm_addon.py` | mitmproxy addon：记录 host/path/method + base64 请求/响应 到 `mitm_b64.jsonl` |
| `full_decode.py` | protobuf wire 解码 → 字段#=值 |
| `extract_save.py` | 解 gzip 玩家存档 → `save_blocks/*.json` |
| `toytycoon_protocol_dict.json` | 422 消息协议字典（字段名对照）|
| `DEPLOY_AND_ONBOARD.md` | 完整部署文档 + 可发给 AI 的话术 |

---

*基于已实测跑通的 `artifacts/toptycoon/MITM_CAPTURE.md`（FULL SUCCESS）整理。*
