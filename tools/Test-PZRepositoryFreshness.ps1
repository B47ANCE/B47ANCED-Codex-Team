param([Parameter(Mandatory=$true)][string]$Repository)
$ErrorActionPreference = 'Stop'
function Invoke-PZGit([string[]]$Commands) {
  $out = & git.exe -C $Repository @Commands 2>&1
  if ($LASTEXITCODE -ne 0) { throw "git $($Commands -join ' ') failed: $out" }
  return ($out | Out-String).Trim()
}
try {
  $root = Invoke-PZGit -Commands @('rev-parse','--show-toplevel')
  $branch = Invoke-PZGit -Commands @('symbolic-ref','--quiet','--short','HEAD')
  $head = Invoke-PZGit -Commands @('rev-parse','HEAD')
  $upstream = Invoke-PZGit -Commands @('rev-parse','--abbrev-ref','--symbolic-full-name','@{upstream}')
  $remote = ($upstream -split '/')[0]
  $status = Invoke-PZGit -Commands @('status','--porcelain=v1','--untracked-files=normal')
  $gitDir = Invoke-PZGit -Commands @('rev-parse','--git-dir')
  $absGitDir = if ([IO.Path]::IsPathRooted($gitDir)) {$gitDir} else {Join-Path $root $gitDir}
  $unfinished = @('MERGE_HEAD','REBASE_HEAD','rebase-apply','rebase-merge','CHERRY_PICK_HEAD') | Where-Object {Test-Path (Join-Path $absGitDir $_)}
  # Fetch is read-only with respect to working-tree files; it updates remote-tracking refs.
  Invoke-PZGit -Commands @('fetch',$remote) | Out-Null
  $counts = Invoke-PZGit -Commands @('rev-list','--left-right','--count',"HEAD...$upstream")
  $parts = $counts -split '\s+'
  $ahead = [int]$parts[0]; $behind = [int]$parts[1]
  $remoteHead = Invoke-PZGit -Commands @('rev-parse',$upstream)
  $defaultRef = ''
  try { $defaultRef = Invoke-PZGit -Commands @('symbolic-ref',"refs/remotes/$remote/HEAD") } catch { $defaultRef = '' }
  $defaultAhead = $null; $defaultBehind = $null
  if ($defaultRef) {
    $d = (Invoke-PZGit -Commands @('rev-list','--left-right','--count',"HEAD...$defaultRef")) -split '\s+'
    $defaultAhead = [int]$d[0]; $defaultBehind = [int]$d[1]
  }
  $result = [ordered]@{ status='PASS'; repository=$root; branch=$branch; head=$head; upstream=$upstream; upstream_sha=$remoteHead; ahead=$ahead; behind=$behind; default_branch_ref=$defaultRef; default_ahead=$defaultAhead; default_behind=$defaultBehind; dirty=([bool]$status); unfinished_operations=@($unfinished); message='' }
  if ($behind -gt 0 -or $unfinished.Count -gt 0) { $result.status='BLOCKED'; $result.message='Behind/diverged upstream or unfinished Git operation; reconcile manually before edits.' }
  elseif ($status) { $result.status='REVIEW'; $result.message='Uncommitted/untracked files exist; inspect before editing.' }
  elseif (-not $defaultRef) { $result.status='REVIEW'; $result.message='Remote default branch could not be identified; verify default-branch freshness manually.' }
  elseif ($defaultBehind -gt 0) { $result.status='REVIEW'; $result.message='Feature branch does not contain latest remote default branch; review before editing.' }
  $result | ConvertTo-Json -Depth 4
  if ($result.status -eq 'BLOCKED') { exit 2 }
  if ($result.status -eq 'REVIEW') { exit 3 }
  exit 0
} catch {
  [ordered]@{status='UNKNOWN';message=$_.Exception.Message;repository=$Repository} | ConvertTo-Json
  exit 4
}
