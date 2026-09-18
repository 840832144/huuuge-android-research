# Pop! Slots 老虎机采集（模块可选，不需要 Frida）

> 目标：采集**老虎机游玩**的请求/响应数值（下注、结果、中奖）。
> 范围：**只做老虎机模块**；大厅机器人识别（`parseUserData` 采样）**不在范围内**，
> 因此**不需要 Frida**，也就绕开了"frida-server 未安装"这个前置阻塞。

## 为什么走网络层

Pop! Slots 的业务流量是 **HTTPS**（引擎 `libBigCasino.so` 内嵌 TLS）。游玩时上行的
spin/下注与下行的结果/中奖都在请求体与响应体里 —— 抓网络即可拿到数值，**不用进程内
hook**。这条路线就是 Toy Tycoon 上已验证的那套（见
`artifacts/toptycoon/TT_CAPTURE_RUNBOOK.md`），工具是游戏无关的。

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
