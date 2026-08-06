# Ohmmanipadmehome Vault

This is an Obsidian vault, not a software project — mostly IT/sysadmin knowledge base (ArchKey Mechanical/electric group companies), Azure certification study notes (AZ-104/200/204), an AI/local-LLM learning project, and personal notes. It's tracked in git as an edit history safety net and as the sync mechanism between this machine and scheduled cloud automation (see Git section below) — not for human collaboration.

## Structure & conventions

- **[[Home]]** is the vault's entry point — links to every topic Hub.
- Notes link to each other with Obsidian `[[wikilinks]]`, not markdown `[]()` links, except for external URLs.
- "Hub" or topic-name notes (e.g. `Azure Hub.md`, `Software.md`, `Networking.md`) act as MOCs (maps of content) — flat lists of `[[links]]` to the notes in that topic, sometimes grouped under plain-text subheadings (no `##` markdown headers in most, just an indented label line — match existing style within a given file rather than introducing markdown headers).
- Before adding a new note, check whether it belongs under an existing Hub rather than creating a new one.
- Preserve existing hand-curated structure in Hub files — append new links rather than reorganizing what's already there, unless asked to.

## AI Agent Toolkit

`AI Agent Toolkit/` (visible in Obsidian) is the authoring/reference space for Claude Code assets: agent designs, skill designs, MCP/tool notes, project-context templates, and goal files. See **[[AI Agent Toolkit Hub]]**.

The actual functional Claude Code config lives in the usual places and is the source of truth Claude Code loads:
- `.claude/agents/` — subagent definitions
- `.claude/skills/` — skill definitions. In this vault specifically, `.claude/skills` is a directory junction pointing at `Claude Skills/` (a normal folder at the vault root) — Obsidian doesn't traverse into junctions when indexing, so the real, Obsidian-editable `SKILL.md` files live at `Claude Skills/<name>/SKILL.md`. Writing to either path works (the junction is transparent), but prefer `Claude Skills/` as the canonical path since that's the real location.
- `.mcp.json` (if present) — MCP server config
- This file (`CLAUDE.md`) — always-loaded project context

When asked to create a new agent or skill "for this vault," write the real file into `.claude/agents/` or `Claude Skills/<name>/SKILL.md`, then add/update its entry in the matching catalog note under `AI Agent Toolkit/` rather than duplicating the full content into Obsidian.

## Git

Baseline-commit-and-diff workflow, backed by a private GitHub remote
(`github.com/Mine1742/ohmmanipadmehome-vault`) — still no CI, no human
collaborators, no PR process to follow. Two automated writers push to this
remote on their own schedules:
- A local Task Scheduler job (`.claude/scripts/vault-sync.ps1`, daily 7am)
  that pulls, commits any local edits, and pushes.
- Two scheduled cloud routines — "Dao of Life Growth Cycle" (Mon/Thu) and
  "Personal Hub Weekly Review" (Mon) — that commit and push their own work.

Normal safety rules still apply (don't force-push, don't discard uncommitted
work), but because of the automated writers, pull before you push, and check
`.claude/scripts/vault-sync.log` if a morning sync looks like it didn't go
through.

**Land on `master`, not a stranded branch.** The human owner's local Obsidian
clone only tracks `master` and doesn't manually merge feature branches. Some
session types (e.g. scheduled cloud routines run via Claude Code on the web)
auto-assign a working branch per session instead of committing straight to
`master`. If you find yourself on such a branch after finishing vault edits —
check with `git branch --show-current` — merge it into `master` and push
`master` too before ending the session, so the human doesn't have to hunt for
or manually merge the work:
```
git fetch origin master
git checkout -B master origin/master
git merge --ff-only <your-working-branch>   # or a regular merge if master moved;
                                             # this vault's notes are mostly
                                             # append-only, so trivial conflicts
                                             # can usually keep both sides
git push origin master
```
Skip this if you're already committing directly to `master`.
