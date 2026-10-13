param(
    [string]$PackageRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [switch]$Installed
)
$ErrorActionPreference = 'Stop'
$expected = 23
$failed = 0
function Check([bool]$Condition, [string]$Message) {
    if ($Condition) { Write-Host "PASS: $Message" -ForegroundColor Green }
    else { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed++ }
}
$root = (Resolve-Path -LiteralPath $PackageRoot).Path
$skillRoot = Join-Path $root '.agents\skills'
Check (Test-Path -LiteralPath (Join-Path $root 'AGENTS.md')) 'Package global AGENTS.md exists'
Check (Test-Path -LiteralPath (Join-Path $root '.codex\config.toml')) 'Package Codex config exists'
Check (Test-Path -LiteralPath (Join-Path $root 'README.md')) 'Package README exists'
Check (Test-Path -LiteralPath (Join-Path $root 'TEAM-ONBOARDING.md')) 'Team onboarding guide exists'
$skills = @(Get-ChildItem -LiteralPath $skillRoot -Directory -ErrorAction SilentlyContinue)
Check ($skills.Count -eq $expected) "Package has exactly $expected skills (found $($skills.Count))"
foreach ($skill in $skills) {
    $file = Join-Path $skill.FullName 'SKILL.md'
    Check ((Test-Path -LiteralPath $file) -and ((Get-Item -LiteralPath $file -ErrorAction SilentlyContinue).Length -gt 0)) "Skill $($skill.Name) has nonempty SKILL.md"
}
$config = Get-Content -LiteralPath (Join-Path $root '.codex\config.toml') -Raw
Check ($config -notmatch '(?im)^\s*(password|token|secret|api_key)\s*=') 'No obvious credential assignments in config.toml'
if ($Installed) {
    $homeDir = [Environment]::GetFolderPath('UserProfile')
    $global = Join-Path $homeDir '.codex\AGENTS.md'
    $userConfig = Join-Path $homeDir '.codex\config.toml'
    $userSkills = Join-Path $homeDir '.agents\skills'
    Check (Test-Path -LiteralPath $global) 'Installed global AGENTS.md exists'
    Check (Test-Path -LiteralPath $userConfig) 'Installed Codex config exists'
    foreach ($skill in $skills) {
        Check (Test-Path -LiteralPath (Join-Path $userSkills ($skill.Name + '\SKILL.md'))) "Installed skill $($skill.Name) exists"
    }
    $codex = Get-Command codex -ErrorAction SilentlyContinue
    Check ($null -ne $codex) 'Codex CLI is available on PATH (desktop/extension users may need manual verification)'
}
if ($failed -gt 0) { Write-Host "$failed verification check(s) failed." -ForegroundColor Red; exit 1 }
Write-Host 'Structural verification passed. Runtime integrations and Codex activation remain NOT TESTED.' -ForegroundColor Green
exit 0
