# 🧰 Linux File Manipulation & Search Cheat Sheet

A practical reference for working efficiently with text files, logs, and codebases.

---

## 🔍 SEARCHING & FILTERING

### **grep**
Search for patterns inside files.
```
grep "keyword" file.txt
grep -i "error" app.log            # Case-insensitive
grep -R "def " .                   # Recursive search through folders
grep -Rl "import flask" .          # List only filenames
grep -n "TODO" *.py                # Show line numbers
grep -A 3 -B 2 "Error" log.txt     # Show 3 lines after & 2 before match
```

---

## ✂️ TEXT REPLACEMENT & EDITING

### **sed (Stream Editor)**
```
sed 's/old/new/' file.txt              # Replace first match per line
sed 's/old/new/g' file.txt             # Replace ALL matches per line
sed -i 's/old/new/g' file.txt          # Edit file in place
sed -i 's/foo/bar/g' *.html            # Replace across multiple files
sed -i '1,10s/http/https/g' file.txt   # Replace only lines 1–10
sed -i '/DEBUG/d' config.py            # Delete lines containing "DEBUG"
sed -i 's/[[:space:]]\+$//' *.py       # Remove trailing spaces
```
🪄 Tip: To preview before saving, omit the -i flag.

---

## 🧮 TEXT EXTRACTION & COLUMN OPERATIONS

### **awk**
```
awk '{print $1}' file.txt              # Print first column
awk '{print $1, $3}' file.txt          # Print first and third columns
awk '/error/ {print $2}' log.txt       # Print second column for error lines
awk 'NR==1 {print}' file.txt           # Print only first line
awk '{sum += $2} END {print sum}' data.txt  # Sum column 2
```

---

## 🧱 FILE COMBINATION & SPLITTING
```
cat file1.txt file2.txt > merged.txt   # Combine files
head -n 20 file.txt                    # Show first 20 lines
tail -n 50 app.log                     # Show last 50 lines
tail -f app.log                        # Follow live updates
split -l 1000 bigfile.txt chunk_       # Split file into 1000-line chunks
sort file.txt | uniq                   # Remove duplicates
```

---

## 🗂️ FILE & DIRECTORY MANAGEMENT
```
ls -lh                                 # Human-readable list
du -sh *                               # Show folder sizes
find . -type f -name "*.log"           # Find files by name
find . -type f -mtime -1               # Files modified in last 24h
find /etc -type f -size +5M            # Files larger than 5MB
cp -r src/ backup/                     # Copy recursively
mv oldname.txt newname.txt             # Rename file
rm -rf build/                          # Delete folder forcefully
```

---

## 🧰 COMPRESSION & ARCHIVES
```
tar -czvf archive.tar.gz folder/       # Create .tar.gz archive
tar -xzvf archive.tar.gz               # Extract archive
zip -r project.zip folder/             # Zip a folder
unzip project.zip                      # Unzip archive
```

---

## 🔒 PERMISSIONS & OWNERSHIP
```
chmod 644 file.txt                     # rw-r--r--
chmod +x script.sh                     # Make executable
chown user:group file.txt              # Change owner
sudo chown -R www-data:www-data /var/www  # Recursively
```

---

## 🧩 ADVANCED COMBOS
```
# Replace string in all .html files within subfolders
find . -type f -name "*.html" -exec sed -i 's/old/new/g' {} +

# Count occurrences of a word in multiple files
grep -Ro "flask" . | wc -l

# Find all Python files over 200 lines
find . -name "*.py" -type f -exec awk 'END {if (NR>200) print FILENAME}' {} \;

# Show top 10 largest files
find . -type f -exec du -h {} + | sort -rh | head -10
```

---

## 🧾 FILE COMPARISON
```
diff file1.txt file2.txt               # Show line-by-line differences
diff -u file1.txt file2.txt | less     # Unified diff format
vimdiff file1.txt file2.txt            # Visual diff in Vim
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Search inside files | `grep "pattern" file` |
| Replace text inline | `sed -i 's/old/new/g' file` |
| Find files by type | `find . -type f -name "*.py"` |
| Show top 10 biggest files | `du -ah . | sort -rh | head -10` |
| Combine & deduplicate | `cat *.txt | sort | uniq > clean.txt` |
| Follow logs live | `tail -f /var/log/syslog` |
| Archive folder | `tar -czvf backup.tar.gz folder/` |

---

## 🧭 Tips
- Add `| less` at the end of long commands to scroll through results.
- Use `!!` to repeat your last command.
- Use `Ctrl + R` to search your command history interactively.
- Always test with `echo` or omit `-i` before bulk-editing files with sed.

---

**Created for:** everyday DevOps, Flask, and system maintenance tasks  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #linux #cli #grep #sed #awk #bash #automation
