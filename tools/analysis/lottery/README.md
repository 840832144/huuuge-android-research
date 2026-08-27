# Lottery 报告事实提取器

这是 TASK-0018 的最小专用分析工具。它只读取一个已经 Finalize 的本机 Session，把 Lottery、Slots、进度和奖励证据转换为脱敏聚合 CSV；不会修改 Collector，也不会复制 Raw、完整 JSON、账号标识或真实 Session ID。

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

输出只使用匿名 Session/实例/账号别名。筹码统一换算成 `B0`：本轮最小已观察付费 Spin Bet。这样可以比较投入与输出，同时避免提交完整余额轨迹。

## 关键口径

- `LotteryToss` 请求与响应按顺序配对，并核对颜色和数量；
- Free Ticket 以 `ticket_collected[]` 计数，并用初始进度、阈值、总 Ticket 使用量和最终进度复核；
- Ticket 账本按“初始 + 购买 + Free threshold + Lottery 奖励 + upgrade-linked − 使用 = 最终”复核；
- `upgrade-linked` 是 `UpdateProgress.level` 后绝对 Ticket 状态增量的时序归因；没有显式 Ticket grant 字段，因此保持 `Estimate`；
- Spin 响应没有直接 Lottery Ticket 字段，因此不输出伪造的“每 Spin 掉落概率”；
- `MissedInfoRead` 是批量 Toss 结果回读，会重复即时奖励并补充已在 Lottery state 中出现的 Board completion 奖励，不重复计入输出。

## 测试

```powershell
python -m unittest discover -s .\tools\analysis\lottery\tests -p "test_*.py"
```
