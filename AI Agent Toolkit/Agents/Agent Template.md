#aiagent #claudecode

[[AI Agent Toolkit Hub]]

Starting point for a new Claude Code subagent. Copy the block below into `.claude/agents/<agent-name>.md` (kebab-case filename) in the target project, fill it in, then add a row to [[Agents Catalog]].

## Format

```markdown
---
name: agent-name
description: >
  When the orchestrator should hand off to this agent, written from the orchestrator's
  point of view. Be specific about trigger conditions — this description is what gets
  matched against, not a general summary of what the agent does.
tools: Read, Grep, Glob
model: sonnet
---

You are [role]. Your job is to [narrow, specific task].

[Explain what "done" looks like, what NOT to do, and any constraints —
read-only vs write access, when to ask before acting, output format.]
```

## Design notes

- **Narrow scope beats broad scope.** An agent that does one thing reliably is more useful than one that does many things vaguely — see [[Agent Engineering]] and [[AI Agents]] for the reasoning.
- `tools:` — omit the field entirely to inherit every tool the parent session has; list explicit tools to restrict it (e.g. a read-only research agent shouldn't get `Edit`/`Write`).
- `model:` — omit to inherit the parent's model; set `sonnet`/`opus`/`haiku` to override for cost/speed/quality tradeoffs.
- `description` is the single most important field — it's what determines whether the agent gets used at all.
