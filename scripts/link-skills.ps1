param([switch]$Check)
$ErrorActionPreference = 'Stop'
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python 3 is required. Install it and rerun this script.' }
$arguments = @((Join-Path $PSScriptRoot 'link-skills.py'))
if ($Check) { $arguments += '--check' }
& $python.Source @arguments
exit $LASTEXITCODE
