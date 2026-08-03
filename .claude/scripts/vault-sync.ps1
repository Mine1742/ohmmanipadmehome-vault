# Daily local sync for the Ohmmanipadmehome vault repo.
# Pulls remote changes (from the cloud routines), auto-commits any local
# uncommitted edits with a generic message, then pushes. Run via Windows
# Task Scheduler at 7am daily - see AI Agent Toolkit notes for setup.

$vaultPath = "C:\Users\mine1\OneDrive\Desktop\Obsidian Vaults\Ohmmanipadmehome"
$logFile = Join-Path $vaultPath ".claude\scripts\vault-sync.log"

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$timestamp] $msg"
}

Set-Location $vaultPath
Log "=== Sync started ==="

$pullOutput = git pull 2>&1 | Out-String
Log "PULL: $pullOutput"

if ($pullOutput -match "CONFLICT") {
    Log "Merge conflict detected - skipping commit/push. Resolve manually, then re-run."
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Log "PULL FAILED (exit $LASTEXITCODE) - skipping commit/push."
    exit 1
}

$status = git status --porcelain
if ($status) {
    git add -A
    $commitMsg = "Auto-sync $(Get-Date -Format yyyy-MM-dd)"
    git commit -m $commitMsg | Out-Null
    Log "COMMIT: $commitMsg"
} else {
    Log "No local changes to commit."
}

$pushOutput = git push 2>&1 | Out-String
Log "PUSH: $pushOutput"
Log "=== Sync finished ==="
