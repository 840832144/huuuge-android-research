param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$SvnWorkingCopyRoot = 'D:\cr_design',
    [string]$TargetRelativePath = 'HuuugeCollector'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
$SvnWorkingCopyRoot = [IO.Path]::GetFullPath($SvnWorkingCopyRoot.TrimEnd('\'))
$target = Join-Path $SvnWorkingCopyRoot $TargetRelativePath

if (-not (Test-Path (Join-Path $RepoRoot '.git'))) {
    throw "Development source is not a Git checkout: $RepoRoot"
}
if (-not (Test-Path (Join-Path $SvnWorkingCopyRoot '.svn'))) {
    throw "SVN working copy root is invalid: $SvnWorkingCopyRoot"
}

$svnUrl = (& svn info --show-item url $SvnWorkingCopyRoot).Trim()
if ($svnUrl -ne 'http://140.143.33.242/svn/cr/x_proj_design/trunk') {
    throw "Unexpected SVN working copy URL: $svnUrl"
}

$files = @(
    'AGENTS.md',
    'CONTRIBUTING.md',
    'CURRENT_STATUS.md',
    'TASKS.md',
    'CHANGELOG.md',
    'COLLAB_LOG.md',
    'README.md',
    'HUUUGE_COLLECTOR_VERSION.txt',
    'HUUUGE_BOOTSTRAP.cmd',
    'HUUUGE_COLLECTOR.cmd',
    'HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md',
    'HUUUGE_DATA_COLLECTION_GUIDE.md',
    'AGENT_DATA_USAGE_GUIDE.md',
    'HUUUGE_DATA_COLLECTION_OVERVIEW.md',
    'AI_DEPLOYMENT_PLAYBOOK.md',
    'MODULE_STRUCTURE_CATALOG.md',
    'RESEARCH_DATA_ARCHITECTURE.md',
    'scripts\huuuge_bootstrap.ps1',
    'scripts\huuuge_controller.ps1',
    'scripts\huuuge_gui.ps1',
    'scripts\build_installer_package.ps1',
    'scripts\sync_svn_package.ps1',
    'scripts\sync_local_runtime.ps1',
    'scripts\discover_bluestacks.ps1',
    'scripts\build_descriptors.py',
    'scripts\build_rpc_inventory.py',
    'scripts\build_module_catalog.py',
    'artifacts\live_probe\README.md',
    'artifacts\live_probe\requirements.txt',
    'artifacts\live_probe\agent.js',
    'artifacts\live_probe\bootstrap_houdini_gadget.py',
    'artifacts\live_probe\live_decode.py',
    'artifacts\live_probe\check_device.ps1',
    'artifacts\live_probe\start_frida_server.ps1',
    'artifacts\module_catalog\module_specs.json'
)

New-Item -ItemType Directory -Force -Path $target | Out-Null
foreach ($relative in $files) {
    $source = Join-Path $RepoRoot $relative
    if (-not (Test-Path -LiteralPath $source)) { throw "Package source missing: $relative" }
    $destination = Join-Path $target $relative
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Force
}

# The descriptor contains schema structure only (no account/session values) and is
# required for a genuinely SVN-first deployment. It remains an ignored local build
# artifact in Git, but the internal planner package carries the validated copy.
$descriptor = Join-Path $RepoRoot 'artifacts\live_probe\huuuge_descriptors.pb'
if (-not (Test-Path -LiteralPath $descriptor)) {
    throw 'Runtime descriptor is missing. Run HUUUGE_BOOTSTRAP.cmd once before publishing the SVN package.'
}
$descriptorDestination = Join-Path $target 'artifacts\live_probe\huuuge_descriptors.pb'
Copy-Item -LiteralPath $descriptor -Destination $descriptorDestination -Force

$readme = @'
# Huuuge 数据采集器（策划 SVN 包）

日常入口：双击 `HUUUGE_COLLECTOR.cmd`。

首次部署或更新：双击 `HUUUGE_BOOTSTRAP.cmd`。该入口从公司 SVN 更新，不要求策划使用 Git。

策划只使用 GUI 六个主操作，不需要选择正在玩的模块或手工打 marker。采集、READY 验证、停止和整理不依赖 AI；需要解读结果时，让 Codex 或 Trae + DeepSeek 先阅读 `AGENT_DATA_USAGE_GUIDE.md`。

安全边界：仅允许 `Pie64_1 / HuuugeResearch` 采集；普通 `Pie64 / BlueStacks 5` 禁止 Root 或 instrumentation。Raw、账号数据、APK、Frida 二进制和密钥不得提交 SVN。

开发源同步：GitHub 私有仓库 `840832144/huuuge-android-research`。每次工具修改应先通过 Git 规范验证，再运行 `scripts\sync_svn_package.ps1` 同步此 SVN 包并分别提交。
'@
$readme = "新电脑发布包：``release\HuuugeCollector_Installer.zip``。解压后双击其中的 ``HUUUGE_BOOTSTRAP.cmd``。`r`n`r`n策划部署手册：``HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md``。`r`n`r`n" + $readme
Set-Content -LiteralPath (Join-Path $target 'SVN_PACKAGE_README.md') -Value $readme -Encoding UTF8

$releaseDirectory = Join-Path $target 'release'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RepoRoot 'scripts\build_installer_package.ps1') `
    -RepoRoot $RepoRoot -OutputDirectory $releaseDirectory
if ($LASTEXITCODE -ne 0) { throw 'Installer package build failed.' }

& svn add --force $target | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'svn add failed.' }
& svn propset svn:ignore ".local`n.venv`ncaptures`n__pycache__`n*.pyc" $target | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'svn:ignore update failed.' }

Write-Host "SVN package synchronized: $target"
Write-Host "Installer package: $(Join-Path $target 'release\HuuugeCollector_Installer.zip')"
Write-Host 'No SVN commit was performed. Review svn status, then commit only this package path.'
Write-Host 'IMPORTANT: Chinese logs must use the CR Python submit tool or an UTF-8 --file; never pass Chinese directly to svn commit -m.'
