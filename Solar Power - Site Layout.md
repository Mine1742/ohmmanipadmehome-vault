#solar

[[Solar Power]] | [[Solar Power - Concept]] | [[Greenhouse Design]]

Site Description (revised — dimensions changed, second canopy added)

- Greenhouse: 12'x8' footprint, freestanding, long axis east–west. South-facing lean-to roof, **9' north wall down to 6' south wall (~4.5:12 pitch, ~20.6°)** — revised down from the original 12'/8' after the user reconsidered the wall heights (see [[Greenhouse Design]] for the full reasoning).
- **Two matching unenclosed lean-to canopies**, one on the west side and one mirroring it on the east side. Each is **6' wide x 6' deep** (not 6'x8' as originally planned) — anchored at the north wall, running only 6' of the greenhouse's 8' depth. Same roofline/pitch as the greenhouse, continuing its roof plane in both directions. No walls, no glazing — panels mount directly on the roof.
- Because each canopy only covers 6' of the 8' depth, its south-facing edge sits partway up the slope rather than at the greenhouse's own south-wall height: **9' at the north edge down to 6.75' at the canopy's south edge** (2' short of the greenhouse's actual south wall).
- Location: Camp Springs, Prince George's County, MD, ~4–4.5 average peak sun hours/day.
- Target array: ~800W–1,000W (from [[Solar Power - Concept]]).

Mounting Decision: Roof-mount on both dedicated open canopies

Two options that don't apply here, for the record: mounting on the greenhouse's own glazed roof would shade the crops underneath (its whole job is to let light through) — not relevant since the canopies are separate, unenclosed structures. A loose ground rack was the prior read on the "pad," but that's not what's being built — these are proper roof surfaces, just open below instead of enclosed.

Since neither canopy carries crops or glazing, mounting panels directly on their roofs is exactly the right call — same as a solar carport or patio cover, now done on both sides symmetrically. Framing on both needs to be sized for panel dead load + wind uplift on top of its own structural loads, consistent with the bracing already flagged for the greenhouse's north wall in [[Greenhouse Design]].

Tilt & Orientation

- Panels face true south on both canopies, fixed by the shared roof pitch: **~20.6° (~4.5:12)** — not a freely chosen angle, since it's set by matching the greenhouse's roofline (revised down from ~26.6° after the wall-height change).
- That's about 12–13° below the ~33° that's ideal for balanced year-round production at this latitude (a bigger gap than the original design's 6–7°) — but a shallower tilt still biases output *toward* summer/higher-sun months and away from deep winter, which lines up reasonably well with a greenhouse mainly operating spring through fall. PV output vs. tilt angle is a fairly flat curve within ±15-20° of optimal, so this is more likely a modest few-percent-of-annual-output cost than a serious one — but it's a real enough gap to note honestly rather than wave off the way the smaller original gap could be.

Shading Analysis

Because both canopies share the greenhouse's exact roof plane and wall heights, there's **no tall wall standing beside either array** the way there would be with a low ground rack behind a full-height wall. The greenhouse's roofline *is* each panel plane's own edge, not a separate obstruction rising above it — so the greenhouse doesn't shade either canopy. This logic is symmetric: it applies to the new east canopy exactly the same way it applied to the original west one.

Remaining shading factors are the ordinary ones for any roof-mounted south-facing array:
- Low, oblique sun near sunrise/sunset — unavoidable for any fixed array, not specific to this site.
- **Confirmed clear:** no trees, fences, or other structures near the site — open sky to the south and east. This was confirmed before the east canopy was added; worth a quick re-check specifically toward the east horizon now that there's an array on that side too, but nothing in the site description suggests it would be different from the west side's result.

Layout & Panel Count (revised — one panel per canopy, not two stacked)

This changed materially once the canopy footprint shrank from 6'x8' to 6'x6'. Each canopy's roof surface is now 6' width × its own sloped depth (6' horizontal run ÷ cos(20.56°) = **6.408' slope length**, confirmed precisely — the angle between the north wall and the roof is 69.44°, the complement of the 20.56° pitch) ≈ **~38.4 sq ft per canopy** (6' × 6.408'), down from ~54 sq ft on the single larger canopy in the original plan.

That's not enough depth for 2 panels stacked front-to-back the way [[Solar Power - System Design]] originally laid out (that needed ~90" of depth for 2 panels at ~44.6" each; only ~77" is available now). **Each canopy fits exactly 1 standard ~400W panel** — but there are now two canopies, so the total is still **2 panels, ~800W combined** — the same array size as before, just split one-per-side instead of stacked on the west alone. The electrical design in [[Solar Power - System Design]] doesn't need to change on the sizing side, only on the physical wiring-run description (see that note for the update).

Mounting Approach

- Standard roof-mount rail-and-clamp hardware on each canopy's rafters/purlins — the same category of hardware used for any pitched-roof solar array, not ground-rack tilt legs. This is now **two separate single-panel installations** (west and east) rather than one two-panel install.
- Canopy framing: build both the same way as the greenhouse's recommended Option A framing in [[Greenhouse Design]] (wood-frame — pressure-treated or cedar), just unenclosed, so all three sections (greenhouse, west canopy, east canopy) read as one continuous build.
- Footing: posts set on concrete piers, consistent with what's recommended for the greenhouse itself given Maryland's frost line (~24"–30") — now needed at both canopies' post locations, not just the west.

Open Questions

- ~~Confirm no trees or other structures shade the site~~ — resolved for the general site; worth a quick re-check specifically toward the east now that there's an array on that side too
- Exact panel model — solar-designer (count is now settled: 1 per canopy, 2 total)
- Rafter/purlin sizing for both canopies needs to account for panel dead load + wind uplift, not just frame weight — worth a structural gut-check when this moves to greenhouse-builder
- ~~Local (county) permitting~~ — resolved with real Prince George's County numbers in [[Greenhouse Design]] (a permit is now required — the combined footprint crossed the county's 150 sq ft threshold)
- Soil conditions at the site (for footing choice, now at 4 canopy corners instead of 2 plus the greenhouse's own footings) — not yet checked

Next Steps

- **solar-designer** — panel/battery/inverter sizing and wiring plan, now that site layout and rough panel count are settled
- **solar-cost-optimizer** — equipment pricing, footing/racking cost comparison, and sourcing once the system is designed

Sources (tilt angle guidance):
- [Solar Panel Angle: how to calculate solar panel tilt angle?](https://sinovoltaics.com/learning-center/system-design/solar-panel-angle-tilt-calculation/)
- [What's the Best Angle for Solar Panels to Get Maximum Output? | Sunrun](https://www.sunrun.com/knowledge-center/best-angle-for-solar-panels)
