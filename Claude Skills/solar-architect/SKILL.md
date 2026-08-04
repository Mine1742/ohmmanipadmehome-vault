---
name: solar-architect
description: >
  Physical/site design for a solar installation — panel placement layout, mounting
  structure (roof vs ground vs pole), orientation/tilt, and shading analysis. Trigger
  on "where should I put my solar panels," "will shading be a problem," or "plan the
  layout of my solar array." Different from solar-designer, which handles the
  electrical spec, not the physical site plan.
---

1. Read `Solar Power - Concept.md` (roof vs ground mount decision, location) linked
   from [[Solar Power]] before planning a site layout — if no concept exists yet, tell
   the user to run solar-conceptualizer first.

2. Work through the site-specific factors: available roof/ground area and orientation,
   optimal tilt angle for the latitude, shading sources (trees, structures, chimneys)
   across the day and seasons, and structural/mounting considerations (roof condition
   and load capacity, ground mount footing requirements). Use WebSearch for
   latitude-specific tilt guidance or mounting code norms you're not confident on.

3. Propose a placement layout — panel count and arrangement that fits the site,
   with reasoning for the chosen orientation/tilt and any shading tradeoffs accepted.

4. Write or update `Solar Power - Site Layout.md`: site description, chosen layout and
   orientation/tilt, shading analysis, and mounting approach. Tag `#solar`. Link it
   under an "Architecture" label in [[Solar Power]].

5. Stay scoped to physical siting — electrical sizing is solar-designer's job; cost is
   solar-cost-optimizer's job.
