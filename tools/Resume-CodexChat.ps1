[CmdletBinding()]
param([guid]$SessionId,[string]$Target,[string]$CodexHome,[switch]$BrowseAll,[switch]$CheckOnly)
$ErrorActionPreference='Stop'
if(-not $BrowseAll -and (-not $Target -or -not(Test-Path -LiteralPath $Target -PathType Container))){throw 'Choose an existing project directory'}
if(-not(Get-Command codex.cmd -ErrorAction SilentlyContinue)){throw 'Codex CLI missing; run the team setup'}
$codexRoot=if($CodexHome){$CodexHome}elseif($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'}
$env:CODEX_HOME=$codexRoot
if($BrowseAll){
 if($CheckOnly){Write-Output 'PASS Codex CLI and configured history store; no chat started';return}
 & codex.cmd --sandbox workspace-write --ask-for-approval on-request --no-alt-screen resume --all
 if($LASTEXITCODE -ne 0){throw 'Cannot browse local chats'}
 return
}
$index=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'chats.local.json') -Raw | ConvertFrom-Json
$chat=@($index.chats | Where-Object {$_.id -eq $SessionId.ToString()})
if($chat.Count -ne 1){throw 'Chat index is missing or ambiguous; refresh saved chats'}
$expectedRoot=[IO.Path]::GetFullPath((Join-Path $codexRoot 'sessions')).TrimEnd('\')+'\'
$sessionPath=[IO.Path]::GetFullPath($chat[0].session_file)
if(-not $sessionPath.StartsWith($expectedRoot,[StringComparison]::OrdinalIgnoreCase)){throw 'Session outside active saved-chat store'}
if(-not(Test-Path -LiteralPath $sessionPath -PathType Leaf)){throw 'Saved chat is no longer available'}
$stream=[IO.FileStream]::new($sessionPath,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
$reader=[IO.StreamReader]::new($stream)
try{$meta=$reader.ReadLine() | ConvertFrom-Json}finally{$reader.Dispose()}
if($meta.type -ne 'session_meta' -or $meta.payload.id -ne $SessionId.ToString()){throw 'Session identity mismatch'}
if($CheckOnly){Write-Output 'PASS saved session identity, project directory and Codex CLI; no chat started';return}
Write-Output 'Resume only after the other surface is idle. Desktop monitor jobs remain on their existing host.'
$answer=Read-Host 'Confirm this chat is idle elsewhere (yes to continue)'
if($answer -ne 'yes'){Write-Output 'Resume cancelled; original history preserved';return}
Set-Location -LiteralPath $Target
& codex.cmd --cd $Target --sandbox workspace-write --ask-for-approval on-request --search --no-alt-screen resume $SessionId.ToString()
if($LASTEXITCODE -ne 0){throw 'Codex could not resume this session; original history was preserved'}
