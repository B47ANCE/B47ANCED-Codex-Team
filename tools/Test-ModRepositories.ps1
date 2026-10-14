param([string]$HomeDirectory=$env:USERPROFILE, [Parameter(Mandatory)][string]$RepositoryRoot)
$ErrorActionPreference='Stop'
$state=Get-Content -LiteralPath (Join-Path $HomeDirectory '.codex/b47anced-team-state.json') -Raw | ConvertFrom-Json
$skillNames=@($state.managed.PSObject.Properties.Name | Where-Object {$_ -match '^global/.agents/skills/([^/]+)/SKILL.md$'} | ForEach-Object {($_ -split '/')[3]})
if($skillNames.Count -ne 23){throw 'Expected 23 managed global skills'}
foreach($name in $skillNames){if(-not(Test-Path -LiteralPath (Join-Path $HomeDirectory ".agents/skills/$name/SKILL.md"))){throw "Missing global skill $name"}}
$projects=@(Get-ChildItem -LiteralPath $RepositoryRoot -Directory)
foreach($project in $projects){
 $guide=Join-Path $project.FullName 'AGENTS.md'
 if(-not(Test-Path -LiteralPath $guide)){throw "Missing project guide: $($project.Name)"}
 if(-not(Get-Content -LiteralPath $guide -Raw).Contains('PZ-CODEX-MANAGED-STARTUP')){throw "Missing startup reference: $($project.Name)"}
}
[pscustomobject]@{Status='PASS';Projects=$projects.Count;GlobalSkills=$skillNames.Count;Ownership='Global team store; project rules/settings independent'} | ConvertTo-Json
