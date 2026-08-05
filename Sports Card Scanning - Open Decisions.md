#personal

[[Sports Card Scanning Hub]]

Decisions needed before scaffolding, with the tradeoffs surfaced during the 2026-08-04 architecture revision (see [[sports_card_scanning_recommendations]]).

Capture app platform
- Native mobile app — best capture UX (live boundary detection, auto-capture) but real dev overhead for a solo hobby project
- PWA / browser camera capture — much less build effort, works on phone or desktop, slightly clunkier capture flow
- Desktop drag-and-drop uploader — least effort, fits a "batch-photograph a stack of cards, then upload" workflow rather than live capture
- **Status:** decided 2026-08-04 — desktop drag-and-drop uploader

Vision-LLM provider
- Claude Sonnet 5 / Opus 5, GPT-5 vision, Gemini — all in the low-90s–97% range on general document-extraction benchmarks; none has a published trading-card-specific benchmark
- **Status:** decided 2026-08-04 — Claude (Sonnet 5 default, Opus 5 available for hard cases) as the scaffold default. Not treated as final — still worth running the [[Sports Card Scanning - Evaluation Results|evaluation set]] against GPT-5/Gemini later if Claude's real-world accuracy on serials/foil disappoints.

Hosting
- Fully local (self-hosted backend on home hardware) vs. a small cloud deployment
- **Status:** decided 2026-08-04 — local/self-hosted. Backend runs on home hardware; SQLite for storage (no separate DB server needed at hobbyist scale); uploader is a browser page served by the same local backend.

Scope confirmation
- Personal collection scale (hundreds–low thousands of cards), not a multi-user product — confirms the hobbyist-scale cost/latency numbers in [[sports_card_scanning_recommendations]] still apply
- **Status:** assumed true unless corrected

Backend language/framework
- No strong constraint from the architecture itself — vision-LLM API + a small DB is workable in Python (FastAPI), Node, or similar
- **Status:** undecided
