param([string]$TaskName='B47ANCED-Codex-Update')
$ErrorActionPreference='Stop'
$updater=Join-Path $env:USERPROFILE '.codex/b47anced-team-tools/Run-Update.ps1'
if(!(Test-Path $updater)){throw "Trusted updater missing: $updater"}
if(Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue){throw 'Existing task retained; review before replacement'}
$identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy RemoteSigned -File "'+$updater+'"')
$trigger=New-ScheduledTaskTrigger -AtLogOn -User $identity
$principal=New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -StartWhenAvailable
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'Validated B47ANCE Codex main-branch updates at sign-in' | Out-Null
Write-Host "Registered $TaskName (runs at logon)."
