# Huuuge 单实例云端部署与验收

供 Codex 执行和 User 本人验收使用。范围来源：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)，正式任务：[TASK-0031](https://github.com/840832144/AI-Workspace/blob/codex/huuuge-cloud-single-instance/tasks/TASK-0031-HUUUGE-CLOUD-SINGLE-INSTANCE.md)。2026-09-29 按 [PR #11 v2-GooglePlay / 5ff7190](https://github.com/840832144/AI-Workspace/blob/5ff7190137f1512f52cddacc0f5d17ce5cc4254e/tasks/support/TASK-0031/CLOUD_DEBUG_PLAN_20260929.md)续接。**Google/Play 安装、无探针游戏与图形恢复已取得真实证据；认证无法读取；云端 ADB 实连受审批阻塞，采集/停止保存未执行。**

## 策划怎么用

1. Codex 在既有云手机核查并按官方方式安装/启用 Google Play/GMS，到原生登录页后通知 User 亲自登录。验证商店可用和认证状态，再从 Google Play 安装/更新或确认 Huuuge。
2. User 在厂商网页亲自登录 Huuuge，完成无探针的大厅/机台普通交互。登录、图形、网络有问题时，Codex 先排障，不接探针掩盖基线故障。
3. Codex 启动云端采集，收到 `ready` 后，请 User 进行普通 Slots 操作，按开始/结束反馈记录观察窗口，确认本轮成功解码业务响应。User 告知结束后正常停止，核对退出、`finalized`、计数及保存结果。`stop-requested` 只是停止请求，`ready` 也不是最终验收通过。

策划操作只需浏览器。Workbench 和阿里云 CLI 是 Codex 使用的管理工具；生产采集、解码及必需的数据转发必须在云端持续运行。除管理工具配置与核验外，采集命令全部由 Codex 在**云端 Linux 执行端**运行。

## 当前手机管理通道（2026-09-29）

官方 eds-aic API 已完成真实手机检查、启用内置 Google 组件和启动商店。User 授权本轮使用已配置的 OAuth Account 身份；上海管理接入点通过精确目标 + 香港业务地域验证，EdsAgent 工作正常。Workbench 仍独立面向 Linux，未用于云手机 ID。实际命令、单次提交/回读及来源见 [管理说明](GOOGLE_READONLY.md)。

网页桌面此前已核验；控制台命令输出未知、工具超时后浏览器自动化保持停止。先查已有任务仅见创建记录，旧命令仍 unknown；新的 API 检查使用独立标记，没有重放未知点击。手机准备不依赖先就绪 Linux 或 Workbench。

## Google 环境实际方法与下一步

1. 已实测 Android 12 / SDK 31 / arm64-v8a / 镜像 26.09.1；三个核心 Google 包存在但禁用，手机到两个官方 Google 域名 HTTPS HEAD 均 302 / exit 0。
2. 复用镜像内置包，使用 Android 官方 `pm enable --user 0` 依次启用 GSF、GMS、Play；均 exit 0，回读 enabled=yes、disabled=no。未下载/侧载 APK、清数据、改 SELinux 或绕过认证。官方支持依据与原命令见上述说明。
3. `am start -W` 成功打开 Play 未登录入口；User 确认“现在有了”并随后确认“Google 已登录”。账号登录由 User 本人完成，期间未读取手机界面、密码、验证码或 Cookie。
4. 商店首页、搜索、详情及 Play Protect 认证分别核验。认证位置按[Google 官方说明](https://support.google.com/googleplay/answer/7165974?hl=zh-Hans)为个人资料 → 设置 → 关于；仅记录认证状态，不记录账号。可启动和登录反馈不能代替下载可用证据。
5. 已在线核对 [Huuuge 官方详情](https://play.google.com/store/apps/details?id=com.huuuge.casino.slots)：包名 `com.huuuge.casino.slots`，开发者 Huuuge Games - Play Together。首次包查询未安装，打开详情后 User 安装并反馈“打开”；随后只读回查 installer=com.android.vending、versionName=12.09.27229、versionCode=1789041595、primaryCpuAbi=arm64-v8a，确认本次 Play 下载。认证记录“无法读取/未确认”（User 暂未找到该项），不记为已认证；首页/搜索未单独验证。不得静默改为第三方 APK。
6. User 已完成无探针 Huuuge 游戏并确认图形修复；已有 Linux 已独立核实，实际结果见 [ACCEPTANCE.md](ACCEPTANCE.md)。先解决下方受控连接与审批阻塞，再准备 Frida/采集。

## Workbench 管理通道（2026-09-29 已安装，未认证/连接）

- 使用[官方文档](https://help.aliyun.com/zh/ecs/user-guide/connect-to-an-instance-through-workbench-cli/)指定发布源的 `latest/workbench-windows-amd64.zip` 与 `checksums.sha256`，校验匹配后解压，仅安装 `workbench.exe` 到 `%LOCALAPPDATA%\Programs\workbench`，加入用户 PATH。官方脚本注释与实际目录不一致，本次未执行其 Program Files 安装分支。没有安装采集组件。
- 实测 `workbench version`：v1.0.1 / commit 86c0aff / built 2026-08-24T07:12:39Z；根帮助、`exec --help`、`config --help`、`list --help` 均读取成功。新终端未继承 PATH 时直接使用该用户目录下的绝对入口，不重复安装。
- 默认 `%USERPROFILE%\.workbench\config.json` 当前不存在；本轮已通过同一获准 OAuth profile 的 ECS Cloud Assistant 管理既有 Linux，无需为此另配 Workbench 凭据。若后续确需 Workbench，先说明具体用途，不输出完整配置或复制凭据。
- Workbench CLI 面向 Linux ECS；云手机 Android 终端不是独立 Linux 采集主机的证明。首次连接可能添加内网 TCP 22 安全组规则，连接前核对既有规则与 User 授权；不新增公网调试端口。
- `exec` 默认超时 30 秒，每次独立 shell；不能用本机持续运行的 CLI/转发维持采集。云端复用稳定会话。upload/download 经 OSS 中转，只用于获准代码或纯结构文件，真实 Raw/账号/密钥不经此路径搬出。

## 本轮图形修复（已执行）

现象：User 能玩，但截图有层错位/文字缺失；当时未接 Frida。只读实况：CPU rendering、GLES SwiftShader、内置 com.android.angle；720×1280 / density240，下面两项设置均 null。

依据[阿里云镜像说明](https://help.aliyun.com/zh/ecp/release-note-of-cloud-phone-system-image)的应用 ANGLE 支持和 [Google ANGLE 官方文档](https://github.com/google/angle/blob/main/doc/DevSetupAndroid.md)，经 EdsAgent 仅为目标应用执行：

```sh
settings put global angle_gl_driver_selection_pkgs com.huuuge.casino.slots
settings put global angle_gl_driver_selection_values angle
am force-stop --user 0 com.huuuge.casino.slots
am start -W --user 0 -n com.huuuge.casino.slots/com.huuuge.casino.BootActivity
```

设置回读准确；限定 Huuuge 进程的日志出现 `ANGLE package enabled: com.android.angle` 和 ANGLE2.1.2 / Vulkan SwiftShader。User 复查后明确“现在好了”。没有设置 all-app ANGLE、改分辨率/密度、清数据、重建或侧载。此前通用 launcher intent 虽 shell exit0，但输出 `unable to resolve Intent`，不记为成功；之后查 launcher 才使用上述真实 Activity。

回滚：仅当当前两项仍精确等于本次包名/angle 时，`settings delete global angle_gl_driver_selection_pkgs` 和 `settings delete global angle_gl_driver_selection_values`，再按上述方式重启 Huuuge；若值已变化先保留并调查，不能删别人的配置。本次前值均 null，未实施回滚，工作状态保留。

## 已有 Linux 与当前连接阻塞（2026-09-29）

- 官方 ECS DescribeInstances 定位香港已有实例，再用 Cloud Assistant 状态与 ECS RunCommand → DescribeInvocationResults 交叉核验目标。Alibaba Cloud Linux3 / x86_64 / 2CPU、约7.4GiB内存、约31GiB根盘可用；Python3.6.8。PATH 未找到 adb/git，任务目录不存在。系统 Python 不适合直接承接当前采集依赖，后续独立运行时准备不能修改系统 Python。
- nginx 在运行，保持原服务/SSH配置不动；不存在某一晨会常见路径不等于主机没有其他服务。没有新增 ECS/NAT/EIP，现有授权与资源可复用。
- Linux→云手机私网5555单次 TCP 超时；手机 ADB 在监听，现有 keypair 绑定存在，Linux 默认与本任务路径未发现私钥。同 VPC 尚未证实；不自行绑定/替换 key。手机 PATH 未找到 ssh/ssh-keygen，反向 SSH 尚非可用路线。
- User 后续在控制台创建公网映射并给出 connect 命令。官方 API 返回唯一手机匹配，外部10001→内部5555；从该 Linux 的单次 TCP connect 成功。真实地址只在受控配置，不写进 Git。Codex 未新增映射或改安全组。
- 拟在该 Linux 的 `/srv/huuuge-private/adb-check` 隔离目录使用 [Google 官方 Platform-Tools](https://developer.android.com/tools/releases/platform-tools)，仅监听 loopback 专用ADB server port15037；单次 connect/get-state，若认证成功只读 Android 版本，随后停止自有 server。执行前被自动审批拒绝，仅报 `blocked by policy`；**云端命令未提交，目录/工具/密钥均未因此创建，ADB 实连仍未验证**。
- 原 controller 只接受私网/loopback，保持 gate。不得用 loopback 代理掩盖公网实际路径，也不把 TCP 成功当作 ADB 认证。新公网入口的持续采集使用不是自动放开的合同；原 PR #11 第6步要求网络/密钥/隧道变更先明确目标与影响并获 User 授权。

下一步仅需 User 明确确认：允许本轮在已核验的云端 Linux 安装官方 ADB，并使用刚建立的现有公网映射做一次连接验证（不新增端口、不改安全组）。原方案约定不开放公网调试端口，且 controller 只支持私网/loopback；本次确认须明确覆盖云端 ADB 安装和 User 已有公网入口，不是重复 OAuth 授权。审批拒绝未说明具体原因，User 确认不保证工具审批通过。得到确认后按审批支持继续；若仍拒绝则停止，不换工具或改写命令绕过。持续采集的网络契约、专用用户/密钥、版本/ABI/descriptor/Frida 准备仍须在连接通过后落实。

## 云端准备

仅使用 User 已有的一台云手机，规格、镜像、地域以现场为准，不购买新资源。Linux 执行端单独核验后，使用独立普通用户、目录和虚拟环境；不改晨会服务、系统 Python、共享 ADB、开机服务或全局防火墙。User 本人负责权限确认，Codex 执行已授权准备，不等待其他技术对接人。

需要通过受控渠道提供：厂商网页入口、实例权限、私网连接、ADB 密钥、当前 Huuuge 版本/ABI、经核验的运行时结构文件和结果路径。真实 endpoint、密钥、原始日志不进入 Git/Issue/聊天。配置模板中的地址和版本均是假定占位，不能直接用于真实采集。

### 1. 准备代码和运行时

在云端取得经 Review 的本仓库 revision。建立专用虚拟环境，安装本目录的最小依赖；现有普通业务采集器仍是 `artifacts/live_probe/live_decode.py`，探针仍是 `agent.js`。

```bash
python3 -m venv /srv/huuuge-private/venv
/srv/huuuge-private/venv/bin/python -m pip install -r deploy/cloud/requirements.txt
```

`huuuge_descriptors.pb` 和 recovered `.proto` **没有随 Git 提交**。Codex 从已有受控运行时取得纯结构 descriptor，放到独立云端运行目录；核对来源版本与 SHA-256，不能搬迁历史 Capture 或登录态。若已有完整 recovered protos，可复用 `scripts/build_descriptors.py`，其构建依赖另在独立环境准备。缺 descriptor 时 `probe/run` 必须阻断。

本机已安装依赖可支持静态/合成测试，不作为云端部署。生产依赖和 Frida server 版本必须一致；这里固定 Frida 17.17.0 是已有采集器的准备基线，尚未证明云手机兼容。

### 2. 连接唯一云手机并核对身份

Codex 在独立用户下准备云端 ADB；私钥放云端受控用户目录，密钥绑定与权限由 User 确认。使用独立 server port，例如 `15037`，连接唯一已授权私网 serial。不要运行默认端口的 `adb kill-server`。

```bash
ADB=/srv/huuuge-tools/platform-tools/adb
"$ADB" -H 127.0.0.1 -P 15037 start-server
# DEVICE 由 Codex 在受控 shell 中设置为目标私网 IPv4:port。
"$ADB" -H 127.0.0.1 -P 15037 connect "$DEVICE"
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell id -u
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell getprop ro.product.cpu.abi
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell dumpsys package com.huuuge.casino.slots
```

成功表现：目标 transport 为 `device`，Root UID 为 `0`，设备和 Huuuge 主 ABI 均为 `arm64-v8a`，读取实际 versionName/versionCode。`probe` 会与配置再次对照，拒绝漂移。不照搬蓝叠地址、Houdini 路径或旧游戏版本。Root/图形/网络不兼容时保留错误，由 Codex 定位，必要权限由 User 确认，不自行提权或扩容。

官方说明：实例版 ADB/远程命令的 Root 行为见[权限说明](https://help.aliyun.com/zh/ecp/faq-how-to-get-root-permission)，具体网络接入见[ADB 连接](https://help.aliyun.com/zh/ecp/how-to-connect-cloud-phone-via-adb)。本文仅采用受控私网路线，**不执行官方文档中的公网 DNAT/开放端口分支**。网页使用可查[终端用户连接说明](https://www.alibabacloud.com/help/en/ecp/how-to-use-cloud-phones-as-an-end-user)。核对日期：2026-09-15；官方产品说明不是 Huuuge 兼容验收。

### 3. 准备设备端 Frida 和云端配置

Codex 提供官方来源、匹配版本的 Android ARM64 Frida server，核验来源和哈希后，仅放入本实例专用目录（例如 `/data/local/tmp/huuuge-cloud/`）。运行前核对路径、占用端口、版本与权限，保存本次专用 PID。监听地址使用设备回环 `127.0.0.1:27042`；日志仅留云实例受控目录。此步骤不需要克隆、改 APK 或复用蓝叠 Gadget。

```bash
# 下列启动由 Codex 在云实例的受控 Root shell 中执行；文件预先校验并赋予执行权限。
nohup /data/local/tmp/huuuge-cloud/frida-server -l 127.0.0.1:27042 \
  > /data/local/tmp/huuuge-cloud/frida.log 2>&1 &
echo $! > /data/local/tmp/huuuge-cloud/frida.pid
```

回到云端 Linux 执行端，为该设备建立专用转发；`--no-rebind` 防止覆盖已有端口：

```bash
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" forward --no-rebind tcp:27043 tcp:27042
```

复制 `cloud.example.json` 到源码目录外的受控配置目录（权限 `0600`），结果根目录归专用用户所有、权限 `0700`。填入已核对的云端绝对路径、实际版本和私网 serial；资源授权真实就绪后才设 `resource_authorized=true`。配置不能证明主机位于云端，主机归属由 Codex 与 User 现场核对；程序拒绝 Windows/macOS runtime，且不会自动回退本机设备。

```bash
PY=/srv/huuuge-private/venv/bin/python
CFG=/srv/huuuge-private/cloud.json
"$PY" scripts/cloud_capture.py --config "$CFG" check
"$PY" scripts/cloud_capture.py --config "$CFG" probe
```

`check` 只验证配置格式；`probe` 只读身份、权限、版本和转发归属。均不代表 READY，也不代表游戏可玩。若现有 Codex 已经批准并部署专用 Gadget，可将 `process` 改为 `Gadget`，但须另外核对它确实属于这台 Huuuge；默认采用原生 ARM64 Frida server，禁止复制旧 Houdini bootstrap。

### 4. 启动、普通操作和结束

先由 User 在厂商网页上确认游戏已登录可玩。Codex 在稳定的云端终端中以前台方式运行 `run`；需要保留终端时复用 Codex 已有会话工具，不新建系统服务。另开一个云端执行终端记录观察和停止。

```bash
"$PY" scripts/cloud_capture.py --config "$CFG" run
# 以下命令在第二个云端执行终端运行。
"$PY" scripts/cloud_capture.py --config "$CFG" status
# 收到 ready，User 确认已在网页中登录且即将进行普通 Slots 操作后：
"$PY" scripts/cloud_capture.py --config "$CFG" play-start
# User 手动操作；待对应响应到达、User 确认操作结束后：
"$PY" scripts/cloud_capture.py --config "$CFG" play-end
"$PY" scripts/cloud_capture.py --config "$CFG" stop
"$PY" scripts/cloud_capture.py --config "$CFG" status
```

`run` 复用现有探针和解码器，目录每次唯一。只有 hook 安装、本轮真实 RPC 和解码文件增长后才发 `ready`。`play-start/end` 是 Codex 根据 User 观察填写的人工证据，只保存本轮序号范围和时间；程序不会点击游戏，也不能替代 User 见证。

正常路径为 `stop-requested → 子进程退出 → index/Raw/JSON/manifest/lifecycle 核对 → finalized`。输出 `cloud-summary.json` 只含计数、起止、状态及操作窗口内的非空 Slots 成功响应数。`ready-for-human-review` 表示代码核验条件齐备，还需 User/ChatGPT 对照真实网页与受控样本做最终 Review。无 Spin 数量配额，不要求所有协议 100% 解码。

### 5. 失败、结果交接和资源收尾

| 现象 | 怎么处理 |
| --- | --- |
| `blocked` / probe 不通过 | 在云端核对配置、依赖、网络、Root、实际版本与转发；不重装本机或开放公网。 |
| READY 超时、Missing symbols 或连接断开 | 正常请求停止，保留当前 Session。按探针符号、游戏版本、连接和解码分别定位，不把旧样本作为成功。 |
| `stop-requested` 后不退出 | 保留日志与 active 状态；Codex 核对该专用进程身份后处理，不 `pkill python`，不结束晨会或共享 ADB。 |
| `incomplete` / `failed` | 保留 Raw 与失败计数；不能写成 finalized。 |
| supervisor 意外退出 | 子进程继承单实例锁；不要启动第二次。先对 active Session 请求 stop，确认退出后运行 `finalize`；退出码缺失仍保持 incomplete，不能补填成功。 |

失败状态不会自动移除 active 入口，防止盲重试。Codex 确认锁已释放、所有本轮进程已退出并完成诊断后，才可把 `active.json` 归档到原 Session；原目录及失败证据保留，再决定是否新试一次。

结果位于配置的私有 `result_root`。Codex 通过受控文件访问提供本轮目录；Git/Issue 仅贴经人工核对的 `cloud-summary.json` 字段，不上传完整日志、Raw、逐条 JSON、逐笔余额或标识。必须在进程退出后再次读取结果，核对实际捕获/成功/失败数以及本轮人工操作对应样本。

结束后，Codex 仅移除本次专用 ADB forward，并根据已验证的专用 PID/可执行路径停止本次 Frida server；采集器不自动删除结果、不关闭共享服务。云手机/执行端是否保留由 User 决定。**采集停止不等于云资源停止计费**；Codex 在控制台查看实例、磁盘、网络的计费项并按 User 决定停用或释放，释放实例或删除结果前须确认。本轮未创建或购买云资源。

## 本轮验收记录

详见 [ACCEPTANCE.md](ACCEPTANCE.md)。仍继续 TASK-0031 与原 PR #2，不新建同目标任务或 PR。当前为 v2 执行修订及实况交接，不代表 Google/云端验收通过；不发布本地安装包或同步历史 SVN 策划安装包。
