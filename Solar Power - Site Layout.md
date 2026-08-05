#solar

[[Solar Power]] | [[Solar Power - Concept]] | [[Greenhouse Design]]

Site Description

- Greenhouse: 12'x8' footprint, freestanding, long axis east–west. South-facing lean-to roof, 12' north wall down to 8' south wall (~6:12 pitch).
- Solar structure: a matching **unenclosed lean-to canopy**, 6' wide, attached to the greenhouse's west side — same roofline, same wall heights (12' back / 8' front), same ~6:12 pitch, continuing the greenhouse's roof plane further west. No walls, no glazing — just the open frame, with panels mounted on its roof. Not a ground rack sitting on a pad.
- Location: Maryland/DC area, ~4–4.5 average peak sun hours/day.
- Target array: ~800W–1,000W (from [[Solar Power - Concept]]).

Mounting Decision: Roof-mount on the dedicated open canopy

Two options that don't apply here, for the record: mounting on the greenhouse's own glazed roof would shade the crops underneath (its whole job is to let light through) — not relevant since the canopy is a separate, unenclosed structure. A loose ground rack was the prior read on the "pad," but that's not what's being built — this is a proper roof surface, just open below instead of enclosed.

Since the canopy carries no crops and no glazing, mounting panels directly on its roof is exactly the right call — same as a solar carport or patio cover. Framing still needs to be sized for panel dead load + wind uplift on top of its own structural loads, consistent with the bracing already flagged for the greenhouse's tall north wall in [[Greenhouse Design]].

Tilt & Orientation

- Panels face true south, fixed by the canopy's own roof pitch: **~26.6° (6:12)** — not a freely chosen angle, since it's set by matching the greenhouse's roofline.
- That's about 6–7° below the ~33° that's ideal for balanced year-round production at this latitude (see prior calc, still valid as a reference point) — but a shallower tilt actually biases output *toward* summer/higher-sun months and away from deep winter, which lines up reasonably well with a greenhouse that's mainly operating spring through fall. Being ~6–7° off the ideal fixed angle typically only costs a small (low single-digit %) amount of annual output — not a real compromise, and worth it for a continuous, structurally simpler roofline instead of a separate rack angle.

Shading Analysis

This is the big change from the earlier ground-rack read: because the canopy shares the greenhouse's exact roof plane and wall heights, there's **no tall wall standing to the east of the panels** the way there would be with a low ground rack behind an 8'–12' wall. The greenhouse's ridge line *is* the panel plane's own back edge, not a separate obstruction rising above it — so the greenhouse doesn't shade its own canopy.

Remaining shading factors are the ordinary ones for any roof-mounted south-facing array:
- Low, oblique sun near sunrise/sunset — unavoidable for any fixed array, not specific to this site.
- **Confirmed clear:** no trees, fences, or other structures near the site — open sky to the south and east. No site-shading risk beyond the universal low-sun-angle effect.

Layout & Panel Count (rough — refine with solar-designer)

Roof surface, not flat pad footprint: the canopy's 6' width × its sloped depth (8' horizontal run ÷ cos(26.6°) ≈ **9' slope length**) gives roughly **54 sq ft of actual roof surface** to mount on — slightly more than the flat 48 sq ft footprint, since tilting the surface adds area. Comfortably fits **~2–3 standard panels** (typical 300–400W panel is ~17–18 sq ft), landing in the 800W–1,000W target range — e.g. 3× ~300W or 2× ~400–450W. Exact count/model is still solar-designer's call.

Mounting Approach

- Standard roof-mount rail-and-clamp hardware on the canopy's rafters/purlins — the same category of hardware used for any pitched-roof solar array, not ground-rack tilt legs.
- Canopy framing: build it the same way as the greenhouse's recommended Option A framing in [[Greenhouse Design]] (wood-frame — pressure-treated or cedar), just unenclosed, so the two structures read as one continuous build rather than mismatched systems.
- Footing: posts set on concrete piers, consistent with what's already recommended for the greenhouse itself given Maryland's frost line (~24"–30").

Open Questions

- ~~Confirm no trees or other structures shade the site~~ — resolved: clear, open sky
- Exact panel model/count — solar-designer
- Rafter/purlin sizing for the canopy needs to account for panel dead load + wind uplift, not just its own frame weight — worth a structural gut-check when this moves to greenhouse-builder
- ~~Local (county) permitting~~ — general Maryland guidance gathered in [[Greenhouse Design]] (permitting note); still needs a direct check with your specific county's permitting office
- Soil conditions at the site (for footing choice) — not yet checked

Next Steps

- **solar-designer** — panel/battery/inverter sizing and wiring plan, now that site layout and rough panel count are settled
- **solar-cost-optimizer** — equipment pricing, footing/racking cost comparison, and sourcing once the system is designed

Sources (tilt angle guidance):
- [Solar Panel Angle: how to calculate solar panel tilt angle?](https://sinovoltaics.com/learning-center/system-design/solar-panel-angle-tilt-calculation/)
- [What's the Best Angle for Solar Panels to Get Maximum Output? | Sunrun](https://www.sunrun.com/knowledge-center/best-angle-for-solar-panels)
