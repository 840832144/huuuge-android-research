# Toy Tycoon (TT) Capture — AI 引导式接入（命令 + 探测 + 何时问用户）

> 给「在这台电脑上用 AI 从零搭建」的场景。AI 按步骤走，能自己探测的就不问；
> 需要用户/策划给的才停下问。**不要照抄任何一台机器的实例名/端口/路径。**

> ★关键决策：**用网络层 mitmproxy，不要用 Frida 进程内 hook。**
> Top Tycoon 是 ARM64 Houdini + il2cpp strip + xLua 静态链接，Frida 钩业务函数
> 走不通；业务是 HTTPS（api-tycoon-101.behefun.com），网络层抓包已实测拿到
> 金币/能量/存档。完整 runbook 见 `TT_CAPTURE_RUNBOOK.md`，话术见
> `tools/analysis/toytycoon/TT_CAPTURE_PROMPT.txt`。

## 仓库资产（clone 后直接可用）
- tools/analysis/toytycoon/mitm_addon.py
- tools/analysis/toytycoon/full_decode.py
- tools/analysis/toytycoon/extract_save.py
- tools/analysis/toytycoon/proto_dump.py
- tools/analysis/toytycoon/TT_CAPTURE_PROMPT.txt   （给 AI 的一键话术）
- artifacts/toptycoon/MITM_CAPTURE.md   （跑通案例 + 字段示例）
- artifacts/toptycoon/TT_CAPTURE_RUNBOOK.md（正确部署 runbook）
- artifacts/toptycoon/PROTOCOL_RECOVERY.md（协议字典来源）

## 步骤

### 1 环境探测
- `adb devices` 拿 adb 端口（127.0.0.1:xxxx）。
- 确认包 `com.monopoly.dream.idle.king` 已装。
- `adb -s <端口> shell su -c id` → uid=0 已 root；uid=2000 未 root。
- 问用户（若需要）：实例在 BlueStacks 的名字、是否允许开 root。

### 2 生成/确认 CA + 算 Android hash（一次性）
- 首次跑 mitmdump 生成 mitmproxy-ca-cert.pem。
- 算 `<hash>.0`（命令见话术第2步）。记录如 b69ec367.0。

### 3 装系统 CA + 开代理
- `adb -s <端口> push mitmproxy-ca-cert.pem /data/local/tmp/mitm-ca.pem`
- 测只读：`adb -s <端口> shell "su -c 'touch /system/etc/security/cacerts/t 2>&1'"`
  → 只读则：mkdir /data/local/cacerts + cp 为 `<hash>.0` + `mount -o bind ... /system/etc/security/cacerts`
  → 可写则直接拷入。
- 开代理：`settings put global http_proxy 10.0.2.2:8080`。

### 4 宿主机跑 mitmproxy（用仓库 addon）
- `mitmdump --listen-port 8080 -s <仓库>\tools\analysis\toytycoon\mitm_addon.py`（后台）
- 问用户：8080 是否可用（被占则换 8081 并同步代理）。

### 5 玩 + 分析
- 用户玩任意模块 → mitm_b64.jsonl 记录 host/path/method + base64 req/resp。
- full_decode.py / extract_save.py 解出字段号=值。

### 6 无 root 时的选择（问用户）
- 开 root（bluestacks.conf 设 enable_root_access=1，字节级无 BOM，备份后改，重启）。
- 或 APK 重打包加证书信任。问用户选哪条。

## 硬性注意（坑）
- 不要 adb reboot（卡死 adbd）；用 BlueStacks 多开管理器重启实例。
- 实例重启后重做第 3 步（bind-mount + 代理会丢）。
- 玩完清代理 `settings put global http_proxy :0`，否则游戏"网络中断"。
- raw/账号/数值留本地，不提交 Git；Git 只放 schema/脚本/文档。

## 成功判据
用户玩后，mitm_b64.jsonl 出现 uploadcoin(金币)/login(uid,用户名)/saveuserdata(gzip 存档)
等记录，full_decode.py 解出 字段号=值。
