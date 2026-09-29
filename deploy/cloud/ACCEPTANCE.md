# TASK-0031 验收记录

- 日期：2026-09-29；执行：Codex；Subagents: none。
- 范围：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)，PR #11 v2-GooglePlay / `5ff7190`；原 Task/PR 不变。
- 当前状态：In Progress；Google/Play 安装及无探针游戏已取得真实证据；云端一次 ADB 验证返回 unauthorized，已断开并停止专用 server；真实采集与停止保存未执行。

## 2026-09-29 按步骤记录

| 步骤 | 实际结果 | 边界 |
| --- | --- | --- |
| 原任务同步 | 两仓 main 合入原分支；Registry 19 canonical / 0 collision / valid | reservation pending-main，未 Complete |
| 管理身份/工具 | User OAuth 配置完成，Account 身份获 User 明确授权；复用 CLI3.5.1/Workbench1.0.1 | 不改 IAM；Workbench 未连接手机/Linux |
| 浏览器与旧命令 | 官方URL、连接窗口和Android桌面曾核验 | 后续工具超时，旧控制台命令 unknown；不重放 |
| 手机 API | eds-aic 上海管理接入点 + 香港业务地域；EdsAgent 子任务 Finished，目标/标记完整 | API 管理成功不代表 ADB/采集成功 |
| Android/Google | Android12/SDK31/ARM64/26.09.1；Google三包原禁用→标准pm enable启用并回读；两官方域名HEAD302/exit0 | 无侧载、清数据、重建或认证绕过 |
| Google 登录 | Play启动后User确认显示并本人登录 | 不读密码/验证码/Cookie/账号页 |
| Huuuge Play 新安装 | 原未安装→User安装后“打开”→installer=com.android.vending、12.09.27229/1789041595、arm64-v8a | 详情/下载安装可用，首页/搜索未单独验证 |
| Play Protect | User暂未找到认证项，无法读取/未确认 | 不把“应该”写成已认证，不反复追问 |
| 无探针游戏 | User“能玩，画面有点问题”→应用专属ANGLE设置→真实BootActivity启动/驱动日志→User“现在好了” | 本轮网页可玩和图形恢复有证据；长期稳定性未测 |
| Linux目标 | 已有香港ECS，Cloud Assistant工作正常；Alibaba Cloud Linux3/x86_64/2CPU/约7.4GiB/约31GiB可用/Python3.6.8 | PATH未找到adb/git；nginx运行，未改服务；不再等待User找主机 |
| 原私网链路 | Linux→phone:5555单次TCP超时；手机5555监听；现有keypair已记录 | 同VPC未证实；未替换绑定；手机未发现ssh/ssh-keygen命令 |
| User新建映射 | 官方API精确匹配本次手机，10001→5555；Linux单次TCP连接成功 | Codex未创建映射/改安全组；TCP不是ADB认证 |
| 本轮收窄授权/复审 | User明确一次云端ADB验证边界；正常默认审批已放行，未关闭审批或换工具 | 前次blocked by policy保留为历史 |
| Platform-Tools安装 | 官方Linux包安装在全新任务目录；ADB1.0.41 / 37.0.1-15733141 | 不改PATH/共享工具；任务key仅在独立目录 |
| ADB实连 | 首次监听参数错误发生在connect前；改localhost并实核仅回环后，connect调用一次：failed to authenticate；get-state exit1/device unauthorized | connect exit0不代表成功；未替换手机绑定、未代授权 |
| ADB结束/回读 | disconnect0、专用server停止0并退出；独立只读回读result-connect.json、进程不存在/专用监听0 | 只证明本次连接诊断收尾，不是采集Session保存验收 |
| 真实采集与停止 | 未启动，无云端Session | 新增解码、退出/flush、保存结果/计数unknown |

## 本轮 ADB 验证授权与保存

User 新授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。

正常工具默认审批本次已放行，经 ECS Cloud Assistant 在任务独立目录安装官方 Platform-Tools；实读 ADB1.0.41 / 37.0.1-15733141。首次 server 因监听参数写法报错退出、未执行 connect；改为官方 localhost 语法后实核仅回环监听。connect 实际调用一次，输出 failed to authenticate；get-state exit1 / device unauthorized。connect 自身 exit0 不能记为成功。

已对唯一目标 disconnect(exit0)，仅停止自己启动的专用 server(exit0)，进程正常退出。另起只读任务回读云端 result-connect.json：connect_attempts=1、记录的进程不存在、专用监听数0；任务目录0700、任务新生 ADB key0600、默认 root key仍不存在。官方手机 API 回读原 keypair 绑定未变、手机RUNNING；nginx/sshd保持active。未读取/输出密钥内容。

## 真实三项验收

| 验收项 | 本轮实际结果 | 尚缺证据 |
| --- | --- | --- |
| 网页登录并正常玩 | User Google登录及Play安装有确认；User实际游戏可玩，ANGLE后图形恢复；无探针基线通过本轮手动反馈 | 未独立观察游戏账号登录过程；长期稳定性未测 |
| 本轮新增采集且成功解码 | 未执行；捕获/成功/失败数unknown | 获准连接、当前build/ABI/descriptor/Frida、真实普通操作对应的新增业务响应 |
| 正常结束并保存 | 未执行；没有Session，最终状态unknown | stop/flush、进程退出、结果回读与计数核对 |

## 管理证据与失败记录

- 实际方法和ANGLE回滚见 [README.md](README.md)，Google/API方法见 [GOOGLE_READONLY.md](GOOGLE_READONLY.md)。原始目标/任务ID、响应、地址和凭据留受控本机，Git只记录脱敏事实。
- Huuuge安装回查、图形只读首次曾在DNS解析阶段失败；在确认未建立连接并查询任务/解析恢复后各只重试一次只读请求。未知变更不重放。
- 通用launcher命令shell exit0但输出无法解析Intent，不记成功；读取真实launcher后显式BootActivity启动Status=ok。ANGLE设置已回读，限定游戏进程日志确认2.1.2/Vulkan SwiftShader；User复查后确认恢复。
- 手机/Linux命令均按唯一目标/子任务或InvokeId回读；Linux结果Success/ExitCode0、完整首尾标记。TCP检查成功是网络层证据，无法证明ADB认证。前次被拒脚本未提交；本轮User新授权后正常默认审批放行，未换工具或关闭审批。实际connect/get-state返回unauthorized，不能记为通过。
- 原controller/decoder的私网gate和停止/保存机制保持；采集代码未改，未接Frida。此次仅一次ADB验证，未读取游戏数据，历史合成CI不是本轮新增数据。
- 无本机持续采集、付费资源创建或晨会服务修改；User自行建立的新公网映射单独记录，不再笼统说“没有公网端口”。

## 历史准备检查（2026-09-15）

- Python 语法检查通过。使用现有 Windows Python 3.12.9 和已安装依赖进行合成测试，没有安装采集组件或启动 ADB/Frida/游戏。
- 本机最终检查：14 项，11 通过、3 项 Linux 专属检查跳过。
- Linux CI 已通过全部 14 项（Python 3.12.14 / protobuf 7.36.1），包括真实子进程锁、SIGTERM 和 supervisor 的 probe → run → 人工窗口 → stop → 退出后文件回读。最终代码证据：[run 34957001266](https://github.com/840832144/huuuge-android-research/actions/runs/34957001266)，代码 commit `9bb241b`；还覆盖最终文件被移除后 finalize 必须返回 incomplete/非零，不能依赖缓存。
- 测试通过伪造的 Frida 接口传送**测试生成的 protobuf 字节**，执行真实 `live_decode.py` 子进程、解码、文件保存和结束路径。合成 3 条、成功 2 条、失败 1 条仅用于证明程序行为，**不是真实 Huuuge 新增数据**。
- 覆盖旧 Session 不覆盖、路径穿越阻断、wrapper 失败 Raw 保留、断连失败、hook 失败、启动异常、缺失文件、未知退出码、人工窗口与脱敏摘要。
- Windows 未配置可用 WSL，本轮不安装 Linux 或云端模拟环境。Linux 锁、SIGTERM、完整 supervisor 路径使用 GitHub CI 合成检查；仍不替代云手机验收。

## Review 与下一步

原业务 PR #2 / 治理 PR #4 交本轮真实进度增量 Review；Task保持In Progress，不标Complete/Accepted。

**本轮授权与结果**：User 新授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。

本轮获准的一次 ADB 验证已结束，当前阻塞是设备鉴权，不再是审批。下一步由 User 本人完成设备授权或在受控环境配置与现有绑定匹配的密钥；不在聊天/Git提供密钥，不替换手机现有绑定，不再自动连接。后续如需再验证须重新明确范围；原真实采集/解码/正常停止保存目标保留，本轮不实施。
