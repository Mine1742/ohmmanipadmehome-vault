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
up in the "Needs Review" list below for inline correction. A price + date
field is shown under every scan result for you to fill in manually (see
"Price tracking" below) — it's not extracted or looked up automatically.

## What's here

- `backend/main.py` — FastAPI app: upload, poll result, review list/submit
- `backend/extraction.py` — single Claude vision call per card, forced
  structured tool-use output (see `RECORD_CARD_FIELDS_TOOL`)
- `backend/canonicalize.py` — Phase 2 canonicalization
  ([[sports_card_scanning_recommendations]] §2): fuzzy-matches extracted
  `player`/`set` values against a local reference table using RapidFuzz. See
  "Canonicalization & enrichment" below for how it works.
- `backend/enrich.py` — fill-in-missing-fields on top of canonicalization:
  looks up low-confidence `card_number`/`team`/`parallel_insert_type` from
  your own growing checklist first, a live web search second. See
  "Canonicalization & enrichment" below.
- `backend/db.py` — SQLite (`data/cards.db`), `cards` + `audit` +
  `players` + `sets` + `checklist_entries` + `web_lookup_log` tables
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
- **Automated** pricing enrichment (the doc's Phase 3 item — a live lookup
  against TCG Price Lookup or similar) is **not** included here — a *manual*
  price field exists instead, see "Price tracking" below.

### Fill-in-missing-fields (`enrich.py`)

Canonicalization above only normalizes *spelling* — it can't tell you a
card's number, team, or parallel/insert type if the vision model couldn't
read them. `enrich.py` does that, built for a collection too large to ever
pre-populate a lookup table for (this was explicitly designed around "millions
of cards, plus non-sports cards and memorabilia" — see [[Hobby Log]]
2026-08-07): a **cache-aside** pattern, not a bulk import.

1. **Local first.** Checks `checklist_entries` — the real source of truth,
   built entirely from your own scans and review corrections, keyed on
   canonical player + canonical set + card_number.
2. **Web fallback**, only when the card's *key* fields are solid (canonical
   player, canonical set, and a confident year — all ≥ 0.85): a second Claude
   API call, reusing your existing `ANTHROPIC_API_KEY`, using Anthropic's
   server-side web-search tool to check card-database sites (tcdb.com,
   Beckett checklists, etc.) for the missing field. Anything found gets
   written back into `checklist_entries`, so the next card with the same
   player+set+card_number hits the fast local path instead of searching
   again.
3. **Cost cap.** Each unique (player, set, target-field) combo is only ever
   attempted once via the web (`web_lookup_log`) — duplicate/near-duplicate
   cards don't re-trigger paid searches for something already known to be
   missing.
4. **Trust.** A web-sourced value is written with confidence held at 0.6 —
   deliberately below the 0.85 review threshold — so it always surfaces once
   in the "Needs Review" list (labeled "from web lookup, unconfirmed") rather
   than silently becoming ground truth. Accept it there and it's written as a
   *verified* `checklist_entries` row, trusted immediately after that. A
   value pulled from your own already-verified checklist is labeled "from
   your checklist" instead.
5. **What's excluded on purpose:** `serial_number`. A print run size
   ("numbered to 150") is a checklist fact; which specific numbered copy you
   physically hold ("45/150") is unique to that card and isn't something any
   lookup can know — that field stays vision/human-only.
6. **Verify the web-search tool version before relying on this.** The exact
   Anthropic web-search tool type string (`WEB_SEARCH_TOOL_TYPE` in
   `enrich.py`, overridable via the `CARD_WEB_SEARCH_TOOL_TYPE` env var)
   reflects what was known at build time — check current API docs if it
   starts failing. Enrichment fails soft either way (a bad tool type, no API
   key, a network error, anything) — it just skips filling that field in
   rather than breaking the scan.

## Price tracking

A `price` (number) and `date_priced` (date) field exist on every card,
editable from the UI right under a scan's result and under each flagged
card in "Needs Review" — `POST /scan/{job_id}/price`, `{"price": 25.00,
"date_priced": "2026-08-10"}` (`date_priced` defaults to today if omitted).

**Deliberately manual, not auto-populated.** Unlike `card_number`/`team`/
etc., a price isn't printed on the card for the vision model to read, and
unlike those fields it isn't a fixed fact — it changes over time and depends
heavily on condition/grade, which isn't currently tracked at all (a PSA 10
vs. a raw/played copy of the same card can differ 10–100x in value). An
auto-lookup version would need its own design (staleness/refresh handling,
a condition/grade field, another paid web-search call per card) — this is
intentionally just the simple version: you look the price up yourself and
log it.

**No browsable "all cards" view yet.** The price form only appears next to
a card right after you scan it, or if that card is currently flagged in
"Needs Review". A card that scanned clean (no fields under threshold) has no
other UI entry point to add/edit its price later — set it right after
scanning, or query/update `cards.db` directly (see "Where your data lives"
in [[Sports Card Scanning Hub]]) until a general browse/edit view exists.

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

**Fill-in-missing-fields (`enrich.py`) smoke-tested 2026-08-07**, local path
only (no `ANTHROPIC_API_KEY` set in the test environment, so the web-lookup
path could only be verified to fail soft, not verified to actually find
anything real): confirmed enrichment doesn't crash without an API key, a
failed web-lookup attempt gets logged so an identical second scan doesn't
retry it, a human correction writes a *verified* `checklist_entries` row,
and a second scan of the same player+set+year then fills the missing
`card_number` from that local row instead of touching the web at all — and
confirmed a fix where sibling "N/A" placeholder values were almost getting
written into the checklist table as if they were confirmed data (fixed
before commit). **The actual web-search call path (Claude's server-side
web-search tool doing a real lookup) has not been tested with a live API
key** — that's the next real thing to verify, including whether
`WEB_SEARCH_TOOL_TYPE` is still the correct tool version.

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
