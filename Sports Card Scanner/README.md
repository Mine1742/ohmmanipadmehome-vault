# Sports Card Scanner

Phase 1 MVP for the project described in [[sports_card_scanning_recommendations]]
and tracked in [[Sports Card Scanning Hub]]. Local, self-hosted, desktop
drag-and-drop uploader — front/back card photos in, a single Claude vision call
extracts structured fields, low-confidence fields get flagged for review.

## Requirements

- Python 3.10+ (uses `X | None` type hints)
- An Anthropic API key with vision access

## Setup

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate  # or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env` in the `Sports Card Scanner/` root (same folder
as this README) and fill in `ANTHROPIC_API_KEY` with your real key. `main.py`
loads it automatically via `python-dotenv` — no need to export it into your
shell yourself.

## Run

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000 — drag-and-drop a front (and optionally back) card
photo, it uploads, scans via Claude, and any field under 0.85 confidence shows
up in the "Needs Review" list below for inline correction.

## What's here

- `backend/main.py` — FastAPI app: upload, poll result, review list/submit
- `backend/extraction.py` — single Claude vision call per card, forced
  structured tool-use output (see `RECORD_CARD_FIELDS_TOOL`)
- `backend/canonicalize.py` — Phase 2 canonicalization & enrichment
  ([[sports_card_scanning_recommendations]] §2): fuzzy-matches extracted
  `player`/`set` values against a local reference table using RapidFuzz. See
  "Canonicalization & enrichment" below for how it works.
- `backend/db.py` — SQLite (`data/cards.db`), `cards` + `audit` +
  `players` + `sets` tables
- `frontend/index.html` — vanilla-JS uploader + review UI, no build step

## Canonicalization & enrichment

Implements [[sports_card_scanning_recommendations]] §2's "Canonicalization &
Enrichment" section, scoped to what's realistic without paid third-party
access:

- **No external reference API is wired in.** The doc lists TCG Price Lookup,
  TCGAPI.net, and the PSA API as possible sources, but none had credentials
  available at build time — and the doc itself flags that sports-card
  coverage from any of them is uncertain anyway. What's implemented instead
  is the doc's explicit fallback: **a self-assembled checklist**, kept as
  `players` and `sets` tables in `cards.db`.
- **The tables grow themselves, in two ways:**
  1. Any `player`/`set` value the vision model extracted with confidence
     ≥ 0.85 and that didn't already fuzzy-match something known gets added
     as a new canonical entry automatically — no manual data entry needed
     as you scan real cards.
  2. Submitting a review correction (in the "Needs Review" UI) teaches the
     table too: the corrected value becomes/updates the canonical entry, and
     the original (wrong) extracted value is recorded as a known alias, so
     future misreads of the same kind resolve to the same canonical value.
- **Matching** uses RapidFuzz (`fuzz.WRatio`) against canonical names +
  aliases; a match ≥ 90 is trusted and attached to the field as
  `canonical_value` / `canonical_id` / `canonical_score` (visible in the API
  response and, for flagged cards, as a "≈ Name (NN% match)" hint in the
  review UI). The model's own `confidence` is never overwritten by a
  canonical match — the two are reported side by side.
- **If a real external source becomes available later**, seed `players`/
  `sets` from it via `db.upsert_player` / `db.upsert_set` instead of (or in
  addition to) the auto-learning above — the matching logic in
  `canonicalize.py` doesn't need to change.
- Team canonicalization and pricing enrichment (the doc's Phase 3 item) are
  **not** included here — team wasn't in the doc's §4 data model, and
  pricing is explicitly scoped to Phase 3, not this pass.

## Known simplifications vs. the full recommendations doc

These are deliberate cuts, not oversights — see
[[sports_card_scanning_recommendations]] §9 for the full phase breakdown:

- No on-device crop/deskew yet (§2) — upload the photo as-is.
- No serial-number retry/zoom fallback yet (§2) — a low-confidence serial
  number just gets flagged for manual review like any other field.
- Single model only (Claude Sonnet 5, `CARD_SCAN_MODEL` env var to override) —
  no evaluation harness yet comparing it against GPT-5/Gemini.
- Only JPEG/PNG are handled explicitly (`extraction.py:_image_block` guesses by
  file extension). iPhone photos default to HEIC, which the Claude API doesn't
  accept — convert to JPEG before uploading until this is handled properly.

## Testing status

Full pipeline verified end-to-end 2026-08-04 with a real card photo and a real
API key: uploaded a 1972-era Topps Julius Erving (Virginia Squires) card photo
through `/scan/upload`, Claude Sonnet 5 correctly extracted player and team
at full confidence, year/set at 0.75, and correctly flagged `card_number` as
low-confidence (0.3, returned `N/A`) — `needs_review` triggered as designed,
and the card showed up correctly via `/scan/list?needs_review=true`.

Only tested against one card so far — treat this as "the pipeline works," not
"accuracy is proven." Worth running a handful more (including a foil/parallel
and a card with a visible serial number) before trusting it at volume. Test
job/image data was deleted after each test run, not left in `data/`.

**Canonicalization (`canonicalize.py`) smoke-tested 2026-08-07** against a
temporary SQLite DB (no Anthropic API key needed for this part, since it
doesn't call the vision model): confirmed a first confident extraction
self-learns as a new canonical player/set, a typo'd re-scan of the same
player fuzzy-matches instead of creating a duplicate, a low-confidence
unmatched value is correctly left uncanonicalized rather than guessed at,
and a review correction both creates the canonical entry and records the
original wrong value as an alias that a later scan resolves through. Not yet
exercised through the real upload pipeline with a live API key — do that
before trusting it against the actual collection.

**Windows gotcha hit during testing:** `kill $!` from a background-launched
git-bash job doesn't map to the real Windows PID for a spawned `uvicorn`
process — the job appeared killed but the server kept running and answering
on the same port. To actually stop a locally-run dev server, find the real
owning process and stop that:
```powershell
$owner = (Get-NetTCPConnection -LocalPort 8123).OwningProcess
Stop-Process -Id $owner -Force
```

## Data

`data/images/` and `data/cards.db` are gitignored — this is your personal
card-photo collection, not something to commit.
