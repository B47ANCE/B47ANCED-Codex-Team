param([string]$RepositoryUrl = '', [string]$Branch = 'main', [switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$cfgPath=Join-Path $PSScriptRoot 'source.json'
$cfg=Get-Content -LiteralPath $cfgPath -Raw | ConvertFrom-Json
if (-not $RepositoryUrl) {
 if (!(Test-Path $cfgPath)) { throw 'Missing local source.json. Run installer with -RepositoryUrl first.' }
 $cfg=Get-Content $cfgPath -Raw | ConvertFrom-Json
 $RepositoryUrl=$cfg.repository_url
}
if ($RepositoryUrl -notmatch '^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(\.git)?$') { throw 'Only approved HTTPS GitHub repository URLs are supported' }
if($RepositoryUrl -ne 'https://github.com/B47ANCE/B47ANCED-Codex-Team.git'){throw 'Unapproved source URL'}
if ($Branch -ne 'main') { throw 'Auto-updater only supports main' }
$lockDir=Join-Path $PSScriptRoot 'update.lock'
if (!(Test-Path (Split-Path $lockDir))) { New-Item -ItemType Directory -Force (Split-Path $lockDir) | Out-Null }
try { New-Item -ItemType Directory -Path $lockDir -ErrorAction Stop | Out-Null } catch { throw 'Update already in progress; refusing concurrent install' }
$tmp=Join-Path $env:TEMP ('b47-team-'+[guid]::NewGuid().ToString('N'))
try {
 & $cfg.git_exe clone --quiet --depth 1 --single-branch --branch main -- $RepositoryUrl $tmp
 if ($LASTEXITCODE -ne 0) { throw 'Git clone failed' }
 $head=(& $cfg.git_exe -C $tmp rev-parse HEAD).Trim()
 $exe=$cfg.python_exe; $prefix=@()
 # Run ONLY the previously installed trusted validator; never execute fetched scripts.
 $trusted=Join-Path $env:USERPROFILE '.codex/b47anced-team-tools/team_config.py'
 if (!(Test-Path $trusted)) { throw 'Trusted bootstrap not installed. Run tools/Install-CodexTeam.ps1 -Initial from reviewed checkout.' }
 if((Get-FileHash -LiteralPath $trusted).Hash.ToLower() -ne $cfg.validator_sha256){throw 'Trusted validator drift; manual review required'}
 & $exe @prefix $trusted validate --source $tmp
 if($LASTEXITCODE -ne 0){throw 'Downloaded configuration failed validation'}
 & $exe $trusted drift --home $env:USERPROFILE
 if($LASTEXITCODE -ne 0){throw 'Managed files drifted; update blocked'}
 $runs=& $cfg.gh_exe api ('repos/B47ANCE/B47ANCED-Codex-Team/actions/runs?head_sha='+$head+'&branch=main&event=push')
 if($LASTEXITCODE -ne 0){throw 'Unable to verify CI'}
 $passed=@(($runs | ConvertFrom-Json).workflow_runs | Where-Object {$_.head_sha -eq $head -and $_.name -eq 'Validate Codex team configuration' -and $_.status -eq 'completed' -and $_.conclusion -eq 'success'})
 if($passed.Count -eq 0){throw 'Exact main commit lacks successful CI'}
 $state=Join-Path $env:USERPROFILE '.codex/b47anced-team-state.json'
 $old=Get-Content $state -Raw | ConvertFrom-Json
 $version=(Get-Content (Join-Path $tmp 'VERSION') -Raw).Trim()
 if([version]($version -split '-')[0] -lt [version]($old.version -split '-')[0]){throw 'Automatic version downgrade blocked'}
 if($old.commit -eq $head){Write-Host "CURRENT $version ($head)";return}
 if($old.version -eq $version){throw 'Changed commit reuses installed version'}
 if($CheckOnly){Write-Host "Validated update available: $head";exit 0}
 $installArgs=@($trusted,'install','--source',$tmp,'--home',$env:USERPROFILE,'--commit',$head)
 if($old.workspace){$installArgs+=@('--workspace',$old.workspace)}
 & $exe @installArgs
 if($LASTEXITCODE -ne 0){throw 'Installation failed'}
 Write-Host "Updated from validated main commit $head"
} finally {
 # Retain downloaded staging as evidence. No recursive cleanup in the updater.
 if(Test-Path $lockDir){Remove-Item -LiteralPath $lockDir -Force}
}
