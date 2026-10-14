param([string]$HomeDirectory=$env:USERPROFILE, [string]$RepositoryPath = '.', [string]$RepositoryUrl = 'https://github.com/B47ANCE/B47ANCED-Codex-Team.git', [string]$PythonExe, [string]$Workspace, [switch]$Initial, [switch]$MigrateExisting)
$ErrorActionPreference = 'Stop'
if(-not(Get-Command git.exe -ErrorAction SilentlyContinue)){throw 'Install Git before setup'}
if(-not(Get-Command gh.exe -ErrorAction SilentlyContinue)){throw 'Install GitHub CLI before setup'}
if(-not $Workspace){
 $state=Join-Path $HomeDirectory '.codex/b47anced-team-state.json'
 if(Test-Path -LiteralPath $state){$Workspace=(Get-Content -LiteralPath $state -Raw | ConvertFrom-Json).workspace}
}
$root = (Resolve-Path $RepositoryPath).Path
if (!(Test-Path (Join-Path $root 'tools/team_config.py'))) { throw 'Missing team_config.py' }
if(-not $PythonExe){
 if(Get-Command py.exe -ErrorAction SilentlyContinue){$PythonExe=(& py.exe -3 -c 'import sys;print(sys.executable)').Trim()}
 elseif(Get-Command python.exe -ErrorAction SilentlyContinue){$PythonExe=(& python.exe -c 'import sys;print(sys.executable)').Trim()}
 else{throw 'Install Python 3.10+ or supply -PythonExe'}
 if($LASTEXITCODE -ne 0){throw 'Python discovery failed; supply -PythonExe'}
}
$exe=$PythonExe; $prefix=@()
& $exe @prefix (Join-Path $root 'tools/team_config.py') validate --source $root
if ($LASTEXITCODE -ne 0) { throw 'Package validation failed' }
$commit=''
try {
 $gitRoot=(& git.exe -C $root rev-parse --show-toplevel 2>$null).Trim()
 if($LASTEXITCODE -eq 0 -and [IO.Path]::GetFullPath($gitRoot).TrimEnd('\') -eq [IO.Path]::GetFullPath($root).TrimEnd('\')){
  $commit=(& git.exe -C $root rev-parse HEAD).Trim()
  if($LASTEXITCODE -ne 0){$commit=''}
 }
} catch {$commit=''}
if($commit){
 $dirty=& git.exe -C $root status --porcelain=v1 --untracked-files=normal
 if($LASTEXITCODE -ne 0){throw 'Cannot inspect source checkout'}
 if($dirty){throw 'Commit or safely reconcile configuration source changes before installation; no files were installed'}
}
if(-not $commit){
 # A downloaded ZIP is accepted only when its validated manifest matches canonical main.
 $commit=(& gh.exe api repos/B47ANCE/B47ANCED-Codex-Team/commits/main --jq .sha).Trim()
 if($LASTEXITCODE -ne 0){throw 'Cannot establish canonical main commit'}
 $encoded=& gh.exe api ('repos/B47ANCE/B47ANCED-Codex-Team/contents/MANIFEST.sha256.json?ref='+$commit) --jq .content
 if($LASTEXITCODE -ne 0){throw 'Cannot verify downloaded ZIP manifest'}
 $remoteBytes=[Convert]::FromBase64String(($encoded -join '').Replace("`n",'').Replace("`r",''))
 $sha=[Security.Cryptography.SHA256]::Create()
 try {$remoteHash=[BitConverter]::ToString($sha.ComputeHash($remoteBytes)).Replace('-','').ToLower()} finally {$sha.Dispose()}
 if((Get-FileHash -LiteralPath (Join-Path $root 'MANIFEST.sha256.json')).Hash.ToLower() -ne $remoteHash){throw 'ZIP does not match canonical main; use the reviewed clone instead'}
}
$args=@((Join-Path $root 'tools/team_config.py'),'install','--source',$root,'--home',$HomeDirectory,'--commit',$commit)
if($Initial){$args+='--initial'}
if($MigrateExisting){$args+='--migrate'}
if($Workspace){$args+=@('--workspace',$Workspace)}
& $exe @args
if ($LASTEXITCODE -ne 0) { throw 'Install failed; managed files preserved or rolled back' }
if ($RepositoryUrl) {
  $local = Join-Path $HomeDirectory '.codex/b47anced-team-tools'
  New-Item -ItemType Directory -Force $local | Out-Null
  @{repository_url=$RepositoryUrl; branch='main'; repository_path=$root; python_exe=$PythonExe; git_exe=(Get-Command git.exe).Source; gh_exe=(Get-Command gh.exe).Source; validator_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'tools/team_config.py')).Hash.ToLower()} | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $local 'source.json')
}

# Trust bootstrap scripts only from the reviewed installer checkout. Future fetched scripts are never executed during that same update.
$trustedDir=Join-Path $HomeDirectory '.codex/b47anced-team-tools'
New-Item -ItemType Directory -Force $trustedDir | Out-Null
Copy-Item (Join-Path $root 'tools/team_config.py') (Join-Path $trustedDir 'team_config.py') -Force
Copy-Item (Join-Path $root 'tools/Update-CodexTeam.ps1') (Join-Path $trustedDir 'Update-CodexTeam.ps1') -Force
Copy-Item (Join-Path $root 'tools/Run-Update.ps1') (Join-Path $trustedDir 'Run-Update.ps1') -Force
