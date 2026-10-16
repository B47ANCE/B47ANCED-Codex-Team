[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE,[string]$PythonExe,[switch]$CheckOnly)
$ErrorActionPreference='Stop'
foreach($name in @('node.exe','npm.cmd','npx.cmd','codex.cmd')){
 if(-not(Get-Command $name -ErrorAction SilentlyContinue)){throw "Missing prerequisite $name. Install Node.js LTS and Codex CLI using docs/MESHY.md; existing integrations were preserved."}
 & $name --version
 if($LASTEXITCODE -ne 0){throw "Prerequisite verification failed: $name"}
}
$nodeVersion=(& node.exe --version).TrimStart('v').Split('.')[0]
if([int]$nodeVersion -lt 18){throw 'Meshy requires Node.js 18+; use a supported Node.js LTS release'}
if(-not $PythonExe){
 if(Get-Command py.exe -ErrorAction SilentlyContinue){$PythonExe=(& py.exe -3 -c 'import sys;print(sys.executable)').Trim()}
 elseif(Get-Command python.exe -ErrorAction SilentlyContinue){$PythonExe=(Get-Command python.exe).Source}
 else{throw 'Install Python 3.11+ or supply -PythonExe'}
}
$codexHome=Join-Path $HomeDirectory '.codex'
if($env:CODEX_HOME -and $HomeDirectory -eq $env:USERPROFILE){$codexHome=$env:CODEX_HOME}
$params=@((Join-Path $PSScriptRoot 'meshy_setup.py'),'--codex-home',$codexHome,'--npx',(Get-Command npx.cmd).Source,'--command',(Get-Command powershell.exe).Source)
if($CheckOnly){$params+='--check'}
& $PythonExe @params
if($LASTEXITCODE -ne 0){throw 'Meshy config was not changed; inspect existing Meshy entry or Python version'}
Write-Output 'Meshy uses pinned official npx package 0.6.4. All tools are exposed with prompt approval policy. Explicit approval is required before spending credits. No paid task was submitted.'
if(-not $CheckOnly){
 & $PythonExe (Join-Path $PSScriptRoot 'test_meshy_connection.py') --codex-home $codexHome
 if($LASTEXITCODE -ne 0){throw 'Meshy is configured but package installation or MCP discovery failed; rerun setup after fixing network/prerequisites'}
}
if(-not [Environment]::GetEnvironmentVariable('MESHY_API_KEY','Process') -and -not [Environment]::GetEnvironmentVariable('MESHY_API_KEY','User')){
 Write-Warning 'API authentication pending. Run tools/Set-MeshyApiKey.ps1 locally, never paste a key into chat. Then restart Codex/VS Code.'
}
