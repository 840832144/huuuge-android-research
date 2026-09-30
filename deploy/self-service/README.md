# TASK-0037 官方Web＋独立采集小面板

## 当前状态

**In Progress：云端常驻、受限SSH＋Frida TLS、HTTPS面板已部署；API真实冒烟10/10/0正常结束并下载，完整V1等待User网页实操。** 详见[部署实况](DEPLOY_RESULT_20260930.md)。

User成员账号已绑定现有云手机，在官方Web成功登录到Android桌面/Huuuge大厅；仅本人反馈，非同事盲测/Android客户端/V1采集验收。TASK-0031 Accepted与原312/312/0、8条Slots响应保留，不算V1新数据。

官方Web负责游戏画面和输入；独立面板负责采集，允许分别登录。可信同事约定轮流，本版不要求SDK内嵌、统一登录、防重连、旧Ticket撤销或强制手机控制交接。**采集锁仅防重复采集，不是手机控制锁。** 厂商咨询已退出本版前置，草稿仅作历史。

## 保留与当前实现

原准备代码完整保留在9b6b21d，沿用登录、SQLite状态、面板、片段编排、封存、下载和AI导出。原collector只补手机心跳，不重写内核。

| 内容 | 位置与当前边界 |
| --- | --- |
| 独立面板/鉴权/采集锁 | self_service/app.py、store.py、templates、static；无iframe/SDK/Ticket接口 |
| 采集编排 | worker.py、collector.py；每片段调用原cloud_capture.py，不调用厂商issue/revoke/disconnect |
| 受保护云运行接入 | capture_runtime.py受限SSH＋Frida TLS已部署；每批仍核验目标与连接，不能用admission=true绕过 |
| 历史SDK调查 | vendor.py保留但服务入口不加载；不用其撤销结果控制采集锁 |
| 含值AI包 | export.py、README_FOR_AI.md；字段白名单、计数/关联/精度、归属下载不变 |
| 云服务 | 两个独立systemd单元已enabled/active，面板只监听回环，由任务HTTPS入口反代 |

原SQLite兼容字段control_generation/ticket/control_revoked和索引名one_phone保留以避免破坏既有准备数据；其不参与当前手机授权。lease当前含义只为单采集任务锁。真实身份、地址、匹配密钥、descriptor、原始数据与运行日志留受控环境，不进Git。

## 当前部署与审批边界

User已批准原DEPLOY_APPROVAL清单，按受限SSH＋每片段Frida TLS部署，保留ADB鉴权/手机目标及版本检查。非root服务不持有Owner的云管理凭据；原手机Root通道仍是采集能力前提。真实入口、面板凭据、目标、密钥只保存在受控环境。

可信HTTPS及Certbot续期dry-run/hook已通过；原HTTP页回读不变。User本机Aurora代理曾关闭面板连接，另行批准只加入该地址的系统代理例外后，默认网络登录/退出复测通过。浏览器工具恢复一次仍失败，停止自动化；实际双标签页由User完成。

新费用、网络/IAM/安全组/防火墙、其他公开入口/共享服务或重启清数据仍按原审批边界。无新增付费资源，不扩大本轮已批准清单，飞书待授权不阻塞。

## 部署与维护流程（本次实施见实况记录）

1. 复用既有Linux，在任务独立目录部署已提交release和隔离Python3.11环境；data为0700、SQLite/凭据0600，不替换系统Python/全局ADB或旧任务目录。
2. 安装本目录requirements及deploy/cloud/requirements.txt。当前入口不需要Web SDK及其Python身份依赖；历史vendor.py依赖仅留注释。
3. 实现并验证受保护CaptureRuntime，准确核对手机、Huuuge版本/ABI/descriptor；每批自动准备Frida TLS，保留证书校验/鉴权；只使用任务专用回环端口。
4. 填写私有workbench配置；无需官方Web密码、Cookie或Ticket。部署先admission=false，真实TLS/清理检查通过后开放。面板别名非管理员，首次随机强密码私有交付且仅哈希进入云端；后续可用既有admin命令受控交互配置，不写明文到命令行/聊天/Git。
5. 经具体部署审批后安装任务独立服务与HTTPS路由。只启动本任务服务；共享nginx变更先nginx -t再精确reload，回滚只移除本任务片段并恢复备份，不影响晨会。
6. 完成云运行检查后开放准入，执行ACCEPTANCE.md的完整A—F真实验收再Review。

## 行为与维护

- 四态固定：开始灰、采集中绿、错误红、结束红；正常结束显示停止图标与“已保存”。准备/停止/打包有明确进度，不冒充已采集。
- 面板默认2秒刷新，10秒无可信更新撤销绿色。绿需本批Hook、真实新增成功解码及手机心跳；暂无RPC但心跳健康可等待，不能凭PID/连接变绿。
- 面板默认3分钟断线宽限，同一操作者旧页面10秒无心跳后可恢复原批次；只交接面板采集操作，不处理官方Web手机连接。
- 最多3次片段启动；故障留下缺口及不可覆盖片段，不以retry-start续写已有结果。结束先关闭desired-state，防止游戏仍开着导致重启采集。
- Stop/flush/回读及本次采集清理确认后释放采集锁；未知就保留采集锁与数据。打包可重试、历史可复下；不会断开官方Web或登出游戏。
- 数据默认不自动删除；空闲5GiB、任务8GiB、单轮64MiB/1小时、导出2GiB运行保护已实现，手机空闲256MiB前置检查。新保留/清理策略另行明示确认，旧312证据排除在本任务清理外。

维护者关闭准入后正常停止当前批次，确认本次进程/转发清理，再停止两个任务单元；升级保留SQLite和数据，只切换本任务release。失败保持红色和数据，不清空目录，不重启主机/手机/晨会，不重做Google环境。

## 策划使用（已开放，完整流程待User实测）

与同事约定轮流 → 官方Web成员登录，进入Huuuge大厅 → 另开采集小面板登录 → 点“开始采集” → 绿后在官方Web普通操作 → 面板点“结束并下载” → 红色“已保存”后取得ZIP。

请保持面板开启；临时断网可在宽限内恢复。下载被浏览器拦截时点“下载本次数据”，以后可在“我的采集”复下。解压后把README_FOR_AI交给已有AI，按团队允许外发范围分析。面板结束不关闭游戏；下一位仍靠同事约定接续使用。

### 本轮实现补充

受鉴权POST SSE维持当前采集页连接，每帧复核登录和归属，减少后台标签页JS计时器限频带来的假超时；实际浏览器冻结/断流/双标签页仍须部署后测。SSE最多一个活动采集页连接，nginx关闭代理缓冲。密钥与真实目标只填写私有workbench.runtime，模板默认不可启动。

已按User明确批准修改本任务SSH/HTTPS及任务单元，实测证据见DEPLOY_RESULT_20260930.md。工具拒绝仍按正常流程处理；完整A—F未完成，不把后端实测当作浏览器渲染/同事使用通过。
