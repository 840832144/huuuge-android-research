# TASK-0037：待User确认的部署变更单（2026-09-30）

状态：**准备代码已实现，尚未执行以下部署变更；准入保持关闭。** 本单是原Task的部署审批，不新建Task。官方Web＋独立采集面板范围保持，TASK-0031 Accepted/312条历史结果保持。

## 一、当前主机实况与纠正

本轮经官方ECS Cloud Assistant、eds-aic RunCommand/DescribeTasks只读检查并回读：
- Linux OpenSSH 8.0p1，支持PermitListen；已有22/80监听，没有443实际监听。nginx有效配置没有ssl_certificate和可复用域名，原“存在HTTPS证书引用”判断是匹配了注释，已纠正。
- Linux现有安全组4条，TCP22/80/443已允许入站；不需要新增安全组、NAT、ADB映射或公网Frida。主机本地防火墙和最终跨网可达性仍需部署前只读复核；若有额外阻挡，不自动改规则。
- 任务端口15555/15038/27044/18738均无监听；/srv空闲约32.8 GB。任务Linux身份/目录尚未创建。
- 手机Android12、ARM64，Huuuge12.09.27229/1789041595进程在运行。厂商Dropbear2025.88监听22；不修改它。没有在已查路径发现OpenSSH客户端，拟在本任务目录部署官方Termux OpenSSH包及必要依赖，兼容性须先验证。
- 旧官方Frida17.17.0、OpenSSL及当前descriptor可复用；此前用错误简写文件名探测到“absent”不代表工具未安装。
- 以上是环境证据，不是SSH隧道/TLS新批次/浏览器V1验收。真实地址、实例ID、主机公钥和完整响应保留私有交接，不进入Git。

## 二、请求一次批准的具体变更

| 变更 | 精确范围 | 影响及限制 | 回滚 |
| --- | --- | --- | --- |
| Linux运行身份 | 新增huuuge-workbench非root系统用户，无sudo；只写/srv/huuuge-self-service/data。新增huuuge-tunnel系统用户，只能用本任务公钥做指定反向转发 | 两个用户只供本任务。Linux无云API权限；常驻不使用Owner OAuth。现有绑定ADB匹配密钥受控复制到任务私有目录，0600归任务用户，不替换手机绑定 | 停本任务单元，撤销隧道公钥，锁定任务用户。保留结果和原TASK-0031文件，不删除用户数据 |
| 保护管理连接 | 手机任务目录/data/local/tmp/task0037/ssh生成专用SSH key；主机固定host key经现有受控API取回并严格固定。手机向现有Linux22建立SSH反向转发，仅Linux127.0.0.1:15555→手机127.0.0.1:5555 | 不使用原公网ADB传输管理明文。Linuxsshd追加本单Match User配置，只允许remote/PermitListen127.0.0.1:15555，无shell/PTY/agent/X11/其他转发，校验后reload。无新增公网监听 | 停经PID/启动时刻核对的本任务手机隧道；移除该公钥和本任务Match块，sshd -t后reload。其他SSH配置、会话及厂商Dropbear保持 |
| 任务服务及工具 | 独立/srv/huuuge-self-service/releases、venv、tools、runtime、data；复用现有Python3.11和匹配descriptor/官方Frida、ADB。安装huuuge-workbench.service与huuuge-worker.service | 系统Python和原服务不替换。Web/worker仅回环18738/15038/27044；手机Frida仅回环27042。服务随Linux启动，手机隧道在本轮常驻并自动重连；手机重启后的恢复另需核验，不写Android init | 关闭准入→正常Stop/Flush/清理→停用本任务单元；保留SQLite、所有批次，切回前一release |
| HTTPS入口及证书 | 以已核验Linux现有公网IP作为HTTPS origin，不买域名。隔离安装官方Certbot≥5.4；先staging检查，确认后签发免费Let’s Encrypt shortlived IP证书。nginx只增加本任务443虚拟主机、80的/.well-known/acme-challenge/精确location | 这是新增可从公网到达的登录入口，需明确批准。采集/API/下载均需面板鉴权；无公开结果目录。80原业务location保持；nginx -t后reload，不restart。IP证书会将该公网IP写入公开证书透明度记录，此项也需User接受 | 移除本任务443虚拟主机和ACME location并nginx -t/reload；停续期timer。证书透明度历史无法撤回；不删除原80业务配置 |
| 证书自动维护 | 任务独立certbot配置/日志/工作目录，systemd续期timer每12小时检查；续期成功且nginx -t通过才reload | 6天证书需续期；到期/失败不降级HTTP或跳过校验。维护timer使用root执行固定证书维护命令，不向应用授予root | 停用本任务renew.timer；保留诊断记录，关闭HTTPS准入直至维护 |
| 容量保护 | 启动和运行检查空闲≥5GiB；任务目录软上限8GiB、单轮64MiB/1小时、导出2GiB；手机/data空闲至少256MiB；worker MemoryMax2G/CPUQuota100%/TasksMax64，Web256M/50%/32 | 达阈值停止新增并正常收尾；停止期间可能有少量在途写入，软阈值不是硬磁盘配额。运行数据及旧312条均不自动删除。超时/容量停止写入事件 | 调整仅任务配置，经确认后生效；不清数据、不变更主机磁盘/配额 |

**不申请**新ECS/云手机、付费域名、额外公网端口、IAM/安全组/防火墙变更。若实际环境要求以上额外改变，停止该步骤并另报具体差异；本批准不覆盖这些事项。

## 三、实际保护路径与权限上限

游戏：本人/同事在厂商官方Web用成员账号；独立于面板，不代理密码、验证码或Cookie。

管理：云手机→现有Linux22的SSH（手机固定Linux host key，Linux只认该手机专用key）→Linux回环15555→专用ADB server15038。ADB保留原绑定key鉴权；Runtime检查回环监听的实际UID，再读固定设备serial摘要/Root/ABI/游戏版本，才允许准备探针。SSH替代的是不加密的公网管理段，非地址伪装。

采集：手机Frida127.0.0.1:27042→上述ADB专用forward→Linux127.0.0.1:27044；另有每片段新Frida TLS证书、固定证书校验与令牌鉴权。手机私钥不离开手机；令牌不放API正文/聊天/Git；结束确认本轮Frida退出后删密钥/令牌、移除准确forward、断开目标、停止专用ADB。清理结果未知时保留锁，不杀未知PID。

Linux服务不持云API身份、不持手机Web登录凭据；但现有Root ADB本身具有手机管理能力，不能描述成平台强制的“仅能读取Huuuge”。面板无任意命令/目标接口，固定任务进程限制由当前代码与受控配置执行；这是实际权限上限。

## 四、部署顺序与停止条件

1. 先获得本单批准；保留原sshd/nginx配置、有效规则摘要和业务基线。真实目标由私有映射指定，绝不从浏览器输入选择。
2. 在隔离目录校验官方手机SSH客户端能执行、依赖齐备和架构正确；失败就停在准备，不覆盖/vendor、系统库或厂商Dropbear。不采用跳过host key验证的替代方法。
3. 建上述最小用户/公钥配置；sshd -t及sshd -T -C user=huuuge-tunnel,...核对限制，再reload。验证合法单一转发、错误host key、shell和其他监听端口均被拒。SSH端口本身现有开放，不改规则。
4. 部署固定Git commit归档，写真实.cloud-revision；复制已核验descriptor及匹配key到私有配置，runtime.example.json作为workbench.runtime填入。先admission=false。
5. 系统单元语法检查、资源限制确认、定向运行；源目录只读，data0700。仅在受控终端通过既有admin命令交互设面板密码，无默认密码、不进命令行/聊天。
6. 经80 webroot完成证书staging验证；staging不作为浏览器可用。获生产可信证书、HTTPS/源站/鉴权/下载保护和续期dry-run通过，再开放准入。外部可达性失败不得自动改防火墙/SG。
7. 实测两个标签页，游戏正常操作、面板后台保持连接超过3分钟；返回面板不误报离线。灰→真实绿→正常红“已保存”，核对新计数、下载及密钥/进程清理。关闭面板/真正断线另测宽限停止；SSE合成检查不能替代浏览器实测。
8. User普通Slots、新分析包、本地AI证据引用、两个面板身份轮流与越权、异常恢复、退出Codex后另跑一轮，全部A—F完成才交完整Review。其间保留失败片段与缺口。

本轮未部署、无V1新包；不能给出可用面板入口。下一步是User批准上表，再由Codex执行，不要求User手工部署。

## 五、实现/验证边界

CaptureRuntime已由阻断桩改为上述运行适配；原controller仅增显式ssh-adb-frida-tls类型，原public模式真实地址校验和其他前置保持。运行journal先于启动，PID/start tick/command防误杀；orphan通过原.run.lock阻止并发，失败保留锁。每段TLS自动准备，当前正负令牌鉴权与证书校验都在真实部署前置内。

后台页采用受鉴权POST SSE，服务端连接维护presence；每帧重核鉴权/所属批次/页面，断流后按原3分钟宽限处理。前台10秒无可信状态撤销绿色；隐藏页计时器不直接触发假红。真实浏览器冻结、网络断流和双标签页时效仍待实测，不能只凭代码保证。

参考：[OpenSSH限制](https://man.openbsd.org/sshd_config)、[Termux官方OpenSSH构建](https://github.com/termux/termux-packages/blob/master/packages/openssh/build.sh)、[Let’s Encrypt IP证书/Certbot≥5.4及webroot续期](https://letsencrypt.org/2026/03/11/shorter-certs-certbot)。均于2026-09-30核对。Subagents: none。
