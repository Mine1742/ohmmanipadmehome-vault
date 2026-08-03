---
name: az-study-guide
description: >
  Draft or expand an Azure certification study-guide note (AZ-104 or AZ-204) for a
  topic not yet well-covered in the vault. Trigger on requests like "write a study
  guide for Azure Key Vault," "deep-dive Azure networking for AZ-104," or "expand my
  notes on managed identities." Matches this vault's existing dense study-guide style,
  not a copy-paste of Microsoft Learn.
---

1. Check whether the topic is already covered: search `AZ 104 Hub.md`, `AZ204 Hub.md`,
   `AZ 200 Hub.md`, and `AZ 104 Summaries.md` for an existing note. If one exists, expand
   it rather than creating a duplicate note.

2. Match the vault's established "newer" study-guide style — the quality bar is
   `AZ-104 — Implement and Manage Virtual Networking.md`, not the older
   `AZ 104 Summaries.md` copy-paste style. That means:
   - A domain-map / where-this-fits-in-the-exam intro
   - Comparison tables (SKUs, defaults, limits) wherever the topic has them
   - ASCII diagrams for architecture patterns where useful
   - Inline "Exam tip" callouts
   - A closing "Lab Skills Checklist" with `- [ ]` checkboxes for hands-on practice

3. If anything about the topic might have changed recently (Azure ships fast — pricing
   tiers, default limits, deprecated features, exam objective weight changes), delegate
   to the `az-exam-research` agent to verify against current Microsoft Learn content
   rather than asserting from training knowledge alone.

4. Name the note to match the existing convention in whichever hub it belongs under —
   look at neighboring notes in that hub for the naming style in use (bracketed
   Title Case vs underscore_style — the two coexist; match the hub you're adding to)
   rather than inventing a third convention.

5. Link the new/expanded note into the correct hub (`AZ 104 Hub.md` or `AZ204 Hub.md`),
   respecting that hub's existing indentation/grouping style — do not add markdown `##`
   headers where the hub doesn't already use them, and do not reorganize existing links.
