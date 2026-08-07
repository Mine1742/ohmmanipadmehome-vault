#personal

[[Personal Hub]]

Dated log of hobby/personal-project progress, tagged by hobby — covers [[HAM Radio
Technician]], [[Sports Card Scanning Hub]], and
anything else. Append-only.

## 2026-08-04 — Sports Card Scanning
Revised [[sports_card_scanning_recommendations]] to reflect current tech: pivoted from
the original custom YOLOv8 + OCR-ensemble architecture to a vision-LLM-first design
(Claude/GPT-5/Gemini structured extraction directly from card photos), based on fresh
research into current model accuracy, commercial competitors (CollX, Ludex, PSA, Card
Ladder), API pricing, and card-database enrichment options. Created
[[Sports Card Scanning Hub]] as the project's MOC (linked from [[Personal Hub]]), plus
[[Sports Card Scanning - Open Decisions]] capturing undecided architecture questions
(capture-app platform, vision-LLM provider, hosting, backend framework) that need
resolving before scaffolding starts.

Resolved the open decisions (desktop uploader, local self-hosted, Claude Sonnet 5
default) and scaffolded the Phase 1 MVP at `Sports Card Scanner/` — FastAPI backend,
SQLite storage, single Claude vision call with structured tool-use output, vanilla-JS
uploader/review UI. Installed Python 3.12 on this machine (via winget) and
smoke-tested the full request path: server boots, upload/result/list endpoints
respond correctly, background extraction runs and fails cleanly without an API key.
Real Claude extraction on an actual card photo is still untested — needs
`ANTHROPIC_API_KEY` set. See [[Sports Card Scanning - Build Plan]].

Added the API key (user's own action — key handling stayed on their side throughout)
and ran the pipeline end-to-end against a real card photo: a 1972-era Topps Julius
Erving (Virginia Squires) card. Claude Sonnet 5 correctly read player and team at
full confidence, year/set at 0.75, and correctly flagged the card number as
low-confidence — routed to the needs-review list exactly as designed. First real
proof the vision-LLM-first architecture works, not just that the plumbing works.
Only tested on one card so far; more real-card testing (foil/parallel, visible
serial number) is the natural next step before scanning the collection for real.

## 2026-08-07 — Sports Card Scanning
Implemented the "Canonicalization & Enrichment" piece of Phase 2 from
[[sports_card_scanning_recommendations]] §2. No external card-database API
(TCG Price Lookup, TCGAPI.net, PSA API) had credentials available, so built the
doc's explicit fallback instead: a self-assembled `players`/`sets` reference
table in `cards.db` that grows on its own — a confident extraction with no
existing match becomes a new canonical entry, and correcting a flagged field in
the review UI teaches the table the right spelling while keeping the original
wrong value as an alias for future matches. RapidFuzz (`fuzz.WRatio`, 90+ score
threshold) does the matching. Added `backend/canonicalize.py`, extended
`db.py`/`schemas.py` accordingly, wired it into both the extraction pipeline and
the review-correction endpoint in `main.py`, and added a "≈ Name (NN% match)"
hint to the review UI. Verified the logic with a standalone smoke test against a
temp SQLite DB (self-learning, typo fuzzy-matching, correctly *not*
canonicalizing a low-confidence value, correction-teaches-alias, and a later
scan resolving that alias back to the canonical name) — no Anthropic API key
needed for that part since it doesn't touch the vision model. Not yet exercised
through the real upload pipeline with a live key; that's the natural next check
before trusting it against the actual collection. See
[[Sports Card Scanning - Build Plan]] and `Sports Card Scanner/README.md` for
full detail.
