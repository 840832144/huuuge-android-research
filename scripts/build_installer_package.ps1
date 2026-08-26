param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) '.local\release'),
    [string]$SourceRevision = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = [IO.Path]::GetFullPath($RepoRoot.TrimEnd('\'))
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory.TrimEnd('\'))
$versionPath = Join-Path $RepoRoot 'HUUUGE_COLLECTOR_VERSION.txt'
$bootstrapPath = Join-Path $RepoRoot 'HUUUGE_BOOTSTRAP.cmd'
$manualPath = Join-Path $RepoRoot 'HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md'

foreach ($required in @($versionPath, $bootstrapPath, $manualPath)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required installer source is missing: $required"
    }
}

$version = (Get-Content -LiteralPath $versionPath -Raw -Encoding UTF8).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Invalid collector version: $version"
}

$sourceDirty = $false
if ([string]::IsNullOrWhiteSpace($SourceRevision)) {
    if (Test-Path -LiteralPath (Join-Path $RepoRoot '.git')) {
        $SourceRevision = ((& git -C $RepoRoot rev-parse HEAD 2>$null) -join '').Trim()
        $sourceDirty = @(& git -C $RepoRoot status --porcelain).Count -gt 0
    } elseif (Get-Command svn -ErrorAction SilentlyContinue) {
        $SourceRevision = ((& svnversion $RepoRoot 2>$null) -join '').Trim()
    }
}
if ([string]::IsNullOrWhiteSpace($SourceRevision)) { $SourceRevision = 'unknown' }

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$stage = Join-Path $OutputDirectory ('.installer_stage_' + [Guid]::NewGuid().ToString('N'))
$zipPath = Join-Path $OutputDirectory 'HuuugeCollector_Installer.zip'

try {
    New-Item -ItemType Directory -Path $stage | Out-Null
    Copy-Item -LiteralPath $bootstrapPath -Destination (Join-Path $stage 'HUUUGE_BOOTSTRAP.cmd')
    Copy-Item -LiteralPath $manualPath -Destination (Join-Path $stage 'HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md')

    $readme = @(
        'Huuuge Collector Installer',
        '',
        '1. Read HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md.',
        '2. Double-click HUUUGE_BOOTSTRAP.cmd.',
        '3. The default install directory is C:\HuuugeCollector.',
        '4. Wait for the Chinese GUI and use Environment Check / Repair.',
        '',
        'This package contains no APK, account data, Frida binary, password, or capture.'
    ) -join "`r`n"
    Set-Content -LiteralPath (Join-Path $stage 'README.txt') -Value $readme -Encoding ASCII

    $fileRows = @()
    foreach ($file in Get-ChildItem -LiteralPath $stage -File | Sort-Object Name) {
        $fileRows += [ordered]@{
            name = $file.Name
            size = $file.Length
            sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    $manifest = [ordered]@{
        schema_version = 1
        package = 'HuuugeCollector_Installer'
        version = $version
        source_revision = $SourceRevision
        source_dirty = $sourceDirty
        svn_url = 'http://140.143.33.242/svn/cr/x_proj_design/trunk/HuuugeCollector'
        default_install_directory = 'C:\HuuugeCollector'
        entry = 'HUUUGE_BOOTSTRAP.cmd'
        safety = [ordered]@{
            normal_bluestacks_instrumentation = $false
            contains_capture_values = $false
            contains_account_data = $false
            contains_third_party_binaries = $false
        }
        files = $fileRows
    }
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $stage 'package_manifest.json') -Encoding UTF8

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    [IO.Compression.ZipFile]::CreateFromDirectory(
        $stage,
        $zipPath,
        [IO.Compression.CompressionLevel]::Optimal,
        $false
    )
    $zip = Get-Item -LiteralPath $zipPath
    $hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Host "Package: $($zip.FullName)"
    Write-Host "Version: $version"
    Write-Host "Bytes: $($zip.Length)"
    Write-Host "SHA256: $hash"
} finally {
    $resolvedOutput = [IO.Path]::GetFullPath($OutputDirectory).TrimEnd('\') + '\'
    $resolvedStage = [IO.Path]::GetFullPath($stage)
    if ($resolvedStage.StartsWith($resolvedOutput, [StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $resolvedStage).StartsWith('.installer_stage_', [StringComparison]::Ordinal)) {
        if (Test-Path -LiteralPath $resolvedStage) {
            Remove-Item -LiteralPath $resolvedStage -Recurse -Force
        }
    } else {
        throw "Refusing to clean unexpected staging path: $resolvedStage"
    }
}
