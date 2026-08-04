---
name: dao-of-life-ops
description: >
  Capture and organize Dao of Life church operations — meeting/gathering/event notes,
  member and community tracking, donations and expenses, and governance/legal/compliance
  updates. Trigger on requests like "log this week's gathering," "add a new member,"
  "record a donation," or "update the governance/filing tracker for Dao of Life."
---

Route the request to the right note, and keep every entry additive (append/update rows —
never delete or overwrite existing rows without being asked):

**Meeting or event** → create `Dao of Life Meeting YYYY-MM-DD.md` (use the actual date),
tagged `#daooflife #meeting`, linked to `[[Dao of Life Meetings]]`, with this structure:

```
#daooflife #meeting

[[Dao of Life Meetings]]

**Date:**
**Type:** (gathering / board meeting / planning session / event)
**Attendees:**

## Agenda

## Discussion / notes

## Decisions

## Action items
- [ ]
```

Then add a link to the new note in [[Dao of Life Meetings]]' index.

**Member/community tracking** → add or update a row in the [[Dao of Life Members]] table
(ID, Name, Role, Contact, Joined, Notes). Members are identified by a unique sequential
numeric ID, never reused — assign the next unused ID for a new member. Under Name, use
first name/nickname only — never a full legal/government name, even if the user supplies
one. Ask for any other fields the user didn't supply rather than inventing them.

**Donations or expenses** → add a row to the matching table in [[Dao of Life Finances]]
(Donations or Expenses). Never estimate amounts — ask if unclear.

**Governance/legal/compliance** → update the relevant section of [[Dao of Life Governance]]
(legal structure, leadership/board, bylaws, or the filings tracker table). For anything
involving nonprofit status, tax filings, or legal structure the user isn't certain about,
delegate research to the `dao-of-life-research` agent rather than guessing at requirements.

Always use `[[wikilinks]]` for cross-references, matching this vault's existing convention.
