---
name: solar-designer
description: >
  Detailed electrical system design for a solar project — panel wattage/count,
  inverter type and sizing, battery bank sizing, and wiring plan. Trigger on "size my
  solar system," "how many panels do I need," or "design the wiring for my solar
  setup." Different from solar-architect, which handles physical placement/mounting,
  not the electrical spec.
---

1. Read `Solar Power - Concept.md` (linked from [[Solar Power]]) for the settled use
   case, grid-tied/off-grid decision, and battery decision before sizing a system —
   if no concept exists yet, tell the user to run solar-conceptualizer first.

2. Size the system from the stated energy needs: daily/monthly kWh usage or load list,
   sun-hours for the location, panel wattage and count, inverter type (string, micro,
   hybrid) and capacity, and battery bank capacity if storage is in scope. Use
   WebSearch for current panel/inverter/battery specs and typical efficiency figures
   rather than relying on possibly-stale training data — this equipment market moves
   fast.

3. Sketch the wiring plan at a level useful for a real install or a licensed
   installer's review: series/parallel panel stringing logic, DC-to-AC path, breaker/
   disconnect points, and any code-relevant callouts (rapid shutdown, grounding) —
   flag clearly that a licensed electrician must verify/pull permits for any real
   installation.

4. Write or update `Solar Power - System Design.md`: panel/inverter/battery spec and
   count, wiring plan description, and assumptions used for sizing. Tag `#solar`.
   Link it under a "System Design" label in [[Solar Power]].

5. Stay scoped to the electrical system spec — physical panel layout and mounting is
   solar-architect's job; cost is solar-cost-optimizer's job.
