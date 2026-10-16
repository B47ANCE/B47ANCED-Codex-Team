[CmdletBinding()]
param([switch]$CheckOnly)
$ErrorActionPreference='Stop'
foreach($name in @('node.exe','npm.cmd','npx.cmd')){
 if(-not(Get-Command $name -ErrorAction SilentlyContinue)){throw 'Install Node.js LTS, reopen PowerShell, then rerun setup'}
 & $name --version
 if($LASTEXITCODE -ne 0){throw "Prerequisite failed: $name"}
}
if(-not(Get-Command codex.cmd -ErrorAction SilentlyContinue)){
 if($CheckOnly){throw 'Codex CLI is missing'}
 & npm.cmd install -g @openai/codex
 if($LASTEXITCODE -ne 0){throw 'Official Codex CLI installation failed'}
 $prefix=(& npm.cmd prefix -g).Trim()
 if($LASTEXITCODE -ne 0){throw 'Cannot locate npm global command directory'}
 if(Test-Path -LiteralPath (Join-Path $prefix 'codex.cmd')){$env:PATH=$prefix+[IO.Path]::PathSeparator+$env:PATH}
}
if(-not(Get-Command codex.cmd -ErrorAction SilentlyContinue)){throw 'Codex CLI is not on PATH; reopen PowerShell and rerun setup'}
& codex.cmd --version
if($LASTEXITCODE -ne 0){throw 'Codex CLI verification failed'}
Write-Output 'Codex CLI ready. Sign in locally with codex login if needed; no credentials or editor settings were changed.'
