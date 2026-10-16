[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE,[string]$Workspace,[string]$RepositoryRoot,[string]$PythonExe,[switch]$Open)
$ErrorActionPreference='Stop'
if(-not $Workspace){
 $state=Join-Path $HomeDirectory '.codex/b47anced-team-state.json'
 if(Test-Path -LiteralPath $state){$Workspace=(Get-Content -LiteralPath $state -Raw | ConvertFrom-Json).workspace}
 if(-not $Workspace){throw 'Supply your existing workspace directory with -Workspace'}
}
if(-not $PythonExe){
 $source=Join-Path $HomeDirectory '.codex/b47anced-team-tools/source.json'
 if(Test-Path -LiteralPath $source){$PythonExe=(Get-Content -LiteralPath $source -Raw | ConvertFrom-Json).python_exe}
 elseif(Get-Command py.exe -ErrorAction SilentlyContinue){$PythonExe=(& py.exe -3 -c 'import sys;print(sys.executable)').Trim()}
 else{throw 'Supply -PythonExe with your Python interpreter'}
}
$hub=Join-Path $HomeDirectory '.codex/b47anced-team/tools'
$teamTools=if(Test-Path -LiteralPath (Join-Path $hub 'test_meshy_connection.py')){$hub}else{$PSScriptRoot}
$workspaceArgs=@((Join-Path $PSScriptRoot 'code_workspace.py'),'--workspace',$Workspace,'--home',$HomeDirectory,'--python',$PythonExe,'--powershell',(Get-Command powershell.exe).Source,'--team-tools',$teamTools,'--source-tools',$PSScriptRoot)
if($RepositoryRoot){$workspaceArgs+=@('--repositories',$RepositoryRoot)}
& $PythonExe @workspaceArgs
if($LASTEXITCODE -ne 0){throw 'Workspace setup refused; existing files were preserved'}
if($Open){
 $code=Get-Command code.cmd -ErrorAction SilentlyContinue
 if(-not $code){
  $candidate=Join-Path $env:LOCALAPPDATA 'Programs/Microsoft VS Code/bin/code.cmd'
  if(Test-Path -LiteralPath $candidate){$code=Get-Item -LiteralPath $candidate}
 }
 if(-not $code){throw 'Workspace created; open B47ANCED.code-workspace manually in VS Code'}
 $exe=if($code.Source){$code.Source}else{$code.FullName}
 & $exe --new-window (Join-Path $Workspace 'B47ANCED.code-workspace')
 if($LASTEXITCODE -ne 0){throw 'Workspace created but VS Code launch failed'}
}
