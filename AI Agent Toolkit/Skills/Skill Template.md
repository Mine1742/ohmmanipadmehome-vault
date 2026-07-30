#aiagent #claudecode

[[AI Agent Toolkit Hub]]

Starting point for a new Claude Code skill. Skills are packaged instructions for a recurring, well-defined kind of task (a deploy checklist, a repo-specific workflow, a review process) — different from an agent, which is a delegated worker with its own context window.

Create the folder `.claude/skills/<skill-name>/` in the target project with a `SKILL.md` inside, then add a row to [[Skills Catalog]].

## Format

```markdown
---
name: skill-name
description: >
  One or two sentences: what this skill does and, critically, WHEN to trigger it.
  Claude matches user requests against this description to decide whether to load
  the skill, so be concrete about trigger phrases/situations, not just the topic.
---

Step-by-step instructions for the task. Written as directions to follow, not prose
explaining the topic. Keep it procedural.
```

## Notes

- Supporting files (reference docs, scripts, templates) can live alongside `SKILL.md` in the same folder — reference them by relative path from the instructions.
- The `description` is doing the same job as an agent's `description`: it's the trigger condition, not a summary. Weak descriptions are the most common reason a skill never fires.
- Prefer a skill over a raw prompt-note (like the ones in [[Prompt Hub]]) when the task is something you expect to repeat and want triggered automatically/by name, rather than something you'll copy-paste manually.
