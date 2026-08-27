# Lottery 报告事实提取器

这是 TASK-0018 的最小专用分析工具。它只读取一个已经 Finalize 的本机 Session，把 Lottery、Slots、购买、进度和奖励证据转换为脱敏聚合 CSV；不会修改 Collector，也不会复制 Raw、完整 JSON、账号标识、购买关联标识或真实 Session ID。

## 输入要求

- `manifest.status = stopped`；
- lifecycle marker 包含 `collector-start`、`hooks-installed`、`collector-ready`、`collector-stop`；
- `index.csv`、Raw、Decoded JSON 和 manifest 计数一致；
- 已生成 `rpc_inventory.csv` 与 `field_paths.csv`。

## 使用

```powershell
python .\tools\analysis\lottery\extract_lottery_facts.py `
  --session-dir <本机Session目录> `
  --analysis-dir <本机Finalize结果目录> `
  --output-dir .\reports\lottery\20260827_lottery-ticket-puzzle `
  --session-alias LOT-20260827-A
```

输出只使用匿名 Session/实例/账号别名。普通 Spin 表示筹码下注，不表示真实货币付费。筹码统一换算成 `B0`：本轮观察到的最低普通下注；策划正文显示为“最低下注单位”。

## 关键口径

- `LotteryToss` 请求与响应按顺序配对，并核对颜色和数量；
- `MakeInAppPurchase` 按预览、初始化响应、带价格的结算请求和奖励响应配对；request/product/store/订单标识只在内存中关联，输出仅保留 `Purchase-N`、金额、币种、票色、票数和附加奖励；
- 每档购买都包含忠诚度，因此 `apparent_cost_per_ticket` 只是礼包总价除以票数，不是纯票价；
- Free Ticket 以 `ticket_collected[]` 计数，并用初始进度、阈值、总 Ticket 使用量和最终进度复核；
- Ticket 账本按“初始 + 购买 + Free threshold + Lottery 奖励 + upgrade-linked − 使用 = 最终”复核；
- `upgrade-linked` 是 `UpdateProgress.level` 后绝对 Ticket 状态增量的时序归因；没有显式 Ticket 发放字段，因此保持 `Estimate`；
- Spin 响应没有直接 Lottery Ticket 字段，因此不输出伪造的“每 Spin 掉落概率”；
- `MissedInfoRead` 是批量 Toss 结果回读，会重复即时奖励并补充已在 Lottery state 中出现的 Board completion 奖励，不重复计入输出。

## 测试

```powershell
python -m unittest discover -s .\tools\analysis\lottery\tests -p "test_*.py"
```

回归测试覆盖购买价格/币种/票色/票数/附加奖励提取、标识移除、不完整购买链路 fail-closed、普通下注命名、奖励分类和统计辅助函数。
