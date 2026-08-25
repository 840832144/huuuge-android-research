param(
    [switch]$Json
)

$ErrorActionPreference = "Stop"

$registryCandidates = @(
    "HKLM:\SOFTWARE\BlueStacks_nxt_cn",
    "HKLM:\SOFTWARE\BlueStacks_nxt",
    "HKLM:\SOFTWARE\WOW6432Node\BlueStacks_nxt_cn",
    "HKLM:\SOFTWARE\WOW6432Node\BlueStacks_nxt"
)

$install = $null
foreach ($candidate in $registryCandidates) {
    if (Test-Path $candidate) {
        $install = Get-ItemProperty $candidate
        break
    }
}

if (-not $install) {
    throw "BlueStacks registry metadata was not found in the supported registry locations."
}

$installDir = [string]$install.InstallDir
$engineDir = [string]$install.DataDir
$dataRoot = [string]$install.UserDefinedDir
if (-not $dataRoot -and $engineDir) {
    $dataRoot = Split-Path -Parent $engineDir.TrimEnd('\')
}

$configPath = Join-Path $dataRoot "bluestacks.conf"
if (-not (Test-Path -LiteralPath $configPath)) {
    throw "BlueStacks config was not found at the registry-derived path: $configPath"
}

$config = @{}
foreach ($line in Get-Content -LiteralPath $configPath -Encoding UTF8) {
    if ($line -match '^(?<key>[^=]+)="(?<value>.*)"$') {
        $config[$Matches.key] = $Matches.value
    }
}

$instanceNames = @(
    $config.Keys |
        Where-Object { $_ -match '^bst\.instance\.([^.]+)\.display_name$' } |
        ForEach-Object { [regex]::Match($_, '^bst\.instance\.([^.]+)\.').Groups[1].Value } |
        Sort-Object -Unique
)

$runningPlayers = @(
    Get-Process HD-Player -ErrorAction SilentlyContinue |
        Select-Object Id, StartTime, MainWindowTitle
)

$instances = foreach ($instance in $instanceNames) {
    $prefix = "bst.instance.$instance."
    $displayName = $config[$prefix + "display_name"]
    $folder = Join-Path $engineDir $instance
    $matchingPlayer = @($runningPlayers | Where-Object { $_.MainWindowTitle -eq $displayName })

    [pscustomobject]@{
        Id = $instance
        DisplayName = $displayName
        AdbPort = $config[$prefix + "adb_port"]
        StatusAdbPort = $config[$prefix + "status.adb_port"]
        AbiList = $config[$prefix + "abi_list"]
        RootFlag = $config[$prefix + "enable_root_access"]
        FirstBoot = $config[$prefix + "first_boot"]
        Folder = $folder
        FolderExists = Test-Path -LiteralPath $folder
        Running = $matchingPlayer.Count -gt 0
        ProcessId = if ($matchingPlayer.Count -eq 1) { $matchingPlayer[0].Id } else { $null }
    }
}

$result = [pscustomobject]@{
    Version = [string]$install.Version
    RegistryKey = $install.PSPath
    InstallDir = $installDir
    DataRoot = $dataRoot
    EngineDir = $engineDir
    LogDir = [string]$install.LogDir
    ConfigPath = $configPath
    GlobalRootingFeature = $config["bst.feature.rooting"]
    Instances = @($instances)
}

if ($Json) {
    $result | ConvertTo-Json -Depth 5
} else {
    $result | Select-Object Version, InstallDir, DataRoot, EngineDir, LogDir, ConfigPath, GlobalRootingFeature | Format-List
    $instances | Format-Table Id, DisplayName, AdbPort, AbiList, RootFlag, FirstBoot, Running, ProcessId, FolderExists -AutoSize
}
