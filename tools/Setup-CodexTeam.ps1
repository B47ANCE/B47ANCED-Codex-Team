[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE, [string]$Workspace,[string]$RepositoryRoot,[string]$PythonExe,[switch]$MigrateExisting,[switch]$EnableUpdates,[switch]$SkipVSCode,[switch]$SkipMeshy)
$ErrorActionPreference='Stop'
if($RepositoryRoot -and -not(Test-Path -LiteralPath $RepositoryRoot -PathType Container)){throw 'RepositoryRoot must be an existing directory; choose your actual mod repository folder'}
$root=Split-Path $PSScriptRoot -Parent
if($Workspace -and -not(Test-Path -LiteralPath $Workspace)){New-Item -ItemType Directory -Path $Workspace | Out-Null}
$initial=-not(Test-Path -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-state.json'))
& (Join-Path $PSScriptRoot 'Install-CodexTeam.ps1') -HomeDirectory $HomeDirectory -RepositoryPath $root -Workspace $Workspace -PythonExe $PythonExe -Initial:$initial -MigrateExisting:$MigrateExisting
if($RepositoryRoot){
 & (Join-Path $PSScriptRoot 'Connect-ModRepositories.ps1') -HomeDirectory $HomeDirectory -RepositoryRoot $RepositoryRoot
 & (Join-Path $PSScriptRoot 'Test-ModRepositories.ps1') -HomeDirectory $HomeDirectory -RepositoryRoot $RepositoryRoot
}
& (Join-Path $PSScriptRoot 'Test-CodexTeamInstall.ps1') -HomeDirectory $HomeDirectory -PackageRoot $root -Installed
if($LASTEXITCODE -ne 0){throw 'Installation check failed'}
if($EnableUpdates){
 & (Join-Path $HomeDirectory '.codex/b47anced-team-tools/Update-CodexTeam.ps1') -HomeDirectory $HomeDirectory -CheckOnly
 & (Join-Path $PSScriptRoot 'Register-CodexTeamUpdater.ps1') -HomeDirectory $HomeDirectory
}
if(-not $SkipVSCode){ & (Join-Path $PSScriptRoot 'Setup-VSCode.ps1') }
if(-not $SkipMeshy){ & (Join-Path $PSScriptRoot 'Setup-Meshy.ps1') -HomeDirectory $HomeDirectory -PythonExe $PythonExe }
