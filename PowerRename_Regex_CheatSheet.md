[[Windows Hub]] #powerrename
# 🛠 PowerRename Regex Cheat Sheet

PowerRename (part of Microsoft PowerToys) supports **regular expressions (regex)** to perform batch file renaming with powerful flexibility.

---

## ✅ Common Task: Remove Everything After Dash or Underscore

**Search for:**
```
[-_].*
```

**Replace with:**
```
```
*(leave empty)*

🧠 **Explanation:**
- `[-_]` matches either a dash `-` or underscore `_`
- `.*` matches everything after the first dash or underscore

---

## 🔁 Other Useful Regex Patterns

### 🔹 1. Remove Numbers from Filenames
**Search for:**
```
\d+
```

**Replace with:**
```
```

**Effect:** `file123.txt` → `file.txt`

---

### 🔹 2. Add Prefix to All Filenames
**Search for:**
```
^(.*)
```

**Replace with:**
```
NEW_$1
```

**Effect:** `report.docx` → `NEW_report.docx`

---

### 🔹 3. Change File Extension
**Search for:**
```
\.txt$
```

**Replace with:**
```
.docx
```

**Effect:** `notes.txt` → `notes.docx`

---

### 🔹 4. Keep Only Filename Without Extension
**Search for:**
```
\..*$
```

**Replace with:**
```
```

**Effect:** `project_final.xlsx` → `project_final`

---

### 🔹 5. Replace Underscores with Spaces
**Search for:**
```
_
```

**Replace with:**
```
(space character)
```

**Effect:** `client_report_2025.pdf` → `client report 2025.pdf`

---

### ✅ Tips

- Always enable the **regex mode** (click the `.*` button in PowerRename).
- Use the **preview pane** to ensure your changes look right before applying.
- `^` = start of string, `$` = end of string
- `\.` = a literal dot (file extension separator)
- `.*` = everything (wildcard)
- `\d` = digit

---

For more patterns, see: [regex101.com](https://regex101.com) to test and learn regex syntax.
