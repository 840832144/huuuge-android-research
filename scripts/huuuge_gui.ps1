param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [switch]$BootstrapOnLoad
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
$Controller = Join-Path $RepoRoot 'scripts\huuuge_controller.ps1'
$LocalRoot = Join-Path $RepoRoot '.local\controller'
$SettingsPath = Join-Path $LocalRoot 'settings.json'
$ActivePath = Join-Path $LocalRoot 'active.json'
$LastPath = Join-Path $LocalRoot 'last_session.json'
New-Item -ItemType Directory -Force -Path $LocalRoot | Out-Null

function Read-Json([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    try { return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json } catch { return $null }
}

function Write-Json([string]$Path, [hashtable]$Value) {
    $temp = "$Path.tmp"
    $Value | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $temp -Encoding UTF8
    Move-Item -LiteralPath $temp -Destination $Path -Force
}

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Huuuge 数据采集器'
$form.Size = New-Object System.Drawing.Size(900, 590)
$form.MinimumSize = New-Object System.Drawing.Size(820, 550)
$form.StartPosition = 'CenterScreen'
$form.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 10)
$form.BackColor = [System.Drawing.Color]::FromArgb(245, 247, 250)

$title = New-Object System.Windows.Forms.Label
$title.Text = 'Huuuge 数据采集器'
$title.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 20, [System.Drawing.FontStyle]::Bold)
$title.Location = New-Object System.Drawing.Point(24, 18)
$title.AutoSize = $true
$form.Controls.Add($title)

$subtitle = New-Object System.Windows.Forms.Label
$subtitle.Text = '只操作 HuuugeResearch；普通 Pie64 永不用于采集。'
$subtitle.ForeColor = [System.Drawing.Color]::DimGray
$subtitle.Location = New-Object System.Drawing.Point(28, 60)
$subtitle.AutoSize = $true
$form.Controls.Add($subtitle)

$statusPanel = New-Object System.Windows.Forms.Panel
$statusPanel.Location = New-Object System.Drawing.Point(24, 92)
$statusPanel.Size = New-Object System.Drawing.Size(835, 74)
$statusPanel.BackColor = [System.Drawing.Color]::White
$statusPanel.BorderStyle = 'FixedSingle'
$form.Controls.Add($statusPanel)

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = '状态：检查中...'
$statusLabel.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 15, [System.Drawing.FontStyle]::Bold)
$statusLabel.Location = New-Object System.Drawing.Point(16, 12)
$statusLabel.AutoSize = $true
$statusPanel.Controls.Add($statusLabel)

$sessionLabel = New-Object System.Windows.Forms.Label
$sessionLabel.Text = 'Session：—'
$sessionLabel.Location = New-Object System.Drawing.Point(18, 45)
$sessionLabel.AutoSize = $true
$statusPanel.Controls.Add($sessionLabel)

function New-ActionButton([string]$Text, [int]$X, [int]$Y, [int]$Width = 250) {
    $button = New-Object System.Windows.Forms.Button
    $button.Text = $Text
    $button.Location = New-Object System.Drawing.Point($X, $Y)
    $button.Size = New-Object System.Drawing.Size($Width, 52)
    $button.FlatStyle = 'Flat'
    $button.BackColor = [System.Drawing.Color]::White
    $button.FlatAppearance.BorderColor = [System.Drawing.Color]::FromArgb(190, 198, 208)
    $form.Controls.Add($button)
    return $button
}

$startButton = New-ActionButton '1. 开始采集' 24 188
$stopButton = New-ActionButton '2. 结束采集并整理' 306 188
$recentButton = New-ActionButton '3. 查看最近结果' 588 188
$repairButton = New-ActionButton '4. 环境检查 / 修复' 24 252
$aiButton = New-ActionButton '5. AI 接管' 306 252
$guideButton = New-ActionButton '6. 打开说明' 588 252
$startButton.BackColor = [System.Drawing.Color]::FromArgb(220, 247, 230)
$stopButton.BackColor = [System.Drawing.Color]::FromArgb(255, 235, 230)

$settingsGroup = New-Object System.Windows.Forms.GroupBox
$settingsGroup.Text = '本机设置'
$settingsGroup.Location = New-Object System.Drawing.Point(24, 322)
$settingsGroup.Size = New-Object System.Drawing.Size(835, 72)
$form.Controls.Add($settingsGroup)

$aiLabel = New-Object System.Windows.Forms.Label
$aiLabel.Text = 'AI：'
$aiLabel.Location = New-Object System.Drawing.Point(16, 31)
$aiLabel.AutoSize = $true
$settingsGroup.Controls.Add($aiLabel)

$aiCombo = New-Object System.Windows.Forms.ComboBox
$aiCombo.DropDownStyle = 'DropDownList'
$aiCombo.Items.AddRange(@('自动', 'Codex', 'Trae + DeepSeek', '不使用 AI'))
$aiCombo.SelectedIndex = 0
$aiCombo.Location = New-Object System.Drawing.Point(56, 25)
$aiCombo.Size = New-Object System.Drawing.Size(180, 32)
$settingsGroup.Controls.Add($aiCombo)

$captureLabel = New-Object System.Windows.Forms.Label
$captureLabel.Text = '本地 Raw 目录：'
$captureLabel.Location = New-Object System.Drawing.Point(260, 31)
$captureLabel.AutoSize = $true
$settingsGroup.Controls.Add($captureLabel)

$captureText = New-Object System.Windows.Forms.TextBox
$captureText.Location = New-Object System.Drawing.Point(370, 25)
$captureText.Size = New-Object System.Drawing.Size(330, 32)
$settingsGroup.Controls.Add($captureText)

$saveSettingsButton = New-Object System.Windows.Forms.Button
$saveSettingsButton.Text = '保存'
$saveSettingsButton.Location = New-Object System.Drawing.Point(716, 23)
$saveSettingsButton.Size = New-Object System.Drawing.Size(98, 36)
$settingsGroup.Controls.Add($saveSettingsButton)

$logBox = New-Object System.Windows.Forms.TextBox
$logBox.Location = New-Object System.Drawing.Point(24, 408)
$logBox.Size = New-Object System.Drawing.Size(835, 130)
$logBox.Multiline = $true
$logBox.ReadOnly = $true
$logBox.ScrollBars = 'Vertical'
$logBox.BackColor = [System.Drawing.Color]::FromArgb(30, 34, 40)
$logBox.ForeColor = [System.Drawing.Color]::Gainsboro
$logBox.Font = New-Object System.Drawing.Font('Consolas', 9)
$form.Controls.Add($logBox)

function Append-Log([string]$Text) {
    $logBox.AppendText("[$(Get-Date -Format 'HH:mm:ss')] $Text`r`n")
    $logBox.SelectionStart = $logBox.TextLength
    $logBox.ScrollToCaret()
}

function Load-Settings {
    $settings = Read-Json $SettingsPath
    if ($null -eq $settings) {
        $captureText.Text = 'C:\huuuge_research\captures'
        return
    }
    $captureText.Text = [string]$settings.capture_root
    switch ([string]$settings.ai_provider) {
        'Codex' { $aiCombo.SelectedIndex = 1 }
        'Trae' { $aiCombo.SelectedIndex = 2 }
        'None' { $aiCombo.SelectedIndex = 3 }
        default { $aiCombo.SelectedIndex = 0 }
    }
}

function Save-Settings {
    $old = Read-Json $SettingsPath
    $provider = @('Auto', 'Codex', 'Trae', 'None')[$aiCombo.SelectedIndex]
    $settings = [ordered]@{
        adb_path = if ($old -and $old.adb_path) { [string]$old.adb_path } else { 'C:\platform-tools\adb.exe' }
        capture_root = $captureText.Text.Trim()
        frida_server_path = if ($old -and $old.frida_server_path) { [string]$old.frida_server_path } else { 'C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64' }
        ai_provider = $provider
        trae_path = if ($old -and $old.trae_path) { [string]$old.trae_path } else { Join-Path $env:LOCALAPPDATA 'Programs\Trae CN\Trae CN.exe' }
    }
    if ([string]::IsNullOrWhiteSpace($settings.capture_root)) { throw 'Raw 目录不能为空。' }
    Write-Json $SettingsPath $settings
    Append-Log '设置已保存（不包含密码或 API Key）。'
}

function Refresh-Status {
    $active = Read-Json $ActivePath
    if ($null -ne $active) {
        $state = Read-Json ([string]$active.state_file)
        if ($null -ne $state) {
            $sessionLabel.Text = "Session：$($state.session_id)｜RPC $($state.message_count)｜Decoded $($state.decoded_count)"
            if ($state.status -eq 'ready') {
                $statusLabel.Text = 'READY，可以开始玩了'
                $statusLabel.ForeColor = [System.Drawing.Color]::ForestGreen
                $startButton.Enabled = $false
                $stopButton.Enabled = $true
                return
            }
            $statusLabel.Text = "状态：$($state.status)"
            $statusLabel.ForeColor = [System.Drawing.Color]::DarkOrange
            $startButton.Enabled = $false
            $stopButton.Enabled = $true
            return
        }
    }
    $last = Read-Json $LastPath
    $statusLabel.Text = '环境待命，当前未采集'
    $statusLabel.ForeColor = [System.Drawing.Color]::SteelBlue
    $sessionLabel.Text = if ($last) { "最近：$($last.session_id)｜RPC $($last.message_count)" } else { 'Session：—' }
    $startButton.Enabled = $true
    $stopButton.Enabled = $false
}

$script:ActionProcess = $null
$script:ActionOutputPath = $null
$script:ActionErrorPath = $null
$script:ActionName = $null

function Complete-Controller {
    if ($null -eq $script:ActionProcess) { return }
    $script:ActionProcess.Refresh()
    if (-not $script:ActionProcess.HasExited) { return }

    $stdout = if (Test-Path -LiteralPath $script:ActionOutputPath) { Get-Content -LiteralPath $script:ActionOutputPath -Raw -ErrorAction SilentlyContinue } else { '' }
    $stderr = if (Test-Path -LiteralPath $script:ActionErrorPath) { Get-Content -LiteralPath $script:ActionErrorPath -Raw -ErrorAction SilentlyContinue } else { '' }
    $combined = (@($stdout, $stderr) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }) -join "`r`n"
    if (-not [string]::IsNullOrWhiteSpace($combined)) { Append-Log $combined.Trim() }
    $exitCode = $script:ActionProcess.ExitCode
    $actionName = $script:ActionName
    $script:ActionProcess.Dispose()
    $script:ActionProcess = $null
    foreach ($button in @($startButton,$stopButton,$recentButton,$repairButton,$aiButton,$guideButton)) { $button.Enabled = $true }
    if ($exitCode -ne 0) {
        $message = if ([string]::IsNullOrWhiteSpace($combined)) { "$actionName 退出码：$exitCode" } else { $combined }
        [System.Windows.Forms.MessageBox]::Show($message, '操作未完成', 'OK', 'Warning') | Out-Null
    }
    Refresh-Status
}

function Run-Controller([string]$Action, [string]$Provider = '') {
    if ($null -ne $script:ActionProcess) { return }
    try { Save-Settings } catch { [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, '设置错误') | Out-Null; return }
    foreach ($button in @($startButton,$stopButton,$recentButton,$repairButton,$aiButton,$guideButton)) { $button.Enabled = $false }
    Append-Log "开始：$Action"
    $guiRuntime = Join-Path $RepoRoot '.local\gui'
    New-Item -ItemType Directory -Force -Path $guiRuntime | Out-Null
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $script:ActionOutputPath = Join-Path $guiRuntime "$stamp.stdout.log"
    $script:ActionErrorPath = Join-Path $guiRuntime "$stamp.stderr.log"
    $script:ActionName = $Action
    $arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $Controller, '-RepoRoot', $RepoRoot, '-Action', $Action)
    if ($Provider) { $arguments += @('-AIProvider', $Provider) }
    try {
        $script:ActionProcess = Start-Process powershell.exe -ArgumentList $arguments -RedirectStandardOutput $script:ActionOutputPath -RedirectStandardError $script:ActionErrorPath -WindowStyle Hidden -PassThru
    } catch {
        foreach ($button in @($startButton,$stopButton,$recentButton,$repairButton,$aiButton,$guideButton)) { $button.Enabled = $true }
        Append-Log "启动失败：$($_.Exception.Message)"
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, '操作失败', 'OK', 'Error') | Out-Null
    }
}

$startButton.Add_Click({ Run-Controller 'Start' })
$stopButton.Add_Click({ Run-Controller 'Stop' })
$recentButton.Add_Click({ Run-Controller 'Recent' })
$repairButton.Add_Click({ Run-Controller 'Preflight' })
$aiButton.Add_Click({ Run-Controller 'AI' @('Auto','Codex','Trae','None')[$aiCombo.SelectedIndex] })
$guideButton.Add_Click({ Start-Process (Join-Path $RepoRoot 'HUUUGE_DATA_COLLECTION_GUIDE.md') })
$saveSettingsButton.Add_Click({ try { Save-Settings } catch { [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, '设置错误') | Out-Null } })

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 2000
$timer.Add_Tick({ Complete-Controller; Refresh-Status })
$timer.Start()

Load-Settings
Refresh-Status
Append-Log 'GUI 已启动。采集不依赖 AI；AI 可选 Codex 或 Trae + DeepSeek。'
$script:BootstrapRequested = [bool]$BootstrapOnLoad
$form.Add_Shown({
    if ($script:BootstrapRequested) {
        $script:BootstrapRequested = $false
        Run-Controller 'Preflight'
    }
})
[void]$form.ShowDialog()
