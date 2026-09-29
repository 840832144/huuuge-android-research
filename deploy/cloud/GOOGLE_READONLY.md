# TASK-0031 云手机检查与 Google 组件准备

2026-09-29；只用于原任务的唯一已购云手机。先只读、再启用已有组件、到登录入口交给 User。管理命令在手机执行，管理 Host 不运行采集器。

## 已验证的管理通道

- 官方阿里云 CLI v3.5.1 已安装并校验发布包，复用用户目录 `Programs/aliyun-cli/aliyun.exe`，不重复安装。Workbench v1.0.1 保留，未用于云手机 ID。
- 产品/API：`eds-aic/2023-09-30`；[RunCommand](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-runcommand) 提交单实例命令，[DescribeTasks](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-describetasks) 按返回的 ChildTaskId 查结果。不使用即将下线的 DescribeInvocations。
- [官方接入点表](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-endpoint)列上海、新加坡。香港是本实例的业务地域；实际管理调用使用上海接入点，DescribeAndroidInstances 以精确 ID + `BizRegionId=cn-hongkong` 返回唯一匹配实例，确认 RUNNING / 镜像 26.09.1。此前香港管理地域的 unknown endpoint 已定位，不能据此认为香港实例不可管。
- `EdsAgent` 已通过真实只读、启用及 Play 启动任务验证；三次均按单实例子任务回读 Finished 和完整输出。这不代表 ADB/Frida/云端 Linux 连接已经可用。

## OAuth 与本轮授权

User 通过[官方 OAuth 浏览器流程](https://help.aliyun.com/zh/cli/oauth-credentials)完成 official-cli 授权及终端配置，profile=`task0031`，mode=OAuth，默认地域 cn-hongkong。新会话复用配置，不输出正文、授权链接、账号 ID/ARN 或凭据。当前已完成，不重配：

```powershell
# 仅配置缺失且 User 确认需要时，由 User 自己执行。
& "$env:LOCALAPPDATA\Programs\aliyun-cli\aliyun.exe" configure --mode OAuth --profile task0031
```

真实 [GetCallerIdentity](https://help.aliyun.com/zh/ram/developer-reference/api-sts-2015-04-01-getcalleridentity) 返回 Account。初次曾建议改用 RAM；User 随后明确“你先用这个调试”，本轮按该授权使用现有身份，仅对已确认的一台手机执行原批准范围。未修改 IAM、权限策略、资源或安全组。不要再把切换 RAM 当作本次前置阻塞，也不要将此次授权扩展到其他任务。

## 目标、提交与结果回读

实例 ID、子任务 ID、原始 API 响应仅保存于受控本机证据目录，不写进 Git。目标来自本次已核验实例，不填示例资源或随意枚举选择。

```powershell
$cli = Join-Path $env:LOCALAPPDATA 'Programs\aliyun-cli\aliyun.exe'
$instanceId = '' # 受控配置中的唯一已核验云手机 ID
if ($instanceId -notmatch '^acp-[a-z0-9]+$') { throw '尚未指定唯一已核验目标' }
$apiArgs = @('--profile', 'task0031', '--region', 'cn-shanghai',
    '--endpoint', 'eds-aic.cn-shanghai.aliyuncs.com', '--version', '2023-09-30')
$targetJson = & $cli eds-aic DescribeAndroidInstances @apiArgs --AndroidInstanceIds.1 $instanceId --BizRegionId cn-hongkong --MaxResults 1
if ($LASTEXITCODE -ne 0) { throw '目标读取失败' }
$targets = @(($targetJson | ConvertFrom-Json).InstanceModel)
if ($targets.Count -ne 1 -or $targets[0].AndroidInstanceId -ne $instanceId -or
    $targets[0].RegionId -ne 'cn-hongkong' -or $targets[0].AndroidInstanceStatus -ne 'RUNNING') {
    throw '目标、地域或运行状态不匹配'
}
```

本次先查询该实例已有任务（Level 2 及不限定 Level），均仅返回一条实例组创建任务，无 NextToken。没有找到前次控制台命令，旧命令仍 unknown；记录缺失不能证明未执行。User 授权继续后，提交带独立标记 `TASK0031_GOOGLE_READONLY_API_20260929_A` 的新只读检查，不重放浏览器点击。

内容来自 [google-readonly-check.sh](google-readonly-check.sh)，换行归一后 Base64 编码。每个操作提交前保存本地 attempt 标记，响应保存后核对唯一 InstanceId 和 ChildTaskId。已有 attempt 或提交结果未知时，只查任务，不重复提交。

```powershell
# $content 是本次已审阅固定命令的 Base64；此片段不是自动重试脚本。
$submitJson = & $cli eds-aic RunCommand @apiArgs --InstanceIds.1 $instanceId --AgentType EdsAgent --Timeout 60 --ContentEncoding Base64 --CommandContent $content
if ($LASTEXITCODE -ne 0) { throw '提交未确认；保存返回并查任务，不重发' }
$infos = @(($submitJson | ConvertFrom-Json).RunCommandInfos)
if ($infos.Count -ne 1 -or $infos[0].InstanceId -ne $instanceId -or !$infos[0].ChildTaskId) {
    throw '提交目标或子任务未确认'
}
$resultJson = & $cli eds-aic DescribeTasks @apiArgs --InstanceId $instanceId --TaskIds.1 $infos[0].ChildTaskId --Level 2
if ($LASTEXITCODE -ne 0) { throw '回读失败，保留 unknown' }
$tasks = @(($resultJson | ConvertFrom-Json).Data)
# 核对唯一 TaskId、InstanceId、TaskStatus；Finished 后检查 Result 完整首尾标记和全部字段。
```

实际 InstanceModel、RunCommandInfos、Data 都是数组；Result 为普通字符串。Finished 只表示任务结束，必须检查命令退出码及输出。保存白名单摘要后重新读取，不能以提交成功代替执行结果。

## 本次真实结果与采用的方法

首次只读：Android 12 / SDK 31 / arm64-v8a；Play、GMS、GSF 均存在且禁用；旧 `com.google.android.gsf.login` 不存在（不据此补装旧组件）。手机对 play.google.com 和 accounts.google.com 的无凭据 HTTPS HEAD 均返回 302 / exit 0；这不证明商店登录或下载可用。

采用方法：复用厂商镜像内置组件，使用 [Android 官方包管理器](https://developer.android.com/tools/adb#pm)启用。[阿里云 FAQ](https://help.aliyun.com/en/ecp/cloud-phone-faq)说明默认支持 GMS，[镜像说明](https://help.aliyun.com/zh/ecp/release-note-of-cloud-phone-system-image)记录 26.09.1 的 GMS 兼容支持；以下是标准 Android 命令，不冒称厂商提供过同名一键安装脚本。

```sh
# 经 EdsAgent 在已核验手机执行；不用本机 ADB 或公网端口。
pm enable --user 0 com.google.android.gsf
pm enable --user 0 com.google.android.gms
pm enable --user 0 com.android.vending
```

实际执行前统一检查三个包存在，任一失败不修改；逐包启用后检查退出码及 `pm list packages -e/-d --user 0` 精确包名。三条均 exit 0，回读 enabled=yes、disabled=no；没有下载、侧载、清数据或重建。

随后通过同一通道单独执行：

```sh
am start -W --user 0 -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p com.android.vending
```

任务 Finished，launch_exit=0、Status=ok，Activity=`com.android.vending/com.google.android.finsky.unauthenticated.activity.UnauthenticatedMainActivity`。User 起初未看到商店，随后明确“现在有了”；未重复启动。随后 User 明确“Google 已登录”，作为手动登录确认记录；登录期间暂停手机界面读取，未截图账号页面或读取密码/验证码/Cookie。登录后首次包查询显示 Huuuge 未安装，官方详情入口启动成功。User 随后安装并反馈“打开”；真实包回读 installer=com.android.vending、versionName=12.09.27229、versionCode=1789041595、primaryCpuAbi=arm64-v8a，确认本次 Play 安装。User 后续暂未找到认证项，记录“无法读取/未确认”；不反复要求查找，也不宣称已认证。

## 后续验收与当前进度

User 已完成无探针 Huuuge 交互；应用专属 ANGLE 解决图形异常，运行日志和 User“现在好了”反馈分别保存。Google 商店详情与新安装链路已实测；首页/搜索未单独验证，认证状态无法读取/未确认。

已有香港 Linux 已通过 ECS 官方 API 与 Cloud Assistant 独立核实。私网 TCP 超时，User 新建公网映射后云端 TCP 成功；官方 ADB 下载与实际 connect 被自动审批拒绝（blocked by policy），命令未提交。未生成/绑定新密钥，未启动 Frida 或采集器。图形设置、回滚、当前连接审批边界见 [部署说明](README.md)，分项结果见 [验收记录](ACCEPTANCE.md)。

浏览器自动化仍因原工具超时保持停止，不重放未知点击；手机和 Linux 官方 API 可用。真实新增解码、正常停止和保存结果回读仍待执行。
