[[Bluebeam]]
# 🖼 Bluebeam Snapshot Tool – Character Cutoff Issue

In **Bluebeam Revu**, the Snapshot Tool occasionally fails to capture full characters — especially letters like **g, y, p, q** (descenders) or **l, h, b** (ascenders). Here's why it happens and how to avoid it.

---

## 🧠 Why It Happens

### 📌 1. Anti-Aliasing and Font Rendering
- Text may be rendered using **vector outlines**, **embedded fonts**, or **flattened raster images**
- Partially flattened or layered content can cause edge artifacts

### 📌 2. Zoom Level Affects Accuracy
- Snapshots are taken at screen resolution
- **Zooming out** may cause Bluebeam to omit thin lines or font strokes

### 📌 3. Bounding Box Snapping
- Bluebeam attempts to "snap" the snapshot tool to text bounding boxes
- Tight bounding boxes may clip descenders or overhanging characters

### 📌 4. Text Line Thickness
- Thin fonts (like Arial Narrow) may fall below the visible capture threshold at normal zoom

---

## ✅ Workarounds and Best Practices

| Strategy | Description |
|----------|-------------|
| 🔍 **Zoom in before snipping** | Use 200–300% zoom for better rendering accuracy |
| ➕ **Draw slightly larger boxes** | Include extra padding around the text when using the Snapshot Tool |
| 🧱 **Flatten the PDF first** | Use `Document > Flatten` to merge layers and simplify rendering |
| 🖨 **Export as image or print** | Use `File > Export > Image` or `Print to Bluebeam PDF` for clean captures |
| 🧭 **Avoid snapping at low zoom levels** | Precision improves when viewing at higher resolution |

---

## 🧪 Tip

Use the keyboard shortcut **Ctrl + Shift + S** to quickly activate the Snapshot Tool and improve workflow when zoomed in.

---

