#personal

[[Personal Hub]]

Personal hobby project: a mobile-to-backend pipeline that photographs sports cards and extracts structured data (player, team, year, set, card number, serial number) into a database. Tracks the project through research, architecture, scaffold, build, test, and finalize.

## Operating Guide

_Living document — update this section whenever how the program is run, accessed, or reviewed changes. Current as of 2026-08-04, Phase 1 MVP. Full dev-oriented setup/troubleshooting detail lives in `Sports Card Scanner/README.md`; this is the "how do I actually use it" version._

**Starting the server**
1. Open a terminal, `cd` into `Sports Card Scanner/backend`
2. First time only: `python -m venv .venv` then `.venv\Scripts\activate` then `pip install -r requirements.txt`
3. Every time: `.venv\Scripts\activate` then `uvicorn main:app --reload --port 8000`
4. Leave that terminal window open — the server runs as long as it's running. Closing the terminal (or Ctrl+C) stops it.

**Using it to scan a card**
1. With the server running, open http://localhost:8000 in a browser
2. Drag/drop (or click to select) a front photo — required — and a back photo — optional but recommended if the serial number is on the back
3. Click "Upload & Scan" — it uploads, then polls automatically until Claude finishes reading the card (a few seconds)
4. Extracted fields show up as JSON on the page

**Reviewing flagged cards**
- Any field the model wasn't confident about (below 0.85) automatically shows up in the "Needs Review" section on the same page, with an editable text box per field
- Type the correct value and click "Save" next to that field — it updates the record and logs the correction
- A card drops off the review list once all its fields are above the confidence threshold

**Where your data lives**
- `Sports Card Scanner/data/cards.db` — SQLite database with every scanned card, its extracted fields, confidence scores, and the raw model response
- `Sports Card Scanner/data/images/` — the uploaded front/back photos, one pair per scan
- Both are **gitignored on purpose** — this is your personal collection data, not something that belongs in the vault's git history. That also means it is **not backed up by the vault's git sync** — back up the `data/` folder separately (e.g. copy it to OneDrive/an external drive periodically) if the collection grows to matter
- To browse the database directly (not just through the review UI), a free tool like [DB Browser for SQLite](https://sqlitebrowser.org/) can open `cards.db` and let you view/query/export all scanned cards as a table

**Stopping the server properly**
- Normally: Ctrl+C in the terminal it's running in, or just close that terminal window
- If a server seems stuck on a port and won't restart cleanly (a real gotcha hit during testing — see `Sports Card Scanner/README.md`), find and stop the actual process:
  ```powershell
  $owner = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
  Stop-Process -Id $owner -Force
  ```

**Known current limits** (see [[sports_card_scanning_recommendations]] for the full picture)
- No canonicalization yet — player/team/set are stored as whatever Claude reads, not matched against a reference checklist
- No serial-number retry/zoom pass yet — a low-confidence serial number just gets flagged like any other field
- Only tested against one real card so far — accuracy at volume is unproven

Recommendations & Architecture
[[sports_card_scanning_recommendations]]
[[Sports Card Scanning - Open Decisions]]

Build
[[Sports Card Scanning - Build Plan]]

Evaluation & Testing
[[Sports Card Scanning - Evaluation Results]]

Progress Log
[[Hobby Log]]
