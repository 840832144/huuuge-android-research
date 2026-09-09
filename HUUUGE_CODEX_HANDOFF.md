# Huuuge Research — Codex Handoff

## 2026-09-09 · TASK-0030 机器人资料线索补充

- Status: Review；继续已有策划阅读版。User 要求补足 DSH 已做的机器人研究及私有策划落地内容，不新建任务。
- [策划源稿](reports/pop-slots/lobby/POP_SLOTS_LOBBY_PLANNER.md)新增第八节：UID聚集、美国地区集中、Guest名称、姓氏重复及姓名位置异常；说明25/28记录与总述29份尚未对齐，不换算机器人比例，也不认定具体账号身份。
- 沿用原研究，不重采。机器人活动过程保留为原研究解释，完整周期和让座仍未确认；完整账号资料未复制。
- 原位补充既有云文档；原正文块、6图、互链与导航条目保留。新增内容与源稿回读匹配，未变更权限或原研究；云端已删除的旧外链未恢复，源稿同步该删减。
- 私有 CR 策划配置与验收建议只保存在获准目录；没有生成配置文件、改原需求/配置/SVN或开发 CR。
- 唯一下一步：User / ChatGPT 审阅补充的研究线索与策划表拆分。Subagents: none。

## 2026-09-09 · TASK-0030 策划阅读版内部发布

- Status: Review（云版）；原离线版已由 ChatGPT Accepted，本轮继续同一正式任务。
- 新入口：[策划阅读版源稿](reports/pop-slots/lobby/POP_SLOTS_LOBBY_PLANNER.md)、[交接](reports/pop-slots/lobby/REVIEW_HANDOFF.md)。原研究稿、离线 HTML 与19条证据继续保留。
- 六张策划配图保留画面，改为日常表达；原图5残留标记已遮盖，并同步离线 HTML。两份互链公司云文档通过既有 Document Assistant 发布，六图、正文、实际链接、公司内可编辑与唯一导航登记均已回读。
- CR 策划对照和内部云链接只保存在私有仓库获准目录；不进入本公共研究记录。
- 本轮只改写与发布，未采集、操作游戏、开发 CR、改原需求/配置/SVN或修改 Provider。
- 唯一下一步：User / ChatGPT 审阅两份云文档，不沿用离线 Accepted 作为云版验收。Subagents: none。

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
