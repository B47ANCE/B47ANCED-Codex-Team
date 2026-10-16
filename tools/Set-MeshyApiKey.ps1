[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
if([Environment]::GetEnvironmentVariable('MESHY_API_KEY','User')){
 Write-Host 'A user-level MESHY_API_KEY already exists; it was preserved.'
 return
}
Write-Host 'Enter your Meshy API key here, never in a chat. Input is masked.'
Write-Host 'It will be stored in your Windows user environment, accessible to your account, not in a repository or Codex config.'
$secret=Read-Host 'MESHY_API_KEY' -AsSecureString
$pointer=[IntPtr]::Zero
try {
 $pointer=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
 $value=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
 if([string]::IsNullOrWhiteSpace($value) -or -not $value.StartsWith('msy_')){throw 'No valid Meshy API key was entered; nothing was saved.'}
 [Environment]::SetEnvironmentVariable('MESHY_API_KEY',$value,'User')
 Write-Host 'Key saved locally. Fully restart VS Code/Codex and open a new terminal to inherit it.'
} finally {
 if($pointer -ne [IntPtr]::Zero){[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)}
 $value=$null
 $secret.Dispose()
}
