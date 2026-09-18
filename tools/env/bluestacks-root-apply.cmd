@echo off
rem BlueStacks root standardization launcher (double-click safe).
rem ASCII-only on purpose; Chinese output comes from the Python script.
rem   no argument        -> check  <first instance found>
rem   apply <instance>   -> patch (needs an Administrator terminal)
rem   revert             -> restore from the upstream .prepatch.bak backups
setlocal EnableExtensions
chcp 65001 >nul 2>&1

set "PY="
where py >nul 2>&1 && for /f "delims=" %%i in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do set "PY=%%i"
if not defined PY for /f "delims=" %%i in ('where python 2^>nul') do if not defined PY set "PY=%%i"
if not defined PY (
  echo [x] Python not found. Install Python 3.11+.
  pause
  exit /b 1
)

set "SCRIPT=%~dp0bluestacks_root.py"
set "ARGS="
if /i "%~1"=="apply"  set "ARGS=apply %~2"
if /i "%~1"=="revert" set "ARGS=revert"
if /i "%~1"=="check"  set "ARGS=check %~2"
if "%~1"=="" set "ARGS=check Pie64_1"

echo Using Python: %PY%
"%PY%" "%SCRIPT%" %ARGS%
echo.
pause
