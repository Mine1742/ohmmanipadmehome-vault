# 📂 Why Move/Copy Commands Appear Only in the Full Document‑Library View

*Created 2025-07-25*

---

## Scenario  

- **Works:** `…/Site%20Owners%20Docs/Forms/AllItems.aspx` → full library UI.  
- **Doesn’t work:** hub‑site home `…/sites/LearningDevelopment` showing same library via web‑part.

---

## 🔍 Explanation

| Where you’re viewing | Actual component | Toolbar shown |
|----------------------|------------------|--------------|
| **Full library page** (`…/Forms/AllItems.aspx`) | Modern Document Library experience | **Move to, Copy to, Rename, Delete** |
| **Hub‑site page** (web‑part) | *Document Library* web‑part (or Highlighted Content) | Minimal: Open, Download, Share |

Web‑parts purposely hide management commands to prevent accidental structural changes and improve page performance.

---

## 🚀 How to Move or Copy Files

1. On the hub page, click **See all** (or the library name).  
2. You enter the full library view (`Forms/AllItems.aspx`).  
3. Select items → **Move to** / **Copy to**.  
4. If classic view appears, choose **Exit classic experience** first.

---

## 🛠 Work‑arounds for Home Page

| Method | Notes |
|--------|-------|
| **Add “Open library” link/button** | Insert Quick Link pointing to the full library page. |
| **Instruct users to click “Open in SharePoint”** | This appears on the web‑part command bar. |
| **Don’t embed—link instead** | If frequent file moves are required, direct users to the library itself. |

---

### Tags  
#sharepoint #moveTo #copyTo #webpart #documentlibrary #archkey
