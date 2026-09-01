param(
    [ValidateSet('Preflight', 'Start', 'Stop', 'Status', 'Recent', 'AI')]
    [string]$Action = 'Status',
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [ValidateSet('Auto', 'Codex', 'Trae', 'None')]
    [string]$AIProvider = 'Auto',
    [int]$ReadyTimeoutSeconds = 150,
    [switch]$ValidationOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
$LocalRoot = Join-Path $RepoRoot '.local\controller'
$ActivePath = Join-Path $LocalRoot 'active.json'
$LastPath = Join-Path $LocalRoot 'last_session.json'
$SettingsPath = Join-Path $LocalRoot 'settings.json'
$AdbDefault = 'C:\platform-tools\adb.exe'
$Serial = '127.0.0.1:5565'
$Package = 'com.huuuge.casino.slots'
$ResearchInstance = 'Pie64_1 / HuuugeResearch'
$NormalInstance = 'Pie64 / BlueStacks 5'
$VenvPython = Join-Path $RepoRoot '.venv\Scripts\python.exe'
$Descriptor = Join-Path $RepoRoot 'artifacts\live_probe\huuuge_descriptors.pb'
$BootstrapHelper = Join-Path $RepoRoot 'artifacts\live_probe\bootstrap_houdini_gadget.py'
$Collector = Join-Path $RepoRoot 'artifacts\live_probe\live_decode.py'
$BootstrapScript = Join-Path $RepoRoot 'scripts\huuuge_bootstrap.ps1'
$InventoryScript = Join-Path $RepoRoot 'scripts\build_rpc_inventory.py'
$CatalogScript = Join-Path $RepoRoot 'scripts\build_module_catalog.py'

New-Item -ItemType Directory -Force -Path $LocalRoot | Out-Null

function Write-JsonAtomic([string]$Path, [hashtable]$Value) {
    $temp = "$Path.tmp"
    $Value | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $temp -Encoding UTF8
    Move-Item -LiteralPath $temp -Destination $Path -Force
}

function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Quote-Native([string]$Value) {
    return '"' + $Value.Replace('"', '\"') + '"'
}

function Start-HiddenProcess([string]$FilePath, [string[]]$Arguments, [string]$Stdout, [string]$Stderr) {
    $argumentLine = ($Arguments | ForEach-Object { Quote-Native $_ }) -join ' '
    return Start-Process -FilePath $FilePath -ArgumentList $argumentLine -WorkingDirectory $RepoRoot `
        -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr -WindowStyle Hidden -PassThru
}

function Get-Settings {
    $settings = Read-JsonFile $SettingsPath
    if ($null -ne $settings) { return $settings }
    $defaults = [ordered]@{
        adb_path = $AdbDefault
        capture_root = 'C:\huuuge_research\captures'
        frida_server_path = 'C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64'
        ai_provider = 'Auto'
        trae_path = Join-Path $env:LOCALAPPDATA 'Programs\Trae CN\Trae CN.exe'
    }
    Write-JsonAtomic $SettingsPath $defaults
    return [pscustomobject]$defaults
}

function Get-SourceRevision {
    if (Test-Path (Join-Path $RepoRoot '.git')) {
        return ((& git -C $RepoRoot rev-parse HEAD 2>$null) -join '').Trim()
    }
    if (Get-Command svn -ErrorAction SilentlyContinue) {
        $revision = ((& svn info --show-item revision $RepoRoot 2>$null) -join '').Trim()
        if ($LASTEXITCODE -eq 0 -and $revision) { return "svn:$revision" }
    }
    return 'unmanaged'
}

function Ensure-ResearchDevice([string]$Adb) {
    if (-not (Test-Path -LiteralPath $Adb)) { throw "ADB 不存在：$Adb" }
    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $Adb connect $Serial 2>$null | Out-Null
        $state = ((& $Adb -s $Serial get-state 2>$null) -join '').Trim()
    } finally {
        $ErrorActionPreference = $previousErrorAction
    }
    if ($state -eq 'device') { return }

    $player = @(
        'C:\Program Files\BlueStacks_nxt_cn\HD-Player.exe',
        'C:\Program Files\BlueStacks_nxt\HD-Player.exe'
    ) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $player) {
        foreach ($key in @('HKLM:\SOFTWARE\BlueStacks_nxt_cn','HKLM:\SOFTWARE\BlueStacks_nxt','HKLM:\SOFTWARE\WOW6432Node\BlueStacks_nxt_cn','HKLM:\SOFTWARE\WOW6432Node\BlueStacks_nxt')) {
            if (Test-Path $key) {
                $candidate = Join-Path ([string](Get-ItemProperty $key).InstallDir) 'HD-Player.exe'
                if (Test-Path -LiteralPath $candidate) { $player = $candidate; break }
            }
        }
    }
    if (-not (Test-Path -LiteralPath $player)) { throw 'HuuugeResearch 未运行，且未找到 HD-Player.exe。' }
    Write-Host '正在启动 HuuugeResearch（仅研究实例）...'
    Start-Process -FilePath $player -ArgumentList '--instance Pie64_1' | Out-Null
    $deadline = (Get-Date).AddSeconds(120)
    do {
        Start-Sleep -Seconds 2
        $previousErrorAction = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            & $Adb connect $Serial 2>$null | Out-Null
            $state = ((& $Adb -s $Serial get-state 2>$null) -join '').Trim()
        } finally {
            $ErrorActionPreference = $previousErrorAction
        }
        if ($state -eq 'device') { return }
    } while ((Get-Date) -lt $deadline)
    throw 'HuuugeResearch 启动超时。普通 Pie64 未被操作。'
}

function Assert-ResearchRoot([string]$Adb) {
    $identity = ((& $Adb -s $Serial shell "/system/xbin/bstk/su -c 'id'" 2>&1) -join ' ')
    if ($identity -notmatch 'uid=0\(root\)') {
        throw "研究实例没有真实 root。不会自动重复 Root；请点 [环境检查/修复] 并让 AI 审核。实际输出：$identity"
    }
    Write-Host '[OK] HuuugeResearch root 已验证。'
}

function Ensure-FridaServer([string]$Adb, [string]$ServerPath) {
    $running = ((& $Adb -s $Serial shell "/system/xbin/bstk/su -c 'pidof huuuge-fs'" 2>$null) -join '').Trim()
    if ($running) {
        $remoteVersion = ((& $Adb -s $Serial shell '/data/local/tmp/huuuge-fs --version' 2>$null) -join '').Trim()
        $hostVersion = ((& $VenvPython -c 'import frida; print(frida.__version__)') -join '').Trim()
        if ($remoteVersion -ne $hostVersion) { throw "Frida 版本不一致：host=$hostVersion server=$remoteVersion" }
        Write-Host "[OK] root Frida server 正在运行（PID $running，版本 $remoteVersion）。"
        return
    }
    if (-not (Test-Path -LiteralPath $ServerPath)) { throw "缺少匹配的 Frida server：$ServerPath" }
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RepoRoot 'artifacts\live_probe\start_frida_server.ps1') `
        -Serial $Serial -ServerPath $ServerPath | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'root Frida server 启动失败。' }
}

function Get-GadgetPath([string]$Adb) {
    $baseLine = @(& $Adb -s $Serial shell "pm path $Package") | Where-Object { $_ -match 'base\.apk' } | Select-Object -First 1
    if (-not $baseLine) { throw '研究实例中没有安装 Huuuge。' }
    $appDir = ($baseLine -replace '^package:', '' -replace '/base\.apk\s*$', '').Trim()
    $gadget = "$appDir/lib/arm64/libhuuuge-gadget.so"
    $gadgetConfig = "$appDir/lib/arm64/libhuuuge-gadget.config.so"
    $exists = ((& $Adb -s $Serial shell "/system/xbin/bstk/su -c 'test -f $gadget && test -f $gadgetConfig && echo OK'" 2>$null) -join '').Trim()
    if ($exists -ne 'OK') {
        throw "研究 APK 目录中缺少 ARM64 Gadget 或 27043 配置（应用更新后需重新部署）：$gadget / $gadgetConfig"
    }
    return $gadget
}

function Get-GameVersion([string]$Adb) {
    $dump = (& $Adb -s $Serial shell "dumpsys package $Package") -join "`n"
    $version = if ($dump -match 'versionName=([^\s]+)') { $Matches[1] } else { 'unknown' }
    $code = if ($dump -match 'versionCode=([^\s]+)') { $Matches[1] } else { 'unknown' }
    return [pscustomobject]@{ Version = $version; Code = $code }
}

function Invoke-Preflight {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BootstrapScript -RepoRoot $RepoRoot -SkipAI -NonInteractive
    if ($LASTEXITCODE -ne 0) { throw "Bootstrap 预检失败（code=$LASTEXITCODE）。" }
}

function Invoke-StartCapture {
    if (-not (Test-Path -LiteralPath $VenvPython)) { throw '缺少 .venv，请先运行“环境检查/修复”。' }
    if (-not (Test-Path -LiteralPath $Descriptor)) { throw '缺少 descriptor，请先运行“环境检查/修复”。' }
    $active = Read-JsonFile $ActivePath
    if ($null -ne $active -and $active.collector_pid) {
        if (Get-Process -Id ([int]$active.collector_pid) -ErrorAction SilentlyContinue) {
            throw "已有采集正在运行：$($active.session_id)"
        }
    }

    $settings = Get-Settings
    $adb = [string]$settings.adb_path
    Ensure-ResearchDevice $adb
    Assert-ResearchRoot $adb
    Ensure-FridaServer $adb ([string]$settings.frida_server_path)
    $gadgetPath = Get-GadgetPath $adb
    $game = Get-GameVersion $adb
    & $adb -s $Serial forward tcp:27043 tcp:27043 | Out-Null

    $sessionId = Get-Date -Format 'yyyyMMdd_HHmmss'
    $controlDir = Join-Path $LocalRoot "sessions\$sessionId"
    New-Item -ItemType Directory -Force -Path $controlDir | Out-Null
    $captureRoot = [IO.Path]::GetFullPath([string]$settings.capture_root)
    New-Item -ItemType Directory -Force -Path $captureRoot | Out-Null
    $sessionDir = Join-Path $captureRoot $sessionId
    $stopFile = Join-Path $controlDir 'stop.request'
    $stateFile = Join-Path $controlDir 'collector_state.json'
    $bootstrapOut = Join-Path $controlDir 'gadget_bootstrap.out.log'
    $bootstrapErr = Join-Path $controlDir 'gadget_bootstrap.err.log'
    $collectorOut = Join-Path $controlDir 'collector.out.log'
    $collectorErr = Join-Path $controlDir 'collector.err.log'

    Write-Host '正在冷启动研究实例中的 Huuuge，并加载 Houdini ARM64 Gadget...'
    $bootstrapProcess = Start-HiddenProcess $VenvPython @(
        $BootstrapHelper, '--device-id', $Serial, '--package', $Package,
        '--gadget-path', $gadgetPath, '--timeout', '120'
    ) $bootstrapOut $bootstrapErr

    $deadline = (Get-Date).AddSeconds(120)
    $gadgetLoaded = $false
    do {
        Start-Sleep -Milliseconds 500
        if (Test-Path $bootstrapOut) {
            $text = Get-Content -LiteralPath $bootstrapOut -Raw -ErrorAction SilentlyContinue
            if ($text -match '"kind":\s*"gadget-load-started"') { $gadgetLoaded = $true; break }
            if ($text -match '"kind":\s*"gadget-error"') { throw "Gadget 加载失败：$text" }
        }
        if ($bootstrapProcess.HasExited -and -not $gadgetLoaded) {
            $errorText = if (Test-Path $bootstrapErr) { Get-Content $bootstrapErr -Raw } else { '' }
            throw "Houdini Gadget bootstrap 提前退出：$errorText"
        }
    } while ((Get-Date) -lt $deadline)
    if (-not $gadgetLoaded) { throw '等待 ARM64 Gadget 开始加载超时。' }

    # Gadget's default on-load policy waits for its first controller. During
    # Houdini loading, a client that connects too early can see a transient
    # "connection closed". Complete one bounded process-list handshake before
    # starting the lossless collector so its only connection is stable.
    $fridaPs = Join-Path (Split-Path -Parent $VenvPython) 'frida-ps.exe'
    if (-not (Test-Path -LiteralPath $fridaPs)) { throw "缺少 Frida CLI：$fridaPs" }
    $gadgetReady = $false
    $gadgetDeadline = (Get-Date).AddSeconds(20)
    do {
        Start-Sleep -Milliseconds 500
        $previousErrorAction = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            $processList = (& $fridaPs -H '127.0.0.1:27043' 2>$null) -join "`n"
        } finally {
            $ErrorActionPreference = $previousErrorAction
        }
        if ($processList -match '(?m)^\s*\d+\s+Gadget\s*$') {
            $gadgetReady = $true
            break
        }
    } while ((Get-Date) -lt $gadgetDeadline)
    if (-not $gadgetReady) { throw 'ARM64 Gadget 端口未在 20 秒内稳定响应。' }

    Write-Host '正在连接 lossless RPC collector 并验证 hooks/落盘...'
    $collectorProcess = Start-HiddenProcess $VenvPython @(
        $Collector,
        '--remote-endpoint', '127.0.0.1:27043', '--process', 'Gadget',
        '--descriptors', $Descriptor, '--out', $captureRoot, '--session-id', $sessionId,
        '--stop-file', $stopFile, '--state-file', $stateFile,
        '--game-version', $game.Version, '--version-code', $game.Code,
        '--research-instance', $ResearchInstance, '--source-revision', (Get-SourceRevision)
    ) $collectorOut $collectorErr

    $activeState = [ordered]@{
        schema_version = 1
        status = 'starting'
        session_id = $sessionId
        session_dir = $sessionDir
        control_dir = $controlDir
        collector_pid = $collectorProcess.Id
        bootstrap_pid = $bootstrapProcess.Id
        stop_file = $stopFile
        state_file = $stateFile
        started_at = (Get-Date).ToString('o')
        research_instance = $ResearchInstance
        normal_instance_protected = $NormalInstance
    }
    Write-JsonAtomic $ActivePath $activeState

    $deadline = (Get-Date).AddSeconds($ReadyTimeoutSeconds)
    do {
        Start-Sleep -Seconds 1
        if ($collectorProcess.HasExited) {
            $errorText = if (Test-Path $collectorErr) { Get-Content $collectorErr -Raw } else { '' }
            throw "Collector 提前退出：$errorText"
        }
        $collectorState = Read-JsonFile $stateFile
        if ($null -ne $collectorState -and $collectorState.status -eq 'ready') {
            $rawCount = @(Get-ChildItem -LiteralPath (Join-Path $sessionDir 'raw') -File -ErrorAction SilentlyContinue).Count
            $jsonCount = @(Get-ChildItem -LiteralPath (Join-Path $sessionDir 'json') -File -ErrorAction SilentlyContinue).Count
            if ($rawCount -gt 0 -and $jsonCount -gt 0 -and (Test-Path (Join-Path $sessionDir 'manifest.json'))) {
                $activeState.status = 'ready'
                $activeState.message_count_at_ready = [int]$collectorState.message_count
                Write-JsonAtomic $ActivePath $activeState
                Write-Host "Session：$sessionId"
                Write-Host "目录：$sessionDir"
                Write-Host 'READY，可以开始玩了'
                return
            }
        }
    } while ((Get-Date) -lt $deadline)

    Set-Content -LiteralPath $stopFile -Value 'timeout' -Encoding ASCII
    throw 'Collector 已连接但未在时限内同时证明 hooks、真实 RPC、raw 与 decoded JSON 落盘。'
}

function Invoke-StopCapture {
    $active = Read-JsonFile $ActivePath
    if ($null -eq $active) { throw '当前没有活动采集。' }
    Set-Content -LiteralPath ([string]$active.stop_file) -Value 'stop' -Encoding ASCII
    $collectorProcess = Get-Process -Id ([int]$active.collector_pid) -ErrorAction SilentlyContinue
    if ($collectorProcess) {
        if (-not $collectorProcess.WaitForExit(20000)) {
            throw 'Collector 未能在 20 秒内 clean stop；没有强制结束，请点“AI 接管”排查。'
        }
    }
    $sessionDir = [string]$active.session_dir
    $manifestPath = Join-Path $sessionDir 'manifest.json'
    $manifest = Read-JsonFile $manifestPath
    if ($null -eq $manifest -or $manifest.status -ne 'stopped') { throw 'manifest 未确认 clean stop/flush。' }

    $analysisDir = if ($ValidationOnly) {
        Join-Path ([string]$active.control_dir) 'results\analysis'
    } else {
        Join-Path $RepoRoot "artifacts\analysis\$($active.session_id)"
    }
    & $VenvPython $InventoryScript $sessionDir --out-dir $analysisDir --descriptors $Descriptor `
        --game-version ([string]$manifest.game_version) --version-code ([string]$manifest.version_code) `
        --frida-version ([string]$manifest.frida_version) --device $ResearchInstance | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'RPC inventory 生成失败。' }

    $catalogDir = if ($ValidationOnly) {
        Join-Path ([string]$active.control_dir) 'results\module_catalog'
    } else {
        Join-Path $RepoRoot 'artifacts\module_catalog'
    }
    & $VenvPython $CatalogScript --descriptors $Descriptor `
        --live-inventory (Join-Path $analysisDir 'rpc_inventory.csv') `
        --live-fields (Join-Path $analysisDir 'field_paths.csv') `
        --capture-session $sessionDir --apk 'C:\huuuge_apk\base.apk' `
        --session-id ([string]$active.session_id) --out-dir $catalogDir | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Module catalog 更新失败。' }

    $result = [ordered]@{
        schema_version = 1
        status = 'finalized'
        session_id = [string]$active.session_id
        session_dir = $sessionDir
        analysis_dir = $analysisDir
        module_catalog_dir = $catalogDir
        validation_only = [bool]$ValidationOnly
        message_count = [int]$manifest.message_count
        decoded_count = [int]$manifest.decoded_count
        finalized_at = (Get-Date).ToString('o')
    }
    Write-JsonAtomic $LastPath $result
    Move-Item -LiteralPath $ActivePath -Destination (Join-Path ([string]$active.control_dir) 'active.finalized.json') -Force
    Write-Host "已 clean stop 并整理：$($active.session_id)"
    Write-Host "RPC：$($manifest.message_count)，解码：$($manifest.decoded_count)"
    Write-Host "结果：$analysisDir"
}

function Show-Status {
    $active = Read-JsonFile $ActivePath
    if ($null -ne $active) {
        $state = Read-JsonFile ([string]$active.state_file)
        if ($null -ne $state) {
            Write-Host "状态：$($state.status)"
            Write-Host "Session：$($state.session_id)"
            Write-Host "RPC：$($state.message_count) / decoded $($state.decoded_count)"
            Write-Host "目录：$($state.session_dir)"
            return
        }
    }
    $last = Read-JsonFile $LastPath
    if ($null -ne $last) {
        Write-Host '状态：未采集'
        Write-Host "最近 Session：$($last.session_id)"
        Write-Host "RPC：$($last.message_count) / decoded $($last.decoded_count)"
        Write-Host "结果：$($last.analysis_dir)"
    } else {
        Write-Host '状态：未采集；没有 GUI 管理的历史 Session。'
    }
}

function Invoke-AIHandoff {
    $settings = Get-Settings
    $provider = if ($AIProvider -ne 'Auto') { $AIProvider } else { [string]$settings.ai_provider }
    if ($provider -eq 'Auto') { $provider = 'Trae' }
    $promptPath = Join-Path $LocalRoot 'AI_HANDOFF_PROMPT.md'
    $prompt = @'
# Huuuge 采集器 AI 接管

请先严格阅读 AGENTS.md、CONTRIBUTING.md、CURRENT_STATUS.md、最新 COLLAB_LOG.md、HUUUGE_DATA_COLLECTION_GUIDE.md、AGENT_DATA_USAGE_GUIDE.md 和 AI_DEPLOYMENT_PLAYBOOK.md。

检查 `.local/bootstrap/` 与 `.local/controller/` 的最新报告，判断当前部署/采集状态。只操作 `Pie64_1 / HuuugeResearch`；禁止对普通 `Pie64` 做 Root 或 instrumentation。不要修改游戏数值、请求或服务器状态。能在本机完成的检查、修复、验证由你直接执行，不要让策划复制终端命令。
'@
    Set-Content -LiteralPath $promptPath -Value $prompt -Encoding UTF8
    Set-Clipboard -Value $prompt
    if ($provider -eq 'Trae') {
        $trae = [string]$settings.trae_path
        if (-not (Test-Path -LiteralPath $trae)) { throw '未找到 Trae，请在 GUI 设置中选择/安装 Trae。' }
        Start-Process -FilePath $trae -ArgumentList (Quote-Native $RepoRoot) | Out-Null
        Write-Host "已打开 Trae（可使用 DeepSeek），交接提示已复制并写入：$promptPath"
        return
    }
    if ($provider -eq 'Codex') {
        $codex = Get-Command codex -ErrorAction SilentlyContinue
        if (-not $codex) { throw '未找到 Codex CLI；请选择 Trae + DeepSeek。' }
        Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoExit', '-Command', "Set-Location '$RepoRoot'; codex") | Out-Null
        Write-Host "已打开 Codex，交接提示已复制并写入：$promptPath"
        return
    }
    Write-Host "AI 未启动；交接提示已生成：$promptPath"
}

switch ($Action) {
    'Preflight' { Invoke-Preflight }
    'Start' { Invoke-StartCapture }
    'Stop' { Invoke-StopCapture }
    'Status' { Show-Status }
    'Recent' {
        Show-Status
        $last = Read-JsonFile $LastPath
        if ($null -ne $last -and (Test-Path ([string]$last.analysis_dir))) {
            Start-Process explorer.exe -ArgumentList (Quote-Native ([string]$last.analysis_dir)) | Out-Null
        }
    }
    'AI' { Invoke-AIHandoff }
}
