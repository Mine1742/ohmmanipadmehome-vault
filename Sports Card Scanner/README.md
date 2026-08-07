# Sports Card Scanner

Phase 1 MVP for the project described in [[sports_card_scanning_recommendations]]
and tracked in [[Sports Card Scanning Hub]]. Local, self-hosted, desktop
drag-and-drop uploader — front/back card photos in, a single Claude vision call
extracts structured fields, low-confidence fields get flagged for review.

## Requirements

- Python 3.10+ (uses `X | None` type hints)
- An Anthropic API key with vision access
- Optional: an eBay Developer Program account, for real eBay API data
  instead of Claude's web-search tool steered at eBay — see "Real eBay API
  integration" below. Everything works without this; it's an upgrade.

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
shell yourself. If you have eBay Developer credentials, add
`EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` too (see "Real eBay API integration").

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
  your own growing checklist first, then real eBay API data if configured,
  then a live web search as the last resort. See "Canonicalization &
  enrichment" below.
- `backend/ebay_api.py` — real eBay Buy API integration (Browse API +
  Marketplace Insights), optional. See "Real eBay API integration" below.
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
- Automated pricing enrichment now exists too, but is deliberately separate
  from this canonicalization mechanism and from the manual `price` field —
  it's on-demand, eBay-sourced, and covered in "Price tracking" below.

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
2. **Fallback**, only when the card's *key* fields are solid (canonical
   player, canonical set, and a confident year — all ≥ 0.85): looks up the
   missing field two possible ways, in order —
   - **Real eBay data**, via `ebay_api.py`'s Browse API (active listings),
     if `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` are configured — see "Real
     eBay API integration" below.
   - **Claude web search**, steered at eBay's current/active listings
     (listing titles reliably include card number, team, and
     parallel/insert type; cross-referenced across a few listings rather
     than trusting one seller's title), if the real API isn't configured
     or returned nothing.
   Either way, the raw material (real listing titles, or Claude's own web
   research) feeds the same forced-structured-output step, so the result
   shape is identical regardless of source — only `source` on the field
   (`ebay_api_lookup` vs `web_lookup`) tells you which one actually found
   it. Anything found gets written back into `checklist_entries`, so the
   next card with the same player+set+card_number hits the fast local path
   instead of searching again.
3. **Cost cap.** Each unique (player, set, target-field) combo is only ever
   attempted once via the fallback (`web_lookup_log`) — duplicate/near-
   duplicate cards don't re-trigger paid searches for something already
   known to be missing.
4. **Trust.** A fallback-sourced value (either source) is written with
   confidence held at 0.6 — deliberately below the 0.85 review threshold —
   so it always surfaces once in the "Needs Review" list (labeled "from web
   lookup, unconfirmed" or "from eBay API, unconfirmed") rather than
   silently becoming ground truth. Accept it there and it's written as a
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

Two separate, never-conflated price fields exist on every card:

### Manual price (`price` / `date_priced`)

What *you* say it's worth or paid — `POST /scan/{job_id}/price`,
`{"price": 25.00, "date_priced": "2026-08-10"}` (`date_priced` defaults to
today if omitted). Never touched automatically. Editable from the UI right
under a scan's result and under each flagged card in "Needs Review".

### eBay-estimated price (`estimated_price` / `estimated_price_date` / `estimated_price_source` / `estimated_price_caveat`)

An on-demand estimate from recently **sold** eBay listings (not active
ones), via `POST /scan/{job_id}/estimate-price` — click "Estimate Price
from eBay" in the UI. Requires `player`/`set`/`year` to already be
confidently known (canonicalized/confirmed) — the endpoint returns 400 if
not, since a price search on an unidentified card would be meaningless.

- **Condition-aware.** Uses the vision-extracted `condition` field (see
  below) so the search targets comps in a comparable condition — a raw/
  played copy and a PSA 10 of the *same card* can differ 10–100x in sold
  price, so an estimate without this would be closer to noise than signal.
- **On-demand only, not automatic per scan, and not cached forever** the
  way `checklist_entries` caches card_number/team (a sold price goes stale;
  a fixed fact like card_number doesn't). Cost is bounded by how often you
  actually click the button, not by scan volume.
- Comes back with a `caveat` string (e.g. "only 2 comps found (~2 comps)",
  "condition assumed since not specified") — read it, this is an estimate
  from a handful of comps, not an appraisal.
- **Two possible sources**, recorded in `estimated_price_source`: real sold
  comps via `ebay_api.py`'s Marketplace Insights API
  (`ebay_api_sold_comps`) if configured and enabled for your eBay
  application, else Claude's web_search tool steered at eBay's sold/
  completed listings (`ebay_websearch_sold_comps`). The UI shows which one
  actually produced a given estimate. See "Real eBay API integration"
  below for setup and for why Marketplace Insights specifically isn't
  automatic on every account.
- Fails soft, same as `enrich.py`'s other web lookups: no API key, a bad
  web-search tool version, no usable sold comps found, or a network error
  all just return a "couldn't estimate" response (502) rather than
  breaking anything else on the card.
- **Known limitation of the web-search fallback specifically, confirmed
  against real usage 2026-08-07: it generally finds fewer comps than
  manually searching eBay yourself.** Claude's web-search tool does a
  general web search — it finds whatever's been crawled/indexed — not a
  live, authenticated browse of eBay's dynamically-rendered, session-
  filtered sold-listings search the way you get by visiting eBay directly.
  The research prompt runs several query variations (with/without card
  number, alternate year/name formats, with/without team) and aggregates
  across them, which narrows the gap — but the real eBay API path above is
  the actual fix for this, not further prompt tuning. If you don't have
  Marketplace Insights access and accuracy matters more than the estimate
  being free/automatic, cross-check against your own manual eBay search.

### Condition (new field on every scan)

`extraction.py` now also asks the vision model for `condition`: an exact
grade read off a visible slab label (e.g. `"PSA 9"`, high confidence, since
that's precisely legible) or a rough visual call for a raw/ungraded card
(`"Raw - Near Mint"` / `"Raw - Excellent"` / `"Raw - Good"` / `"Raw - Poor"`,
kept at moderate confidence since visual condition assessment from a photo
alone is inherently imprecise). This exists specifically to make the eBay
price estimate above condition-aware — it's not canonicalized or
checklist-cached (excluded for the same reason as `serial_number`:
condition is a fact about your specific physical copy, not a checklist
fact true for every copy of that card).

**No browsable "all cards" view yet.** Both price forms only appear next to
a card right after you scan it, or if that card is currently flagged in
"Needs Review". A card that scanned clean (no fields under threshold) has no
other UI entry point to add/edit its price later — set it right after
scanning, or query/update `cards.db` directly (see "Where your data lives"
in [[Sports Card Scanning Hub]]) until a general browse/edit view exists.

## Real eBay API integration (`ebay_api.py`)

Optional upgrade over the Claude-web-search-steered-at-eBay approach above,
for accounts with an eBay Developer Program account. Real API data is
preferred automatically wherever it's configured — nothing else changes
about how you use the app.

### Setup

1. Get your app's keys from [developer.ebay.com](https://developer.ebay.com/)
   — you need the **Client ID (App ID)** and **Client Secret (Cert ID)**
   from your application's keyset. Use your **production** keyset, not
   sandbox — sandbox only returns eBay's fake test data, not real listings.
2. Add to `Sports Card Scanner/.env` (same file as `ANTHROPIC_API_KEY`, see
   `.env.example`):
   ```
   EBAY_CLIENT_ID=your-app-id
   EBAY_CLIENT_SECRET=your-cert-id
   ```
3. Restart the server. That's it — no code changes needed. `ebay_api.configured()`
   detects the env vars automatically; `enrich.py` prefers real API data
   wherever it's available and falls back to Claude web search otherwise.

### The two APIs behave differently — read this before assuming everything works

- **Browse API** (active listings, used for card-detail lookups —
  card_number/team/parallel_insert_type): generally available to any
  registered application, no extra approval needed. This part should just
  work once your credentials are in `.env`.
- **Marketplace Insights API** (SOLD listings, used for price estimation):
  **historically requires separate approval in eBay's developer program —
  not automatically enabled on every account.** Check your application's
  details on developer.ebay.com to confirm whether Marketplace Insights
  shows as an available/enabled API. If it's not enabled for your app,
  `ebay_api.search_sold_listings` will simply return `None` every time
  (auth succeeds, the call itself fails or comes back empty) and price
  estimation transparently falls back to the Claude web-search path —
  nothing breaks, you just don't get the accuracy upgrade for prices
  specifically. Card-detail lookups via Browse API are unaffected either
  way.

### Auth model

OAuth 2.0 client-credentials grant (an "Application access token") — no
per-eBay-account login or user consent flow, since this only ever searches
public listing data, never touches a specific eBay account or seller
inventory. Tokens are fetched and cached in memory (`ebay_api._token_cache`),
refreshed automatically before they expire.

### Verify it's working

Once configured, scan a card and check the `source` field on any filled-in
`card_number`/`team`/`parallel_insert_type` in the JSON response, or the
`[from eBay API, unconfirmed]` tag in the review UI — that confirms the
Browse API path is being used instead of web search. For price, click
"Estimate Price from eBay" and check whether the tag reads "via eBay API,
real sold comps" or "via web search, may undercount" — that tells you
directly whether Marketplace Insights is actually working for your account.

**Check the server terminal too.** `ebay_api.py` logs every failure with a
reason (`[ebay_api] GET ... returned 403: ...`, an OAuth token failure, an
unrecognized response shape) rather than failing completely silently, and
`enrich.py` logs how many real listings each lookup actually found
(`[enrich] Browse API for '...': N listings`). If a field or estimate keeps
falling back to web search, this is where to look first — it tells you
*why* (not enabled for your app, wrong credentials, genuinely zero results,
etc.) instead of leaving you guessing.

**Important caching gotcha if you're adding eBay credentials to an app
that's already been scanning cards:** card-detail lookups (not price
estimates — those aren't cached) that already failed once under the
web-search-only fallback are cached as "don't retry" per player+set+
year+field. This cache is now keyed to include whether eBay API is
configured, so *future* lookups for a player+set+year+field combo that
previously failed will get a fresh attempt with the better source instead
of being blocked forever by the old failure. There's currently no "retry
enrichment" action for a card already sitting in the review list, though —
enrichment only runs (a) at scan time, or (b) implicitly, the first time a
given player+set+year+field combo is looked up under a given source tier.
So a field that's *already* stuck unfilled on a card you scanned before
adding credentials won't retroactively fill itself in on that same card;
the practical fix for one already-stuck card is to type the correct value
in yourself (a human correction) — which also teaches the checklist table,
so the *next* card with that same player+set+card_number resolves
instantly from the local cache either way.

### Caveat

`MARKETPLACE_INSIGHTS_URL` in `ebay_api.py` (a `v1_beta` endpoint) and the
response shape `search_sold_listings` expects reflect what was documented
at build time — eBay's Beta APIs are more likely to change shape than
stable ones. If it stops working, `search_sold_listings` is written to
treat an unrecognized response as "unavailable" (returns `None`, falls back
to web search) rather than guessing at a different shape, so a shape change
degrades gracefully instead of returning wrong data — but it's still worth
checking eBay's current API docs if this seems to have stopped working
after previously working.

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

**eBay-targeting + `condition` field + price estimation smoke-tested
2026-08-07** via a real `fastapi.testclient.TestClient` run against the
actual app (not just calling functions directly): confirmed `condition` is
now a field the vision tool schema requests, confirmed
`POST /scan/{job_id}/estimate-price` correctly 400s when player/set/year
aren't confidently known (no wasted lookup attempted), correctly 502s
rather than crashing when `ANTHROPIC_API_KEY` isn't set, correctly 404s on
an unknown job, and confirmed a full `ScanResult` round-trip includes all
four new estimated-price fields. **Still not tested: an actual eBay
sold-listings search with a live API key** — same open item as the rest of
the web-lookup path.

**Two real bugs found and fixed via actual usage, 2026-08-07 (post-deploy).**
Real usage caught what pre-deploy smoke tests missed:

- `CardFields.condition` was a required field with no default. Every card
  scanned *before* `condition` existed had no key for it in its stored
  `fields_json`, so Pydantic rejected the card outright the moment this was
  deployed — broke `GET /scan/list` and `POST /scan/{job_id}/review` (500)
  for every pre-existing card, confirmed directly from the running
  server's error log. Fixed by giving every `CardFields` attribute a
  `default_factory=FieldValue` instead of a bare required type, so a
  missing key just shows that field as unset rather than failing to load
  the whole card — also closes off the same bug for any future field
  addition, not just this one. Verified against an exact repro of the
  broken card.
- `GET /scan/list` validated every returned row through `CardFields`
  inline — a single malformed/legacy row would take the *entire* list
  down with it, silently hiding the review/edit UI for every other card
  too (this is very likely what caused the `condition` bug above to look
  like "the whole review list vanished" rather than "one old card is
  broken"). Fixed by catching per-row and skipping/logging a bad row
  instead of failing the whole request. The frontend's `loadReviewList()`
  also no longer hangs at "Loading…" forever on a failed fetch — it now
  shows the actual error. Verified with a deliberately corrupted row
  alongside a valid one: the valid card now still loads.

**Real eBay API integration (`ebay_api.py`) smoke-tested 2026-08-07**, unit
level only — no real `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` available in this
session to test against real eBay data: confirmed every function returns
`None` cleanly (never raises) when unconfigured; confirmed `_format_ebay_api_results`
produces the expected summary text from both active and sold-listing shaped
data, including missing-price/missing-condition items; confirmed that with
fake credentials configured, a real network/auth attempt against eBay's
OAuth endpoint still fails soft to `None` rather than raising, whether that
failure is a connection error or an auth rejection. Re-ran the full existing
TestClient suite (old-shaped cards, estimate-price gating, full ScanResult
round-trip) to confirm the internal enrich.py restructuring didn't regress
anything. **Not yet tested: actual eBay API calls with real credentials** —
that's on you to verify once your keys are in `.env`; see "Real eBay API
integration" → "Verify it's working" for how to confirm the `source` tags
show `ebay_api_lookup`/`ebay_api_sold_comps` instead of the web-search
fallback values.

**Real eBay credentials added and used for the first time, 2026-08-07** —
surfaced a real gap: `card_number` stayed unfilled on a card despite
player/set/year all being confidently known and eBay credentials now being
configured. Root cause: `web_lookup_log`'s "attempt once ever" cache was
keyed only by player+set+year+field, not by which lookup *source* was
tried — a failed attempt from before eBay credentials existed permanently
blocked a retry with the new, better source. Fixed by including whether
eBay API is configured in the cache key, verified with a direct repro
(logging a failed web-search-tier attempt, then confirming the eBay-tier
key is untouched/retryable). Also added diagnostic logging throughout
`ebay_api.py` and `enrich.py` (previously every failure was completely
silent) so a stuck field or an estimate still falling back to web search
is debuggable from the server terminal instead of a guess — see "Real eBay
API integration" → "Verify it's working". Re-ran the full TestClient
regression suite; no regressions.

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
