[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][ValidateSet('codex','resume','freshness','versions','verify-team','update-check','update','rollback-preview','meshy-balance','meshy-key','mcp-list','overview-refresh','overview-open','overview-watch')][string]$Action,
 [string]$Target,[string]$RepositoryRoot,[string]$Workspace,[Parameter(Mandatory=$true)][string]$TeamTools,
 [Parameter(Mandatory=$true)][string]$HomeDirectory,[string]$PythonExe
)
$ErrorActionPreference='Stop'
if($Action -in @('codex','resume','freshness','versions')){
 if(-not $Target -or -not(Test-Path -LiteralPath $Target -PathType Container)){throw 'Choose an existing project folder'}
}
if($Action -like 'overview-*'){
 if(-not $PythonExe -or -not $Workspace -or -not $RepositoryRoot){throw 'Overview requires configured Python, workspace and repository root'}
 $runtime=Join-Path $PSScriptRoot 'overview'
 $overviewArgs=@((Join-Path $runtime 'mod_overview.py'),'--repositories',$RepositoryRoot,'--catalog',(Join-Path $runtime 'catalog.json'),'--template',(Join-Path $runtime 'view.json'),'--output',(Join-Path $Workspace 'mod-overview'))
 if($Action -eq 'overview-watch'){$overviewArgs+='--watch'}
 & $PythonExe @overviewArgs
 if($LASTEXITCODE -ne 0){throw 'Overview refresh failed; prior output preserved'}
 if($Action -eq 'overview-open'){Start-Process -FilePath (Join-Path $Workspace 'mod-overview/index.html') -WindowStyle Hidden}
 return
}
switch($Action){
 'codex' {
  Set-Location -LiteralPath $Target
  & codex.cmd --cd $Target --sandbox workspace-write --ask-for-approval on-request --search --no-alt-screen
 }
 'resume' {
  Set-Location -LiteralPath $Target
  & codex.cmd --cd $Target --sandbox workspace-write --ask-for-approval on-request --search --no-alt-screen resume
 }
 'freshness' { & (Join-Path $TeamTools 'Test-PZRepositoryFreshness.ps1') -Repository $Target }
 'versions' {
  $script=Join-Path $Target 'scripts/check_versions.py'
  if(-not(Test-Path -LiteralPath $script -PathType Leaf)){throw 'This project has no scripts/check_versions.py. Inspect its own documented validation commands in Codex; no version was invented.'}
  if(-not $PythonExe){throw 'Python interpreter not configured for this workspace'}
  Push-Location -LiteralPath $Target
  try { & $PythonExe $script } finally { Pop-Location }
 }
 'verify-team' {
  if(-not $RepositoryRoot){throw 'This workspace has no configured mod repository root'}
  & (Join-Path $TeamTools 'Test-ModRepositories.ps1') -HomeDirectory $HomeDirectory -RepositoryRoot $RepositoryRoot
 }
 'update-check' { & (Join-Path $HomeDirectory '.codex/b47anced-team-tools/Update-CodexTeam.ps1') -HomeDirectory $HomeDirectory -CheckOnly }
 'update' { & (Join-Path $HomeDirectory '.codex/b47anced-team-tools/Update-CodexTeam.ps1') -HomeDirectory $HomeDirectory }
 'rollback-preview' { & (Join-Path $TeamTools 'Restore-CodexTeam.ps1') -HomeDirectory $HomeDirectory -CheckOnly }
 'meshy-balance' {
  if(-not $PythonExe){throw 'Python interpreter not configured for this workspace'}
  $codexHome=Join-Path $HomeDirectory '.codex'
  if($env:CODEX_HOME){$codexHome=$env:CODEX_HOME}
  & $PythonExe (Join-Path $TeamTools 'test_meshy_connection.py') --codex-home $codexHome --balance
 }
 'meshy-key' { & (Join-Path $TeamTools 'Set-MeshyApiKey.ps1') }
 'mcp-list' {
  $raw=& codex.cmd mcp list --json
  if($LASTEXITCODE -ne 0){throw 'Cannot inspect MCP configuration'}
  # Avoid printing server environment values or authentication material.
  $raw | ConvertFrom-Json | ForEach-Object { [pscustomobject]@{Name=$_.name;Enabled=$_.enabled} } | Format-Table
 }
}
if($LASTEXITCODE){throw "Workflow $Action returned failure ($LASTEXITCODE)"}
