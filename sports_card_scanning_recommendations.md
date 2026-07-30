# Sports Card Scanning & Data Extraction – Technical Recommendations

This document provides a clear, structured specification for building a mobile-to-backend pipeline that can capture sports card images, extract data fields accurately, and populate a database. It is written for implementation by an AI coding agent or development team.

---

## 1. High‑Level Architecture

### **Overall Workflow**
1. User captures card photo with mobile app.
2. Mobile performs lightweight preprocessing (optional: detection + auto‑crop).
3. Image is uploaded to backend API.
4. Backend runs:
   - Object detection (card + field ROIs)
   - Image cleanup (crop, deskew, perspective correction)
   - OCR (ensemble) per field
   - Canonicalization + fuzzy matching
   - External DB enrichment (optional)
   - Confidence scoring
5. Results stored in database with raw OCR + confidence.
6. Low‑confidence fields flagged for human review.

---

## 2. Key Components & Tools

### **Object Detection (ROI Identification)**
- Recommended models:
  - **YOLOv8** (Ultralytics)
  - Detectron2 (alternative)
- Required bounding boxes:
  - Entire card
  - Player name
  - Team name
  - Year
  - Set name
  - Card number
  - Serial number / limited edition number
  - Barcode/QR (if present)

### **OCR (Text Extraction)**
Use an **ensemble OCR pipeline**:
- **EasyOCR** (deep learning; good on stylized fonts)
- **Tesseract** (fast; good for sharp text)
- **Optional cloud OCR for highest accuracy:**
  - Google Vision
  - AWS Textract
  - Azure OCR

Combine results with:
- Confidence‑weighted majority vote
- Numeric‑only mode for serial and card numbers
- Regex cleanup

### **Post‑Processing & Normalization**
- Remove punctuation, excessive spacing, OCR artifacts
- Standardize team names, player names, set names using:
  - Fuzzy matching (RapidFuzz)
  - Canonical tables
- Year normalization using patterns: `YYYY`, `'YY` → canonicalization

### **Enrichment** (Optional but Highly Recommended)
Cross‑reference extracted data with one or more authoritative sources:
- Beckett
- PSA population reports
- eBay API (for listing matching)
- Sports card dataset(s) you own

Purpose: Determine exact set, variant, and print year when OCR is ambiguous.

### **Confidence Scoring**
Store these per field:
- text OCR confidence (mean of detected characters)
- ensemble agreement score
- fuzzy‑match distance to canonical data
- final overall field confidence

Mark fields under 0.85 threshold for manual review.

---

## 3. Image Preprocessing Pipeline

1. **Denoise:** bilateral filter or non‑local means
2. **Sharpening:** unsharp mask
3. **Perspective Correction:** four‑point transform based on detector output
4. **Autocrop:** use detected card boundary
5. **Glare reduction:** CLAHE histogram equalization
6. **Super‑resolution (optional):** ESRGAN or Real‑ESRGAN
7. **Color normalization:** white‑balance correction

---

## 4. Data Model (Database Schema)

### **cards Table**
- id (PK)
- player_id (FK)
- set_id (FK)
- year (int)
- card_number (string)
- serial_number (string)
- raw_ocr_json (json)
- field_confidence_json (json)
- image_path (string)
- created_at (timestamp)

### **players Table**
- id (PK)
- full_name
- canonical_name
- aliases (json)

### **sets Table**
- id (PK)
- name
- year
- manufacturer

### **audit Table** (optional)
- card_id (FK)
- corrected_field
- old_value
- new_value
- reviewer
- timestamp

---

## 5. API Specification (Backend)

### **POST /scan/upload**
- Input: image file + metadata
- Output:
```json
{
  "status": "received",
  "job_id": "uuid"
}
```

### **GET /scan/result/{job_id}**
- Output:
```json
{
  "status": "complete",
  "fields": {
    "player": {"value": "Ken Griffey Jr", "confidence": 0.93},
    "team": {"value": "Mariners", "confidence": 0.88},
    "year": {"value": 1989, "confidence": 0.96},
    "set": {"value": "Upper Deck", "confidence": 0.91},
    "card_number": {"value": "#1", "confidence": 0.97},
    "serial": {"value": "N/A", "confidence": 1.0}
  },
  "needs_review": false
}
```

---

## 6. Training Dataset Specifications

### **Minimum Requirements**
- 1,000+ real-world card photos
- Angles, lighting variations, glare, shadows
- Cards in sleeves, toploaders, graded slabs
- Labelled bounding boxes for all key fields

### **Augmentation**
- Brightness/contrast shifts
- Random rotations (±15°)
- Perspective warp
- Simulated glare
- Blurring (light motion, Gaussian)
- JPEG compression artifacts

---

## 7. Client‑Side (Mobile App) Recommendations

- Auto‑capture when steady + card detected
- On‑screen card outline alignment
- Live glare detection suggestions
- Local compression to reduce upload size
- Optional on‑device TFLite detection for speed
- Retry prompt if image quality is too low

---

## 8. Human‑in‑the‑Loop Workflow

- Backend flags low-confidence fields (<0.85)
- Reviewer UI shows cropped field + OCR candidates
- Reviewer selects correct value or edits manually
- Reviewed data stored for retraining models
- Batch retrain monthly or when 200+ corrections accumulate

---

## 9. Implementation Priorities (Milestones)

### **Phase 1 – MVP**
- Upload endpoint
- Basic card detection (YOLOv8)
- Simple perspective correction
- OCR using EasyOCR + Tesseract
- Store raw OCR & confidence

### **Phase 2 – Accuracy Upgrade**
- Ensemble OCR + voting logic
- Canonicalization + fuzzy matching
- Confidence scoring system
- Human review interface

### **Phase 3 – Production Quality**
- External DB matching (Beckett/PSA/eBay)
- Super-resolution for low-quality images
- Data enrichment workflows
- Retraining automation

---

## 10. Summary
This document defines a full blueprint for building a highly accurate sports‑card scanning and data‑extraction system. The core requirements for accuracy are:
- Strong ROI detection (YOLOv8)
- Ensemble OCR
- Heavy canonicalization & fuzzy matching
- Human review fallback
- Continuous retraining

This approach supports not just sports cards but also photos, tickets, autographs, and other memorabilia with text content.

---

If you want, I can also create:
- A companion API spec
- A full database ER diagram
- A ready‑to‑deploy FastAPI backend template
- A YOLOv8 dataset folder structure + labeling guidelines

