@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Huuuge Collector Bootstrap

set "DEFAULT_DIR=C:\HuuugeCollector"
set "SVN_URL=http://140.143.33.242/svn/cr/x_proj_design/trunk/HuuugeCollector"

echo.
echo ================================================
echo   Huuuge Collector - SVN Bootstrap / Update
echo ================================================
echo.

rem Development checkout: Git remains the engineering source of truth.
if exist "%~dp0scripts\huuuge_bootstrap.ps1" (
  for %%I in ("%~dp0.") do set "REPO_DIR=%%~fI"
  if exist "%~dp0.git" goto :RUN
  call :FIND_SVN
  if defined SVN_EXE (
    "%SVN_EXE%" info "%REPO_DIR%" >nul 2>nul
    if not errorlevel 1 (
      echo [STEP] Updating collector from SVN
      "%SVN_EXE%" update "%REPO_DIR%"
      if errorlevel 1 goto :FAIL
    )
  )
  goto :RUN
)

if defined HUUUGE_COLLECTOR_DIR (
  set "REPO_DIR=%HUUUGE_COLLECTOR_DIR%"
) else (
  set "REPO_DIR=%DEFAULT_DIR%"
)

call :FIND_SVN
if not defined SVN_EXE (
  echo [ERROR] SVN command-line client was not found.
  echo Install TortoiseSVN with command-line client tools, then retry.
  goto :FAIL
)

if not exist "%REPO_DIR%\.svn" (
  echo [STEP] Checking out collector from SVN to %REPO_DIR%
  "%SVN_EXE%" checkout "%SVN_URL%" "%REPO_DIR%"
  if errorlevel 1 goto :FAIL
) else (
  echo [STEP] Updating collector from SVN
  "%SVN_EXE%" update "%REPO_DIR%"
  if errorlevel 1 goto :FAIL
)

:RUN
if not exist "%REPO_DIR%\scripts\huuuge_bootstrap.ps1" goto :FAIL

if /I "%~1"=="--console" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%REPO_DIR%\scripts\huuuge_bootstrap.ps1" -RepoRoot "%REPO_DIR%"
  set "RC=!ERRORLEVEL!"
  echo.
  if not "!RC!"=="0" echo [WARN] Preflight failed. Check %REPO_DIR%\.local\bootstrap\
  pause
  exit /b !RC!
)

if not exist "%REPO_DIR%\scripts\huuuge_gui.ps1" goto :FAIL
start "Huuuge Collector" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -File "%REPO_DIR%\scripts\huuuge_gui.ps1" -RepoRoot "%REPO_DIR%" -BootstrapOnLoad
exit /b 0

:FIND_SVN
set "SVN_EXE="
where svn.exe >nul 2>nul && set "SVN_EXE=svn.exe"
if not defined SVN_EXE if exist "C:\Program Files\TortoiseSVN\bin\svn.exe" set "SVN_EXE=C:\Program Files\TortoiseSVN\bin\svn.exe"
exit /b 0

:FAIL
echo.
echo [STOP] Collector could not start.
echo No BlueStacks Root/host patch or normal Pie64 instrumentation was performed.
echo.
pause
exit /b 1
