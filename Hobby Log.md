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
