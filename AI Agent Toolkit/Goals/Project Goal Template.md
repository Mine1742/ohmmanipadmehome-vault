#aiagent #claudecode

[[AI Agent Toolkit Hub]]

A goal file captures what you're currently trying to accomplish on a specific project/initiative — separate from `CLAUDE.md` (which is stable, rarely-changing context) because goals change often and shouldn't cause CLAUDE.md churn. Point an agent at this file explicitly when starting a session, or reference it from CLAUDE.md as "see GOALS.md for current objective."

## Template

```markdown
# Goal: <short name>

**Status:** active | paused | done
**Started:** <date>

## Objective

One or two sentences — what does "done" look like?

## Success criteria

- Concrete, checkable conditions, not vibes

## Constraints

- Scope boundaries: what NOT to do / touch
- Deadlines, if any

## Current state

- Where things stand right now (update as you go — this section is expected to go stale, that's fine)

## Open questions

- Decisions not yet made that are blocking progress
```

## Notes

- One goal file per initiative, not one giant running list — a stale goal file is worse than no goal file, so archive or delete it when done rather than leaving it to rot.
- For quick one-off tasks, don't bother — this is for anything spanning multiple sessions.
