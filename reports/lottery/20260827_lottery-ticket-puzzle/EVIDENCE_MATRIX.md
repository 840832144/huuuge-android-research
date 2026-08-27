# Evidence Matrix

## 引用清单

| Citation ID | 来源 | 范围 | 等级 |
| --- | --- | --- | --- |
| HGR-20260827-RUN-001 | Finalized manifest、markers、inventory、field paths | Session 完整性与样本量 | L3 |
| HGR-20260827-RUN-002 | 346 对 LotteryToss 请求/响应 | 消耗、免费进度、即时奖励、拼图完成 | L3 |
| HGR-20260827-RUN-003 | 票余额状态与来源总账 | 购买、返还、直接奖励、升级关联残差 | L3 |
| HGR-20260827-RUN-004 | 588 Spin、45 FreeSpin 与成长事件 | Bet 档、Spin 成本、直接票字段缺失 | L3 |
| HGR-20260827-RUN-005 | 奖励对象与结果回读 | 奖励分类、去重与 B0 输出 | L3 |
| HGR-20260827-CFG-001 | 73 个 Lottery 配置事件 | 阈值、批量上限、奖励池形状、multiplier | L2 |
| HGR-20260827-SCH-001 | Protobuf descriptor | endpoint 与字段语义 | L1 |
| HGR-20260827-MAN-001 | 用户现场说明 | 部分 Lottery 道具与升级相关 | L0 |

## 关键 Claim

| Claim | 类型 | 等级 | 引用 | 限制 |
| --- | --- | --- | --- | --- |
| Session 正常 Finalize，8712/8712 解码 | Confirmed | L3 | RUN-001 | 单版本、单账号 |
| 346 次 Toss、消耗 933 张票 | Confirmed | L3 | RUN-002 | 单 Session |
| 四类票与对应消耗量 | Confirmed | L3 | RUN-002、CFG-001 | 只覆盖本次可见票色 |
| 每累计消耗 7 张返 1 Bronze | Confirmed | L3 | RUN-002、CFG-001 | 只确认当前版本/配置 |
| 直接 Lottery 奖励给出 60 张票 | Confirmed | L3 | RUN-002、RUN-003 | 即时来源，不做最终付费归因 |
| SpinResponse 不含直接票 grant | Confirmed | L3 | RUN-004、SCH-001 | 不等于所有未来版本永远没有 |
| 六次升级后出现合计 16 张 Bronze | Confirmed | L3 | RUN-003、RUN-004 | 确认余额变化，不等于确认 grant endpoint |
| 16 张票归因于升级奖励 | Estimate | L3 | RUN-003、RUN-004、MAN-001 | 缺 UI 或显式 reward payload |
| 更高 Bet 提高升级票效率 | Hypothesis | L0 | RUN-004 | Bet、等级区间与时长混杂 |
| 5 次拼图完成及其筹码输出 | Confirmed | L3 | RUN-002、RUN-005 | 初始板面未知，Gold 单次大额主导 |
| 奖励池 variant 数量 | Confirmed | L2 | CFG-001 | 没有权重，不能当概率 |
| 117.516 倍输出/Spin 成本 | Estimate | L3 | RUN-004、RUN-005 | 不含付费票价格，不是 RTP/EV |
| 调整阈值、升级节点和拼图目标 | Decision proposal | L0 | 本报告 CR | 必须另行实验与评审 |

## 完整性判断

Lottery 从原 `L2 Configured / Visible` 提升为 `L3 Runtime Observed`，因为已有 primary LotteryToss 闭环。尚不满足 L4：缺 Runtime、UI、Manual 与 Schema/Config 的完整多源验证，尤其升级奖励来源和完整活动周期仍未闭环。
