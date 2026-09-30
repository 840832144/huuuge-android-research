# TASK-0037 部署实况与接续验收

- 日期：2026-09-30；Actor：Codex；Subagents：none。
- 状态：**云端已部署、可由User进行Web实操；完整V1仍为In Progress**。
- 实际运行代码：`216b298d84598f555d5126dc5465daed9e610657`；原TASK-0031 Accepted及312/312/0不变。

## 授权与实际变更

User已明确批准[部署清单](DEPLOY_APPROVAL_20260930.md)，包含两个无sudo任务身份、受限SSH、本任务systemd、既有IP的HTTPS及证书透明度公开记录；后又明确批准仅该面板地址的本机系统代理例外。没有新增付费资源、云IAM/安全组/防火墙/公网ADB映射，没有重启手机或修改厂商SSH、Google环境、晨会服务。

Linux任务目录为`/srv/huuuge-self-service`，root拥有不可由服务修改的release、venv与工具；`huuuge-workbench`只写本任务data，`huuuge-tunnel`无Shell、无sudo。原匹配ADB密钥复制到任务私有目录0600，原手机绑定不变。运行服务不持有Owner的云API/OAuth凭据。

## 实际保护通道

1. 手机任务目录内OpenSSH客户端向现有Linux SSH22建立加密连接，固定HostKey、仅公钥；只允许反向转发Linux回环15555至手机回环5555。Linux内核监听回读归属独立tunnel身份。Shell通道请求和未批准回环端口转发实测均拒绝。
2. 专用ADB server只监听Linux回环15038，保留已有ADB鉴权、手机序列摘要/包名/版本/ABI/Root核验。该管理通道走SSH，不使用原未加密公网ADB映射。
3. 每片段在手机任务目录生成独立证书/私钥/token；Frida仅手机回环27042，通过本次ADB回环27044转发。证书验证、错误令牌拒绝及正确鉴权实测通过。
4. 正常停止后先flush/封存，再核对PID/start tick/command并停止本次Frida/ADB、移除精确转发、删除本轮密钥/token，之后才释放采集锁并发布ZIP。常驻SSH运输通道保留；它不是仍在采集。

手机Root是现有采集前提；Linux服务虽然无sudo，仍可经匹配ADB访问本台Root手机。这不是平台强制的只读手机身份。面板没有任意命令/目标选择入口，采集不修改游戏数值、不代替User操作游戏。

## 官方工具与实际安装方法

- Linux复用既有官方Platform-Tools及已核验descriptor，Python3.11独立venv安装仓库固定依赖，Frida17.17.0；系统Python保持。
- 手机无需安装Termux应用：从[官方Termux bootstrap发布](https://github.com/termux/termux-packages/releases)获取解包工具，按[官方包仓](https://packages.termux.dev/apt/termux-main/)Packages.gz元数据核验包SHA256，在`/data/local/tmp/task0037/ssh`提取OpenSSH10.5p1及依赖，未执行系统包安装脚本、未覆盖系统SSH。手机实跑`ssh -V`确认OpenSSH10.5p1/OpenSSL3.6.3。
- 复用原官方Frida17.17.0、OpenSSL及配套库到task0037/tools。独立OpenSSL没有原Termux全局配置，因此证书命令显式`-config /dev/null`，继续指定CN/SAN、独立路径和有效期；[官方参数说明](https://docs.openssl.org/3.6/man1/openssl-req/)。
- OpenSSH8.0不接受Match中的ChallengeResponseAuthentication；已删除这个无效指令，保留AuthenticationMethods publickey、PasswordAuthentication no、PermitListen、MaxSessions0等限制。实际`sshd -t`与用户条件配置回读后才reload。

## 常驻与HTTPS

- `huuuge-workbench`：回环18738、非root、MemoryMax256MiB/CPU50%/TasksMax32。
- `huuuge-worker`：非root、MemoryMax2GiB/CPU100%/TasksMax64。
- 两服务enabled/active，NoNewPrivileges和ProtectSystem=strict回读通过；没有本机持续采集进程。空闲5GiB/任务8GiB/单批64MiB或1小时/导出2GiB/手机256MiB保护保持；不自动删除数据。
- 独立Certbot5.8.0先用staging签发，再取得生产IP证书；HTTP01仅增加ACME验证location，原HTTP首页状态与内容回读一致。新增443任务server反代回环面板，证书验证通过，未鉴权API401。
- `huuuge-cert-renew.timer`每12小时检查，含随机错峰；生产配置的`renew --dry-run --run-deploy-hooks`成功，hook先nginx -t再reload。原两个HTTP server_name冲突警告是既有配置，未扩范围清理。
- 面板账号为独立非管理员别名，随机强密码只存User本机受限私有文件；云端仅存哈希，未传明文密码到云助手命令。阿里云/Google账号密码和Cookie未读取或导出。

真实入口、账号、目标、密钥和完整日志仅在受控环境。User本机入口说明为私有`TASK-0037-WEB-ACCESS.md`；不把其内容复制到Git、聊天或截图。

## 本轮真实证据及边界

| 验证 | 实际结果 | 不扩大为 |
| --- | --- | --- |
| TLS生命周期预检 | 目标/版本/descriptor一致，证书与正反令牌验证通过，清理后专用端口0 | 未启动collector，无游戏消息 |
| API真实采集冒烟 | 新批次10捕获/10解码成功/0失败；实际start→collecting→ended/saved，1片段finalized、complete=1、lease=0 | 没有手动游戏操作，不是浏览器UI/完整V1验收 |
| 停止和下载回读 | 清理标记确认、专用ADB/Frida监听0；ZIP实际HTTPS下载、8个文件、10行消息，计数与云端封存一致 | 不以HTTP202或PID存在当成功 |
| 本地AI有限读包 | 4对GetPlayerList、1对GetJackpotValues；无Spin；未在白名单的值正确省略 | 不证明下注/收益/免费转分析，不满足完整C项 |
| 公网HTTPS与鉴权 | 云端及User电脑直连验证证书、登录、安全Cookie、状态、退出通过 | 浏览器渲染未代验 |
| User首次网页尝试 | ERR_CONNECTION_CLOSED；同机系统代理路径复现，直连成功 | 不是云采集失败 |
| 本机网络修正 | User另行批准后，只添加面板地址到系统代理例外；旧列表私有备份、代理开关/服务地址不变；默认网络路径登录/退出复测通过 | 未关闭代理、未改Aurora配置或云网络 |

浏览器工具`getState`失败；按正常reset恢复一次后仍为`nodeRepl.fetch request failed`，已停止浏览器自动化，无未知点击重放。User正接续实际浏览器测试，页面显示、双标签页大于3分钟、新Slots包、轮流使用、异常恢复和无管理会话验收仍待实际证据。

局部验证：216b298在真实Linux环境Runtime8/8；[Linux合成CI](https://github.com/840832144/huuuge-android-research/actions/runs/36690624479)通过。合成CI、上述真实API冒烟、User网页验收分别记录，不互相替代。

## 当前接续与回滚

准入已开启且冒烟批次已正常结束。请User刷新私有说明中的面板，点开始，绿后在官方Web做普通Slots操作并保持双页至少3分钟，然后结束并下载。Codex随后按本批回读计数/完整性/清理和AI包；A—F全部完成后才交完整Review。

维护者回滚时先关闭准入、正常收尾并确认本批释放，再停任务单元；移除本任务443与ACME片段，nginx -t后reload；撤回本任务SSH Match和公钥并检查后reload。保留数据和TASK-0031旧目录，不整体恢复可能被其他任务更新的共享配置。手机监督进程按其PID/start tick确认后停止。系统代理例外只撤回本次添加地址；若原列表已被并发修改，先核对，不能覆盖整表。

飞书同步仍待授权，不阻塞当前测试；两原Draft PR保持，原TASK-0031结果不变。
