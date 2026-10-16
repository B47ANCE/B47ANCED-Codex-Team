[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$NpxPath)
$ErrorActionPreference='Stop'
# Windows user environment changes are not inherited by already running editors.
if(-not $env:MESHY_API_KEY){$env:MESHY_API_KEY=[Environment]::GetEnvironmentVariable('MESHY_API_KEY','User')}
$env:TRANSPORT='stdio'
$env:MESHY_API_HOST='https://api.meshy.ai'
& $NpxPath -y '@meshy-ai/meshy-mcp-server@0.6.4'
exit $LASTEXITCODE
