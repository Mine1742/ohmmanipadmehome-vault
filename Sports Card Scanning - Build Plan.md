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
- **Fill-in-missing-fields enrichment — done 2026-08-07.** `backend/enrich.py`
  + `checklist_entries`/`web_lookup_log` tables. Explicit follow-up after
  realizing the collection is genuinely large-scale (millions of cards, plus
  non-sports cards/memorabilia) — no static/pre-populated lookup table could
  cover that, so this is a cache-aside design instead: for a low-confidence
  `card_number`/`team`/`parallel_insert_type` (not `serial_number` — that's
  unique per physical card, not a checklist fact), check the local
  `checklist_entries` table first, fall back to a live web search (a second
  Claude API call using the existing `ANTHROPIC_API_KEY` and Anthropic's
  server-side web-search tool) if nothing local exists and the key fields
  (canonical player/set, confident year) are solid. A found web value writes
  back into `checklist_entries` so the next matching card hits the local
  path; each unique (player, set, target-field) combo is only ever attempted
  once via the web (`web_lookup_log` gates repeats, capping cost at
  collection scale). Web-sourced values are written below the review
  threshold on purpose (unconfirmed) — accepting one in review promotes it
  to a *verified* checklist row. Local-path logic smoke-tested against a temp
  DB (fail-soft with no API key, attempt-gating, correction-teaches-
  verified-row, second scan resolves from the local table — plus a real bug
  caught and fixed in testing, where sibling "N/A" placeholder values were
  almost written into the checklist table as if confirmed). **The actual
  live web-search call path has not been tested with a real API key** — next
  concrete step before trusting this at volume. Full detail:
  `Sports Card Scanner/README.md` → "Fill-in-missing-fields (`enrich.py`)".
- On-device crop/deskew (or just accept as-shot photos if accuracy is already
  good enough without it — worth checking before building this) — not started
- Targeted retry/zoom pass for low-confidence fields, especially serial
  number — not started
- Evaluation set (recommendations doc §6) — 50-100 hand-labeled personal card
  photos, run against Claude/GPT-5/Gemini to confirm Claude is still the right
  default once real accuracy data exists — not started

Phase 3 – Production Quality — not started
- Serial-number OCR fallback (PaddleOCR-VL/GLM-OCR) for cases Claude misses
- Pricing/enrichment via a dedicated card-data API (TCG Price Lookup etc.) —
  superseded in practice by the eBay-targeted approach below, though a real
  official API could still replace it for more structured/reliable data
- Batch API usage for bulk re-scans
- Periodic re-run of the evaluation set to catch model/prompt regressions

Outside the original doc's phases (added by direct request)
- **Manual price tracking — done 2026-08-07.** `cards.price` +
  `cards.date_priced` columns (with an idempotent `ALTER TABLE` migration in
  `db.init_db()` so an already-existing `cards.db` picks up the columns
  without data loss — verified against a simulated pre-migration DB), a
  `POST /scan/{job_id}/price` endpoint, and a price+date form in the UI under
  every scan result and every flagged review card. Deliberately manual, not
  looked up — price isn't printed on a card for vision to read, isn't a
  fixed fact like card_number (it changes over time), and is heavily
  condition/grade-dependent, which isn't tracked yet.
- **Condition field — done 2026-08-07.** Added `condition` to
  `extraction.py`'s vision schema: exact grade off a visible slab label
  (high confidence) or a rough raw/ungraded call (moderate confidence,
  since visual assessment from a photo is inherently imprecise). Not
  canonicalized/checklist-cached — same reasoning as `serial_number`,
  condition is a fact about the specific physical copy, not a checklist
  fact true for every copy of that card.
- **eBay-targeted enrichment + on-demand eBay price estimation — done
  2026-08-07.** By direct request: option to steer the existing
  `enrich.py` web-search fallback (card_number/team/parallel_insert_type)
  at eBay's *current* listings specifically, rather than generic
  checklist/database sites, and add a genuinely new capability -- an
  `estimated_price`/`estimated_price_date`/`estimated_price_source`/
  `estimated_price_caveat` set of fields, condition-aware (uses the new
  `condition` field), sourced from eBay's recently-*sold* listings via a
  second Claude API call (same two-call research-then-structure pattern as
  the rest of `enrich.py`). Deliberately **not** an official eBay API
  integration (Browse API / Marketplace Insights) -- that would need the
  owner to register for eBay developer credentials and possibly gated
  sold-data API access; this reuses the existing `ANTHROPIC_API_KEY` and
  Claude's web-search tool instead, at the cost of relying on general web
  search actually surfacing decent eBay results rather than a structured
  API response. Deliberately kept **separate from and never overwriting**
  the manual price field, and deliberately **not** run automatically per
  scan or cached the way `checklist_entries` caches card_number/team --
  price goes stale, so it's on-demand only
  (`POST /scan/{job_id}/estimate-price`), gated on player/set/year already
  being confidently known. New endpoint + the full pipeline verified with a
  real `fastapi.testclient.TestClient` run (400/502/404 gating all correct,
  full `ScanResult` round-trip).
- **Real-usage fixes — done 2026-08-07.** First live use surfaced three
  real issues beyond what pre-deploy smoke tests caught:
  1. `CardFields.condition` had no default, so every card scanned before
     `condition` existed broke on load (500 on `/scan/list` and
     `/scan/{job_id}/review`) -- fixed with `default_factory=FieldValue`
     on every `CardFields` attribute.
  2. `/scan/list` validated rows inline, so that one broken card's error
     took the *entire* review list down with it, hiding the edit/confirm
     UI for every card -- fixed by catching and skipping a bad row
     per-card instead of failing the whole request; the frontend also no
     longer hangs at "Loading…" forever on a failed fetch.
  3. The eBay price estimate found meaningfully fewer comps than manually
     searching eBay -- a real, structural limitation of steering a
     general web-search tool at eBay rather than eBay's own live sold-
     listings search, not something prompt tuning alone fully closes.
     Narrowed (not eliminated) by having the research prompt run several
     query variations (with/without card number, alternate year/name
     formats) and aggregate across them, and by raising the web-search
     tool's `max_uses` from 3 to 8.
  Full detail on all three: `Sports Card Scanner/README.md` → "Testing
  status".

See [[Hobby Log]] for the dated narrative.
