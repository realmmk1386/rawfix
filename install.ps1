<#
.SYNOPSIS
    Installs the RawFix skill for Antigravity, Claude Code, and Codex on Windows.
.PARAMETER Target
    Target assistant: 'All' (default), 'Antigravity', 'Claude', or 'Codex'.
#>

param (
    [ValidateSet('All', 'Antigravity', 'Claude', 'Codex')]
    [string]$Target = 'All'
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Installing RawFix Skill for AI Coding Agents     " -ForegroundColor Cyan
Write-Host " Target: $Target                                  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check Python Dependencies
Write-Host "`n[*] Checking Python prerequisites..." -ForegroundColor Yellow
try {
    & python -c "import pypdf, PIL; print('[+] Python dependencies pypdf and pillow are installed.')"
} catch {
    Write-Host "[!] Missing required Python libraries. Installing pypdf and pillow..." -ForegroundColor Yellow
    & pip install pypdf pillow
}

function Install-ToDir ($destDir, $agentName) {
    Write-Host "`n[*] Installing for $agentName -> $destDir" -ForegroundColor Green
    if (!(Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    
    # Copy SKILL.md
    Copy-Item -Path (Join-Path $ScriptDir "SKILL.md") -Destination (Join-Path $destDir "SKILL.md") -Force
    
    # Copy scripts
    $destScripts = Join-Path $destDir "scripts"
    if (!(Test-Path $destScripts)) {
        New-Item -ItemType Directory -Path $destScripts -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $ScriptDir "scripts\*") -Destination $destScripts -Force
    
    Write-Host "[+] Successfully installed for $agentName." -ForegroundColor Green
}

# 2. Antigravity
if ($Target -eq 'All' -or $Target -eq 'Antigravity') {
    $antigravityDir = Join-Path $env:USERPROFILE ".gemini\config\skills\rawfix"
    Install-ToDir $antigravityDir "Antigravity"
}

# 3. Claude Code
if ($Target -eq 'All' -or $Target -eq 'Claude') {
    $claudeSkillDir = Join-Path $env:USERPROFILE ".claude\skills\rawfix"
    Install-ToDir $claudeSkillDir "Claude Code"
    
    # Copy Claude command
    $claudeCmdDir = Join-Path $env:USERPROFILE ".claude\commands"
    if (!(Test-Path $claudeCmdDir)) {
        New-Item -ItemType Directory -Path $claudeCmdDir -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $ScriptDir ".claude\commands\rawfix.md") -Destination (Join-Path $claudeCmdDir "rawfix.md") -Force
    Write-Host "[+] Claude Code slash command installed at $claudeCmdDir\rawfix.md" -ForegroundColor Green
}

# 4. Codex / OpenAI
if ($Target -eq 'All' -or $Target -eq 'Codex') {
    $codexDir = Join-Path $env:USERPROFILE ".codex\skills\rawfix"
    Install-ToDir $codexDir "Codex / Universal Agent"
}

Write-Host "`n[✓] RawFix installation complete! You can now use /rawfix in your chats." -ForegroundColor Cyan
