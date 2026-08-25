param(
  [string]$Serial,
  [string]$Package = "com.huuuge.casino.slots"
)

$ErrorActionPreference = "Stop"
$adb = "C:\platform-tools\adb.exe"
if (-not (Test-Path $adb)) {
  throw "ADB not found at $adb"
}

$deviceLines = @(& $adb devices | Select-Object -Skip 1 | Where-Object { $_ -match '\S' })
if (-not $Serial) {
  $online = @($deviceLines | Where-Object { $_ -match '\sdevice$' })
  if ($online.Count -ne 1) {
    throw "Specify -Serial because exactly one online ADB device was not found. Devices: $($deviceLines -join '; ')"
  }
  $Serial = ($online[0] -split '\s+')[0]
}

$target = @("-s", $Serial)
Write-Host "=== Target ==="
Write-Host $Serial
& $adb @target get-state

Write-Host "`n=== Android / ABI / native bridge ==="
foreach ($prop in @(
  "ro.build.version.release",
  "ro.build.version.sdk",
  "ro.product.cpu.abi",
  "ro.product.cpu.abilist",
  "ro.dalvik.vm.native.bridge",
  "ro.debuggable",
  "ro.secure",
  "bst.enable_root_access",
  "bst.config.bindmount"
)) {
  $value = & $adb @target shell getprop $prop
  Write-Host "$prop=$value"
}

Write-Host "`n=== Shell identity ==="
& $adb @target shell id

Write-Host "`n=== Root command diagnostics (no adb root side effect) ==="
foreach ($su in @("/system/xbin/bstk/su", "/system/xbin/su")) {
  $result = & $adb @target shell "$su -c 'id'; echo exit=`$?" 2>&1
  Write-Host "[$su] $($result -join ' ')"
}

Write-Host "`n=== Huuuge package / process ==="
& $adb @target shell pm path $Package
$appPid = ((& $adb @target shell pidof $Package) -join "").Trim()
Write-Host "pid=$appPid"
& $adb @target shell dumpsys package $Package |
  Select-String -Pattern "primaryCpuAbi|secondaryCpuAbi|legacyNativeLibraryDir|versionName|versionCode"
