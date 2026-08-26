@echo off
setlocal EnableExtensions
for %%I in ("%~dp0.") do set "REPO_DIR=%%~fI"
if not exist "%REPO_DIR%\scripts\huuuge_gui.ps1" (
  echo [ERROR] Missing scripts\huuuge_gui.ps1
  pause
  exit /b 1
)
start "Huuuge Collector" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -File "%REPO_DIR%\scripts\huuuge_gui.ps1" -RepoRoot "%REPO_DIR%"
exit /b 0
