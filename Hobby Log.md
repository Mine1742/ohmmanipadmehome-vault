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

Extended pricing to use eBay specifically, by request: (1) steered enrich.py's
existing card-detail web-search fallback (card_number/team/parallel_insert_type)
at eBay's current listings specifically instead of generic checklist sites,
since listing titles reliably carry that info; (2) added a genuinely new
on-demand price-estimation feature sourced from eBay's recently *sold*
listings. Two real design questions came up before building the price part,
both resolved before writing code: whether to go through eBay's actual
developer API (Browse API + Marketplace Insights for sold data) or steer
Claude's existing web-search tool at eBay -- went with the latter, since it
needed no new credentials and the sold-data API has historically been
gated/requires approval; and whether a price estimate without any condition
signal would even be meaningful -- it wouldn't (a raw copy vs. a graded PSA 10
of the same card can differ 10-100x), so added a `condition` field to
extraction.py's vision schema first (exact grade off a visible slab label, or
a rough raw/ungraded call) specifically so the price search could be
condition-matched.

Kept the eBay estimate strictly separate from the manual price field --
different columns, never overwrites it -- and deliberately did NOT fold it
into `checklist_entries`'s caching pattern the way card_number/team are
cached: a sold price goes stale in a way a card's printed number never does,
so it's on-demand only (a new "Estimate Price from eBay" button /
`POST /scan/{job_id}/estimate-price`), gated on player/set/year already being
confidently known, and comes back with a caveat string (comp count, condition
caveats) rather than a bare number. Verified the new endpoint's gating and
fail-soft behavior with a real `fastapi.testclient.TestClient` run against the
actual app (400 when key fields aren't confident, 502 without an API key
rather than a crash, 404 on an unknown job, full ScanResult round-trip) --
first time testing went through the real app instance rather than calling
functions directly. The live eBay web-search call itself is still untested
with a real API key, same open item as the rest of `enrich.py`. See
[[Sports Card Scanning - Build Plan]] and `Sports Card Scanner/README.md` for
full detail.

First real usage (owner scanning actual cards) surfaced three issues the
smoke tests above didn't catch, all fixed same day:

1. Server crash confirmed directly from the owner's error log: `CardFields.
   condition` had no default, so any card scanned before `condition` existed
   (no key for it in stored fields_json) broke Pydantic validation entirely --
   500'd `GET /scan/list` and `POST /scan/{job_id}/review` for every
   pre-existing card. Root cause: my smoke tests only ever built fresh field
   dicts that included every field, so they never exercised what loading back
   *real, older* data actually looks like. Fixed by giving every `CardFields`
   attribute a `default_factory=FieldValue` instead of a bare required type --
   a missing key now just shows as unset instead of failing the whole card,
   which also forecloses the same bug for any future field addition.
2. Related, worse compounding bug: `/scan/list` validated every row inline,
   so ONE broken card's error took the entire review list down with it --
   this is almost certainly why the owner reported losing the ability to
   edit/confirm fields at all, not just for one card. Fixed by catching and
   skipping a bad row per-card rather than failing the whole request, and
   made the frontend surface a real error instead of hanging at "Loading…"
   forever on a failed fetch -- that silent-hang behavior is exactly what
   made the first bug invisible instead of obviously broken.
3. The eBay price estimate found fewer comps than the owner got searching
   eBay manually (1-2 comps automated vs. many by hand). Real, structural
   limitation, not a simple bug: Claude's web-search tool does a general web
   search (whatever's crawled/indexed), not a live authenticated eBay
   session with dynamic sold-listings filtering. Narrowed by having the
   research prompt explicitly run several query variations (with/without
   card number, alternate year/name formats) and aggregate across them
   rather than stopping at one search, and by raising the web-search tool's
   max_uses from 3 to 8 -- but said clearly in the docs that this can't be
   fully closed without switching to eBay's actual API, which was already
   flagged as the honest tradeoff when this was built.

Both bugs verified fixed with exact repros (an old-shaped card with no
condition key; a deliberately corrupted row alongside a valid one) before
pushing. See [[Sports Card Scanning - Build Plan]] and
`Sports Card Scanner/README.md`'s "Testing status" for full detail.

Owner got an eBay Developer Program account and asked to actually use it,
following up directly on the "real API vs. web search" tradeoff flagged
when eBay-targeting was first built. Added `backend/ebay_api.py`: OAuth
client-credentials auth (a cached "Application access token," no per-user
eBay login needed since this only searches public listings) + eBay's Browse
API (active listings) + Marketplace Insights API (sold listings) -- entirely
optional, additive, and preferred automatically over the existing
Claude-web-search approach wherever `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET`
are configured. Restructured `enrich.py` so real eBay data and Claude's own
web research both feed the *same* forced-structured-output step -- only
where the raw material comes from changes, not the result shape, which kept
the diff clean and meant the existing test suite mostly just needed
re-running rather than rewriting.

Flagged clearly, both in code comments and in the README, that the two eBay
APIs are not equally available: Browse API (card details) works on any
standard developer account, but Marketplace Insights (sold comps -- the
actual fix for the price-undercounting problem from the previous entry) has
historically needed separate approval and isn't automatic. Built
`search_sold_listings` to treat any unrecognized response shape as
"unavailable" rather than guessing, so if eBay's beta endpoint shape has
shifted since this was written, it fails soft into the web-search fallback
instead of silently returning wrong data.

No real eBay credentials were available in this session to test actual API
responses -- tested what's testable without them: unconfigured state
returns `None` everywhere without raising, the eBay-results-to-summary
formatting function produces correct output for both active/sold shapes
including missing price/condition fields, and a real network+auth attempt
against eBay's OAuth endpoint with deliberately fake credentials still fails
soft to `None` rather than raising (confirmed this actually hit eBay's real
servers, not just a local exception). Re-ran the full existing TestClient
suite to confirm the enrich.py restructuring didn't regress the
already-working paths. Added a "Verify it's working" section to the README
so the owner can confirm for themselves once real credentials are in
`.env` -- the review UI now tags every filled-in field and price estimate
with which source actually produced it (`ebay_api_lookup`/
`ebay_api_sold_comps` vs. the web-search fallback values), so it's directly
visible rather than something to guess at. See
[[Sports Card Scanning - Build Plan]] and `Sports Card Scanner/README.md`'s
"Real eBay API integration" section for full detail.

Owner's eBay app showed as "(Non Compliant)" in the developer console --
turned out to be eBay's Marketplace Account Deletion notification
requirement, unrelated to anything built here. Researched it live rather
than guessing (the app only does public client-credentials searches, never
touches a specific eBay user's account, so the "not persisting eBay data"
exemption toggle was the right fit, not standing up a public HTTPS
notification endpoint). Also walked through where the Cert ID (Client
Secret) actually lives in eBay's console -- a different page than the App
ID, easy to miss -- and flagged clearly that it's not the same thing as the
console's short-lived "OAuth Application Token" (which would silently stop
working after ~2 hours if pasted into `.env` instead).

First real use with real credentials added surfaced an actual gap:
`card_number` stayed stuck unfilled on a card even with player/set/year all
confidently known and credentials configured. Root cause: `web_lookup_log`'s
"attempt once ever" cache was keyed only by player+set+year+field, not by
which lookup source was tried -- a failure from before eBay credentials
existed was permanently blocking a retry with the new, better source.
Fixed by folding whether eBay API is configured into the cache key itself,
verified with a direct repro. Separately, the price estimate was still
using the web-search fallback after credentials were added, and there was
no way to tell why -- every failure path in `ebay_api.py` was completely
silent. Added diagnostic print logging throughout `ebay_api.py` and at the
decision point in `enrich.py`, so a stuck field or a fallback-sourced
estimate is now debuggable from the server terminal (which HTTP status,
which reason) instead of a guess. Re-ran the full TestClient regression
suite -- no regressions. Also documented honestly, in the README, that
there's currently no "retry enrichment" action for an already-scanned card
sitting in the review list -- the cache-key fix helps future lookups, not
retroactively fixing a field already stuck on a card scanned before
credentials existed; a manual correction is the practical fix for those,
and it teaches the checklist table too.
