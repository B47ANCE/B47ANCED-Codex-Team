[CmdletBinding()]
param([switch]$CheckOnly)
$ErrorActionPreference='Stop'
function Find-TeamVSCode {
 $command=Get-Command code.cmd -ErrorAction SilentlyContinue
 if($command){return $command.Source}
 foreach($base in @($env:LOCALAPPDATA,$env:ProgramFiles,${env:ProgramFiles(x86)})){
  if(-not $base){continue}
  foreach($relative in @('Programs/Microsoft VS Code/bin/code.cmd','Microsoft VS Code/bin/code.cmd')){
   $candidate=Join-Path $base $relative
   if(Test-Path -LiteralPath $candidate -PathType Leaf){return $candidate}
  }
 }
}
$code=Find-TeamVSCode
if(-not $code){
 if($CheckOnly){throw 'VS Code not found. Run tools/Setup-VSCode.ps1 to install it.'}
 $winget=Get-Command winget.exe -ErrorAction SilentlyContinue
 if(-not $winget){throw 'Install VS Code from https://code.visualstudio.com/Download or install Microsoft App Installer, then rerun setup.'}
 & $winget.Source install --id Microsoft.VisualStudioCode --exact --source winget --scope user --silent --accept-package-agreements --accept-source-agreements --disable-interactivity
 if($LASTEXITCODE -ne 0){throw "VS Code installation failed ($LASTEXITCODE). Existing team configuration is preserved."}
 $code=Find-TeamVSCode
 if(-not $code){throw 'VS Code CLI not found after installation; reopen PowerShell and rerun setup.'}
}
$extensions=@(& $code --list-extensions)
if($LASTEXITCODE -ne 0){throw 'Cannot enumerate VS Code extensions'}
if($extensions -notcontains 'openai.chatgpt'){
 if($CheckOnly){throw 'Official Codex extension openai.chatgpt is missing'}
 & $code --install-extension openai.chatgpt
 if($LASTEXITCODE -ne 0){throw 'Codex extension installation failed'}
}
$extensions=@(& $code --list-extensions --show-versions)
if($LASTEXITCODE -ne 0 -or -not($extensions -match '^openai\.chatgpt@')){throw 'Codex extension verification failed'}
& $code --version
if($LASTEXITCODE -ne 0){throw 'VS Code version verification failed'}
$extensions | Where-Object {$_ -match '^openai\.chatgpt@'}
Write-Output "VS Code CLI: $code"
Write-Output 'Open a project folder in VS Code, choose the Codex sidebar, and sign in with your own account if prompted. Editor settings and credentials were not rewritten.'
