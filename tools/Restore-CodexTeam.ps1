[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE, [switch]$CheckOnly)
$ErrorActionPreference='Stop'
# Run only from a manually reviewed checkout, never automatically fetched tools.
$cfg=Get-Content -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-tools/source.json') -Raw | ConvertFrom-Json
$rollbackArgs=@((Join-Path $PSScriptRoot 'rollback_team.py'),'--home',$HomeDirectory)
if($CheckOnly){$rollbackArgs+='--check-only'}
& $cfg.python_exe @rollbackArgs
if($LASTEXITCODE -ne 0){throw 'Rollback refused or failed; inspect the error and retained backup'}
