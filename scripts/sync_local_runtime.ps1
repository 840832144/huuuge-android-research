$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$probe = Join-Path $repo "artifacts\live_probe"
New-Item -ItemType Directory -Force -Path $probe | Out-Null

$descCandidates = @(
  "C:\huuuge_live_probe\huuuge_descriptors.pb",
  "C:\huuuge_research\artifacts\live_probe\huuuge_descriptors.pb"
)

$found = $null
foreach ($p in $descCandidates) {
  if (Test-Path $p) { $found = $p; break }
}

if ($found) {
  Copy-Item $found (Join-Path $probe "huuuge_descriptors.pb") -Force
  Write-Host "[OK] descriptor synced from $found"
} else {
  Write-Warning "No local huuuge_descriptors.pb found. If recovered .proto files are present, run: py scripts\build_descriptors.py"
}

$apkDir = "C:\huuuge_apk"
if (Test-Path $apkDir) {
  Write-Host "[OK] APK directory exists: $apkDir"
  Get-ChildItem $apkDir -Filter *.apk | Select-Object Name,Length,FullName
} else {
  Write-Warning "APK directory not found at $apkDir"
}

$adb = "C:\platform-tools\adb.exe"
if (Test-Path $adb) {
  Write-Host "[OK] ADB: $adb"
  & $adb devices
} else {
  Write-Warning "ADB not found at $adb"
}
