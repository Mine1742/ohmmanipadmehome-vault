# 📝 Git Cheat Sheet

## 🔍 Check Status
```bash
git status
```

## ➕ Stage Changes
```bash
git add .
# or add specific files
git add app/models.py
```

## 💾 Commit
```bash
git commit -m "Your descriptive commit message"
```

## 🚀 Push to Remote
```bash
git push
```

## 🔗 Setup Remote (first-time only)
```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

## ⬇️ Pull Latest Changes
```bash
git pull origin main
```

---

## 🌿 Branching Basics

### Create a New Branch
```bash
git checkout -b feature/my-new-feature
```

### Switch Branches
```bash
git checkout main
git checkout feature/my-new-feature
```

### List Branches
```bash
git branch
```

### Push Branch to Remote
```bash
git push -u origin feature/my-new-feature
```

---

## 🔀 Merging & Rebasing

### Merge Feature into Main
```bash
git checkout main
git pull origin main   # get latest
git merge feature/my-new-feature
git push origin main
```

### Rebase (keep history cleaner)
```bash
git checkout feature/my-new-feature
git pull --rebase origin main
```

---

## 🧹 Cleaning Up

### Delete Local Branch
```bash
git branch -d feature/my-old-feature
```

### Delete Remote Branch
```bash
git push origin --delete feature/my-old-feature
```

---

## ⚠️ Troubleshooting / Useful Commands

### Undo Last Commit (keep changes staged)
```bash
git reset --soft HEAD~1
```

### Undo Last Commit (discard changes)
```bash
git reset --hard HEAD~1
```

### See Commit History
```bash
git log --oneline --graph --decorate --all
```

### Stash Changes (save without committing)
```bash
git stash
git stash pop
```

---
