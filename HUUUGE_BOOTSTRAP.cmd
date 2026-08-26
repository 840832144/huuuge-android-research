@echo off
setlocal EnableExtensions
chcp 65001 >nul
title Huuuge Research Bootstrap

set "DEFAULT_REPO=C:\huuuge_research"
set "REPO_URL=https://github.com/840832144/huuuge-android-research.git"

echo.
echo ================================================
echo   Huuuge Casino Data Research - Bootstrap
echo ================================================
echo.

rem If this CMD is already inside the repository, use the current repository.
if exist "%~dp0scripts\huuuge_bootstrap.ps1" (
  set "REPO_DIR=%~dp0"
  goto :RUN_BOOTSTRAP
)

if defined HUUUGE_REPO_DIR (
  set "REPO_DIR=%HUUUGE_REPO_DIR%"
) else (
  set "REPO_DIR=%DEFAULT_REPO%"
)

where git >nul 2>nul
if errorlevel 1 (
  echo [INFO] Git is not installed or not on PATH.
  where winget >nul 2>nul
  if errorlevel 1 (
    echo [ERROR] Git is required and winget is not available.
    echo Install Git for Windows, then run this file again.
    goto :FAIL
  )
  set /p INSTALL_GIT="Install Git for Windows with winget now? [Y/N]: "
  if /I not "%INSTALL_GIT%"=="Y" goto :FAIL
  winget install --id Git.Git -e --source winget
  if errorlevel 1 goto :FAIL
  set "PATH=%PATH%;C:\Program Files\Git\cmd"
)

if not exist "%REPO_DIR%\.git" (
  echo [STEP] Cloning private research repository to %REPO_DIR%
  echo [NOTE] The first clone may open GitHub authentication once.
  git clone "%REPO_URL%" "%REPO_DIR%"
  if errorlevel 1 goto :FAIL
) else (
  echo [OK] Existing repository found: %REPO_DIR%
)

:RUN_BOOTSTRAP
if not exist "%REPO_DIR%\scripts\huuuge_bootstrap.ps1" (
  echo [ERROR] Bootstrap PowerShell script is missing.
  goto :FAIL
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%REPO_DIR%\scripts\huuuge_bootstrap.ps1" -RepoRoot "%REPO_DIR%"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo [DONE] Bootstrap/preflight finished.
  echo Repository: %REPO_DIR%
) else (
  echo [WARN] Bootstrap finished with code %RC%.
  echo Check %REPO_DIR%\.local\bootstrap\ for the report.
)
echo.
pause
exit /b %RC%

:FAIL
echo.
echo [STOP] Bootstrap could not continue.
echo No BlueStacks root/host patch was performed by this launcher.
echo.
pause
exit /b 1
