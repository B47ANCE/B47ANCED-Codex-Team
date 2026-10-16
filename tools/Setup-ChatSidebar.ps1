[CmdletBinding()]
param([string]$HomeDirectory=$env:USERPROFILE,[string]$PythonExe,[string]$CodeExe,[switch]$CheckOnly)
$ErrorActionPreference='Stop'
# Alternate homes are test/config targets, never implicit authorization to change
# the current user's editor. A caller must explicitly supply its isolated CLI.
if($HomeDirectory -ne $env:USERPROFILE -and -not $CodeExe){throw 'Alternate HomeDirectory requires an explicit isolated CodeExe'}
if(-not $PythonExe){$PythonExe=(Get-Content -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-tools/source.json') -Raw | ConvertFrom-Json).python_exe}
if(-not $PythonExe -or -not(Test-Path -LiteralPath $PythonExe -PathType Leaf)){throw 'A verified Python executable is required'}
if(-not $CodeExe){
 $found=Get-Command code.cmd -ErrorAction SilentlyContinue
 if($found){$CodeExe=$found.Source}
 else{$candidate=Join-Path $env:LOCALAPPDATA 'Programs/Microsoft VS Code/bin/code.cmd';if(Test-Path -LiteralPath $candidate){$CodeExe=$candidate}}
 if(-not $CodeExe){$candidate=Join-Path $env:ProgramFiles 'Microsoft VS Code/bin/code.cmd';if(Test-Path -LiteralPath $candidate){$CodeExe=$candidate}}
}
if(-not $CodeExe){throw 'Run Setup-VSCode.ps1 first'}
$extensions=@(& $CodeExe --list-extensions --show-versions)
if($LASTEXITCODE -ne 0){throw 'Cannot enumerate VS Code extensions'}
if(-not($extensions -match '^openai\.chatgpt@')){throw 'Official openai.chatgpt extension is required'}
$version=(Get-Content -LiteralPath (Join-Path $PSScriptRoot 'chat-sidebar/package.json') -Raw | ConvertFrom-Json).version
$installed=@($extensions | Where-Object {$_ -match '^b47ance\.codex-chat-sidebar@'})
if($CheckOnly){
 if($installed -notcontains "b47ance.codex-chat-sidebar@$version"){throw 'Expected sidebar companion version is not installed'}
 Write-Output "Sidebar companion verified: $version (history content is not inspected by setup)";return
}
if($installed.Count -and [version]($installed[0].Split('@')[-1]) -gt [version]$version){throw 'A newer sidebar companion exists; refusing downgrade'}
$folder=Join-Path $HomeDirectory '.codex/chat-sidebar-build'
if(-not(Test-Path -LiteralPath $folder)){New-Item -ItemType Directory -Path $folder | Out-Null}
# Unique output preserves previous local packages for recovery. No personal
# history is embedded; only this developer's Python executable is configured.
$vsix=Join-Path $folder ("codex-chat-sidebar-$version-"+[guid]::NewGuid().ToString('N')+'.vsix')
& $PythonExe (Join-Path $PSScriptRoot 'build_chat_sidebar.py') --output $vsix --python $PythonExe
if($LASTEXITCODE -ne 0){throw 'Offline sidebar package build failed'}
& $CodeExe --install-extension $vsix --force
if($LASTEXITCODE -ne 0){throw 'Sidebar companion installation failed; original histories/settings were not changed'}
$extensions=@(& $CodeExe --list-extensions --show-versions)
if($LASTEXITCODE -ne 0 -or $extensions -notcontains "b47ance.codex-chat-sidebar@$version"){throw 'Sidebar companion verification failed'}
Write-Output "Sidebar companion $version installed. Open Codex in VS Code: All Existing Chats. Reload an already open editor window if needed. No conversations were started."
