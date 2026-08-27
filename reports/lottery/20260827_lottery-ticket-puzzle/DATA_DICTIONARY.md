# 数据字典

## 通用字段

| 字段 | 含义 |
| --- | --- |
| `session_alias` | 脱敏样本别名，不对应真实目录名 |
| `claim_type` | `Confirmed`、`Estimate`、`Hypothesis` 或 `Decision proposal`；只用于技术附件 |
| `evidence_source` | Schema、Config、Runtime、UI、Manual 或组合来源 |
| `evidence_level` | Huuuge L0–L4 Evidence Level |
| `sample_count` | 当前行使用的样本数，不代表全活动样本 |
| `limits` | 适用范围、缺失项和禁止外推事项 |
| `B0` | 本次最低普通下注，只在技术表中作为筹码归一化单位；正文写“最低下注单位” |

## 术语

- **普通下注 / 筹码下注：**玩家消耗游戏筹码进行 Spin，不等于真实货币支付。
- **Free Spin：**不单独消耗本次下注筹码的免费旋转。
- **付费 / 充值 / 购买：**玩家使用真实货币完成的交易。
- **表观每票成本：**礼包总价除以票数；礼包含其他奖励时不能当作纯票价。

## 文件说明

### SESSION_SUMMARY.csv

记录 Finalize 状态、时间、版本、哈希和样本量。使用 `regular_spin_requests / responses` 表示普通下注。

### PURCHASES.csv

每笔成功购买使用 `Purchase-1...N`。字段包括金额、币种、票色、票数、忠诚度、其他奖励类型和表观每票成本。真实 request、product、store 和订单标识只用于本机关联，不进入 CSV。

`bundle_has_other_rewards=True` 时，`apparent_cost_per_ticket` 只能比较礼包表面价格，不能把全部金额归因给票。

### LOTTERY_ACTION_STATS.csv

每个票色一行。`single_*` 只统计单抽；`bulk_calls` 与 `ticket_units` 包含批量抽。Wilson 区间保留在技术表，不进入策划正文。

### SLOT_ITEM_DROP_STATS.csv

`regular_spins` 表示普通筹码下注。`direct_ticket_field_present=False` 表示 Spin 结果中没有直接发票字段，不表示“掉落率已确认是 0”。`upgrade_linked_*` 是升级后票余额变化的时序/总账归因。

### REWARD_OUTPUT_STATS.csv

`reward_objects` 是奖励对象数，`quantity_sum` 是可相加道具数量；筹码统一写入 `normalized_chip_*_b0`。即时奖励与拼图完成奖励分行，避免重复。

### PROGRESSION_MODEL.csv

记录累计补回阈值、票来源、消耗、最终库存和升级关联事件。购买行的金额与礼包组成在 `PURCHASES.csv`。

### RETURN_MODEL.csv

- `regular_spin_chip_cost`：普通下注筹码消耗，不是付费金额。
- `real_money_spend`：真实货币购买金额，本次为 SGD。
- `chip_reward_output_over_regular_spin_chip_cost_excluding_purchases`：只用于技术核对，排除真实货币购买，不是 RTP、ROI 或付费回收率。
- `ticket_ledger_balance_check`：票务总账校验，必须为 0。

## 脱敏规则

- 不提交真实 Session、账号/玩家、request、product、store、订单标识、完整消息、绝对本地路径或逐时余额轨迹。
- 筹码只使用相对最低下注单位；票数、金额和币种作为本次机制/交易事实保留。
- User 的现场确认只用于证明四次交易是本人真实操作，不替代运行记录中的金额与发放结果。
