[CmdletBinding()]
param([Parameter(Mandatory)][string]$RepositoryRoot)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $RepositoryRoot).Path
$globalGuide=Join-Path $env:USERPROFILE '.codex/AGENTS.md'
if(-not(Test-Path -LiteralPath $globalGuide)){throw 'Install the shared guide first'}
$block=@"
<!-- PZ-CODEX-MANAGED-STARTUP -->
Read the current global rules at $globalGuide before work.
Team skills are installed at $(Join-Path $env:USERPROFILE '.agents/skills').
Preserve project-specific identity, instructions, source, local settings and runtime evidence.
<!-- /PZ-CODEX-MANAGED-STARTUP -->
"@
$pattern='(?s)<!-- PZ-CODEX-MANAGED-STARTUP -->.*?<!-- /PZ-CODEX-MANAGED-STARTUP -->'
foreach($project in Get-ChildItem -LiteralPath $root -Directory){
 $guide=Join-Path $project.FullName 'AGENTS.md'
 $old=if(Test-Path -LiteralPath $guide){Get-Content -LiteralPath $guide -Raw}else{''}
 if($old.Contains('<!-- PZ-CODEX-MANAGED-STARTUP -->') -and -not[regex]::IsMatch($old,$pattern)){throw "Malformed startup: $guide"}
 $new=if([regex]::IsMatch($old,$pattern)){[regex]::Replace($old,$pattern,[Text.RegularExpressions.MatchEvaluator]{param($match) $block})}else{$old.TrimEnd()+"`n`n"+$block+"`n"}
 if($new -ne $old){
  if($old){$backup=Join-Path $env:USERPROFILE ('.codex/b47anced-project-backups/'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Path $backup -Force | Out-Null;Copy-Item -LiteralPath $guide -Destination (Join-Path $backup 'AGENTS.md')}
  Set-Content -LiteralPath $guide -Value $new -NoNewline -Encoding UTF8
 }
}
