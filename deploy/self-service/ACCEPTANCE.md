# TASK-0037 V1 验收记录

- Date: 2026-09-30；Actor: Codex；Subagents: none。
- Status: In Progress。云部署和真实API冒烟已通过；A—F完整网页/同事/异常验收尚未完成，尚不交完整Review。
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
| A | 同事仅浏览器使用官方Web成员登录＋独立小面板 | User本人官方Web＋面板登录/完整短流程通过；独立同事盲测未验证 |
| B | 本轮真实消息、四态/时长/计数/刷新及错误显示 | User报告短Web流程完成并下载370/370/0；API恢复实际error→start→collecting且缺口保留。User取消追加三分钟测试，长时后台稳定性/浏览器错误渲染未代验 |
| C | 新包下载/复下，现有本地AI读包回答实际游戏问题并定位证据 | User新370条ZIP已下载/云端核对/API同身份复下完全一致；本地AI完成25对Spin、2对FreeSpin及字段问题、序号证据 |
| D | 两个面板身份按约定轮流各一轮；单采集任务防重复，停止/下载归属 | 两身份顺序新采；真实API重复开始409、越权停止/下载404。人员为User及Codex技术验证，不扩大为两位独立策划或手机控制锁 |
| E | 刷新/断线/worker停止/游戏退出/恢复及导出下载重试 | 真实worker中断恢复/新片段/缺口/收尾通过；API过期页claim及旧页409通过；真实浏览器断线、下载错误重试等未验 |
| F | 无Codex管理会话仍可新采，定向重启任务服务并恢复 | 两单元enabled/active；定向worker故障自动恢复通过；无本地采集进程，退出Codex后再新采仍待User实测 |

## 当前下一步

User本人短Web闭环和本地AI已通过；按User决定不再要求追加三分钟。独立同事使用、实际浏览器断线/下载异常及退出Codex后新轮等剩余，完成A—F才完整Review。部署/原TASK-0031边界保持。

## 2026-09-30 Runtime阶段（未部署）

- 代码：CaptureRuntime、明确SSH管理通道＋Frida TLS、片段密钥/令牌生成清理、进程PID/start tick/command归属、运行容量与时长、后台页受鉴权SSE、停止准备期取消、清理后才发布下载。
- 本地证据：panel21通过、Runtime7通过/1Linux跳过、controller16通过/5Linux跳过、descriptor4通过；合计48通过/6跳过，JS语法通过。均为合成/本地边界；失败的首次Runtime fixture缺授权/版本字段已改为显式synthetic，未放松产品配置校验。专用测试venv最初缺protobuf，已在该venv安装原cloud requirements后回归通过。
- 只读环境：OpenSSH8.0/PermitListen、任务端口空闲、Linux32.8GB；SG已有22/80/443，nginx有效配置无TLS且无443监听，纠正旧误判。手机原官方Frida工具存在，旧错误简写路径“absent”不作为未安装证据。
- 尚未验证：官方手机SSH客户端及实际受限隧道、TLS本轮真实生命周期、systemd常驻、可信HTTPS/续期、双标签页超过3分钟、新真实分析包、本地AI、轮流/异常/退出Codex后新批次。A—F不勾选；无V1新计数。
- 需User确认：DEPLOY_APPROVAL_20260930.md的最小身份、SSH/HTTPS及本任务服务变更；完整影响、停止条件及回滚已写明。未实际修改共享服务、网络/IAM或晨会；飞书待授权不阻塞。Subagents: none。

Linux合成CI [run36686925269](https://github.com/840832144/huuuge-android-research/actions/runs/36686925269) 在业务代码5ef40531a2c8e268dce6e98b8fbd158f9f9a1b94通过：controller21＋descriptor4＋panel21＋Runtime8，共54/54、无跳过。包含真实Linux本地进程/回环socket的合成边界测试；不是目标云手机或V1验收。

## 2026-09-30 已部署与真实API冒烟

Status: **In Progress / 云端已部署，完整V1待实操验收**。User已批准原具体部署清单及IP证书透明度记录，实际运行代码216b298。两个无sudo身份、限定回环SSH管理通道、独立Python与任务常驻服务、可信HTTPS及续期已上线。每片段TLS准备、错误token拒绝、准确目标与清理通过；原TASK-0031 Accepted/312/312/0保持，不新建Task。

本轮API真实冒烟：**10捕获/10解码成功/0失败**，1段finalized，正常停止/保存后complete=1、lease=0，下载8文件ZIP并回读10行消息；专用Frida/ADB和转发已清理，常驻加密隧道保留。没有操作游戏；本地AI仅确认4对GetPlayerList、1对GetJackpotValues，无Spin，不能替代User Slots/含值分析验收。

User首次网页报ERR_CONNECTION_CLOSED。同机系统代理路径复现，直连HTTPS及登录正常；User另行批准后只添加面板地址的系统代理例外，默认网络路径复测通过，其他代理设置不变。浏览器工具reset后仍nodeRepl.fetch request failed，已停止自动化，不冒称网页渲染通过。当前下一步：User刷新私有入口，双标签页普通Slots至少3分钟、结束下载；随后回读其新批次并完成轮流/异常/无管理会话A—F。仍不交完整Review。

完整部署方法、影响、证据与回滚见[部署实况](DEPLOY_RESULT_20260930.md)。入口/密码/真实目标/原始数据只留私有环境。Linux运行资源上限与容量保护生效，无新增费用/IAM/SG/防火墙/公网ADB映射，无重启/清数据或晨会变更。飞书待授权不阻塞，Subagents: none。

## 本轮User验收与技术恢复（取代上文待User实操状态）

Status: **In Progress / 已可Web使用，User本轮闭环通过**。User确认“流程完成，已保存并下载”，提交的新包与云端同批及再次HTTPS下载一致：**370捕获/370解码成功/0失败**，约91秒，1段finalized、无记录缺口、complete=1、lease=0。含25对Spin和2对FreeSpin；本地AI已从新包回答下注字段、免费转及Jackpot标记问题并提供片段/序号，未计算未经证实的RTP/净收益。

User明确本次就验收这一时长，不再追加三分钟测试。规格已同步为本次约91秒短流程验收；较长后台稳定性未测，代码中原3分钟断线宽限不变。不是同事盲测或Android客户端结果。

独立短API恢复检查：两非管理员面板身份顺序新采，重复开始409、越权停止/下载404、错误页面停止409；任务worker被定向中断后systemd恢复并开新片段，旧缺口保留；过期采集页11秒后可claim，旧页停止409。该测试新批次14/14/0、两片段，明确incomplete/error且可下载，正常收尾后锁释放；未伪装为完整。最后回读当前采集0、专用ADB/Frida监听0，云端任务服务及限定SSH隧道保持运行。

实际代码216b298，已批准部署与入口说明见[部署实况](DEPLOY_RESULT_20260930.md)，最少结果见[脱敏回执](RESULT_USER_20260930.json)。原TASK-0031 Accepted及312/312/0不变，10/10/0的早期API冒烟也与User370条分开。代理例外仅User批准的面板地址，默认网络及User网页均通过；浏览器工具错误后保持停止，没有代验UI。

完整V1剩余：独立同事使用、实际浏览器短断线/下载异常重试、退出Codex管理会话后的新轮等，按原A—F单列。未要求User再做三分钟测试，未标完整Review/Done；原Draft PR继续。飞书待授权不阻塞。Subagents: none。
