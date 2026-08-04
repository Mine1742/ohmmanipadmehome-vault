---
name: vault-skill-creator
description: >
  Create a new Claude Code skill for this vault, following its established
  design → write → catalog workflow. Trigger on requests like "create a skill for X,"
  "make a skill to do Y," or "I need a skill for [recurring task]." Also use to fix an
  existing skill whose description isn't triggering reliably, or to check whether a new
  request overlaps with a skill that already exists.
---

1. **Scope narrowly.** One well-defined recurring task per skill, not a general-purpose
   catch-all — narrow scope beats broad scope (see [[Agent Engineering]] and
   [[AI Agents]] in `AI Agent Toolkit/`, the same reasoning applies to skills). If the
   request is really several distinct tasks, split it into multiple skills rather than
   one do-everything skill — e.g. this vault's Dao of Life tooling is six separate
   skills (ops, teaching, service-planning, donor-letter, board-resolutions,
   social-media), not one.

2. **Check for overlap first.** Read `AI Agent Toolkit/Skills/Skills Catalog.md` for
   existing skills before creating a new one. If there's real overlap, expand the
   existing skill instead of duplicating — but a new skill is still right when the
   trigger condition or output is genuinely different (e.g. `dao-of-life-ops` logs what
   already happened; `dao-of-life-service-planning` plans what hasn't happened yet).

3. **Write the skill file** at `Claude Skills/<kebab-case-name>/SKILL.md` — this is the
   real, Obsidian-visible location; `.claude/skills` is a junction pointing at it (both
   paths work, but write to `Claude Skills/` since that's what Obsidian indexes and lets
   you edit directly). Match the format in `AI Agent Toolkit/Skills/Skill Template.md`:
   - `name`: kebab-case, must match the folder name.
   - `description`: the single most important field. 1–2 sentences covering WHAT the
     skill does and WHEN to trigger it — concrete trigger phrases the user might
     actually say, not just a topic summary. A weak description is the most common
     reason a skill never fires.
   - Body: procedural, numbered step-by-step instructions to follow — not prose
     explaining the topic. Reference other vault notes with `[[wikilinks]]` where the
     skill needs to read/write them.
   - Match this vault's existing naming convention for the domain it belongs to
     (`dao-of-life-*`, `az-*`, `venture-*`, `life-*`, etc.) rather than inventing a new
     scheme — if it's a genuinely new domain, establish a short consistent prefix for it.

4. **Consider whether part of the job belongs in an agent instead.** If the skill needs
   open-ended research/web lookups that would bloat the main conversation's context,
   have it delegate that piece to a dedicated agent (see
   `AI Agent Toolkit/Agents/Agent Template.md`) rather than doing everything inline —
   agents are read-only research delegates in this vault's convention; skills do the
   writing/filing.

5. **Register it**: add one row to `AI Agent Toolkit/Skills/Skills Catalog.md` — Name,
   Project/Repo, Purpose, Status.

6. **Confirm it's live** — a newly written skill is available immediately, no restart
   needed. Tell the user it's ready and give one example trigger phrase.

For heavier skill-authoring needs beyond this vault's lightweight convention —
performance evals, benchmarking, variance analysis — the global `skill-creator` skill
(from the `anthropic-skills` plugin) is also available; this skill is specifically for
staying consistent with this vault's own established pattern.
