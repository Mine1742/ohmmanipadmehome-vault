#personal

[[Sports Card Scanning Hub]]

Tracks what's actually been built against the phases in
[[sports_card_scanning_recommendations]] §9. Code lives at `Sports Card Scanner/`
in the vault root (not an Obsidian note — see its own `README.md`), resolved
per [[Sports Card Scanning - Open Decisions]]: desktop drag-and-drop uploader,
local self-hosted backend, Claude Sonnet 5 as the default vision model.

Phase 1 – MVP — **scaffolded and smoke-tested 2026-08-04**
- FastAPI backend (`backend/main.py`): upload endpoint, background extraction,
  result polling, review list/submit
- Single Claude vision call per card (`backend/extraction.py`), forced
  structured tool-use output covering player/team/year/set/card_number/
  serial_number/parallel_insert_type/notable_flags with per-field confidence
- SQLite storage (`backend/db.py`): `cards` + `audit` tables
- Vanilla-JS uploader + review UI (`frontend/index.html`), no build step
- Python 3.12 installed on this machine (via winget), `python-dotenv` wired in
  so `.env` loads automatically, and the full pipeline verified end-to-end
  with a real card and a real API key: uploaded a 1972 Topps Julius Erving
  card, Claude Sonnet 5 correctly read player/team at full confidence, year/
  set at 0.75, and correctly flagged the card number as low-confidence and
  routed it to the needs-review list. See `Sports Card Scanner/README.md`
  "Testing status" for full detail, including a Windows dev-server-cleanup
  gotcha worth knowing about.
- **Next:** run a few more real cards (foil/parallel, visible serial number)
  to stress the known weak points before scanning the collection for real.

Phase 2 – Accuracy Upgrade — in progress
- **Canonicalization — done 2026-08-07.** `backend/canonicalize.py` +
  `players`/`sets` tables in `db.py`. No external reference API (no
  credentials for TCG Price Lookup / TCGAPI.net / PSA API) — implements the
  doc's self-assembled-checklist fallback instead: the table auto-learns
  from confident extractions and from review corrections (with the
  original wrong value kept as an alias), matched via RapidFuzz at a 90+
  score threshold. Wired into both the extraction pipeline
  (`_run_extraction`) and the review-correction endpoint. Schema/API
  extended (`FieldValue.canonical_value/_id/_score`) so it's actually
  visible, not silently dropped by Pydantic; review UI shows a "≈ Name (NN%
  match)" hint. Logic smoke-tested against a temp DB (self-learn, typo
  fuzzy-match, low-confidence non-match, correction-teaches-alias, alias
  resolves on a later scan) — not yet exercised through the real pipeline
  with a live API key. See `Sports Card Scanner/README.md` →
  "Canonicalization & enrichment" for full detail, and
  [[Sports Card Scanning Hub]]'s Operating Guide for the user-facing version.
- On-device crop/deskew (or just accept as-shot photos if accuracy is already
  good enough without it — worth checking before building this) — not started
- Targeted retry/zoom pass for low-confidence fields, especially serial
  number — not started
- Evaluation set (recommendations doc §6) — 50-100 hand-labeled personal card
  photos, run against Claude/GPT-5/Gemini to confirm Claude is still the right
  default once real accuracy data exists — not started

Phase 3 – Production Quality — not started
- Serial-number OCR fallback (PaddleOCR-VL/GLM-OCR) for cases Claude misses
- Pricing/enrichment via TCG Price Lookup
- Batch API usage for bulk re-scans
- Periodic re-run of the evaluation set to catch model/prompt regressions

See [[Hobby Log]] for the dated narrative.
