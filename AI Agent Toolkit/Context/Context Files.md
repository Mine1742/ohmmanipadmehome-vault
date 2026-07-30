#aiagent #claudecode

[[AI Agent Toolkit Hub]]

`CLAUDE.md` is the file Claude Code automatically reads at the start of every session in a project — it's always-on context, not something you have to remind it of. This vault's own copy is at the vault root: [[CLAUDE]].

## What belongs in a CLAUDE.md

- Project structure/conventions a fresh session couldn't infer in one read
- Commands: how to build, test, lint, run
- Things you've had to correct Claude on before (house style, gotchas, "don't do X")
- Pointers to where things live, not the things themselves

## What doesn't belong

- Anything that goes stale fast (current task status, TODOs) — that belongs in a [[Project Goal Template|goal file]] or the conversation itself, not CLAUDE.md
- Long reference material — link out to it instead of pasting it in, or it just eats context budget every single session

## Nested CLAUDE.md files

Claude Code also reads a `CLAUDE.md` in the current working subdirectory in addition to the project root one, if present — useful for a monorepo where different subprojects need different context. Not needed in this vault (flat structure).

## Starting a new project

Use [[Project Context Template]].
