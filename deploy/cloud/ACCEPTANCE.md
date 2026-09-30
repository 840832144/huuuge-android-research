# TASK-0031 验收记录

## 2026-09-30 正式评审收口

TASK-0031 Round 1 **Accepted**，阻塞修改无；[正式评审](https://github.com/840832144/AI-Workspace/pull/4#pullrequestreview-5361181770)已落库。312/312/0、8条Slots响应及原结果快照保持不变，不重新采集。原PR待User决定合并，reservation pending-main；canonical进入main后才finalize并收口Complete。新自助V1另行登记后继Task，本试点不增加新功能。Subagents: none。

## 2026-09-30 — 一轮真实云端验收结果（Review）

User 新授权接续原治理 [ADB阶段评审](https://github.com/840832144/AI-Workspace/pull/4#issuecomment-5902430771)：本轮允许本台 Huuuge 的 Frida/一个新批次及正常收尾，复用既有主机、手机、ADB和匹配密钥。新增费用、网络/IAM变更、重启/清数据仍须另行确认；本轮均未执行。Subagents: none。

| 验收项 | 本轮真实证据 | 结论 |
| --- | --- | --- |
| 网页正常玩 | 原Google Play来源/无探针ANGLE修复已确认；本轮User亲自打开大厅，READY后普通Slots，回复“操作完成，游戏正常” | 通过本轮操作；长期稳定性未测 |
| 通道保护 | Frida TLS1.3 / TLS_AES_256_GCM_SHA384；固定手机证书；错误证书与令牌拒绝，正确令牌通过；两端仅回环 | Frida业务数据受保护，传统公网ADB本身仍未加密 |
| 新增采集/解码 | 312捕获 / 312成功 / 0失败；手动窗口8条SlotsGameServer.Spin响应；抽读seq130/141，解码业务字段非空 | 真实新增通过；不是合成或旧Session |
| 正常停止保存 | 10:59:50.285—11:03:22.133（UTC+8）；play-end、stop、子进程exit0；finalized，ready-for-human-review | 已停止、flush并保存 |
| 停止后的独立回读 | 原controller重新扫描manifest/index/messages、Raw/JSON；计数仍312/312/0，active Session不存在 | 已保存结果可回读 |
| 本次进程清理 | 手机Frida退出，Linux采集/专用ADB退出，精确forward移除、专用监听0；手机/Linux临时TLS私钥和令牌已移除 | 完成；原匹配ADB密钥保留 |
| 既有环境 | 手机RUNNING、原绑定/映射与4条SG入站规则不变；nginx/sshd active；系统Python3.6.8不变 | 未改网络/IAM/既有服务，未新增资源 |

实际执行源码：`03fb399201d08c878c74322347b652bc8e8a2414`。环境：Python3.11.13独立venv，官方Frida17.17.0 ARM64，protobuf7.36.2/lz4 4.4.5；Android12/ARM64，Huuuge12.09.27229/1789041595。当前APK静态提取40-file descriptor，依赖完整；旧36-file仅30个字节一致，未照搬旧版。

**失败与重试如实保留**：第一次decoder在创建Session/挂接前因内置Google descriptor版本冲突退出。修正当前descriptor优先加载、把同一loader纳入probe，并补启动前失败摘要后，仅对同一已分配ID执行一次受限retry-start；原失败日志/状态保留，未创建第二批次。实际运行前云端Linux **24/24合成检查通过**，这些测试不计入312条。收尾脚本首次因ADB forward输出末尾空行断言失败，未执行删除；只读确认唯一目标后修正空行解析，完成清理并独立复核。

证据索引（受控云端任务目录内，不发布原值）：`transport-verification.json`、`stop-readback.json`、`cleanup-summary.json`、`final-readback.json`、`results/last.json`及其Session的manifest/index/messages/Raw/JSON/manual-play；同ID的`.startup-failure.json`、原`.log`、`.retry-start.log`保留。本机受控任务目录保存官方API的提交/回读、手机清理结果及绑定/映射/SG比较，Git仅保留[脱敏摘要](RESULT_20260930.json)。

部署方法见 [TLS_TRANSPORT.md](TLS_TRANSPORT.md)。Play Protect认证仍为无法读取/未确认，商店首页/搜索及长期稳定性未单独验证。当前执行阻塞为无；正式Review未完成，不自动标Accepted/Complete或合并PR。下文为历史证据，不代表当前状态。

## 2026-09-29 — 历史基线与单次ADB阶段

- 日期：2026-09-29；执行：Codex；Subagents: none。
- 范围：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)，PR #11 v2-GooglePlay / `5ff7190`；原 Task/PR 不变。
- 当前状态：In Progress；Google/Play 安装及无探针游戏已取得真实证据；匹配密钥的云端ADB复验已通过，已断开并停止专用server；真实采集与停止保存未执行。

## 2026-09-29 按步骤记录

| 步骤 | 实际结果 | 边界 |
| --- | --- | --- |
| 原任务同步 | 两仓 main 合入原分支；Registry 19 canonical / 0 collision / valid | reservation pending-main，未 Complete |
| 管理身份/工具 | User OAuth 配置完成，Account 身份获 User 明确授权；复用 CLI3.5.1/Workbench1.0.1 | 不改IAM；Workbench只读精确目标查询通过，未创建SSH会话 |
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
| 后续匹配私钥只读核对 | User指定已有绑定与本机目录；API回读匹配；本机受控程序公钥指纹与手机可信公钥匹配 | 未输出密钥/指纹；密文下发与云端配置通过；单独获准复验返回device |
| 匹配密钥ADB复验 | User单独允许一次复验；connect成功、get-state=device/exit0；disconnect/停止均exit0 | 独立回读结果、PID不存在、监听0；无Frida/采集 |
| 本轮Workbench与密钥配置 | CredentialsCmd复用OAuth，精确Linux查询通过；CMS密文经SendFile下发，云端公钥比较一致，目录0700/文件0600 | Workbench SSH未尝试；原绑定/安全组未变，临时传输材料清理；配置阶段新增connect0 |
| 真实采集与停止 | 未启动，无云端Session | 新增解码、退出/flush、保存结果/计数unknown |

## 2026-09-29 历史ADB验证授权与保存

User 新授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。

正常工具默认审批本次已放行，经 ECS Cloud Assistant 在任务独立目录安装官方 Platform-Tools；实读 ADB1.0.41 / 37.0.1-15733141。首次 server 因监听参数写法报错退出、未执行 connect；改为官方 localhost 语法后实核仅回环监听。connect 实际调用一次，输出 failed to authenticate；get-state exit1 / device unauthorized。connect 自身 exit0 不能记为成功。

已对唯一目标 disconnect(exit0)，仅停止自己启动的专用 server(exit0)，进程正常退出。另起只读任务回读云端 result-connect.json：connect_attempts=1、记录的进程不存在、专用监听数0；任务目录0700、任务新生 ADB key0600、默认 root key仍不存在。官方手机 API 回读原 keypair 绑定未变、手机RUNNING；nginx/sshd保持active。未读取/输出密钥内容。

## 2026-09-29 当时的三项验收状态

| 验收项 | 本轮实际结果 | 尚缺证据 |
| --- | --- | --- |
| 网页登录并正常玩 | User Google登录及Play安装有确认；User实际游戏可玩，ANGLE后图形恢复；无探针基线通过本轮手动反馈 | 未独立观察游戏账号登录过程；长期稳定性未测 |
| 本轮新增采集且成功解码 | 未执行；捕获/成功/失败数unknown | 获准连接、当前build/ABI/descriptor/Frida、真实普通操作对应的新增业务响应 |
| 正常结束并保存 | 未执行；没有Session，最终状态unknown | stop/flush、进程退出、结果回读与计数核对 |

## 2026-09-29 管理证据与失败记录

- 实际方法和ANGLE回滚见 [README.md](README.md)，Google/API方法见 [GOOGLE_READONLY.md](GOOGLE_READONLY.md)。原始目标/任务ID、响应、地址和凭据留受控本机，Git只记录脱敏事实。
- Huuuge安装回查、图形只读首次曾在DNS解析阶段失败；在确认未建立连接并查询任务/解析恢复后各只重试一次只读请求。未知变更不重放。
- 通用launcher命令shell exit0但输出无法解析Intent，不记成功；读取真实launcher后显式BootActivity启动Status=ok。ANGLE设置已回读，限定游戏进程日志确认2.1.2/Vulkan SwiftShader；User复查后确认恢复。
- 手机/Linux命令均按唯一目标/子任务或InvokeId回读；Linux结果Success/ExitCode0、完整首尾标记。TCP检查成功是网络层证据，无法证明ADB认证。前次被拒脚本未提交；本轮User新授权后正常默认审批放行，未换工具或关闭审批。首次connect/get-state返回unauthorized，保留失败记录；匹配密钥配置后单独获准复验返回device，两次证据分别保存。
- 原controller/decoder的私网gate和停止/保存机制保持；采集代码未改，未接Frida。此次仅一次ADB验证，未读取游戏数据，历史合成CI不是本轮新增数据。
- 无本机持续采集、付费资源创建或晨会服务修改；User自行建立的新公网映射单独记录，不再笼统说“没有公网端口”。

## 历史准备检查（2026-09-15）

- Python 语法检查通过。使用现有 Windows Python 3.12.9 和已安装依赖进行合成测试，没有安装采集组件或启动 ADB/Frida/游戏。
- 本机最终检查：14 项，11 通过、3 项 Linux 专属检查跳过。
- Linux CI 已通过全部 14 项（Python 3.12.14 / protobuf 7.36.1），包括真实子进程锁、SIGTERM 和 supervisor 的 probe → run → 人工窗口 → stop → 退出后文件回读。最终代码证据：[run 34957001266](https://github.com/840832144/huuuge-android-research/actions/runs/34957001266)，代码 commit `9bb241b`；还覆盖最终文件被移除后 finalize 必须返回 incomplete/非零，不能依赖缓存。
- 测试通过伪造的 Frida 接口传送**测试生成的 protobuf 字节**，执行真实 `live_decode.py` 子进程、解码、文件保存和结束路径。合成 3 条、成功 2 条、失败 1 条仅用于证明程序行为，**不是真实 Huuuge 新增数据**。
- 覆盖旧 Session 不覆盖、路径穿越阻断、wrapper 失败 Raw 保留、断连失败、hook 失败、启动异常、缺失文件、未知退出码、人工窗口与脱敏摘要。
- Windows 未配置可用 WSL，本轮不安装 Linux 或云端模拟环境。Linux 锁、SIGTERM、完整 supervisor 路径使用 GitHub CI 合成检查；仍不替代云手机验收。

## 2026-09-29 历史Review与当时下一步

原业务 PR #2 / 治理 PR #4 交本轮真实进度增量 Review；Task保持In Progress，不标Complete/Accepted。

**前次单次ADB验证授权**：User 当时授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。

User委托Codex接手本地管理与云端密钥配置。Workbench经本机CredentialsCmd适配复用原OAuth临时STS，唯一Linux目标只读查询通过；未创建Workbench SSH会话。实际远程执行继续用ECS Cloud Assistant，OpenSSL CMS加密后只下发密文，云端公钥比较一致，匹配私钥已放入独立目录，0700/0600。

User随后明确允许新的一次ADB复验。正常工具审批通过，本次connect实际1次成功，get-state=device/exit0；disconnect与专用server停止均exit0。独立回读保存结果、记录PID不存在/专用监听0；一次性传输材料已清理，原任务key保留、默认root key不存在，手机绑定/安全组规则未变，nginx/sshd仍active。无Frida/采集。

本次连接验证已完成，无需User再找主机、上传密钥或重新绑定。下一阶段明确持续连接与Frida/真实采集范围后继续原验收目标；当前保持停止，真实新增解码、采集正常结束和保存结果回读仍未执行。
