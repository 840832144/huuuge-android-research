# Evidence Matrix

本页是技术审计附件。策划正文使用“已确认 / 本次样本观察 / 待验证 / 策划建议”，这里保留完整 Claim 与 L0–L4。

## 引用清单

| Citation ID | 来源 | 范围 | 等级 |
| --- | --- | --- | --- |
| HGR-20260827-RUN-001 | Finalized manifest、markers、inventory、field paths | 样本完整性 | L3 |
| HGR-20260827-RUN-002 | 346 对抽奖请求/响应 | 消耗、累计补回、即时奖励、拼图完成 | L3 |
| HGR-20260827-RUN-003 | 票余额状态与来源总账 | 购买、补回、直接奖励、升级关联残差 | L3 |
| HGR-20260827-RUN-004 | 588 次普通下注、45 次 Free Spin 与成长事件 | 下注档、筹码消耗、直接票字段缺失 | L3 |
| HGR-20260827-RUN-005 | 奖励对象与结果回看 | 奖励分类、去重与筹码换算 | L3 |
| HGR-20260827-RUN-006 | 4 组两阶段购买链路 | 金额、币种、票色、票数、忠诚度、成功状态 | L3 |
| HGR-20260827-CFG-001 | 73 个 Lottery 配置事件 | 阈值、批量上限、奖励池形状、倍率 | L2 |
| HGR-20260827-SCH-001 | Protobuf descriptor | endpoint 与字段语义 | L1 |
| HGR-20260827-MAN-001 | User 现场确认 | 四次真实货币购买由 User 执行；部分道具与升级相关 | L0 |

## 关键 Claim

| Claim | 类型 | 等级 | 引用 | 限制 |
| --- | --- | --- | --- | --- |
| 样本正常 Finalize，8712/8712 解码 | Confirmed | L3 | RUN-001 | 单版本、单账号 |
| 346 次抽奖、消耗 933 张票 | Confirmed | L3 | RUN-002 | 单次实玩 |
| 每累计消耗 7 张补回 1 Bronze | Confirmed | L3 | RUN-002、CFG-001 | 只确认当前版本/配置 |
| 四笔购买全部成功，合计 54.43 SGD | Confirmed | L3 | RUN-006、MAN-001 | 只代表本次 User 操作 |
| 四笔购买发放 763 张票与 235 忠诚度 | Confirmed | L3 | RUN-006、RUN-003 | 每个礼包均含其他奖励 |
| 表观每票成本 | Estimate | L3 | RUN-006 | 未扣除忠诚度价值，不是纯票价 |
| 抽奖直接奖励 60 张票 | Confirmed | L3 | RUN-002、RUN-003 | 直接来源，不做最终付费归因 |
| 普通下注结果不含直接票字段 | Confirmed | L3 | RUN-004、SCH-001 | 不代表所有未来版本永远没有 |
| 六次升级后出现合计 16 张 Bronze | Confirmed | L3 | RUN-003、RUN-004 | 确认余额变化，不等于确认发放动作 |
| 16 张票由升级奖励发放 | Estimate | L3 | RUN-003、RUN-004、MAN-001 | 缺逐次 UI 弹窗或显式奖励字段 |
| 更高下注提高升级票效率 | Hypothesis | L0 | RUN-004 | 下注、等级区间与时长混杂 |
| 5 次拼图完成及其筹码输出 | Confirmed | L3 | RUN-002、RUN-005 | 起始板面未知，Gold 单次大奖主导 |
| 奖励池变体数量 | Confirmed | L2 | CFG-001 | 没有权重，不能当概率 |
| 筹码奖励输出 ÷ 普通下注筹码消耗（不含充值）= 117.516 | Estimate | L3 | RUN-004、RUN-005 | 仅技术对照；不是 RTP、ROI 或付费回收率 |
| 调整阈值、升级节点和拼图目标 | Decision proposal | L0 | CR 建议 | 必须另行实验与评审 |

## 购买链路脱敏规则

购买关联在本机使用 request、product、store 与订单标识完成。版本化事实层只保留：

- `Purchase-1...4`；
- 成功状态；
- `local_price` 与 `local_currency_code`；
- 匿名票色与票数；
- 忠诚度与其他奖励类型；
- 表观每票成本和限制。

任何关联标识均未写入 Git、飞书或本页。

## 完整性判断

Lottery 为 `L3 Runtime Observed`，因为已有主抽奖和购买链路闭环。尚不满足 L4：升级奖励缺少逐次 UI 对照，拼图不是完整空板周期，也没有第二账号/版本复验。
