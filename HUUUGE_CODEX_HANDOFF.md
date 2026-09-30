# Huuuge Research — Codex Handoff

## 2026-09-30 — TASK-0037 当前交接（范围调整后）

- 原Task：AI-Workspace/tasks/TASK-0037-HUUUGE-SELF-SERVICE-V1.md；Status In Progress。分支codex/huuuge-self-service-v1，关联Accepted TASK-0031；不新建Task，不向旧试点PR加功能。
- User成员账号已在官方Web到Android桌面/Huuuge大厅，仅User本人反馈；同事盲测、Android客户端和V1新批次均未通过。
- 官方Web玩固定游戏账号＋独立采集小面板，分别登录，可信同事约定轮流。删除强制防重连/旧凭证撤销/手机控制交接验收；采集锁不等于手机控制锁。基本鉴权、单采集任务、批次和下载归属继续保留。
- 准备代码保留于9b6b21d；当前页面/API/worker已脱离SDK。vendor.py保留历史且不加载，原数据库兼容字段保留但不参与手机授权。CaptureRuntime只明确阻止尚未实现的云连接，不把旧SDK撤销门槛换名继续当阻塞。
- 受保护连接、常驻运行/TLS轮换/进程清理/容量保护及HTTPS入口仍待实现或核验；无V1真实采集，尚不能Review。不得把admission开关或测试替身当云实现。
- 下一步：核实并实现现有Linux到手机的受保护路径，复用原controller；根据真实需求提出精确身份/网络/IAM/公开入口/共享服务变更与回滚，待Owner确认。取消SDK后不预设云API身份必须新增；不等厂家撤销工单。
- 原TASK-0031 Accepted、312/312/0及8条Slots结果不动。A—F真实验收全部仍有待办，范围以更新后的原规格为准；完整采集/下载/本地AI不推迟，不接其他游戏。
- 本轮仅本地代码/资料与合成验证；不做本地安装包/SVN镜像，不修改晨会。Subagents: none。
- 当前Draft入口：业务PR #3、AI-Workspace治理PR #13。1c9c364的Linux合成CI run36682709050共42/42通过、无跳过；完整真实V1仍未验，不交完整Review，不自动合并。

## 2026-09-30 正式评审收口

TASK-0031 Round 1 **Accepted**，阻塞修改无；[正式评审](https://github.com/840832144/AI-Workspace/pull/4#pullrequestreview-5361181770)已落库。312/312/0、8条Slots响应及原结果快照保持不变，不重新采集。原PR待User决定合并，reservation pending-main；canonical进入main后才finalize并收口Complete。新自助V1另行登记后继Task，本试点不增加新功能。Subagents: none。

## 2026-09-30 — TASK-0031 真实云端闭环完成，交 Review

- 本轮一台既有云手机、一个新批次；真实捕获 **312**、解码成功 **312**、失败 **0**。User 手动窗口内回读 **8 条 SlotsGameServer.Spin 响应**，业务字段非空；User 确认“操作完成，游戏正常”。
- 采集时间 2026-09-30 10:59:50.285—11:03:22.133（UTC+8）；play-end/stop/子进程均 exit0，`finalized` / `ready-for-human-review`。清理后独立回读 index、Raw、JSON、manifest 与计数一致，无 active Session。
- 实际运行源码 `03fb399201d08c878c74322347b652bc8e8a2414`；既有 Python3.11.13 独立 venv、Frida17.17.0、protobuf7.36.2、lz4 4.4.5，当前 APK 静态提取40-file descriptor。云端 Linux **24/24 合成检查**与上述真实采集分开记录。
- 原 controller 最小适配显式公网 ADB + Frida TLS、准确包名/PID、当前 descriptor 预检与一次受限启动重试，目标/版本/ABI/Root/forward 校验保留。真实 TLS1.3、固定手机证书、错误证书/令牌拒绝及正确令牌鉴权通过。传统公网 ADB 本身仍未加密；业务数据由 Frida TLS 保护。
- 首次 decoder 在创建 Session/挂接前因内置 descriptor 版本冲突退出；修复后只对同一已分配批次重试一次，保留原失败状态、日志及启动摘要。没有第二个采集批次，没有用旧结构替代当前结构。
- 本次 Frida、采集进程、专用 ADB server 已退出，精确 forward 已移除，专用监听为0；临时 TLS 私钥/令牌已清理。原匹配 ADB key 保留；手机 RUNNING、绑定/公网映射及4条安全组入站规则未变，nginx/sshd active，系统 Python3.6.8 未替换。没有新增资源/费用、网络/IAM变更或晨会修改。
- Google 三个内置包已按 Android 官方 pm enable 方法启用，User 登录并从 Play 安装 Huuuge；原无探针图形修复和可玩反馈保留。本轮 Huuuge12.09.27229/1789041595、Android12/ARM64；Play Protect 认证仍未确认，长期稳定性未测。
- 当前无执行阻塞；等待原业务 PR #2 / 治理 PR #4 Review，不标 Complete/Accepted。真实数据、配置、地址与密钥只留受控环境；本机不持续采集。Subagents: none。

本轮部署见 [TLS_TRANSPORT.md](deploy/cloud/TLS_TRANSPORT.md)，结果见 [ACCEPTANCE.md](deploy/cloud/ACCEPTANCE.md)。下文旧授权/阻塞均为对应日期历史，不再作为当前下一步。

## 2026-09-29 — TASK-0031 v2-GooglePlay 续接

- 状态：In Progress；Google/Play 安装及无探针游戏已取得真实证据；匹配密钥的云端ADB复验已通过，已断开并停止专用server；真实采集与停止保存未执行。
- 原业务 PR #2 / 治理 PR #4 交增量 Review，不新建任务/PR。方案 PR #11 / `5ff7190`。

- 原 Task/PR 保留，按 PR #11 v2-GooglePlay / `5ff7190` 续接；业务 main `6cdb1d6`、治理 main `b0a36c8` 已同步。Registry 19 canonical / 0 collision / valid，reservation pending-main；Subagents: none。
- User 已完成 official-cli OAuth，GetCallerIdentity=Account；User 明确“你先用这个调试”，继续使用已有授权身份，不再要求切换 RAM。未改 IAM。Workbench v1.0.1 与 Aliyun CLI v3.5.1 复用不重装；Workbench 已通过 CredentialsCmd 复用现有 OAuth 临时凭据并查询匹配Linux；未创建SSH会话，未用于云手机ID。
- 云手机实际管理通道为官方 eds-aic/2023-09-30 上海接入点 + 香港 BizRegionId，经精确唯一实例校验；EdsAgent RunCommand → DescribeTasks 已真实通过。浏览器先前恢复已核验官方 URL/原连接窗口；后续超时仍停止自动化，旧控制台命令 unknown，不重放点击。
- Android 12 / SDK31 / arm64-v8a / 镜像26.09.1。Play/GMS/GSF 原存在但禁用；以 Android 官方 `pm enable --user 0` 启用三个内置包，均 exit0 且回读 enabled=yes/disabled=no。两个 Google 官方域名 HEAD=302/exit0。未侧载、清数据、重建或修改认证。
- Play 启动成功后 User 亲自 Google 登录。Huuuge 首次未安装，User 经官方详情完成新安装并反馈“打开”；包管理器回读 installer=com.android.vending、12.09.27229 / 1789041595、arm64-v8a。商店详情与下载安装可用；首页/搜索未单独验证。Play Protect 认证记录“无法读取/未确认”（User 暂未找到该项），不宣称已认证，也不反复要求查找。
- User 无探针游戏反馈“能玩，画面有点问题”，截图存在错位/缺字。实读 CPU 渲染、GLES SwiftShader、内置 com.android.angle，两项应用 ANGLE 设置原为 null。仅为 Huuuge 设置 angle 后重启该应用；通用 launcher intent 报无法解析，查真实 launcher 后以 com.huuuge.casino.BootActivity 启动，Status=ok。限定该进程日志确认 ANGLE/Vulkan SwiftShader 生效；User 随后确认“现在好了”。本轮无探针网页可玩/图形恢复有真实证据，长期稳定性未测。
- 按 User 要求自行核实到已有香港 Linux ECS；官方 ECS Cloud Assistant 状态正常，并用 ECS RunCommand → DescribeInvocationResults 实读 Alibaba Cloud Linux3、x86_64、2CPU/约7.4GiB内存、根盘约31GiB可用、Python3.6.8。PATH 未找到 adb/git，任务目录不存在；nginx 在运行，未修改/重启既有服务。没有新增 ECS/NAT/EIP。
- 原私网 phone:5555 从该 Linux 单次 TCP 检查超时；未证实同 VPC，默认/任务路径 ADB key 均未发现，手机现有 keypair 绑定已记录但未替换。手机未发现 ssh/ssh-keygen 命令，因此反向 SSH 仅为未实施备选，不宣称已具备通道。
- User 随后提供控制台新建公网 ADB 映射及 connect 命令。官方 ListInstanceAdbAttributes 返回唯一匹配手机，外部10001→内部5555；从已有 Linux 单次 TCP 连接成功。该映射由 User 建立，Codex 未创建映射、改安全组或导出 Cookie；真实 IP/实例标识不入 Git。
- 前次自动审批拒绝（blocked by policy）属于历史；User 明确收窄授权后，本次正常默认审批已放行，没有关闭审批或换工具绕过。User 新授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。
- 正常工具默认审批本次已放行，经 ECS Cloud Assistant 在任务独立目录安装官方 Platform-Tools；实读 ADB1.0.41 / 37.0.1-15733141。首次 server 因监听参数写法报错退出、未执行 connect；改为官方 localhost 语法后实核仅回环监听。connect 实际调用一次，输出 failed to authenticate；get-state exit1 / device unauthorized。connect 自身 exit0 不能记为成功。
- 已对唯一目标 disconnect(exit0)，仅停止自己启动的专用 server(exit0)，进程正常退出。另起只读任务回读云端 result-connect.json：connect_attempts=1、记录的进程不存在、专用监听数0；任务目录0700、任务新生 ADB key0600、默认 root key仍不存在。官方手机 API 回读原 keypair 绑定未变、手机RUNNING；nginx/sshd保持active。未读取/输出密钥内容。
- 原 controller 仅允许私网/loopback transport，校验保持不变，不用代理伪装公网地址。User 本轮授权仅限既有入口的一次连接验证，不包含持续采集；如后续采用公网采集，仍需独立明确范围并最小适配/Review。无 Frida、采集 Session 或新增解码计数，正常停止/保存回读仍未执行。

**前次单次ADB验证授权**：User 当时授权仅限既有云端 Linux 独立目录安装官方 Android Platform-Tools，使用 User 已建且已核验的公网映射做一次 connect/get-state；server 仅回环，不覆盖共享工具/已有密钥，不替换手机绑定，保留鉴权。本轮禁止 Frida/采集、重启/清数据及资源/映射/安全组/防火墙/IAM/既有服务变更；需要授权/密钥配置交 User 本人。

User委托Codex接手本地管理与云端密钥配置。Workbench经本机CredentialsCmd适配复用原OAuth临时STS，唯一Linux目标只读查询通过；未创建Workbench SSH会话。实际远程执行继续用ECS Cloud Assistant，OpenSSL CMS加密后只下发密文，云端公钥比较一致，匹配私钥已放入独立目录，0700/0600。

User随后明确允许新的一次ADB复验。正常工具审批通过，本次connect实际1次成功，get-state=device/exit0；disconnect与专用server停止均exit0。独立回读保存结果、记录PID不存在/专用监听0；一次性传输材料已清理，原任务key保留、默认root key不存在，手机绑定/安全组规则未变，nginx/sshd仍active。无Frida/采集。

本次连接验证已完成，无需User再找主机、上传密钥或重新绑定。下一阶段明确持续连接与Frida/真实采集范围后继续原验收目标；当前保持停止，真实新增解码、采集正常结束和保存结果回读仍未执行。

实际方法、图形回滚及结果见 [部署说明](deploy/cloud/README.md)、[验收记录](deploy/cloud/ACCEPTANCE.md)。原始响应、目标与凭据留受控本机；无本机采集、无 SVN 本地包、未触碰晨会。Subagents: none。

## 2026-09-15 — TASK-0031 单实例云端准备

- 当前：代码准备交 Review；User 确认资源未就绪，真实三项验收均未执行。
- Review：[PR #2](https://github.com/840832144/huuuge-android-research/pull/2)；代码 `9bb241b`，Linux [CI 34957001266](https://github.com/840832144/huuuge-android-research/actions/runs/34957001266) 14/14 合成检查通过，无真实云环境验收。
- 执行与说明：`scripts/cloud_capture.py`、`deploy/cloud/README.md`、`deploy/cloud/ACCEPTANCE.md`、`tests/test_cloud_capture.py`。
- AI-Workspace Task：[TASK-0031](https://github.com/840832144/AI-Workspace/blob/codex/huuuge-cloud-single-instance/tasks/TASK-0031-HUUUGE-CLOUD-SINGLE-INSTANCE.md)，业务入口：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)。
- 下一动作：ChatGPT Review 准备代码，技术提供云端资源与匹配结构文件后，User 亲自网页操作完成真实闭环。不得用下方历史本机结果作为云端成功。
- 未修改晨会服务、共享系统环境、历史 Raw 或其他 Agent 工作；本轮不发布 SVN 本地安装包。Subagents: none。

## 2026-09-01 Big Fish target correction

The user confirmed that the requested same-room shared-win feature is in Big Fish Casino, not Huuge Casino. Continue `TASK-0020` from `CURRENT_STATUS.md` and `TASKS.md`.

- Package: `com.selfawaregames.acecasino` 21.3.8 / 1293; ARM64 `libgame.so`; Cocos2d JavaScript; HTTP JSON through `SANetworkInterface.serverRequest`.
- The staged Big Fish Gadget is verified through Houdini on ADB-forwarded port `27044`; Huuge remains on `27043`.
- New code: `artifacts/bigfish_probe/agent.js` and `bigfish_capture.py`.
- Last local capture: `C:\bigfish_research\captures\20260901_171000`, stopped with zero HTTP events. Native Hooks/eval worked, but no `collector-installed` acknowledgement was observed; do not report READY.
- Next: resolve access to `SANetworkInterface`, then prove one ordinary request/response pair. Do not reuse Huuge protobuf descriptors or the Huuge Agent.
- Raw APKs, resources and captures stay local under `C:\bigfish_research`.
- Subagents: none.

- Updated: 2026-08-27 16:11 +08:00
- Actor: Codex
- Task: TASK-0018
- State: Waiting for ChatGPT Review Round 2
- Review Round 1: Needs changes at `b278afa70a01b4c40b72aec62b6d8bbd6f909ac4`
- Subagents: none

## Objective

根据 Review Round 1 修订 Lottery 数值拆解：以策划阅读顺序重组报告，重新提取真实充值记录，严格区分普通筹码下注、Free Spin 与真实货币购买，补齐 Extractor 测试，并替换原飞书文档而不创建副本。

## Completed

- 主报告改为策划优先结构：玩法 → 玩家实际行为 → 票来源 → 消耗与进度 → 奖励 → 付费与价值 → 策划结论 → 技术附录。
- 主体证据标签统一为“已确认 / 本次样本观察 / 待验证 / 策划建议”；L0-L4、endpoint 和 B0 仅保留在证据或技术说明中。
- 本地按请求链重新配对 `MakeInAppPurchase`，仅输出脱敏购买序号与聚合字段，不输出请求、商品、商店、订单或账号标识。
- Extractor 新增 `PURCHASES.csv`、真实货币购买汇总和失败链路闭合校验；公共字段统一使用普通筹码下注命名。
- 单元测试扩展到 7 个，覆盖购买提取、未完成链路 fail-closed、普通下注命名和礼包其他奖励提示。
- 先搜索并确认唯一同名飞书文档，再原位替换。最终仍为原文档 `IK5adiJyWoHVJzxlovEcjxiWnO3`，没有调用创建接口。

## Confirmed Baseline

- Finalize 别名 `LOT-20260827-A`：manifest `stopped`，四个生命周期 marker 完整，8712/8712 RPC 解码。
- 346 次 Toss 消耗 933 张票：Bronze 756、Silver 60、Gold 79、Black 38。
- 588 次普通筹码下注与 45 次 Free Spin 均完成请求/响应配对；两者均不是 Lottery 真实货币购买。
- 四次真实货币购买全部成功，共 54.43 SGD；礼包合计发放 763 张 Lottery 票和 235 loyalty points。
- 每个礼包同时含 loyalty points，因此每张票表观成本只能作为礼包描述性比值，不能当作独立票价或长期付费价值结论。
- 免费票规则在本 Session 精确闭环：初始进度 1，每消耗 7 张任意票返 1 Bronze，共 133 张，最终进度 3。
- 购买 763 张、Lottery 直接奖励 60 张、阈值返还 133 张、升级关联 16 张，票务总账差为 0。
- 六次等级变化后合计新增 16 Bronze 的状态变化为已确认；升级因果仍为本次样本观察，不能提升为配置事实。

## Report and Feishu Validation

- Git 主报告标题只出现一次，章节顺序和 Review 要求一致。
- 117.516 仅出现在技术附录，表述为“筹码奖励输出 / 普通 Spin 筹码成本（不含充值购买）”；明确不是 RTP、ROI 或付费回报。
- 飞书回读为 367 blocks、4568 个正文字符、单一标题；策划章节顺序、四条购买记录、54.43 SGD、763 张票、235 loyalty points、588 次普通下注与 45 次 Free Spin 均存在。
- 飞书权限回读为 `tenant_editable`，目标为企业，权限为编辑。
- 替换过程中一次正文清理表达式产生空正文；已立即使用完整本地报告恢复，并在最终回读中验证正文、章节和权限全部正确。没有创建重复文档，也没有丢失本地数据。

## Evidence Boundaries

- 已确认：Finalize、Toss/Spin 计数、票消耗、阈值返还、四次购买的本地金额/币种/礼包发放、即时奖励、拼图完成、票余额变化和总账。
- 本次样本观察：16 张 Bronze 与升级的时序关联，以及所有依赖 B0 的描述性比值。
- 待验证：不同等级区间、不同下注档和完整活动周期下的稳定分布。
- 策划建议：仅作为后续方案或实验建议，不冒充线上配置、概率或长期回报结论。
- 未提交真实 Session/account/request/product/store/order 标识、原始 JSON、绝对筹码余额、完整余额轨迹、credentials 或绝对本地路径。

## Files for Review

- `reports/lottery/20260827_lottery-ticket-puzzle/LOTTERY_NUMERICAL_BREAKDOWN.md`
- `reports/lottery/20260827_lottery-ticket-puzzle/PLAYFLOW_AND_LOGIC.md`
- `reports/lottery/20260827_lottery-ticket-puzzle/EVIDENCE_MATRIX.md`
- `reports/lottery/20260827_lottery-ticket-puzzle/CR_RECOMMENDATIONS.md`
- `reports/lottery/20260827_lottery-ticket-puzzle/PURCHASES.csv`
- `reports/lottery/20260827_lottery-ticket-puzzle/*.csv`
- `tools/analysis/lottery/extract_lottery_facts.py`
- `tools/analysis/lottery/tests/test_extract_lottery_facts.py`

## Validation

- `python -m py_compile tools/analysis/lottery/extract_lottery_facts.py` passed。
- `python -m unittest discover -s tools/analysis/lottery/tests -v`：7/7 passed。
- Extractor 对 Finalized Session 重跑通过：4 次购买、54.43 SGD、763 张购买票、235 loyalty points、票务总账差 0。
- 生成文件和报告中的下注与真实货币购买术语已严格分离；`PURCHASES.csv` 不含请求、商品、商店或订单标识字段。
- Feishu search-before-replace、原文档替换、正文回读和 company-editable 权限回读通过。
- 未修改 Collector、游戏、服务端、CR 仓库或 SVN。

## Risks / TODO

- 升级奖励缺少显式 grant payload 或 UI 录屏，不能提升为配置事实。
- Reward config 未暴露权重，单 Session 命中率不能当作配置概率。
- 起始拼图板面与完整活动周期未知，不能从 5/933 推导稳定完成成本。
- 四个购买礼包均含其他奖励，不能把表观每票成本直接用于跨礼包价值排名。

## Exact Next Action

ChatGPT 对修订后的 Git 报告、Extractor 测试和原飞书文档执行 Review Round 2。Review 通过前不自动新增采集、不改 Collector、不提交 CR 或 SVN。
