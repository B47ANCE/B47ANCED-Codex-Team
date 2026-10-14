$ErrorActionPreference='Stop'
$log=Join-Path $PSScriptRoot 'last-update.log'
try {
 & (Join-Path $PSScriptRoot 'Update-CodexTeam.ps1') *> $log
 if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
 exit 0
} catch {
 $_.Exception.Message | Add-Content -LiteralPath $log
 exit 1
}
