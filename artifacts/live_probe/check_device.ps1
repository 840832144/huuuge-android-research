$adb = "C:\platform-tools\adb.exe"
if (-not (Test-Path $adb)) {
  Write-Host "ADB not found at $adb" -ForegroundColor Red
  exit 1
}

Write-Host "=== ADB devices ==="
& $adb devices
Write-Host "`n=== ABI ==="
& $adb shell getprop ro.product.cpu.abilist
Write-Host "`n=== Android ==="
& $adb shell getprop ro.build.version.release
Write-Host "`n=== shell uid ==="
& $adb shell id
Write-Host "`n=== adb root test ==="
& $adb root
Start-Sleep -Seconds 1
& $adb shell id
Write-Host "`n=== su test ==="
& $adb shell su -c id
