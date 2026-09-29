# TASK-0031 云手机只读检查

2026-09-29；只用于原任务的唯一已购云手机。当前网页桌面已确认；控制台只读命令点过一次执行，但未返回结果。**先查旧任务，不重新提交命令。**

## 已核验的管理通道

- 产品/API 版本：`eds-aic/2023-09-30`。官方 [RunCommand](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-runcommand) 提交命令，[DescribeTasks](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-describetasks) 查进度和结果。旧 DescribeInvocations 已被官方标记即将下线，本流程不用。
- 官方阿里云 CLI [v3.5.1 Windows amd64 发布包](https://github.com/aliyun/aliyun-cli/releases/tag/v3.5.1) 与发布资产 SHA-256 匹配，安装到管理 Host 的用户目录 `Programs/aliyun-cli`；版本及两个 API 的帮助已回读。Workbench v1.0.1 原安装保留，不用于云手机 ID。
- CLI 内置映射与[官方接入点表](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-endpoint)均仅列上海、新加坡；以香港地域做离线预演返回 `unknown endpoint for eds-aic/cn-hongkong`。实例所在地域不能直接当成 API 管理接入点。当前尚未取得此香港实例对应接入点的证据，不猜域名、不切换地域实查。
- 权限尚未验证。两份 API 文档未透出具体授权信息，不等于免认证，也不足以编造 RAM action/resource 策略。User 确认本次目标和所需 API 权限，不申请管理员权限；API 层的 RunCommand 能执行写命令，本次仅允许下方固定只读内容。

## User 只需完成的本地配置步骤

在自己的 PowerShell 中执行下列官方 [STS 交互配置](https://help.aliyun.com/zh/cli/temporary-security-credentials-sts-token)，填入已获准用于本次检查的临时凭据，默认地域填 `cn-hongkong`。只回复配置完成；不要向聊天提供任何值或配置文件。当前未发现 CLI 默认配置、标准凭据文件或相关环境变量；不读取浏览器 Cookie，不要求安装 OAuth 管理应用。

```powershell
& "$env:LOCALAPPDATA\Programs\aliyun-cli\aliyun.exe" configure --mode StsToken --profile task0031
```

STS 会过期；没有此类凭据时保留未配置，不改用主账号长期密钥。此步骤只解决身份配置，不能代替接入点/实例权限核验。

## Codex 执行顺序（凭据及接入点确认后）

从仓库根目录执行。实例 ID、任务 ID 和原始 API 返回仅留受控会话，不进 Git。下面空值是有意设置的阻断项；不能直接复制后盲填示例地域。

```powershell
$cli = Join-Path $env:LOCALAPPDATA 'Programs\aliyun-cli\aliyun.exe'
$instanceId = '' # 填入本次已核验的唯一云手机 ID
$apiRegion = ''  # 厂商证据确认的管理地域，不从实例地域推测
$apiEndpoint = '' # 同一证据确认的官方接入点
if ($instanceId -notmatch '^acp-[a-z0-9]+$' -or !$apiRegion -or !$apiEndpoint) {
    throw '先核验唯一实例与其官方管理接入点'
}
$common = @('eds-aic', '--version', '2023-09-30', '--profile', 'task0031',
    '--region', $apiRegion, '--endpoint', $apiEndpoint)

# 第一步仅查该实例，保留原始结果于会话变量，不输出完整响应。
$taskJson = & $cli @common DescribeTasks --InstanceId $instanceId --Level 2 --MaxResults 20
if ($LASTEXITCODE -ne 0) { throw '查询失败；检查权限/接入点，不提交新命令' }
$taskPage = $taskJson | ConvertFrom-Json
```

检查任务的实例归属、时间、类型以及 `Param` 中 `TASK0031_GOOGLE_READONLY_BEGIN` 标记，寻找本轮控制台提交。按返回 `NextToken` 逐页继续**同一实例**查询；空首页不能证明命令未提交。只向交接输出脱敏状态和固定脚本结果。运行中/等待中继续查同一 TaskId；失败/跳过记录原状态；提交或结果未知均不自动重试。

仅当旧任务已查清、确需重新执行且获准时，用固定脚本提交一次。`AgentType` 也要依据实际实例支持的命令通道核验，不能凭官方示例认定为 EdsAgent。

```powershell
$agentType = '' # 现场核验为 EdsAgent 或 CloudAssistant 后填写
if ($agentType -notin @('EdsAgent', 'CloudAssistant')) { throw '命令通道尚未核验' }
$commandText = [IO.File]::ReadAllText((Join-Path (Get-Location) 'deploy/cloud/google-readonly-check.sh')).Replace("`r`n", "`n")
$content = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($commandText))
$submitJson = & $cli @common RunCommand --InstanceIds.1 $instanceId --AgentType $agentType --Timeout 60 --ContentEncoding Base64 --CommandContent $content
if ($LASTEXITCODE -ne 0) { throw '提交结果未知；先查任务，不重复提交' }
$submitted = $submitJson | ConvertFrom-Json
# 从返回值核对唯一 InstanceId，保存 ChildTaskId / TaskId / InvokeId。
# 优先使用该实例的 ChildTaskId；不要混淆 RequestId、InvokeId 和 TaskId。
$childTaskId = '' # 从已核对返回中取得，不猜测
if (!$childTaskId) { throw '没有可核验的实例级任务 ID，回到 DescribeTasks' }
$resultJson = & $cli @common DescribeTasks --InstanceId $instanceId --TaskIds.1 $childTaskId --Level 2
if ($LASTEXITCODE -ne 0) { throw '结果读取失败；保留 unknown' }
$resultPage = $resultJson | ConvertFrom-Json
```

以上是逐步维护命令，不是自动执行器。`Finished` 还须核对 `Result` 的实际格式、完整首尾标记及全部检查字段；没有有效输出、字段缺失或错误均记录 unknown，不能推断组件不存在。保存脱敏结果后回读，核对确属本次任务。官方 CLI 帮助的响应聚合示例与文档数组展示存在差异，按真实返回解析，不预设一条未经验证的 JSON 路径。

## 固定检查及证据边界

[google-readonly-check.sh](google-readonly-check.sh) 只读 Android release/SDK/ABI、UTC、四个 Google 包在 user 0 下的存在/启用/禁用状态，并对 `play.google.com`、`accounts.google.com` 做无凭据 HTTPS HEAD。只输出包状态、HTTP 状态码及退出码；无 curl 则报告检查不可用，不补装工具。HEAD 成功不是商店登录/下载可用的证明。

不安装/启用/清数据/重启/重建，不启动 Frida，不开 ADB 端口，不新建 ECS/NAT。读到组件实况后，再按原批准范围选择厂商适用的 Google Play/GMS 方法，到登录页通知 User。Linux 执行端核验独立推进。

本轮仅 `bash -n` 通过，以及以虚构实例、官方上海接入点完成两个 API 的 `--cli-dry-run` 参数预演；没有发出 API 请求，不能证明香港目标可达。网页命令输出仍 unknown，Google 安装、商店、无探针游戏与真实采集/停止保存均未通过。
