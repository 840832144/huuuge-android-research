# 数据字典

## 通用字段

| 字段 | 含义 |
| --- | --- |
| `session_alias` | 脱敏 Session 别名；不对应真实目录名 |
| `claim_type` | `Confirmed`、`Estimate`、`Hypothesis` 或 `Decision proposal` |
| `evidence_source` | Schema、Config、Runtime、UI、Manual 或组合来源 |
| `evidence_level` | Huuuge L0–L4 Evidence Level |
| `sample_count` | 当前行实际使用的样本数，不代表全活动样本 |
| `limits` | 适用范围、缺失项和禁止外推事项 |
| `B0` | 本 Session 观测到的最低付费 Spin bet；用于筹码归一化 |

## 文件说明

### SESSION_SUMMARY.csv

只记录 Finalize 状态、时间范围、版本、哈希、RPC 数量和结构化产物数量。账号、设备和 Session 均使用别名。

### LOTTERY_ACTION_STATS.csv

每个 `ticket_color` 一行。`single_*` 只统计单抽；`bulk_calls` 与 `ticket_units` 仍包含批量抽。Wilson 区间用于描述筹码命中率的不确定性。

### SLOT_ITEM_DROP_STATS.csv

`direct_ticket_field_present=False` 表示 Spin payload 中没有直接 Lottery ticket grant 字段，不表示“确认掉落率为 0”。`upgrade_linked_*` 是等级变化后的时序/总账归因。

### REWARD_OUTPUT_STATS.csv

`reward_objects` 是奖励对象数，`quantity_sum` 是可相加道具数量；筹码统一写入 `normalized_chip_*_b0`。拼图完成奖励和即时奖励分行，避免重复。

### PROGRESSION_MODEL.csv

记录免费票阈值、票务来源、消耗、最终库存、升级关联事件和场景边界。`scenario_*` 是描述或公式，不是长期概率模型。

### RETURN_MODEL.csv

`gross_chip_output_over_paid_spin_cost` 缺少付费票价格，只能做本 Session 的描述性对照。`ticket_ledger_balance_check` 必须为 0。

## 脱敏规则

- 不提交真实 Session ID、账号/玩家标识、完整 RPC JSON、绝对本地路径或逐时余额轨迹。
- 筹码只使用 B0 相对值；票数量作为活动机制事实保留。
- SHA-256 用于证明输入版本，不包含 credential。
