param([string]$HomeDirectory=$env:USERPROFILE, [Parameter(Mandatory)][string]$RepositoryRoot)
$ErrorActionPreference='Stop'
$state=Get-Content -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-state.json') -Raw | ConvertFrom-Json
$skillNames=@($state.managed.PSObject.Properties.Name | Where-Object {$_ -match '^global/.agents/skills/([^/]+)/SKILL.md$'} | ForEach-Object {($_ -split '/')[3]})
if($skillNames.Count -ne 23){throw 'Expected 23 managed global skills'}
foreach($name in $skillNames){if(-not(Test-Path -LiteralPath (Join-Path $HomeDirectory ".agents/skills/$name/SKILL.md"))){throw "Missing global skill $name"}}
# Managed worktrees are a container, not another mod repository.
$projects=@(Get-ChildItem -LiteralPath $RepositoryRoot -Directory | Where-Object {$_.Name -ne '.worktrees'})
$globalGuide=(Join-Path $HomeDirectory '.codex/AGENTS.md').Replace('\','/')
$portableGuide='(?<![\w./:%~$-])(?:%USERPROFILE%|\$env:USERPROFILE|~)/\.codex/AGENTS\.md(?![\w/]|\.[\w./])'
$absoluteGuide='(?<![\w./:%~$-])'+[regex]::Escape($globalGuide)+'(?![\w/]|\.[\w./])'
foreach($project in $projects){
 $guide=Join-Path $project.FullName 'AGENTS.md'
 if(-not(Test-Path -LiteralPath $guide)){throw "Missing project guide: $($project.Name)"}
 $text=[string](Get-Content -LiteralPath $guide -Raw)
 $normalized=$text.Replace('\','/')
 $managed=$text.Contains('PZ-CODEX-MANAGED-STARTUP')
 $custom=($normalized -match $portableGuide) -or ($normalized -match $absoluteGuide)
 if(-not($managed -or $custom)){throw "Missing startup reference: $($project.Name). Reference the global .codex/AGENTS.md or retain the managed startup block."}
}
[pscustomobject]@{Status='PASS';Projects=$projects.Count;GlobalSkills=$skillNames.Count;Ownership='Global team store; project rules/settings independent'} | ConvertTo-Json
