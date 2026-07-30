
git status        # What changed?
git log --oneline # What commits exist?
git remote -v     # Where can I push?
git branch        # What branch am I on?


## Git Workflow for Multi-Environment Development

### 1. Understanding Your Branches

You have several branches:

- **main** - Your primary/production branch
- **master** - Looks like an older default branch (GitHub switched from master to main)
- **Feature branches** - Like `claude/setup-local-environment-...` (where you are now)

### 2. Essential Git Commands for Your Workflow

#### Checking What's Different

```bash
# See what you've changed locally (not yet staged)
git diff

# See what's staged for commit
git diff --cached

# Compare your current branch with main
git diff main

# Compare your local branch with the remote version
git diff origin/claude/setup-local-environment-01QXvHq5LnK54Tx1oowpsZvE

# See what files have changed
git status
```

#### Keeping in Sync with GitHub

```bash
# Download latest changes from GitHub (doesn't modify your files)
git fetch origin

# See all branches and where they are
git branch -a

# Update your current branch with latest from GitHub
git pull origin <branch-name>

# Push your changes to GitHub
git push origin <branch-name>
```

### 3. Recommended Workflow for Working with Multiple AI Tools

Here's the workflow I recommend:

#### A. Starting Work (Any Environment)

```bash
# 1. Make sure you're on the right branch
git checkout main  # or your feature branch

# 2. Get latest changes from GitHub
git pull origin main

# 3. Create a new branch for your feature
git checkout -b feature/your-feature-name

# 4. Make your changes with Claude Code/Copilot/etc.
```

#### B. Saving Your Work

```bash
# 1. See what changed
git status
git diff

# 2. Stage files you want to commit
git add <file>          # Add specific file
git add .               # Add all changes
git add -A              # Add all changes including deletions

# 3. Commit with a clear message
git commit -m "feat: describe what you did"

# 4. Push to GitHub
git push origin feature/your-feature-name
```

#### C. Switching Between Environments

```bash
# Before switching environments, always commit and push:
git add -A
git commit -m "WIP: working on feature X"
git push origin your-branch-name

# In the new environment, pull the latest:
git fetch origin
git checkout your-branch-name
git pull origin your-branch-name
```

### 4. Comparing Local vs GitHub

Let me create a simple script to show you the comparison:

Bash

⎿Fetch latest from GitHub

IN

cd dao-of-life && git fetch origin

Bash

⎿Show current status comparison

IN

cd dao-of-life && echo "=== Current Branch ===" && git branch --show-current && echo "" && echo "=== Files Changed Locally (Staged) ===" && git diff --cached --name-status | head -20

### 5. Important Notes About Your Current Staged Files

I notice you have some files staged that probably **shouldn't** be committed to GitHub:

- `.test-tokens/*` - Test tokens (security risk!)
- `test-results/*` - Test output files
- `playwright-report/*` - Test reports

These should be in your [.gitignore](vscode-webview://0jmtd80gfcikptmm3nosgc2ksc2s9n1mofhgqe4pi07lehmtsmts/.gitignore) file. Let me check:

Read [c:\Local Dev Workspaces\BMAD\dao-of-life\.gitignore](vscode-webview://0jmtd80gfcikptmm3nosgc2ksc2s9n1mofhgqe4pi07lehmtsmts/index.html?id=729ba549-d41d-4565-bffd-4b1962f7a52e&parentId=1&origin=6b812025-4f82-4091-b622-412980aec70e&swVersion=4&extensionId=Anthropic.claude-code&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&session=40e90f34-106c-4416-9c03-76b84341e15f#)

I need to help you prevent committing sensitive test files. Let me update your .gitignore and unstage those files:

Edit [c:\Local Dev Workspaces\BMAD\dao-of-life\.gitignore](vscode-webview://0jmtd80gfcikptmm3nosgc2ksc2s9n1mofhgqe4pi07lehmtsmts/index.html?id=729ba549-d41d-4565-bffd-4b1962f7a52e&parentId=1&origin=6b812025-4f82-4091-b622-412980aec70e&swVersion=4&extensionId=Anthropic.claude-code&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&session=40e90f34-106c-4416-9c03-76b84341e15f#)




## Complete Git Workflow Guide for Multi-Environment Development

### Your Current Status (Much Better Now!)

Good news! I've cleaned up your staged files. Now you only have the important files ready to commit:

- Documentation files
- Test configuration
- Test code (but not test outputs)
- The updated .gitignore

### Quick Reference Commands

#### 1. Before Starting Work (Any Environment)

```bash
cd dao-of-life
git fetch origin                    # Check for updates
git status                          # See what branch you're on
git pull origin <branch-name>       # Get latest changes
```

#### 2. Compare Local vs GitHub

```bash
# See differences between local and remote
git fetch origin
git diff origin/<branch-name>

# See what commits are different
git log origin/<branch-name>..HEAD    # What you have locally that's not on GitHub
git log HEAD..origin/<branch-name>    # What's on GitHub that you don't have

# Visual comparison of all branches
git log --oneline --graph --all --decorate -20
```

#### 3. Switching AI Environments

**Before leaving your current environment:**

```bash
git add -A
git commit -m "WIP: describe what you were working on"
git push origin <branch-name>
```

**When starting in a new environment:**

```bash
git fetch origin
git checkout <branch-name>
git pull origin <branch-name>
```

#### 4. When You're Done with Changes

```bash
# Check what changed
git status
git diff

# Stage the .gitignore change too
git add .gitignore

# Commit everything
git commit -m "feat: add e2e tests and test documentation"

# Push to GitHub
git push origin claude/setup-local-environment-01QXvHq5LnK54Tx1oowpsZvE
```

### Best Practices for Your Workflow

1. **Always Fetch Before Starting Work**
    
    ```bash
    git fetch origin && git status
    ```
    
2. **Commit Often** - Small, focused commits are better
    
    ```bash
    git add <specific-files>
    git commit -m "descriptive message"
    ```
    
3. **Push Regularly** - Don't let local changes pile up
    
    ```bash
    git push origin <branch-name>
    ```
    
4. **Use Descriptive Branch Names**
    
    - `feature/user-authentication`
    - `fix/login-bug`
    - `docs/add-readme`
5. **Check for Conflicts Early**
    
    ```bash
    git fetch origin
    git merge origin/<branch-name> --no-commit --no-ff
    # If conflicts, resolve them before committing
    ```
    

### Visual Git Status Alias (Optional)

You can add this to your git config for a nice visual status:

```bash
git config --global alias.st "status -sb"
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

Then use:

- `git st` for quick status
- `git lg` for pretty log

### Your Next Steps

Right now you should:

1. **Add the .gitignore change:**
    
    ```bash
    git add .gitignore
    ```
    
2. **Review what you're about to commit:**
    
    ```bash
    git status
    git diff --cached
    ```
    
3. **Commit your changes:**
    
    ```bash
    git commit -m "feat: add e2e tests for magic link authentication and update gitignore"
    ```
    
4. **Push to GitHub:**
    
    ```bash
    git push origin claude/setup-local-environment-01QXvHq5LnK54Tx1oowpsZvE
    ```