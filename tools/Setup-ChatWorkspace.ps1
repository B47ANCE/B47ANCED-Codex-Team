[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE,[string]$Workspace,[string]$PythonExe)
$ErrorActionPreference='Stop'
$state=Join-Path $HomeDirectory '.codex/b47anced-team-state.json'
if(-not $Workspace){$Workspace=(Get-Content -LiteralPath $state -Raw | ConvertFrom-Json).workspace}
if(-not $Workspace){throw 'Supply the existing team workspace directory'}
if(-not $PythonExe){$PythonExe=(Get-Content -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-tools/source.json') -Raw | ConvertFrom-Json).python_exe}
$codexHome=Join-Path $HomeDirectory '.codex'
if($env:CODEX_HOME -and $HomeDirectory -eq $env:USERPROFILE){$codexHome=$env:CODEX_HOME}
& $PythonExe (Join-Path $PSScriptRoot 'chat_workspace.py') --home $codexHome --base (Join-Path $Workspace 'B47ANCED.code-workspace') --output (Join-Path $Workspace 'B47ANCED-Saved-Chats.code-workspace')
if($LASTEXITCODE -ne 0){throw 'Saved-chat setup refused; existing history and custom files preserved'}
