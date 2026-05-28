# make-packages.ps1 -- rebuild every dist\<name>.zip from packages\<name>\.
#
# Usage:
#   .\scripts\make-packages.ps1            # rebuild all
#   .\scripts\make-packages.ps1 -Only ado-doc-workflow,how-i-ai
#   .\scripts\make-packages.ps1 -DryRun    # show what would be packaged, don't write
#
# Run from the repo root. Idempotent. Existing zips are overwritten.

[CmdletBinding()]
param(
  [string[]] $Only,
  [switch]   $DryRun
)

$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$pkgRoot  = Join-Path $repoRoot 'packages'
$distRoot = Join-Path $repoRoot 'dist'

if (-not (Test-Path $pkgRoot)) {
  throw "packages\ not found at $pkgRoot"
}
if (-not (Test-Path $distRoot)) {
  New-Item -ItemType Directory -Path $distRoot | Out-Null
}

# Skip junk that shouldn't ship even if it lingered in the source tree.
$excludePatterns = @('__pycache__', '*.pyc', '*.pyo', '.pytest_cache', '.venv', 'venv', '.DS_Store', 'Thumbs.db')

function ShouldInclude([System.IO.FileSystemInfo]$item) {
  foreach ($pat in $excludePatterns) {
    if ($item.Name -like $pat) { return $false }
    if ($item.FullName -like "*\$pat\*") { return $false }
  }
  return $true
}

$packages = Get-ChildItem $pkgRoot -Directory | Sort-Object Name
if ($Only) {
  $packages = $packages | Where-Object { $Only -contains $_.Name }
  $missing = $Only | Where-Object { -not ($packages.Name -contains $_) }
  if ($missing) { Write-Warning ("Unknown package(s): {0}" -f ($missing -join ', ')) }
}

if (-not $packages) {
  Write-Warning "No packages to build."
  return
}

$results = @()
foreach ($pkg in $packages) {
  $zipPath = Join-Path $distRoot ($pkg.Name + '.zip')
  $files = Get-ChildItem $pkg.FullName -Recurse -File | Where-Object { ShouldInclude $_ }

  if ($DryRun) {
    Write-Host ("`n[DRYRUN] {0} -> {1}" -f $pkg.Name, $zipPath) -ForegroundColor Yellow
    $files | ForEach-Object { "  " + $_.FullName.Substring($pkg.FullName.Length + 1) }
    continue
  }

  if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

  $items = $files | ForEach-Object { $_.FullName }
  if (-not $items) { Write-Warning "Skipping $($pkg.Name): no files after filtering."; continue }

  # Compress-Archive in PS 5.1 emits paths relative to whatever you hand it; to keep
  # entries flat under the package root, cd into the package folder for the call.
  Push-Location $pkg.FullName
  try {
    $relItems = $files | ForEach-Object { $_.FullName.Substring($pkg.FullName.Length + 1) }
    Compress-Archive -Path $relItems -DestinationPath $zipPath -Force
  } finally {
    Pop-Location
  }

  $size = (Get-Item $zipPath).Length
  $results += [pscustomobject]@{
    Package = $pkg.Name
    Files   = $files.Count
    Bytes   = $size
    Zip     = $zipPath
  }
}

if (-not $DryRun) {
  Write-Host ""
  Write-Host "=== Built ===" -ForegroundColor Cyan
  $results | Format-Table Package, Files, @{ n='Size (KB)'; e={ [math]::Round($_.Bytes/1KB, 1) } }, Zip -AutoSize
}
