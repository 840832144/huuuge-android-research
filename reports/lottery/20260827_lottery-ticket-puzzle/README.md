# Huuuge Lottery 活动数值拆解

本目录是 TASK-0018 的脱敏交付。主报告按游戏策划阅读顺序说明玩法、实际游玩、充值购票、票的来源与消耗、奖励、价值观察和策划建议；技术证据单独保留在附录。

## 先看这三份

- [`LOTTERY_NUMERICAL_BREAKDOWN.md`](LOTTERY_NUMERICAL_BREAKDOWN.md)：完整策划报告，也是飞书正文来源。
- [`PLAYFLOW_AND_LOGIC.md`](PLAYFLOW_AND_LOGIC.md)：活动循环和机制边界。
- [`CR_RECOMMENDATIONS.md`](CR_RECOMMENDATIONS.md)：等待评审的设计候选。

## 本次关键事实

- 约 1 小时 58 分钟实玩；588 次普通筹码下注，另有 45 次 Free Spin。
- 346 次抽奖，消耗 933 张票。
- 4 次真实货币购票，合计 54.43 SGD；获得 763 张票和 235 点忠诚度。
- 每累计消耗 7 张票补回 1 张 Bronze，本次补回 133 张。
- 抽奖直接奖励 60 张票；六次升级后的余额增长合计 16 张 Bronze，升级因果仍待进一步验证。

## 结构化事实表

- `SESSION_SUMMARY.csv`：样本时间、版本和完整性。
- `PURCHASES.csv`：Purchase-1...4 的金额、币种、票色、票数和附加忠诚度；不含任何关联标识。
- `LOTTERY_ACTION_STATS.csv`：按票色统计抽奖、批量、命中与拼图完成。
- `SLOT_ITEM_DROP_STATS.csv`：普通下注、Free Spin 和升级关联票的边界。
- `REWARD_OUTPUT_STATS.csv`：奖励类别与最低下注单位换算。
- `PROGRESSION_MODEL.csv`：票务来源、消耗、累计补回和进度。
- `RETURN_MODEL.csv`：真实货币投入、普通下注筹码消耗、奖励输出与票务总账。

## 证据附件

- [`EVIDENCE_MATRIX.md`](EVIDENCE_MATRIX.md)：Claim、L0–L4、技术定位与限制。
- [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)：字段、单位和脱敏规则。

主报告使用“已确认 / 本次样本观察 / 待验证 / 策划建议”。技术附件继续使用完整 Evidence Level，Lottery 当前为 `L3 Runtime Observed`，尚未达到 L4 多源验证。
