param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [switch]$SkipAI
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

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
if (-not (Test-Path (Join-Path $RepoRoot '.git'))) {
    throw "Not a Git repository: $RepoRoot"
}

$localRoot = Join-Path $RepoRoot '.local\bootstrap'
New-Item -ItemType Directory -Force -Path $localRoot | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$summaryPath = Join-Path $localRoot "bootstrap_$stamp.md"
$lines = New-Object System.Collections.Generic.List[string]

function Add-Summary([string]$Line) {
    $script:lines.Add($Line)
}

Add-Summary '# Huuuge Local Bootstrap Report'
Add-Summary ''
Add-Summary "- Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Add-Summary "- Repo: $RepoRoot"

Write-Step '1. Update repository safely'
$git = Resolve-CommandPath 'git'
if (-not $git) { throw 'Git is required.' }

$dirty = @(& $git -C $RepoRoot status --porcelain)
if ($dirty.Count -gt 0) {
    Write-Warn 'Working tree has local changes. Preserving them; running fetch only, not pull.'
    & $git -C $RepoRoot fetch origin
    Add-Summary '- Git: local changes detected; fetched remote only.'
} else {
    & $git -C $RepoRoot pull --ff-only
    if ($LASTEXITCODE -ne 0) { throw 'git pull --ff-only failed.' }
    Write-Ok 'Repository is up to date.'
    Add-Summary '- Git: clean working tree; fast-forward update completed.'
}

$head = (& $git -C $RepoRoot rev-parse HEAD).Trim()
Add-Summary "- HEAD: `$head`"

Write-Step '2. Create/verify isolated Python environment'
$hostPython = Resolve-CommandPath 'py'
if (-not $hostPython) { $hostPython = Resolve-CommandPath 'python' }
if (-not $hostPython) {
    Write-Warn 'Python was not found. Install Python 3, then rerun bootstrap.'
    Add-Summary '- Python: MISSING'
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
    Add-Summary "- Python: READY (`.venv`)"
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
    }
} else {
    Write-Warn 'ADB not found at C:\platform-tools\adb.exe.'
    Add-Summary '- ADB: MISSING at validated path.'
}

Write-Step '6. Prepare local-AI handoff'
$aiPromptPath = Join-Path $localRoot 'CODEX_BOOTSTRAP_PROMPT.md'
$aiOutputPath = Join-Path $localRoot "codex_preflight_$stamp.txt"
$aiPrompt = @"
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
"@
Set-Content -Path $aiPromptPath -Value $aiPrompt -Encoding UTF8
Add-Summary "- AI prompt: `.local/bootstrap/CODEX_BOOTSTRAP_PROMPT.md`"

$codex = Resolve-CommandPath 'codex'
if ($SkipAI) {
    Write-Warn 'Local AI step skipped by -SkipAI.'
    Add-Summary '- Codex preflight: skipped.'
} elseif ($codex) {
    Write-Host "Codex detected: $codex"
    Write-Host 'Running non-interactive SAFE preflight. First-time Codex sign-in may still require user interaction.'
    Push-Location $RepoRoot
    try {
        Get-Content -Raw $aiPromptPath | & $codex exec 2>&1 |
            Tee-Object -FilePath $aiOutputPath | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-Ok 'Codex preflight completed.'
            Add-Summary "- Codex preflight: completed; see `.local/bootstrap/$([IO.Path]::GetFileName($aiOutputPath))`."
        } else {
            Write-Warn "Codex preflight exited with code $LASTEXITCODE. The user may need to run `codex` once and sign in."
            Add-Summary "- Codex preflight: exit code $LASTEXITCODE; login/setup may be required."
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Warn 'Codex CLI is not installed. This does not block the safe bootstrap; local AI integration remains pending.'
    Write-Host 'Official Codex Windows install is documented in HUUUGE_DATA_COLLECTION_GUIDE.md.'
    Add-Summary '- Codex: NOT INSTALLED / not on PATH.'
}

Write-Step '7. Finish'
Add-Summary ''
Add-Summary '## Safety note'
Add-Summary ''
Add-Summary 'This bootstrap does not perform BlueStacks root/host patching. If that is required, the local AI must follow AI_DEPLOYMENT_PLAYBOOK.md and obtain explicit user approval after showing backup/rollback scope.'
Set-Content -Path $summaryPath -Value ($lines -join "`r`n") -Encoding UTF8

Write-Host "`nBootstrap report: $summaryPath" -ForegroundColor Yellow
Write-Host 'No BlueStacks root/host patch was executed by this script.' -ForegroundColor Yellow
Write-Host 'If the local AI report says READY, proceed to the capture workflow. Otherwise let the local AI continue from the exact next action after any required approval.' -ForegroundColor Yellow

exit 0
