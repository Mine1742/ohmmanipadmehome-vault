# Daily local sync for the Ohmmanipadmehome vault repo.
# Commits any local edits FIRST (so the working tree is clean), then pulls
# with rebase+autostash, then pushes. Committing before pulling avoids the
# common "local changes would be overwritten by merge" failure. On any
# pull/rebase problem it aborts cleanly and skips the push rather than
# leaving conflict markers sitting in vault notes - check vault-sync.log
# if a morning's sync didn't go through. Run via Windows Task Scheduler at
# 7am daily - see AI Agent Toolkit notes for setup.

$vaultPath = "C:\Users\mine1\OneDrive\Desktop\Obsidian Vaults\Ohmmanipadmehome"
$logFile = Join-Path $vaultPath ".claude\scripts\vault-sync.log"

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$timestamp] $msg"
}

Set-Location $vaultPath
Log "=== Sync started ==="

$status = git status --porcelain
if ($status) {
    git add -A
    $commitMsg = "Auto-sync $(Get-Date -Format yyyy-MM-dd)"
    git commit -m $commitMsg | Out-Null
    Log "COMMIT: $commitMsg"
} else {
    Log "No local changes to commit."
}

$pullOutput = git pull --rebase --autostash 2>&1 | Out-String
Log "PULL: $pullOutput"

if ($LASTEXITCODE -ne 0) {
    Log "PULL/REBASE FAILED OR CONFLICTED (exit $LASTEXITCODE) - aborting rebase, leaving today's commit intact locally, skipping push. Resolve manually, then re-run."
    git rebase --abort 2>&1 | Out-Null
    exit 1
}

$pushOutput = git push 2>&1 | Out-String
Log "PUSH: $pushOutput"
Log "=== Sync finished ==="
