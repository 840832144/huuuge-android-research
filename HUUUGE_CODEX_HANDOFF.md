# Huuuge Research — Codex Handoff

## 2026-09-29 — TASK-0031 v2-GooglePlay 续接

- 状态 In Progress。继续原 Task、业务 PR #2 和治理 PR #4，方案为 [PR #11 / 5ff7190](https://github.com/840832144/AI-Workspace/blob/5ff7190137f1512f52cddacc0f5d17ce5cc4254e/tasks/support/TASK-0031/CLOUD_DEBUG_PLAN_20260929.md)，不新建任务/PR。User 本人负责权限、登录和手动游戏，Codex 负责 Google 准备。
- 已安全合入业务 main `6cdb1d6`（保留双方状态/日志），定向复查 controller → decoder → 停止/回读；该调用链仅同步一处上游 CLI 帮助文案，未重写采集器或运行探针。治理 main `b0a36c8` 同步后 Registry 19 canonical / 0 collision / valid。
- Workbench CLI 官方 Windows 包安装到用户 Programs/workbench、加入用户 PATH；官方 SHA-256 校验通过，v1.0.1 / `86c0aff`，帮助已核验。默认配置文件尚不存在，没有读取凭据、连接 ECS 或更改安全组。
- 后续按支持流程恢复一次，读取同一官方 instanceLayouts URL、已打开的连接窗口与实际 Android 桌面；此前连接已生效，没有重放连接点击。唯一已购目标仍可用，香港/4c8g32G/Android 12/26.09.1。控制台远程命令只选择该实例，固定脚本全文回读匹配后仅执行一次；输出为空。关闭命令表单时报 `js execution timed out; kernel reset, rerun your request`，浏览器自动化现已停止。命令结果 unknown，不能推断 Google 包缺失或网络不可达。
- User 授权的官方 API 备用通道已准备：阿里云 CLI v3.5.1 官方包校验、版本/帮助已核验；固定脚本语法和 RunCommand/DescribeTasks 虚构实例离线预演通过，没有 API 调用。未发现默认配置/标准凭据环境变量；香港地域预演返回 unknown endpoint，官方表与 CLI 仅列上海/新加坡。香港实例的实际管理接入点和 AgentType 仍待核实，不猜测或跨地域试查；Workbench 不用于云手机 ID。
- [部署说明](deploy/cloud/README.md)已补谷歌官方准备顺序、本人登录节点、商店获取 Huuuge、管理工具实况及只读 API 步骤；[验收记录](deploy/cloud/ACCEPTANCE.md)区分网页桌面已确认、命令结果未知与尚未验证的 Google/游戏/采集项目。原始数据/账号不进 Git。
- 下一步：User 只需按[只读管理说明](deploy/cloud/GOOGLE_READONLY.md)在本机配置受限 STS profile；接入点核实后先 DescribeTasks 定向查回已有命令，未知结果不重发 RunCommand。取得组件状态后由 Codex 按适用官方方法准备 Google，到原生登录页通知 User。Linux/Workbench 另行核验，不阻止手机准备；无探针基线通过后才采集，最终 Stop→退出→保存结果回读。
- 当前没有云端 Session 或真实计数，尚未交付完整成功。未增加付费资源/公网端口，未动晨会、历史 Capture 或本机采集；不发布 SVN 安装包。Subagents: none。

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
