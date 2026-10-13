param([string]$RepositoryPath = '.', [string]$RepositoryUrl = '', [string]$PythonExe, [string]$Workspace, [switch]$Initial, [switch]$MigrateExisting)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $RepositoryPath).Path
if (!(Test-Path (Join-Path $root 'tools/team_config.py'))) { throw 'Missing team_config.py' }
if(-not $PythonExe){throw 'Explicit verified PythonExe required'}
$exe=$PythonExe; $prefix=@()
& $exe @prefix (Join-Path $root 'tools/team_config.py') validate --source $root
if ($LASTEXITCODE -ne 0) { throw 'Package validation failed' }
$commit=(& git.exe -C $root rev-parse HEAD).Trim()
if($LASTEXITCODE -ne 0){throw 'Source commit required'}
$args=@((Join-Path $root 'tools/team_config.py'),'install','--source',$root,'--home',$env:USERPROFILE,'--commit',$commit)
if($Initial){$args+='--initial'}
if($MigrateExisting){$args+='--migrate'}
if($Workspace){$args+=@('--workspace',$Workspace)}
& $exe @args
if ($LASTEXITCODE -ne 0) { throw 'Install failed; managed files preserved or rolled back' }
if ($RepositoryUrl) {
  $local = Join-Path $env:LOCALAPPDATA 'B47ANCED-Codex-Team'
  New-Item -ItemType Directory -Force $local | Out-Null
  @{repository_url=$RepositoryUrl; repository_path=$root; python_exe=$PythonExe; gh_exe=(Get-Command gh.exe).Source; validator_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'tools/team_config.py')).Hash.ToLower()} | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $local 'source.json')
}

# Trust bootstrap scripts only from the reviewed installer checkout. Future fetched scripts are never executed during that same update.
$trustedDir=Join-Path $env:USERPROFILE '.codex/b47anced-team-tools'
New-Item -ItemType Directory -Force $trustedDir | Out-Null
Copy-Item (Join-Path $root 'tools/team_config.py') (Join-Path $trustedDir 'team_config.py') -Force
Copy-Item (Join-Path $root 'tools/Update-CodexTeam.ps1') (Join-Path $trustedDir 'Update-CodexTeam.ps1') -Force
