---
name: greenhouse-builder
description: >
  Turn a greenhouse design into a construction sequence — build steps, tools/hardware
  needed, and a rough schedule. Trigger on "help me build my greenhouse," "what's the
  construction order for my greenhouse," or "what tools do I need to build this."
  Different from greenhouse-designer (what to build) — this is how to actually build it.
---

1. Read `Greenhouse Design.md` (linked from [[Greenhouse]]) for the chosen structure
   type, dimensions, and materials before planning construction — don't plan a build
   for a design that hasn't been settled. If no design exists yet, tell the user to run
   greenhouse-designer first.

2. Break the build into an ordered sequence appropriate to the structure type (typical
   phases: site prep & leveling, foundation/base, framing, glazing/covering, door &
   vent installation, utility hookups). Use WebSearch for technique specifics you're
   not confident on (anchoring methods, glazing installation order) rather than
   guessing.

3. List tools and hardware needed per phase, and flag any step that typically needs a
   permit, inspection, or a second person/professional (electrical, gas line, large
   foundation work).

4. Write or update `Greenhouse Build Plan.md`: ordered build steps as a checklist
   (`- [ ]`), tools/hardware list, and any permit/professional-help flags. Tag
   `#greenhouse`. Link it under a "Build" label in [[Greenhouse]] — add that label if
   it doesn't exist yet, without disturbing the existing labels/links.

5. This is a plan, not a log — if the user reports actual build progress (what they
   did on a given day), that belongs in [[Hobby Log]] via the life-hobby-log skill,
   not here.
