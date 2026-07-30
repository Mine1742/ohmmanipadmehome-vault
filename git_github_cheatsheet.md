# 🧬 Git & GitHub Cheat Sheet

Essential commands and workflows for version control, collaboration, and DevOps integration.

---

## ⚙️ SETUP & CONFIGURATION

```bash
git config --global user.name "Albert Smith"
git config --global user.email "albert@example.com"
git config --global core.editor "code --wait"
git config --list
```

To verify config:
```bash
git config user.name
git config user.email
```

---

## 📁 REPOSITORY MANAGEMENT

```bash
git init                             # Initialize local repo
git clone https://github.com/user/repo.git
git remote -v                        # List remotes
git remote add origin https://github.com/user/repo.git
git remote set-url origin git@github.com:user/repo.git
```

---

## 💾 STAGING & COMMITTING

```bash
git status                           # Check status
git add file.txt                     # Stage specific file
git add .                            # Stage all changes
git commit -m "Add new feature"
git commit --amend -m "Updated commit message"
git restore --staged file.txt        # Unstage file
```

---

## 🌿 BRANCHING & MERGING

```bash
git branch                           # List branches
git branch new-feature               # Create branch
git checkout new-feature             # Switch branch
git switch -c hotfix                 # Create and switch branch
git merge new-feature                # Merge into current branch
git branch -d new-feature            # Delete branch
git log --oneline --graph --all
```

---

## 🧭 SYNCHRONIZATION

```bash
git pull origin main                 # Fetch + merge from remote
git fetch origin                     # Fetch only
git push origin main                 # Push changes
git push -u origin main              # Set upstream
git push --force                     # Force push (use carefully)
```

---

## 🔍 INSPECTION & HISTORY

```bash
git log --oneline
git show HEAD
git diff                             # Compare unstaged changes
git diff --staged                    # Compare staged changes
git blame file.txt                   # Show commit history per line
git reflog                           # Show all reference logs
```

---

## 🧱 STASH & RESET

```bash
git stash save "WIP before update"
git stash list
git stash apply                      # Restore most recent stash
git stash pop                        # Apply and remove
git stash drop stash@{1}
git reset --soft HEAD~1              # Undo last commit, keep changes
git reset --hard HEAD~1              # Undo commit & delete changes
```

---

## 🧩 TAGS & RELEASES

```bash
git tag -a v1.0 -m "First release"
git tag
git push origin v1.0
git push origin --tags
git checkout v1.0
```

---

## 🔐 SSH AUTHENTICATION

```bash
ssh-keygen -t ed25519 -C "albert@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Add the key to GitHub → **Settings → SSH and GPG keys**

---

## 🌐 GITHUB WORKFLOWS

### **Create a new repo from CLI**
```bash
gh repo create my-project --public --source=. --remote=origin
gh repo clone my-project
```

### **Common Actions**
```bash
gh issue create --title "Bug report" --body "Steps to reproduce..."
gh pr create --base main --head feature-branch --title "Add new feature"
gh pr status
gh pr merge --squash
```

---

## 🧾 COLLABORATION & REVIEW

```bash
git fetch origin pull/ID/head:pr-ID
git checkout pr-ID
git diff main..feature-branch
git cherry-pick <commit-hash>
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Initialize repo | `git init` |
| Clone remote | `git clone URL` |
| Create new branch | `git checkout -b feature` |
| Stage & commit | `git add . && git commit -m "msg"` |
| Push to GitHub | `git push origin main` |
| Undo last commit | `git reset --soft HEAD~1` |
| View history graph | `git log --oneline --graph --all` |
| Merge PR | `gh pr merge --squash` |

---

## 💡 TIPS

- Use `git restore` to safely revert local changes.  
- Use `git log -p` to see patches for each commit.  
- Always pull before pushing to avoid conflicts.  
- Protect `main` branch and use Pull Requests for merges.  
- Use `.gitignore` to exclude build artifacts and secrets.  
- Add automation with **GitHub Actions** YAML workflows.

---

**Created for:** Git and GitHub daily DevOps tasks  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #git #github #versioncontrol #devops #automation
