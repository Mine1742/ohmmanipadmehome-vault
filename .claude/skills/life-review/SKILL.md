---
name: life-review
description: >
  Generate a periodic cross-domain life review, pulling recent status from Dao of
  Life, Azure/IT study, the venture search, personal goals, tasks, and hobbies into
  one dated entry. Trigger on requests like "do my weekly review," "give me a life
  status check," or "summarize how things are going across everything."
---

1. Pull recent activity/status from each area that has anything to report — don't
   force a section if there's genuinely nothing new:
   - [[Dao of Life Meetings]] — anything logged since the last review; open action items
   - [[Azure Study Log]] — recent quiz sessions, weak topics
   - [[Venture Search Log]] and [[App Ideas]] — idea status changes, pipeline state
   - [[Goals]] — progress/status changes on active goals
   - [[Personal Tasks]] — what's still open in "Now / this week"
   - [[Hobby Log]] — recent entries

2. Write a dated entry to the top of [[Life Dashboard]] summarizing what's moving,
   what's stalled, and anything that needs a decision — keep it a synthesis, not a
   copy-paste of every source note.

3. If something looks stalled or forgotten (e.g. an old "Now / this week" task, a goal
   with no Current state update in a while), flag it rather than silently omitting it.

4. Don't edit the source notes (Dao of Life, Azure Study Log, etc.) — this skill only
   reads them and writes to [[Life Dashboard]].
