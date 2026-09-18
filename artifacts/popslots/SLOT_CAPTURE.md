# Pop! Slots 老虎机采集（模块可选）

> 目标：采集**老虎机游玩**的请求/响应数值（下注、结果、中奖）。
> 范围：**只做老虎机模块**；大厅机器人识别（`parseUserData` 采样）**不在范围内**。

## ⚠️ 实测结论（2026-09-17，在真机实例上验证）

原先设想的"系统代理 + mitmproxy"路线**对 Pop! Slots 无效**，两条实测证据：

| 检验 | 结果 | 含义 |
|---|---|---|
| 游戏进程到代理 `10.0.2.2:8899` 的连接 | **0 个** | 引擎根本没往代理发 |
| 游戏进程直连 `:443` 的连接 | **5 个**（Cloudflare / Google / AWS）| 它自己直连出去 |
| mitmproxy 同期抓到的 | 只有**别的 App**（大麦）的 8 条 | 证书与代理链路本身是好的，只是游戏不用它 |

→ **Shaker 引擎（`libBigCasino.so`）不读 Android 全局 HTTP 代理**（全局代理只对
OkHttp/HttpURLConnection 一类生效）。所以"设备设代理"这条路对 Pop! Slots 走不通。

第二条实测：**hook 引擎导出的 TLS 函数只能拿到密文**。

| hook 目标 | 命中 |
|---|---|
| `libBigCasino.so!SSL_write` / `SSL_read` / `SSL_write_ex` | **0 次** |
| `libssl.so!SSL_write` | 0 次 |
| `libcrypto.so!BIO_write` | 有命中，但内容是 **TLS 记录**（`16 03 01` 握手、`15 03 03` alert）|

→ 引擎的**明文边界不在导出的 `SSL_write/SSL_read` 上**，直接 hook TLS 层拿不到明文。

补充：符号枚举显示 `libBigCasino.so` **静态链接了 OpenSSL / curl / nghttp2**
（数百个 `SSL_*` / `tls_*` / `curl_*` / `nghttp2_*` 导出），所以明文路径确实在进程内，
只是位置不同。已看到的**明文 JSON 边界**候选（引擎自己的解析/回调层）：

- `CDSWebActionHandler::onWebActionResult(bool, Json::Value)`
- `PurchaseOffer::parse(Json::Value)`
- `CostumesCacheManager::onModelFetched(char const*, rapidjson::GenericDocument...)`
- 以及一批 `*Handler::handleCallback(...)`（含 `GameFrameBonusSlotHandler` 等 slot 相关）

## 结论与下一步

- ❌ 代理路线：**对本品无效**（不要再按它操作）。
- ⚠️ TLS hook 路线：只能拿密文，需要改为 hook 引擎**明文边界**（JSON handler / 各自模块的
  `handleCallback`），才能按模块取到数值。这属于**需要在研究机上完成的逆向工作**，
  **不是使用者该做的事**。
- ⏳ 因此目前**还没有可以交给使用者的"一条命令"采集方式**。下一步由研究机完成：
  1. 在 slot 相关 handler 上做候选 hook，确认能拿到明文（含下注/结果/中奖字段）；
  2. 让输出沿用 `tools/capture/` 的 JSONL 格式（`endpoints.py` / `select_module.py` 即可继续用）；
  3. 把"下载并启动 frida-server + 转发端口"也包成一键（自检脚本 `pop_doctor.py` 已能判就绪）。

> 下面的步骤保留作**参考资料**（证书安装、代理设置本身是可用的，只是 Pop! Slots 不经过它；
> 将来若用于会走系统代理的 App 仍然有效）。

---


## 前置条件

| 项 | 要求 |
|---|---|
| 实例 root | ✅ 需要（用于把 CA 装进系统信任区）。`adb -s <serial> root` 或 `su` 都行 |
| 模拟器/游戏 | 实例在跑，Pop! Slots 已安装 |
| 宿主机 | Python + mitmproxy；能与设备互通（BlueStacks 下宿主为 `10.0.2.2`）|
| Frida | ❌ **不需要** |

## 步骤

```bash
# 0) 取代码（工具在 main 上）
git fetch origin && git checkout main && git pull

# 1) 生成 CA 并算出 Android 系统证书的文件名（一次性）
#    首次运行 mitmdump 会生成 mitmproxy-ca-cert.pem；用 python + cryptography 算
#    subject_hash_old（见 TT_CAPTURE_RUNBOOK.md 的「第 0 步」，同一套方法）

# 2) 把 CA 装进系统信任区（/system 只读时用 bind-mount，与 TT 完全相同的做法）
adb -s <serial> push mitmproxy-ca-cert.pem /data/local/tmp/mitm-ca.pem
adb -s <serial> shell "su -c 'mkdir -p /data/local/cacerts && cp /data/local/tmp/mitm-ca.pem /data/local/cacerts/<hash>.0 && chmod 644 /data/local/cacerts/<hash>.0'"
adb -s <serial> shell "su -c 'mount -o bind /data/local/cacerts /system/etc/security/cacerts'"
#    adbd root 通道（没有 su 二进制）时：先 adb root，然后去掉 su -c 前缀直接跑
adb -s <serial> shell "su -c 'ls /system/etc/security/cacerts/<hash>.0'"   # 校验

# 3) 设备走宿主 mitmproxy
adb -s <serial> shell "settings put global http_proxy 10.0.2.2:8080"

# 4) 宿主起采集（模块无关，先全采）
mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py

# 5) 进游戏玩老虎机（从大厅进机台开始转）——采集自动写 mitm_b64.jsonl
```

## 6) 选择"老虎机"这个模块

采集本身不区分模块；**由你来选**：

```bash
# 看有哪些端点、体是什么形状（json / protobuf / gzip / binary）
python tools/capture/endpoints.py mitm_b64.jsonl --show-body 3
python tools/capture/endpoints.py mitm_b64.jsonl --grep slot

# 自己写映射（把上一步看到的模式填进去）
cp tools/capture/modules.example.json modules.json
#   {"slots": ["/slots/", "spin"], ...}

# 只挑老虎机模块
python tools/capture/select_module.py mitm_b64.jsonl --module slots --out slots.jsonl
```

也可以在采集时就直接过滤，只记老虎机相关的流：

```bash
MITM_FILTER='/slots/' mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py
```

## 7) 解码

按 `endpoints.py` 报的形状选解码方式（详见 `tools/capture/README.md`）：

- `json` → `json.loads(base64.b64decode(...))`
- `protobuf?` → `python tools/analysis/toytycoon/full_decode.py`（读 `$MITM_IN`，通用 wire 解码）
- `gzip` → 先 `gzip.decompress`（参考 `extract_save.py` 的写法）

## ⚠️ 关键判定点：内嵌 TLS 是否信任我们的 CA

Pop! Slots 的 TLS 内嵌在 `libBigCasino.so` 里（不是系统 `libssl.so`）。**若它用自带的
根证书库或做证书绑定，mitmproxy 就解不开**，表现为：设备上网正常，但**采集里看不到
游戏的业务 host**（只有系统/其它 App 的流量）。

- **能看到业务 host 并被解密** → 不 pinning，继续步骤 6/7。
- **看不到** → 走备用路线：Frida hook `libBigCasino.so` 的 `SSL_write`/`SSL_read`
  （该库确实导出了这些符号）。这条需要 **frida-server**，也就是
  `artifacts/popslots/ENVIRONMENT_LOCK.md` 里那套前置（自检工具：
  `python tools/analysis/popslots/pop_doctor.py`）。

## 注意

- 采集内容含账号/会话/数值，**只留本地，不入 Git**（`.gitignore` 已排除 `*.jsonl`）。
- 采完**清掉设备代理**：`adb -s <serial> shell "settings put global http_proxy :0"`，
  否则游戏会报"网络中断"。
- 实例重启后 bind-mount 与代理都会丢，需要重做步骤 2–3。
- 不要用 `adb reboot`（会卡死 adbd）。
