# Huuuge Lottery 活动数值拆解

本目录是 TASK-0018 的脱敏交付。分析对象为别名 `LOT-20260827-A`，原始 Session、账号标识、绝对筹码余额和逐条明细仅保留在本机，不进入 Git。

## 阅读顺序

1. [`LOTTERY_NUMERICAL_BREAKDOWN.md`](LOTTERY_NUMERICAL_BREAKDOWN.md)：结论与数值基线。
2. [`PLAYFLOW_AND_LOGIC.md`](PLAYFLOW_AND_LOGIC.md)：玩法、消耗、进度和产出链路。
3. [`EVIDENCE_MATRIX.md`](EVIDENCE_MATRIX.md)：每条关键结论的证据等级与限制。
4. [`CR_RECOMMENDATIONS.md`](CR_RECOMMENDATIONS.md)：可供策划评审的 CR 候选，不是已确认规则。
5. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)：CSV 字段和统一口径。

## 结构化数据

- `SESSION_SUMMARY.csv`：Finalize 完整性和样本规模。
- `LOTTERY_ACTION_STATS.csv`：按票色统计抽取、批量、命中与拼图完成。
- `SLOT_ITEM_DROP_STATS.csv`：Spin 与升级关联产出的边界。
- `REWARD_OUTPUT_STATS.csv`：奖励类别与 B0 归一化输出。
- `PROGRESSION_MODEL.csv`：票务来源、消耗、免费进度和场景模型。
- `RETURN_MODEL.csv`：筹码成本、奖励输出和票务总账。

## 结论标签

- `Confirmed`：可由本次 Runtime、Config 或 Schema 直接复核。
- `Estimate`：由已确认数据计算或时序归因，但仍受样本范围限制。
- `Hypothesis`：待额外采集或 UI 对照验证。
- `Decision proposal`：面向 CR 的设计建议，不代表线上规则。

Lottery 模块当前可提升为 `L3 Runtime Observed`，但尚未达到 `L4 Triangulated`：缺少完整 UI 录屏、完整活动周期和第二账号/版本复验。
