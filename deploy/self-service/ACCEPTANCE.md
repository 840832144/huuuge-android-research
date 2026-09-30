# TASK-0037 V1 验收记录

- Date: 2026-09-30；Actor: Codex；Subagents: none。
- Status: In Progress。A—F全部未完成，尚不交完整Review。
- 关联：TASK-0031 Accepted，原312/312/0、8条Slots响应不变；不作为V1新增数据。

## 本轮真实外部检查

| 检查 | 结果 | 边界 |
| --- | --- | --- |
| 官方API读取原单台手机 | RUNNING，Android12，StreamMode1 | 同一既有目标，无新资源 |
| 终端用户 | 官方eds-user DescribeUsers返回1个用户 | 不公开身份；CLI内置metadata缺少API，用官方`--force --version 2021-03-08`正常调用，不绕过IAM或工具审批 |
| SDK登录能力 | BatchGetAcpConnectionTicket=Finished；官方Web SDK回调onConnected | 输入关闭，网页提示视频自动播放被阻止；不是本轮正常游戏验收 |
| 官方断连 | DisconnectAndroidInstance返回成功，页面出现2027 | 仅证明管理侧断开 |
| 旧Ticket重连 | 断开后原Ticket曾重新出现onConnected；换发后凭证内容确实变化，后续原Ticket出现2507 | 2507是网关错误，不能记为旧凭证已撤销；隔离门槛未通过 |
| SDK收尾 | 关闭测试页和本次回环测试server，最后API回读SessionStatus=disconnect、手机RUNNING | 未输入游戏操作、未启动Frida/采集、无新游戏消息 |
| 私网ADB | Linux对该手机已知私网5555做一次TCP连接检查，TimeoutError | 未连接公网ADB、未改路由/SG/防火墙 |
| 常驻身份 | DescribeInstanceRamRole返回本实例无已挂载RAM角色 | 不代表账号中不存在可授权身份；尚未新增权限 |
| 现安全策略 | 剪贴板/文件/摄像头/本地盘当前允许 | 未修改，不能向普通工作台用户开放 |
| HTTPS候选 | nginx active、2份配置含证书引用；证书元数据命令未成功 | 尚未确认可用origin或证书，不冒称已可发布 |

CLI有两次DNS超时：ECS只读命令以原ClientToken重试后成功，无重复命令；EDS断连在确认DNS失败后重试。敏感返回保留受控任务目录，Git仅存上述最少结论。

## 本地合成检查（不计云端验收）

- `tests/test_self_service.py`：登录/CSRF/限流/到期、并发租约、第二身份与标签页拒绝、desired-state先关闭、越权下载、旧页面迟到请求、刷新宽限、心跳/真实数据绿色门槛、恢复新片段、撤销不明保持占用、停止/下载重试、ZIP计数/配对/大整数/脱敏。
- 原controller/decoder回归：保留TLS/真实地址/目标绑定、原retry-start边界和失败数据；新增手机心跳不增加RPC的测试。
- Windows上Linux锁、POSIX信号/TLS权限和完整Linux supervisor检查需单列跳过；不把本机通过写成云端通过。
- JS语法检查通过；实际工作台浏览器交互、SDK生产策略及完整A—F仍待验。
- 初次导出测试发现Windows只读文件句柄fsync失败，改为读写句柄后通过；心跳测试发现console局部`state`变量遮蔽状态字典，最小改名后通过。

## 全阶段真实验收

| 项 | 必须取得的证据 | 当前结果 |
| --- | --- | --- |
| A | 未参与开发策划从一台无采集工具的电脑简单登录、看到可玩画面 | 未验证 |
| B | 本轮真实消息、四态/时长/计数/刷新及错误显示 | 未验证；V1真实捕获/成功/失败均无可报告批次 |
| C | 新包下载/复下，现有本地AI读包回答实际游戏问题并定位证据 | 未验证；合成样例不代替真人读包 |
| D | 两真实身份各一轮，重叠/越权/旧凭证攻击均拒绝 | 未验证；厂商撤销当前是阻塞 |
| E | 刷新/断线/worker停止/游戏退出/恢复及导出下载重试 | 合成覆盖部分；真实未验证 |
| F | 无Codex管理会话仍可新采，定向重启任务服务并恢复 | 未部署；真实未验证 |

## 下一门槛

先由Owner确认是否提交已准备的厂商咨询；在现有实例上落实可验证的凭证撤销与应用控制。取得适用方法后再提交精确云身份/受保护通道/HTTPS与独立策略变更审批并实施，不购买、不改共享服务来碰运气。
