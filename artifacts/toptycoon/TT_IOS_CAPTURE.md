# Top Tycoon iOS 采集方案（不越狱 + Trust Store + mitmproxy）

> 目标：iPhone 上采集 Top Tycoon 逐把 Spin 的数值，供策划拆值。
> 方法：**不越狱**，安装 mitmproxy CA 描述文件 + 开启信任 + HTTP 代理，用
> mitmproxy 抓 HTTPS。协议与 Android 完全一样（`api-tycoon-101.behefun.com`
> + protobuf），可直接复用 Android 的解码脚本（full_decode/extract_save）。

## 0. 方案选择依据

- iPhone **没越狱** + **接近大号的测试号** → 必须避免"越狱/重签名/改包"（封号风险）。
- **方案 B（不越狱 + Trust Store）**：装描述文件信任 CA + mitmproxy。不动系统、
  不进 root、不改包，风险最低。
- Android 端已证明 **TT 不做证书 pinning**；iOS 是**同一款 Unity 游戏**，大概率
  也不 pinning → 方案 B 应能直接抓。

## 1. 前提（实测确认）

**唯一关键前提：TT iOS 是否做证书 pinning。**
- 判断方法：装证书 + 开代理后，看 mitmproxy 能否解出 HTTPS 明文。
  - 能解出 `api-tycoon-101.behefun.com` 的明文 → **不 pinning**，方案 B 直接成。
  - `mitm_stderr` 报证书错误/握手失败/抓不到业务 host → **有 pinning**，需升级
    （越狱 + Frida pinning bypass，风险高，接近大号测试号慎用）。

## 2. 电脑侧准备（已就绪）

| 项 | 值 |
|---|---|
| CA | `C:\bigfish_research\toptycoon\mitm\mitmproxy-ca-cert.cer`（1172B，iOS 可用）|
| mitmdump | `$env:APPDATA\Python\Python312\Scripts\mitmdump.exe` |
| 电脑局域网 IP | `192.168.110.63`（iepconfig 实测，给 iPhone 设代理用）|
| 记录 addon | `C:\bigfish_research\toptycoon\mitm_addon.py` |
| 解码 | `full_decode.py` / `extract_save.py` |

## 3. 步骤

### 3.1 iPhone 安装并信任 CA（两步都要，缺一不可）
1. **装描述文件**：把 `.cer` 传到 iPhone（AirDrop / 邮件 / Safari 打开 `.cer`）
   → 提示安装 → **设置→通用→VPN与设备管理** 里安装该描述文件。
2. **开启信任**：**设置→通用→关于本机→证书信任设置** → 找到 mitmproxy CA
   → **打开开关**（这步必须，否则 iOS 不信任）。

### 3.2 iPhone 设 HTTP 代理
- **设置→Wi-Fi→当前网络→HTTP 代理→手动**：
  - 服务器 = `192.168.110.63`
  - 端口 = `8080`

### 3.3 电脑跑 mitmproxy（带 addon，后台）
```powershell
Start-Process "$env:APPDATA\Python\Python312\Scripts\mitmdump.exe" `
  -ArgumentList "--listen-port","8080","--set","confdir=C:\bigfish_research\toptycoon\mitm","-s","C:\bigfish_research\toptycoon\mitm_addon.py" `
  -WindowStyle Hidden
```

### 3.4 iPhone 打开 TT 玩 → 分析
- iPhone 打开 Top Tycoon 玩任意模块 → mitmproxy 记录 → `mitm_b64.jsonl` 增长。
- 解码（与 Android 同一套）：
```powershell
python C:\bigfish_research\toptycoon\full_decode.py
python C:\bigfish_research\toptycoon\extract_save.py
```

## 4. 风险/注意

- **方案 B 最安全**（不越狱、不进系统、不改包），接近大号测试号风险低。
- **若实测有 pinning** → 方案 B 抓不到 → 需升级（越狱 + Frida bypass），
  适合真机测试号，**接近大号慎用**。
- **每次重启 iPhone 不用重装 CA**（信任是持久的），但 **HTTP 代理要重新设**（重启丢）。
- **测试完清代理**（iPhone Wi-Fi → HTTP 代理 → 关/自动），否则 iPhone 也"网络中断"。

## 5. 成功判据

iPhone 玩一会儿，`mitm_b64.jsonl` 出现 `uploadcoin`(金币)/`login`(uid,用户名)/
`saveuserdata`(gzip 存档) 记录，`full_decode.py` 解出字段号=值。
