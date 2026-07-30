#aiagent #claudecode

[[AI Agent Toolkit Hub]]

Starting point for a new project's `CLAUDE.md`. Copy into the new project's root, trim what doesn't apply, fill in the rest — don't leave placeholder sections unfilled, delete them instead.

## Template

```markdown
# <Project Name>

One paragraph: what this project is, who it's for, current stage (prototype / production / etc).

## Structure

- Key directories and what lives in each
- Where the entry point is
- Anything organized non-obviously (e.g. "tests mirror src/ but under __tests__/")

## Commands

- Install: `...`
- Run: `...`
- Test: `...`
- Lint/format: `...`
- Build: `...`

## Conventions

- Code style rules not enforced by a linter
- Patterns to follow / patterns to avoid, with why
- Anything you've corrected an agent on before, worth locking in

## Constraints

- Things that must never happen (e.g. "never touch prod config directly")
- External dependencies / services this project talks to
```

See also [[Project Goal Template]] for capturing what you're currently trying to accomplish, which is separate from this file and shouldn't live in CLAUDE.md.
