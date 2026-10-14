[CmdletBinding()]
param([string]$Workspace,[string]$RepositoryRoot,[string]$PythonExe,[switch]$MigrateExisting,[switch]$EnableUpdates)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($Workspace -and -not(Test-Path -LiteralPath $Workspace)){New-Item -ItemType Directory -Path $Workspace | Out-Null}
$initial=-not(Test-Path -LiteralPath (Join-Path $env:USERPROFILE '.codex/b47anced-team-state.json'))
& (Join-Path $PSScriptRoot 'Install-CodexTeam.ps1') -RepositoryPath $root -Workspace $Workspace -PythonExe $PythonExe -Initial:$initial -MigrateExisting:$MigrateExisting
if($RepositoryRoot){
 & (Join-Path $PSScriptRoot 'Connect-ModRepositories.ps1') -RepositoryRoot $RepositoryRoot
 & (Join-Path $PSScriptRoot 'Test-ModRepositories.ps1') -RepositoryRoot $RepositoryRoot
}
& (Join-Path $PSScriptRoot 'Test-CodexTeamInstall.ps1') -PackageRoot $root -Installed
if($LASTEXITCODE -ne 0){throw 'Installation check failed'}
if($EnableUpdates){
 & (Join-Path $env:USERPROFILE '.codex/b47anced-team-tools/Update-CodexTeam.ps1') -CheckOnly
 & (Join-Path $PSScriptRoot 'Register-CodexTeamUpdater.ps1')
}
