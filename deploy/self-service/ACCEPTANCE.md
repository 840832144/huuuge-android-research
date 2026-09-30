# TASK-0037 V1 验收记录

- Date: 2026-09-30；Actor: Codex；Subagents: none。
- Status: In Progress。A—F全部未完成，尚不交完整Review。
- 关联：TASK-0031 Accepted，原312/312/0、8条Slots响应不变；不作为V1新增数据。

## User成员账号实测（2026-09-30范围调整时反馈）

User确认已创建成员账号并绑定现有云手机，官方Web登录成功，进入Android桌面及Huuuge大厅。结果：**User成员账号实测通过**。本记录由Codex依据User反馈登记，未读取其账号密码、验证码或Cookie；不是同事盲测、Android客户端、Codex独立复测或V1采集验收。

当前范围是官方Web游戏＋独立采集小面板，分别登录、约定轮流。SDK内嵌/统一登录/强制防重连/旧凭证撤销/控制交接不再验收；保留采集防重、基本鉴权和批次/下载归属。以下旧SDK调查事实保留，但不作为当前阻塞。

## 前序真实外部检查（历史，不代表当前登录态）

| 检查 | 结果 | 边界 |
| --- | --- | --- |
| 官方API读取原单台手机 | RUNNING，Android12，StreamMode1 | 同一既有目标，无新资源 |
| 终端用户 | 官方eds-user DescribeUsers返回1个用户 | 不公开身份；CLI内置metadata缺少API，用官方`--force --version 2021-03-08`正常调用，不绕过IAM或工具审批 |
| SDK登录能力 | BatchGetAcpConnectionTicket=Finished；官方Web SDK回调onConnected | 输入关闭，网页提示视频自动播放被阻止；不是本轮正常游戏验收 |
| 官方断连 | DisconnectAndroidInstance返回成功，页面出现2027 | 仅证明管理侧断开 |
| 旧Ticket重连 | 断开后原Ticket曾重新出现onConnected；换发后凭证内容确实变化，后续原Ticket出现2507 | 2507是网关错误，不能记为旧凭证已撤销；原控制隔离未证实；当前已取消该项验收 |
| SDK收尾 | 关闭测试页和本次回环测试server，最后API回读SessionStatus=disconnect、手机RUNNING | 未输入游戏操作、未启动Frida/采集、无新游戏消息 |
| 私网ADB | Linux对该手机已知私网5555做一次TCP连接检查，TimeoutError | 未连接公网ADB、未改路由/SG/防火墙 |
| 常驻身份 | DescribeInstanceRamRole返回本实例无已挂载RAM角色 | 不代表账号中不存在可授权身份；尚未新增权限 |
| 现安全策略 | 剪贴板/文件/摄像头/本地盘当前允许 | 未修改；面板不代理这些能力，官方成员权限未因本轮扩大 |
| HTTPS候选 | nginx active、2份配置含证书引用；证书元数据命令未成功 | 尚未确认可用origin或证书，不冒称已可发布 |

CLI有两次DNS超时：ECS只读命令以原ClientToken重试后成功，无重复命令；EDS断连在确认DNS失败后重试。敏感返回保留受控任务目录，Git仅存上述最少结论。

## 本地合成检查（不计云端验收）

- 范围调整后实跑：`test_self_service.py` **17/17通过**；覆盖无SDK/Ticket入口、正常结束不调用厂商凭证接口、清理失败保留采集锁、归属下载和未实现云接入拒绝启动。
- Linux合成CI：[run36682709050](https://github.com/840832144/huuuge-android-research/actions/runs/36682709050) / 源码1c9c364；controller21、descriptor4、panel17，**42/42通过，无跳过**。不是既有云手机/云Linux部署或真实新增数据验收。
- `test_cloud_capture.py` **21项中16通过、5项Linux专属跳过**；JS面板/探针语法检查通过。均为Windows本机局部结果，不是新云端实测。
- `tests/test_self_service.py`：登录/CSRF/限流/到期、并发租约、第二身份与标签页拒绝、desired-state先关闭、越权下载、旧页面迟到请求、刷新宽限、心跳/真实数据绿色门槛、恢复新片段、采集清理不明保持采集锁、停止/下载重试、ZIP计数/配对/大整数/脱敏。
- 原controller/decoder回归：保留TLS/真实地址/目标绑定、原retry-start边界和失败数据；新增手机心跳不增加RPC的测试。
- Windows上Linux锁、POSIX信号/TLS权限和完整Linux supervisor检查需单列跳过；不把本机通过写成云端通过。
- JS语法检查通过；实际小面板浏览器交互及完整A—F仍待验。
- 初次导出测试发现Windows只读文件句柄fsync失败，改为读写句柄后通过；心跳测试发现console局部`state`变量遮蔽状态字典，最小改名后通过。

## 全阶段真实验收

| 项 | 必须取得的证据 | 当前结果 |
| --- | --- | --- |
| A | 同事仅浏览器使用官方Web成员登录＋独立小面板 | User本人官方Web入口通过；同事盲测及面板全流程未验证 |
| B | 本轮真实消息、四态/时长/计数/刷新及错误显示 | 未验证；V1真实捕获/成功/失败均无可报告批次 |
| C | 新包下载/复下，现有本地AI读包回答实际游戏问题并定位证据 | 未验证；合成样例不代替真人读包 |
| D | 两个面板身份按约定轮流各一轮；单采集任务防重复，停止/下载归属 | 合成覆盖防重复及权限；真实未验证。不验收手机防重连/旧凭证撤销/控制交接 |
| E | 刷新/断线/worker停止/游戏退出/恢复及导出下载重试 | 合成覆盖部分；真实未验证 |
| F | 无Codex管理会话仍可新采，定向重启任务服务并恢复 | 未部署；真实未验证 |

## 当前下一步

完成受保护采集连接与云常驻适配、TLS轮换/清理和容量保护，核定面板HTTPS及实际必要身份。需要费用、网络/IAM、公开入口或共享服务改动时先提交具体变更/影响/回滚；不等厂家撤销工单。真实A—F仍待执行，原TASK-0031结果不重算。

## 2026-09-30 Runtime阶段（未部署）

- 代码：CaptureRuntime、明确SSH管理通道＋Frida TLS、片段密钥/令牌生成清理、进程PID/start tick/command归属、运行容量与时长、后台页受鉴权SSE、停止准备期取消、清理后才发布下载。
- 本地证据：panel21通过、Runtime7通过/1Linux跳过、controller16通过/5Linux跳过、descriptor4通过；合计48通过/6跳过，JS语法通过。均为合成/本地边界；失败的首次Runtime fixture缺授权/版本字段已改为显式synthetic，未放松产品配置校验。专用测试venv最初缺protobuf，已在该venv安装原cloud requirements后回归通过。
- 只读环境：OpenSSH8.0/PermitListen、任务端口空闲、Linux32.8GB；SG已有22/80/443，nginx有效配置无TLS且无443监听，纠正旧误判。手机原官方Frida工具存在，旧错误简写路径“absent”不作为未安装证据。
- 尚未验证：官方手机SSH客户端及实际受限隧道、TLS本轮真实生命周期、systemd常驻、可信HTTPS/续期、双标签页超过3分钟、新真实分析包、本地AI、轮流/异常/退出Codex后新批次。A—F不勾选；无V1新计数。
- 需User确认：DEPLOY_APPROVAL_20260930.md的最小身份、SSH/HTTPS及本任务服务变更；完整影响、停止条件及回滚已写明。未实际修改共享服务、网络/IAM或晨会；飞书待授权不阻塞。Subagents: none。

Linux合成CI [run36686925269](https://github.com/840832144/huuuge-android-research/actions/runs/36686925269) 在业务代码5ef40531a2c8e268dce6e98b8fbd158f9f9a1b94通过：controller21＋descriptor4＋panel21＋Runtime8，共54/54、无跳过。包含真实Linux本地进程/回环socket的合成边界测试；不是目标云手机或V1验收。
