param(
  [Parameter(Mandatory=$true)]
  [string]$ServerPath
)
$adb = "C:\platform-tools\adb.exe"
if (-not (Test-Path $ServerPath)) {
  Write-Host "frida-server file not found: $ServerPath" -ForegroundColor Red
  exit 1
}

& $adb push $ServerPath /data/local/tmp/huuuge-fs
& $adb shell chmod 755 /data/local/tmp/huuuge-fs

Write-Host "Trying root shell..."
& $adb shell "su -c '/data/local/tmp/huuuge-fs >/dev/null 2>&1 &'"
Start-Sleep -Seconds 2

Write-Host "Testing Frida process list..."
frida-ps -U
