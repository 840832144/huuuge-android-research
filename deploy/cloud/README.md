# Huuuge 单实例云端部署与验收

供技术配置和策划验收使用。范围来源：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)，正式任务：[TASK-0031](https://github.com/840832144/AI-Workspace/blob/codex/huuuge-cloud-single-instance/tasks/TASK-0031-HUUUGE-CLOUD-SINGLE-INSTANCE.md)。**当前仅完成代码准备；资源未就绪，真实云端三项验收均未执行。**

## 策划怎么用

1. 技术通过公司受控渠道提供厂商现成 Web 入口与实例分配。策划在浏览器中亲自登录云手机上的 Huuuge，确认能进入游戏并正常交互。遇到登录、图形或网络错误，先反馈技术处理。
2. 技术启动云端采集，收到 `ready` 后，请策划进行一次普通 Slots 操作。技术按策划的开始/结束反馈记录观察窗口，确认本轮出现成功解码的业务响应。`ready` 只说明探针和新增数据链已工作，不等于三项验收通过。
3. 策划告知操作结束，技术停止并核对 `finalized`、计数和结果可读性，再提供脱敏摘要。`stop-requested` 仅表示已请求停止，不表示已保存。

策划电脑仅需浏览器。下面的命令全部由技术在**云端 Linux 执行端**运行。

## 技术准备

首选候选为 User 已批准的一台无影云手机实例版、4核8GiB；实际地域、可售规格、网络、费用和权限由 User/技术确认。优先用已有 Linux 云服的独立普通用户、独立目录和虚拟环境；不改晨会服务、系统 Python、共享 ADB、开机服务或全局防火墙。资源未就绪时停在准备阶段。

需要通过受控渠道提供：厂商网页入口、实例权限、私网连接、ADB 密钥、当前 Huuuge 版本/ABI、经核验的运行时结构文件和结果路径。真实 endpoint、密钥、原始日志不进入 Git/Issue/聊天。配置模板中的地址和版本均是假定占位，不能直接用于真实采集。

### 1. 准备代码和运行时

在云端取得经 Review 的本仓库 revision。建立专用虚拟环境，安装本目录的最小依赖；现有普通业务采集器仍是 `artifacts/live_probe/live_decode.py`，探针仍是 `agent.js`。

```bash
python3 -m venv /srv/huuuge-private/venv
/srv/huuuge-private/venv/bin/python -m pip install -r deploy/cloud/requirements.txt
```

`huuuge_descriptors.pb` 和 recovered `.proto` **没有随 Git 提交**。技术从已有受控运行时取得纯结构 descriptor，放到独立云端运行目录；核对来源版本与 SHA-256，不能搬迁历史 Capture 或登录态。若已有完整 recovered protos，可复用 `scripts/build_descriptors.py`，其构建依赖另在独立环境准备。缺 descriptor 时 `probe/run` 必须阻断。

本机已安装依赖可支持静态/合成测试，不作为云端部署。生产依赖和 Frida server 版本必须一致；这里固定 Frida 17.17.0 是已有采集器的准备基线，尚未证明云手机兼容。

### 2. 连接唯一云手机并核对身份

技术在独立用户下准备云端 ADB；私钥放云端受控用户目录，密钥绑定与权限由管理员办理。使用独立 server port，例如 `15037`，连接唯一已授权私网 serial。不要运行默认端口的 `adb kill-server`。

```bash
ADB=/srv/huuuge-tools/platform-tools/adb
"$ADB" -H 127.0.0.1 -P 15037 start-server
# DEVICE 由技术在受控 shell 中设置为目标私网 IPv4:port。
"$ADB" -H 127.0.0.1 -P 15037 connect "$DEVICE"
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell id -u
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell getprop ro.product.cpu.abi
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" shell dumpsys package com.huuuge.casino.slots
```

成功表现：目标 transport 为 `device`，Root UID 为 `0`，设备和 Huuuge 主 ABI 均为 `arm64-v8a`，读取实际 versionName/versionCode。`probe` 会与配置再次对照，拒绝漂移。不照搬蓝叠地址、Houdini 路径或旧游戏版本。Root/图形/网络不兼容时保留错误，交技术确认，不自行提权或扩容。

官方说明：实例版 ADB/远程命令的 Root 行为见[权限说明](https://help.aliyun.com/zh/ecp/faq-how-to-get-root-permission)，具体网络接入见[ADB 连接](https://help.aliyun.com/zh/ecp/how-to-connect-cloud-phone-via-adb)。本文仅采用受控私网路线，**不执行官方文档中的公网 DNAT/开放端口分支**。网页使用可查[终端用户连接说明](https://www.alibabacloud.com/help/en/ecp/how-to-use-cloud-phones-as-an-end-user)。核对日期：2026-09-15；官方产品说明不是 Huuuge 兼容验收。

### 3. 准备设备端 Frida 和云端配置

技术提供官方来源、匹配版本的 Android ARM64 Frida server，核验来源和哈希后，仅放入本实例专用目录（例如 `/data/local/tmp/huuuge-cloud/`）。运行前核对路径、占用端口、版本与权限，保存本次专用 PID。监听地址使用设备回环 `127.0.0.1:27042`；日志仅留云实例受控目录。此步骤不需要克隆、改 APK 或复用蓝叠 Gadget。

```bash
# 下列启动由技术在云实例的受控 Root shell 中执行；文件预先校验并赋予执行权限。
nohup /data/local/tmp/huuuge-cloud/frida-server -l 127.0.0.1:27042 \
  > /data/local/tmp/huuuge-cloud/frida.log 2>&1 &
echo $! > /data/local/tmp/huuuge-cloud/frida.pid
```

回到云端 Linux 执行端，为该设备建立专用转发；`--no-rebind` 防止覆盖已有端口：

```bash
"$ADB" -H 127.0.0.1 -P 15037 -s "$DEVICE" forward --no-rebind tcp:27043 tcp:27042
```

复制 `cloud.example.json` 到源码目录外的受控配置目录（权限 `0600`），结果根目录归专用用户所有、权限 `0700`。填入已核对的云端绝对路径、实际版本和私网 serial；资源授权真实就绪后才设 `resource_authorized=true`。配置不能证明主机位于云端，主机归属由技术与 User 现场核对；程序拒绝 Windows/macOS runtime，且不会自动回退本机设备。

```bash
PY=/srv/huuuge-private/venv/bin/python
CFG=/srv/huuuge-private/cloud.json
"$PY" scripts/cloud_capture.py --config "$CFG" check
"$PY" scripts/cloud_capture.py --config "$CFG" probe
```

`check` 只验证配置格式；`probe` 只读身份、权限、版本和转发归属。均不代表 READY，也不代表游戏可玩。若现有技术已经批准并部署专用 Gadget，可将 `process` 改为 `Gadget`，但须另外核对它确实属于这台 Huuuge；默认采用原生 ARM64 Frida server，禁止复制旧 Houdini bootstrap。

### 4. 启动、普通操作和结束

先由 User 在厂商网页上确认游戏已登录可玩。技术在稳定的云端终端中以前台方式运行 `run`；需要保留终端时复用技术已有会话工具，不新建系统服务。另开一个云端技术终端记录观察和停止。

```bash
"$PY" scripts/cloud_capture.py --config "$CFG" run
# 以下命令在第二个云端技术终端运行。
"$PY" scripts/cloud_capture.py --config "$CFG" status
# 收到 ready，User 确认已在网页中登录且即将进行普通 Slots 操作后：
"$PY" scripts/cloud_capture.py --config "$CFG" play-start
# User 手动操作；待对应响应到达、User 确认操作结束后：
"$PY" scripts/cloud_capture.py --config "$CFG" play-end
"$PY" scripts/cloud_capture.py --config "$CFG" stop
"$PY" scripts/cloud_capture.py --config "$CFG" status
```

`run` 复用现有探针和解码器，目录每次唯一。只有 hook 安装、本轮真实 RPC 和解码文件增长后才发 `ready`。`play-start/end` 是技术根据 User 观察填写的人工证据，只保存本轮序号范围和时间；程序不会点击游戏，也不能替代 User 见证。

正常路径为 `stop-requested → 子进程退出 → index/Raw/JSON/manifest/lifecycle 核对 → finalized`。输出 `cloud-summary.json` 只含计数、起止、状态及操作窗口内的非空 Slots 成功响应数。`ready-for-human-review` 表示代码核验条件齐备，还需 User/ChatGPT 对照真实网页与受控样本做最终 Review。无 Spin 数量配额，不要求所有协议 100% 解码。

### 5. 失败、结果交接和资源收尾

| 现象 | 怎么处理 |
| --- | --- |
| `blocked` / probe 不通过 | 在云端核对配置、依赖、网络、Root、实际版本与转发；不重装本机或开放公网。 |
| READY 超时、Missing symbols 或连接断开 | 正常请求停止，保留当前 Session。按探针符号、游戏版本、连接和解码分别定位，不把旧样本作为成功。 |
| `stop-requested` 后不退出 | 保留日志与 active 状态；技术核对该专用进程身份后处理，不 `pkill python`，不结束晨会或共享 ADB。 |
| `incomplete` / `failed` | 保留 Raw 与失败计数；不能写成 finalized。 |
| supervisor 意外退出 | 子进程继承单实例锁；不要启动第二次。先对 active Session 请求 stop，确认退出后运行 `finalize`；退出码缺失仍保持 incomplete，不能补填成功。 |

失败状态不会自动移除 active 入口，防止盲重试。技术确认锁已释放、所有本轮进程已退出并完成诊断后，才可把 `active.json` 归档到原 Session；原目录及失败证据保留，再决定是否新试一次。

结果位于配置的私有 `result_root`。技术通过受控文件访问提供本轮目录；Git/Issue 仅贴经人工核对的 `cloud-summary.json` 字段，不上传完整日志、Raw、逐条 JSON、逐笔余额或标识。必须在进程退出后再次读取结果，核对实际捕获/成功/失败数以及本轮人工操作对应样本。

结束后，技术仅移除本次专用 ADB forward，并根据已验证的专用 PID/可执行路径停止本次 Frida server；采集器不自动删除结果、不关闭共享服务。云手机/执行端是否保留由 User 决定。**采集停止不等于云资源停止计费**；技术在控制台查看实例、磁盘、网络的计费项并按 User 决定停用或释放，释放实例或删除结果前须确认。本轮未创建或购买云资源。

## 本轮验收记录

详见 [ACCEPTANCE.md](ACCEPTANCE.md)。资源就绪后仍继续 TASK-0031，不新建同目标任务。当前提交是云端准备 Review，不发布本地安装包，不同步历史 SVN 策划安装包；这是 Issue v3 的明确范围。
