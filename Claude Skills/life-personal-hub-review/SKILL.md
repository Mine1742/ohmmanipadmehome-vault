---
name: life-personal-hub-review
description: >
  Generate a periodic review of everything linked under [[Personal Hub]] —
  goals, tasks, hobbies, and personal-interest domains (greenhouse, solar, gardening,
  job search, misc reference notes) — ending in concrete recommendations, not just
  status. Trigger on "review my personal hub," "weekly personal hub check," or when
  running on its scheduled cadence. Different from life-review, which is a broader
  cross-domain pull that also includes Dao of Life and Azure study and does not
  itself end in recommendations.
---

1. Read [[Personal Hub]] fresh each run to get the current list of linked notes —
   don't work from a hardcoded list, since new notes get appended over time.

2. For each linked note, assess recent activity relative to its own nature:
   - Dated logs ([[Hobby Log]], [[Personal Tasks]], [[Goals]], [[App Ideas]]) — same
     staleness check as life-review: what's new since the last review, what hasn't
     moved.
   - Domain hubs ([[Greenhouse]], [[Solar Power]], [[Gardening]]) — check whether any
     child notes exist under their labels yet, or whether the domain is still an
     empty shell with no design/log activity.
   - Static reference notes ([[Skills to learn]], [[Automations]], [[Job links]],
     hobby reference notes) — check whether there's an open/actionable item sitting
     unaddressed.

3. For every item that's stalled, empty, or has an obvious next step, write a
   concrete recommendation — a specific next action, not just "this hasn't moved."
   E.g. not "Greenhouse is still empty" but "no design work has started on the
   greenhouse — if it's still a priority, run greenhouse-designer with your available
   footprint to get it moving." Skip items with nothing to report rather than padding
   the review.

4. Close with a short "if you only do one thing" pick — the single highest-leverage
   recommendation across everything reviewed.

5. Append a dated entry to [[Life Dashboard]] under its own heading
   `## Personal Hub Review — <date>` (distinct from life-review's bare `## <date>`
   entries so the two don't blend together) — newest entry on top, append-only, don't
   edit past entries or the source notes.
