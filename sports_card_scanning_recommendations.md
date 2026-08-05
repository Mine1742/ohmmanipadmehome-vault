# Sports Card Scanning & Data Extraction – Technical Recommendations

_Revised 2026-08-04. Superseded the original classic-CV design below — vision-LLM capability moved fast enough since the first draft that a custom YOLO+OCR-ensemble pipeline is no longer the right default for a hobbyist-scale project. See [[Sports Card Scanning Hub]] for project tracking._

This document specifies a mobile-to-backend pipeline that captures sports card images, extracts data fields accurately, and populates a database. Written for implementation by an AI coding agent or by hand, at hobbyist scale (a personal collection — hundreds to a few thousand cards, not a commercial SaaS).

---

## 0. What changed from the original design, and why

The original spec (custom YOLOv8 field-detector + EasyOCR/Tesseract ensemble + RapidFuzz canonicalization, with monthly retraining) made sense when general OCR was the best available text-reading tool. As of August 2026, frontier vision-LLMs (Claude Sonnet 5 / Opus 5, GPT-5 vision, Gemini) can read a card photo and return structured JSON for most fields in a single API call, at low-90s-to-97% accuracy on document-style extraction benchmarks — competitive with or better than a hand-built OCR ensemble, without training or maintaining any models yourself.

This **eliminates the need for**: custom object-detection training, an OCR ensemble with voting logic, and a monthly retraining loop.

This **does not eliminate the need for**: on-device crop/deskew for a good capture UX, a fallback path for small serial numbers and foil/holographic glare (the vision-LLM benchmarks above are not card-specific, and serial numbers are exactly the kind of tiny-print-in-a-large-frame case where general vision-LLMs are weakest), and a canonicalization/enrichment layer against a reference card database (no vision-LLM knows your exact checklist of parallels).

No public benchmark tests vision-LLMs on trading cards specifically (foil surfaces, small serials, angled toploader glare) — validate accuracy against your own sample of card photos before committing to this architecture for real.

---

## 1. High-Level Architecture

### **Overall Workflow**
1. User captures card photo (front + back) with mobile app or web camera capture.
2. On-device: detect card edges, auto-crop, deskew/straighten. No field-level detection needed on-device.
3. Image uploaded to backend API.
4. Backend runs:
   - **Single vision-LLM call** with a structured-output schema (player, team, year, set, card number, serial/print number, parallel/insert type) — see [§2](#2-key-components--tools).
   - **Targeted retry** for low-confidence or missing fields — especially serial number — using a cropped zoom of that region, either re-sent to the vision-LLM or run through a specialized OCR model.
   - **Canonicalization** against a reference card database (fuzzy match player/set/team names, resolve year/parallel).
   - **Confidence scoring** (LLM self-reported confidence + cross-check on retry).
5. Results stored in database with raw model output + confidence.
6. Low-confidence fields flagged for human review.

---

## 2. Key Components & Tools

### **On-Device Capture Assist (crop/deskew only)**
Purpose is a snappy capture UX and a clean image before upload — not field extraction.
- **YOLO26** (Jan 2026, edge-optimized, NMS-free, ~43% faster CPU inference than YOLO11-N) or **RF-DETR** (Apache-2.0) via TFLite/CoreML if you want a custom-trained card-boundary detector.
- Simpler alternative: a document-scanner SDK with built-in real-time boundary detection + perspective deskew (e.g., Dynamsoft Capture Vision) — likely less work than training a custom model for a hobbyist build.
- YOLOv8 still works but is dated relative to the above.

### **Field Extraction (primary): Vision-LLM structured output**
- **Recommended:** Claude Sonnet 5 (or Opus 5 for the hardest cases — vintage, heavy foil) via the Claude API, using a JSON schema / structured-output request for: player, team, year, set, card_number, serial_number, parallel_insert_type, notable_flags (autograph/relic).
- Alternatives: GPT-5 vision, Gemini — comparable accuracy on document-extraction benchmarks (mid-90s%); worth A/B testing all three against a sample of ~50 of your own cards before picking one, since none has a published trading-card-specific benchmark.
- Send front and back in one call where possible (most fields are on the front; serial numbers are sometimes on the back).
- Prompt should describe card layout conventions (position of card number, typical serial format like "12/99") to reduce misreads.

### **Serial Number / Small-Print Fallback**
This is the highest-risk field for a general vision-LLM. If confidence is low or the value looks malformed (not matching `\d+/\d+` or similar):
- Crop tightly to the serial-number region (from the on-device boundary detection or a second LLM call asking "where is the serial number located") and re-run extraction on the zoomed crop.
- Consider a specialized OCR model tuned for small print (PaddleOCR-VL, GLM-OCR) as a second opinion on the cropped region, rather than a general OCR ensemble.

### **Canonicalization & Enrichment**
No unified official canonicalization API exists (PSA/Beckett/TCGplayer don't offer one). Build a reference table from:
- **TCG Price Lookup** (launched June 2026) — 300K+ cards across 8 TCGs, TCGplayer/eBay pricing, PSA/BGS/CGC graded values.
- **TCGAPI.net** — deep set/promo/variant/grading-ID coverage (stronger on non-sports TCGs; check sports coverage).
- **PSA API** — cert-number/pop-report lookup (grading verification, not general card ID).
- Scraped/manually-entered set checklists for anything not covered above — for sports cards specifically, no third party has sports-card coverage close to CollX's proprietary (non-public) 17–20M-card database, so expect to self-assemble gaps.
- **RapidFuzz** still earns its keep here — fuzzy-matching extracted values against this reference table, not against raw OCR noise.

### **Confidence Scoring**
Store per field:
- LLM self-reported confidence (ask the model to include this in its structured response)
- Agreement between initial pass and retry/zoom pass, where a retry happened
- Fuzzy-match distance to canonical reference data
- Final overall field confidence

Mark fields under a 0.85 threshold for manual review — same bar as before, cheaper to hit now since a review is a targeted re-crop-and-ask rather than a full ensemble re-run.

---

## 3. Image Preprocessing Pipeline

Lighter than the original design — vision-LLMs are considerably more robust to lighting/angle/blur variation than a classic OCR pipeline, so heavy preprocessing mostly isn't needed before the main extraction call.

1. **Autocrop + deskew:** from on-device boundary detection (see §2).
2. **Glare check:** flag (don't necessarily correct) likely glare on foil/holographic cards — worth a recapture prompt to the user rather than software correction.
3. **Super-resolution (optional, targeted):** only worth applying to a serial-number crop that's genuinely too low-res to read, not the whole image.

Denoise/sharpen/full-frame color normalization from the original design are no longer worth the complexity — drop unless testing shows a specific accuracy problem they'd fix.

---

## 4. Data Model (Database Schema)

### **cards Table**
- id (PK)
- player_id (FK)
- set_id (FK)
- year (int)
- card_number (string)
- serial_number (string)
- extraction_method (enum: `llm_primary`, `llm_retry_crop`, `ocr_fallback`, `manual`)
- model_used (string — e.g. `claude-sonnet-5`)
- raw_llm_response_json (json)
- field_confidence_json (json)
- image_path_front (string)
- image_path_back (string)
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
- Input: image file(s) (front, optionally back) + metadata
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
  "extraction_method": "llm_primary",
  "model_used": "claude-sonnet-5",
  "fields": {
    "player": {"value": "Ken Griffey Jr", "confidence": 0.97},
    "team": {"value": "Mariners", "confidence": 0.95},
    "year": {"value": 1989, "confidence": 0.98},
    "set": {"value": "Upper Deck", "confidence": 0.96},
    "card_number": {"value": "#1", "confidence": 0.98},
    "serial_number": {"value": "N/A", "confidence": 1.0}
  },
  "needs_review": false
}
```

---

## 6. Evaluation Set (replaces "Training Dataset")

No custom detection/OCR model means no training dataset requirement — but you still need a **held-out evaluation set** to pick a vision-LLM and tune the prompt/schema:
- 50–100 of your own card photos, hand-labeled with ground truth, covering:
  - Modern base cards, vintage cards, foil/holographic parallels, graded slabs, cards in sleeves/toploaders
  - Varied lighting, angle, glare
- Run this set against each candidate model (Claude, GPT-5, Gemini) and compare per-field accuracy — pay particular attention to serial-number accuracy, since that's the expected weak point.
- Re-run the same eval set whenever you change the prompt/schema or swap models, to catch regressions.

If you do end up training a custom on-device boundary detector (§2), that still needs its own small labeled set of card-boundary bounding boxes — a much smaller lift than the original full-field-detection dataset.

---

## 7. Client‑Side (Mobile/Capture App) Recommendations

- Auto-capture when steady + card boundary detected
- On-screen card outline alignment
- Glare warning + recapture prompt (rather than software glare correction)
- Local image compression before upload
- Retry prompt if image quality is too low
- **Open scope question:** at hobbyist scale, a full native mobile app may be more than needed — a simple PWA using the browser camera API, or even a desktop drag-and-drop uploader for batch-scanning a physical stack of cards, could hit the same goal with far less build effort. Worth deciding deliberately rather than defaulting to "build a mobile app." See [[Sports Card Scanning Hub]].

---

## 8. Human‑in‑the‑Loop Workflow

- Backend flags low-confidence fields (<0.85)
- Reviewer UI shows cropped field + extracted value + retry/zoom result if one was run
- Reviewer selects correct value or edits manually
- Reviewed corrections logged to the audit table
- No model retraining loop needed — corrections mainly feed back into prompt/schema refinement and the canonicalization reference table, checked periodically against the evaluation set (§6)

---

## 9. Implementation Priorities (Milestones)

### **Phase 1 – MVP**
- Upload endpoint (front + back image)
- Single vision-LLM extraction call with structured JSON schema
- Store raw response + fields + confidence
- Minimal review UI for low-confidence fields

### **Phase 2 – Accuracy Upgrade**
- On-device crop/deskew for capture UX
- Targeted retry/zoom pass for low-confidence fields, especially serial number
- Canonicalization against reference table (TCG Price Lookup / TCGAPI.net / self-assembled checklist) with RapidFuzz
- Evaluation set (§6) built and run against 2–3 candidate models to lock in the primary model

### **Phase 3 – Production Quality**
- Serial-number OCR fallback (PaddleOCR-VL/GLM-OCR) for cases the vision-LLM still misses
- Pricing/enrichment via TCG Price Lookup
- Batch API usage (Anthropic Batches API, ~50% cost reduction) for bulk re-scans
- Periodic re-run of the evaluation set to catch model/prompt regressions

---

## 10. Summary
This is a vision-LLM-first architecture: a single structured-extraction API call does the work that used to require a trained object detector plus an OCR ensemble plus fuzzy-matching logic. Core requirements for accuracy are now:
- A clean, well-cropped input image (lightweight on-device detection, not a trained field-detector)
- A well-specified extraction schema/prompt, validated against your own evaluation set across 2–3 candidate models
- A targeted fallback for serial numbers and foil/glare cases specifically
- Canonicalization against a reference card database
- Human review fallback for anything under threshold

At hobbyist scale (~2,000 cards, front+back), total vision-LLM API cost is roughly **$15–90 one-time** (Claude Sonnet/Opus pricing, Aug 2026) — cheap enough that build effort, not API spend, is the real cost driver. This collapses the original three-phase "train a detector, build an OCR ensemble, retrain monthly" plan into something buildable by one person without a training pipeline.

This approach still supports non-sports-card use (tickets, autographs, other memorabilia with text content) — the structured-extraction schema is the only thing that changes.
