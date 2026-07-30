# Ohmmanipadmehome Vault

This is an Obsidian vault, not a software project — mostly IT/sysadmin knowledge base (ArchKey Mechanical/electric group companies), Azure certification study notes (AZ-104/200/204), an AI/local-LLM learning project, and personal notes. It's tracked in git purely as an edit history safety net, not for collaboration.

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
- `.claude/skills/` — skill definitions
- `.mcp.json` (if present) — MCP server config
- This file (`CLAUDE.md`) — always-loaded project context

When asked to create a new agent or skill "for this vault," write the real file into `.claude/agents/` or `.claude/skills/`, then add/update its entry in the matching catalog note under `AI Agent Toolkit/` rather than duplicating the full content into Obsidian.

## Git

Baseline-commit-and-diff workflow: this repo has no remote, no CI, no collaborators. Normal safety rules still apply (don't force-push, don't discard uncommitted work) but there's no PR process to follow.
