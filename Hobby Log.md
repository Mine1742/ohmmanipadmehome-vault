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

Clarified an important scope point about that canonicalization work: it normalizes
*spelling* of already-extracted player/set values, it does not fill in fields the
vision model couldn't read at all. The owner's actual collection is millions of
cards plus non-sports cards and memorabilia — far too large for any static or
pre-populated lookup table, ruling out the "generate a complete sports card
lookup table" framing initially assumed. Landed on a cache-aside design instead:
for a low-confidence `card_number`/`team`/`parallel_insert_type`, check a local
`checklist_entries` table first, fall back to a live web search only if nothing
local exists and the key fields (canonical player/set, confident year) are
solid, and write anything found back into the local table so the same gap is
never searched twice.

Implemented as `backend/enrich.py` + `checklist_entries`/`web_lookup_log`
tables. The web fallback reuses the existing `ANTHROPIC_API_KEY` via a second
Claude API call using Anthropic's server-side web-search tool (searches
card-database sites like tcdb.com/Beckett rather than a maintained scraper) —
no new credential needed. Web-sourced values are written below the review
threshold on purpose so they always get a quick human glance before being
trusted; accepting one in review promotes it to a verified checklist row.
Wired into both the extraction pipeline and the review-correction endpoint,
alongside a `source` tag (`local_lookup`/`web_lookup`/`human_review`) surfaced
in the review UI so it's always clear where a value came from. Deliberately
excluded `serial_number` — a print-run size is a checklist fact, but which
specific numbered copy is physically in hand isn't something any lookup can
know.

Smoke-tested the local half of the pipeline against a temp DB: fails soft with
no API key, a failed web-lookup attempt gets logged so an identical scan
doesn't retry it, a human correction writes a verified checklist row, and a
second scan of the same player+set+year fills the missing field from that
local row. Caught and fixed a real bug during testing — sibling "N/A"
placeholder values were almost getting written into the checklist table as if
they were confirmed data. The live web-search call itself hasn't been
exercised with a real API key yet; that's the next concrete thing to verify,
including whether the web-search tool version string in `enrich.py` is still
current. See [[Sports Card Scanning - Build Plan]] and
`Sports Card Scanner/README.md` for full detail.

Added a manual `price` + `date_priced` field per card, by request — deliberately
not auto-looked-up: unlike card_number/team, price changes over time and is
heavily condition/grade-dependent (which isn't tracked at all yet), so an
accurate auto-lookup would need its own design pass rather than reusing
`enrich.py`'s pattern as-is. `cards.db` already had real data on the owner's
machine by this point, so used an idempotent `ALTER TABLE` migration in
`db.init_db()` rather than assuming a fresh table — verified against a
simulated pre-migration DB that the existing row survives and repeated
restarts don't error. Added a price+date form to the UI, shown right after any
scan completes and next to each flagged review card. Known gap, called out in
the docs rather than left implicit: there's no general "browse all cards" view
yet, so a card that scans clean (nothing flagged) only gets one chance at
having its price set, right after that scan.
