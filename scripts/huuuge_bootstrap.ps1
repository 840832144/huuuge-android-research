param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [ValidateSet('Auto', 'Git', 'Svn', 'None')]
    [string]$SourceMode = 'Auto',
    [ValidateSet('Auto', 'Codex', 'Trae', 'None')]
    [string]$AIProvider = 'Auto',
    [switch]$SkipAI,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Step([string]$Text) {
    Write-Host "`n=== $Text ===" -ForegroundColor Cyan
}

function Write-Ok([string]$Text) {
    Write-Host "[OK] $Text" -ForegroundColor Green
}

function Write-Warn([string]$Text) {
    Write-Warning $Text
}

function Resolve-CommandPath([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) { return $null }
    return $cmd.Source
}

function Test-CommandRunnable([string]$Path, [string[]]$Arguments = @('--version')) {
    try {
        $output = @(& $Path @Arguments 2>&1)
        return [pscustomobject]@{
            Runnable = ($LASTEXITCODE -eq 0)
            ExitCode = $LASTEXITCODE
            Output = ($output -join "`n")
        }
    } catch {
        return [pscustomobject]@{
            Runnable = $false
            ExitCode = -1
            Output = $_.Exception.Message
        }
    }
}

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
if ($SourceMode -eq 'Auto') {
    if (Test-Path (Join-Path $RepoRoot '.git')) { $SourceMode = 'Git' }
    elseif (Get-Command svn -ErrorAction SilentlyContinue) {
        & svn info $RepoRoot *> $null
        if ($LASTEXITCODE -eq 0) { $SourceMode = 'Svn' } else { $SourceMode = 'None' }
    } else { $SourceMode = 'None' }
}
if ($SourceMode -eq 'Git' -and -not (Test-Path (Join-Path $RepoRoot '.git'))) {
    throw "Git source mode selected but this is not a Git repository: $RepoRoot"
}
if ($SourceMode -eq 'Svn') {
    $svnCheck = Resolve-CommandPath 'svn'
    if (-not $svnCheck) { throw 'SVN source mode selected but svn is not available.' }
    & $svnCheck info $RepoRoot *> $null
    if ($LASTEXITCODE -ne 0) { throw "SVN source mode selected but this is not an SVN working copy: $RepoRoot" }
}

$localRoot = Join-Path $RepoRoot '.local\bootstrap'
New-Item -ItemType Directory -Force -Path $localRoot | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$summaryPath = Join-Path $localRoot "bootstrap_$stamp.md"
$lines = New-Object System.Collections.Generic.List[string]
$issues = New-Object System.Collections.Generic.List[string]

function Add-Summary([string]$Line) {
    $script:lines.Add($Line)
}

Add-Summary '# Huuuge Local Bootstrap Report'
Add-Summary ''
Add-Summary "- Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Add-Summary "- Repo: $RepoRoot"
Add-Summary "- Source mode: $SourceMode"

Write-Step '1. Update repository safely'
if ($SourceMode -eq 'Git') {
    $git = Resolve-CommandPath 'git'
    if (-not $git) { throw 'Git is required for this development checkout.' }
    $dirty = @(& $git -C $RepoRoot status --porcelain)
    if ($dirty.Count -gt 0) {
        Write-Warn 'Git working tree has local changes. Preserving them; running fetch only, not pull.'
        & $git -C $RepoRoot fetch origin
        if ($LASTEXITCODE -ne 0) { throw 'git fetch origin failed.' }
        Add-Summary '- Git: local changes detected; fetched remote only.'
    } else {
        & $git -C $RepoRoot pull --ff-only
        if ($LASTEXITCODE -ne 0) { throw 'git pull --ff-only failed.' }
        Write-Ok 'Git repository is up to date.'
        Add-Summary '- Git: clean working tree; fast-forward update completed.'
    }
    $head = (& $git -C $RepoRoot rev-parse HEAD).Trim()
    Add-Summary ('- Git HEAD: `{0}`' -f $head)
} elseif ($SourceMode -eq 'Svn') {
    $svn = Resolve-CommandPath 'svn'
    if (-not $svn) { throw 'SVN command line client is required for the planner package.' }
    $svnDirty = @(& $svn status $RepoRoot | Where-Object { $_ -notmatch '^\?' })
    if ($LASTEXITCODE -ne 0) { throw 'svn status failed.' }
    if ($svnDirty.Count -gt 0) {
        Write-Warn 'SVN working copy has versioned local changes. Preserving them; update was skipped.'
        Add-Summary '- SVN: versioned local changes detected; update skipped.'
    } else {
        & $svn update $RepoRoot | Out-Host
        if ($LASTEXITCODE -ne 0) { throw 'svn update failed.' }
        Write-Ok 'SVN planner package is up to date.'
        Add-Summary '- SVN: clean working copy; update completed.'
    }
    $revision = (& $svn info --show-item revision $RepoRoot).Trim()
    Add-Summary ('- SVN revision: `{0}`' -f $revision)
} else {
    Write-Warn 'No Git/SVN metadata was found. Continuing without source update.'
    Add-Summary '- Source update: skipped (unmanaged directory).'
}

Write-Step '2. Create/verify isolated Python environment'
$hostPython = Resolve-CommandPath 'py'
if (-not $hostPython) { $hostPython = Resolve-CommandPath 'python' }
if (-not $hostPython) {
    Write-Warn 'Python was not found. Install Python 3, then rerun bootstrap.'
    Add-Summary '- Python: MISSING'
    $issues.Add('Python 3 is missing.')
} else {
    $venv = Join-Path $RepoRoot '.venv'
    $venvPython = Join-Path $venv 'Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        Write-Host "Creating .venv ..."
        if ([IO.Path]::GetFileName($hostPython) -ieq 'py.exe') {
            & $hostPython -3 -m venv $venv
        } else {
            & $hostPython -m venv $venv
        }
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython)) {
            throw 'Failed to create Python virtual environment.'
        }
    }

    $requirements = Join-Path $RepoRoot 'artifacts\live_probe\requirements.txt'
    & $venvPython -m pip install -U pip | Out-Host
    & $venvPython -m pip install -r $requirements | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Failed to install Python requirements.' }
    Write-Ok "Python environment ready: $venvPython"
    Add-Summary '- Python: READY (`.venv`)'
}

Write-Step '3. Sync local runtime artifacts'
$syncScript = Join-Path $RepoRoot 'scripts\sync_local_runtime.ps1'
try {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $syncScript 2>&1 |
        Tee-Object -FilePath (Join-Path $localRoot "sync_runtime_$stamp.txt") | Out-Host
    Add-Summary '- Runtime sync: completed; see local sync log.'
} catch {
    Write-Warn "Runtime sync reported a problem: $($_.Exception.Message)"
    Add-Summary '- Runtime sync: incomplete; see local sync log.'
}

$descriptor = Join-Path $RepoRoot 'artifacts\live_probe\huuuge_descriptors.pb'
if (-not (Test-Path $descriptor)) {
    $buildDescriptors = Join-Path $RepoRoot 'scripts\build_descriptors.py'
    if ((Test-Path $buildDescriptors) -and (Test-Path (Join-Path $RepoRoot '.venv\Scripts\python.exe'))) {
        Write-Host 'Descriptor not found; attempting reproducible build from recovered schemas ...'
        & (Join-Path $RepoRoot '.venv\Scripts\python.exe') $buildDescriptors | Out-Host
    }
}
if (Test-Path $descriptor) {
    Write-Ok 'Descriptor set is available.'
    Add-Summary '- Descriptor: READY'
} else {
    Write-Warn 'Descriptor set is still missing. Local AI should resolve recovered-schema/runtime state.'
    Add-Summary '- Descriptor: MISSING'
    $issues.Add('Protobuf descriptor is missing.')
}

Write-Step '4. Discover BlueStacks / research environment'
$discoverScript = Join-Path $RepoRoot 'scripts\discover_bluestacks.ps1'
$discoverLog = Join-Path $localRoot "bluestacks_$stamp.txt"
try {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $discoverScript 2>&1 |
        Tee-Object -FilePath $discoverLog | Out-Host
    Add-Summary '- BlueStacks discovery: completed.'
} catch {
    Write-Warn "BlueStacks discovery failed: $($_.Exception.Message)"
    Add-Summary '- BlueStacks discovery: FAILED'
    $issues.Add('BlueStacks discovery failed.')
}

Write-Step '5. Check known research ADB target (read-only)'
$adb = 'C:\platform-tools\adb.exe'
$checkDevice = Join-Path $RepoRoot 'artifacts\live_probe\check_device.ps1'
$deviceLog = Join-Path $localRoot "device_5565_$stamp.txt"
if (Test-Path $adb) {
    try {
        & $adb connect '127.0.0.1:5565' | Out-Host
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $checkDevice -Serial '127.0.0.1:5565' 2>&1 |
            Tee-Object -FilePath $deviceLog | Out-Host
        Write-Ok 'Research device check completed.'
        Add-Summary '- Research ADB 127.0.0.1:5565: checked.'
    } catch {
        Write-Warn 'Research ADB target is not ready yet. This is normal on a new machine before the research instance is created/started.'
        Add-Summary '- Research ADB 127.0.0.1:5565: NOT READY / requires local deployment.'
        $issues.Add('Research ADB target 127.0.0.1:5565 is not ready.')
    }
} else {
    Write-Warn 'ADB not found at C:\platform-tools\adb.exe.'
    Add-Summary '- ADB: MISSING at validated path.'
    $issues.Add('ADB is missing at C:\platform-tools\adb.exe.')
}

Write-Step '6. Check pinned Frida runtime (read-only)'
$expectedFridaVersion = '17.17.0'
$venvPython = Join-Path $RepoRoot '.venv\Scripts\python.exe'
$fridaServer = 'C:\huuuge_research\tools\frida-17.17.0\frida-server-17.17.0-android-x86_64'
if (Test-Path -LiteralPath $venvPython) {
    $hostFridaVersion = ((& $venvPython -c 'import frida; print(frida.__version__)' 2>$null) -join '').Trim()
    if ($LASTEXITCODE -eq 0 -and $hostFridaVersion -eq $expectedFridaVersion) {
        Write-Ok "Host Frida version is pinned: $hostFridaVersion"
        Add-Summary "- Host Frida: READY ($hostFridaVersion)"
    } else {
        Write-Warn "Host Frida must be $expectedFridaVersion; observed: $hostFridaVersion"
        Add-Summary "- Host Frida: MISMATCH / expected $expectedFridaVersion, observed $hostFridaVersion"
        $issues.Add("Host Frida is not pinned to $expectedFridaVersion.")
    }
} else {
    Add-Summary '- Host Frida: NOT CHECKED (Python environment missing)'
}

if (Test-Path -LiteralPath $fridaServer) {
    Write-Ok 'Pinned x86_64 Frida server file is available.'
    Add-Summary '- Local x86_64 Frida server: READY'
} else {
    Write-Warn "Pinned Frida server is missing: $fridaServer"
    Add-Summary '- Local x86_64 Frida server: MISSING'
    $issues.Add('Pinned x86_64 Frida server file is missing from the local runtime directory.')
}

if (Test-Path -LiteralPath $adb) {
    $deviceState = ((& $adb -s '127.0.0.1:5565' get-state 2>$null) -join '').Trim()
    if ($deviceState -eq 'device') {
        $packagePathLine = @(& $adb -s '127.0.0.1:5565' shell 'pm path com.huuuge.casino.slots' 2>$null) |
            Where-Object { $_ -match 'base\.apk' } | Select-Object -First 1
        if ($packagePathLine) {
            $appDir = ($packagePathLine -replace '^package:', '' -replace '/base\.apk\s*$', '').Trim()
            $gadgetPath = "$appDir/lib/arm64/libhuuuge-gadget.so"
            $gadgetCheck = ((& $adb -s '127.0.0.1:5565' shell "/system/xbin/bstk/su -c 'test -f $gadgetPath && echo OK'" 2>$null) -join '').Trim()
            if ($gadgetCheck -eq 'OK') {
                Write-Ok 'ARM64 Gadget is staged in the research app directory.'
                Add-Summary '- Research ARM64 Gadget: READY'
            } else {
                Write-Warn 'ARM64 Gadget is not staged in the research app directory.'
                Add-Summary '- Research ARM64 Gadget: MISSING / one-time approved setup required'
                $issues.Add('Research ARM64 Gadget is not staged.')
            }
        } else {
            Add-Summary '- Huuuge in research instance: MISSING'
            $issues.Add('Huuuge Casino is not installed in the research instance.')
        }
    } else {
        Add-Summary '- Research Frida/Gadget state: NOT CHECKED (device offline)'
    }
}

Write-Step '7. Prepare local-AI handoff'
$aiPromptPath = Join-Path $localRoot 'CODEX_BOOTSTRAP_PROMPT.md'
$aiOutputPath = Join-Path $localRoot "codex_preflight_$stamp.txt"
$aiPrompt = @'
You are the local deployment assistant for the Huuuge Casino research collector.

Read these files in order before doing anything:
1. AGENTS.md
2. CONTRIBUTING.md
3. HUUUGE_DATA_COLLECTION_GUIDE.md
4. AI_DEPLOYMENT_PLAYBOOK.md
5. CURRENT_STATUS.md
6. latest COLLAB_LOG.md
7. TASKS.md
8. CHANGELOG.md

Then inspect the local preflight files under .local/bootstrap generated in this run.

This is a SAFE PREFLIGHT ONLY. Do not modify BlueStacks host binaries, VHDX files, root state, account data, game data, or server state in this step. Do not install third-party binaries in this step.

Return a concise Chinese deployment assessment for a game designer:
- current deployment state S0-S8 from AI_DEPLOYMENT_PLAYBOOK.md;
- what is already READY;
- exact next action;
- whether explicit user approval is required before any machine-level change;
- if the environment is already research-ready, say READY and identify the next capture action.

Do not ask the user to paste terminal output that you can inspect locally.
'@
Set-Content -Path $aiPromptPath -Value $aiPrompt -Encoding UTF8
Add-Summary '- AI prompt: `.local/bootstrap/CODEX_BOOTSTRAP_PROMPT.md`'

$codex = Resolve-CommandPath 'codex'
if ($SkipAI -or $AIProvider -eq 'None') {
    Write-Warn 'Local AI step skipped by -SkipAI.'
    Add-Summary '- Codex preflight: skipped.'
} elseif ($AIProvider -eq 'Trae' -or ($AIProvider -eq 'Auto' -and -not $codex)) {
    Write-Host 'Trae handoff selected. The GUI can open Trae with this repository and the generated safe-preflight prompt.'
    Add-Summary '- AI preflight: Trae handoff prompt prepared; interactive review remains in Trae.'
} elseif ($codex) {
    $codexProbe = Test-CommandRunnable -Path $codex
    if (-not $codexProbe.Runnable) {
        Write-Warn "A Codex executable was detected but cannot be launched: $($codexProbe.Output)"
        Add-Summary '- Codex preflight: executable detected but not runnable; use Trae or install/login to Codex CLI.'
    } else {
    Write-Host "Runnable Codex CLI detected: $codex"
    Write-Host 'Running non-interactive SAFE preflight in a read-only sandbox.'
    Push-Location $RepoRoot
    try {
        Get-Content -Raw $aiPromptPath | & $codex exec --sandbox read-only - 2>&1 |
            Tee-Object -FilePath $aiOutputPath | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-Ok 'Codex preflight completed.'
            Add-Summary ('- Codex preflight: completed; see `.local/bootstrap/{0}`.' -f [IO.Path]::GetFileName($aiOutputPath))
        } else {
            Write-Warn "Codex preflight exited with code $LASTEXITCODE. The user may need to run Codex CLI once and sign in."
            Add-Summary "- Codex preflight: exit code $LASTEXITCODE; login/setup may be required."
        }
    } finally {
        Pop-Location
    }
    }
} else {
    Write-Warn 'No supported local AI CLI is runnable. This does not block the safe bootstrap.'
    Add-Summary '- AI: no runnable CLI; use the GUI Trae handoff or install/login to Codex CLI.'
}

Write-Step '8. Finish'
Add-Summary ''
Add-Summary '## Result'
Add-Summary ''
if ($issues.Count -eq 0) {
    Add-Summary '- Overall: READY FOR GUI VALIDATION'
    Write-Ok 'Bootstrap checks are ready for GUI validation.'
} else {
    Add-Summary '- Overall: ACTION REQUIRED'
    foreach ($issue in $issues) { Add-Summary "- Action: $issue" }
    Write-Warn "Bootstrap completed with $($issues.Count) action item(s). The GUI and AI handoff remain available."
}
Add-Summary ''
Add-Summary '## Safety note'
Add-Summary ''
Add-Summary 'This bootstrap does not perform BlueStacks root/host patching. If that is required, the local AI must follow AI_DEPLOYMENT_PLAYBOOK.md and obtain explicit user approval after showing backup/rollback scope.'
Set-Content -Path $summaryPath -Value ($lines -join "`r`n") -Encoding UTF8

$versionFile = Join-Path $RepoRoot 'HUUUGE_COLLECTOR_VERSION.txt'
$latestReport = [ordered]@{
    schema_version = 1
    time = (Get-Date).ToString('o')
    collector_version = if (Test-Path -LiteralPath $versionFile) {
        (Get-Content -LiteralPath $versionFile -Raw -Encoding UTF8).Trim()
    } else { 'unknown' }
    source_mode = $SourceMode
    status = if ($issues.Count -eq 0) { 'ready_for_gui_validation' } else { 'action_required' }
    action_items = @($issues)
    report = $summaryPath
}
$latestReport | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $localRoot 'latest.json') -Encoding UTF8

Write-Host "`nBootstrap report: $summaryPath" -ForegroundColor Yellow
Write-Host 'No BlueStacks root/host patch was executed by this script.' -ForegroundColor Yellow
Write-Host 'If the local AI report says READY, proceed to the capture workflow. Otherwise let the local AI continue from the exact next action after any required approval.' -ForegroundColor Yellow

exit 0
