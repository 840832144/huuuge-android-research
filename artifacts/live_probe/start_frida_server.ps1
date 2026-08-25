param(
  [Parameter(Mandatory=$true)]
  [string]$ServerPath,
  [string]$Serial,
  [string]$RemotePath = "/data/local/tmp/huuuge-fs",
  [switch]$DiagnosticShellMode
)

$ErrorActionPreference = "Stop"
$adb = "C:\platform-tools\adb.exe"
if (-not (Test-Path $ServerPath)) {
  throw "frida-server file not found: $ServerPath"
}
if (-not (Test-Path $adb)) {
  throw "ADB not found at $adb"
}

if (-not $Serial) {
  $online = @(& $adb devices | Select-Object -Skip 1 | Where-Object { $_ -match '\sdevice$' })
  if ($online.Count -ne 1) {
    throw "Specify -Serial because exactly one online ADB device was not found."
  }
  $Serial = ($online[0] -split '\s+')[0]
}

$target = @("-s", $Serial)
& $adb @target get-state | Out-Null
& $adb @target push $ServerPath $RemotePath
& $adb @target shell chmod 755 $RemotePath

$serverVersion = (& $adb @target shell "$RemotePath --version").Trim()
$hostVersion = (py -c "import frida; print(frida.__version__)").Trim()
Write-Host "Host Frida:   $hostVersion"
Write-Host "Server Frida: $serverVersion"
if ($hostVersion -ne $serverVersion) {
  throw "Host/server Frida version mismatch."
}

$rootLauncher = $null
foreach ($su in @("/system/xbin/bstk/su", "/system/xbin/su")) {
  $identity = (& $adb @target shell "$su -c 'id'" 2>&1) -join " "
  if ($identity -match 'uid=0\(root\)') {
    $rootLauncher = $su
    break
  }
}

if ($rootLauncher) {
  Write-Host "Starting frida-server through $rootLauncher"
  & $adb @target shell "$rootLauncher -c '$RemotePath -D >$RemotePath.log 2>&1 </dev/null'"
} elseif ($DiagnosticShellMode) {
  Write-Warning "Starting frida-server as shell for enumeration diagnostics only; attaching to Huuuge is expected to fail."
  & $adb @target shell "$RemotePath -D >$RemotePath.log 2>&1 </dev/null"
} else {
  throw "No usable root launcher. Re-run only after a root command returns uid=0, or use -DiagnosticShellMode to prove enumeration/permission behavior."
}

Write-Host "Testing Frida process list..."
$fridaPs = Get-Command frida-ps -ErrorAction SilentlyContinue
if ($fridaPs) {
  & $fridaPs.Source -D $Serial
} else {
  py -c "import frida; d=frida.get_device_manager().get_device('$Serial', timeout=10); print('Device:', d.name); print('Processes:', len(d.enumerate_processes()))"
}
