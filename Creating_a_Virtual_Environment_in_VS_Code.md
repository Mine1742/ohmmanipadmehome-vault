# Creating a Virtual Environment in VS Code

## Prerequisites
- [Python](https://www.python.org/downloads/) installed  
  (check with `python --version` or `python3 --version`)  
- [Visual Studio Code](https://code.visualstudio.com/) installed with the **Python extension**  
- A project folder ready (e.g., `my_project`)

---

## 1. Open Your Project in VS Code
1. Launch **VS Code**  
2. Go to **File → Open Folder...** and select your project folder  

---

## 2. Create the Virtual Environment
Open the integrated terminal in VS Code (`Ctrl+`` or **View → Terminal**) and run:

**Windows (PowerShell or Command Prompt):**
```powershell
python -m venv .venv
```

**Mac/Linux (bash/zsh):**
```bash
python3 -m venv .venv
```

> `.venv` is the environment folder created inside your project.  
> You can name it something else, but `.venv` is a common convention.  

---

## 3. Activate the Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Mac/Linux (bash/zsh):**
  ```bash
  source .venv/bin/activate
  ```

After activation, you’ll see `(.venv)` before the command prompt.  

---

## 4. Configure VS Code to Use the Virtual Environment
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the **Command Palette**  
2. Search for **Python: Select Interpreter**  
3. Choose the interpreter pointing to your `.venv` (e.g., `.venv/bin/python` or `.venv\Scripts\python.exe`)  

---

## 5. Verify Setup
In the terminal, run:
```bash
which python    # Mac/Linux
where python    # Windows
```

It should point to your `.venv` folder.  

Install packages inside the environment:
```bash
pip install requests
```

---

✅ Your Python project is now isolated in a virtual environment inside VS Code.  

---

## Tags
#Python #Venv #VSCode #Troubleshooting #Setup
