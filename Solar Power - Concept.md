#solar

[[Solar Power]] | [[Greenhouse]]

Use Case

Off-grid solar power system for the [[Greenhouse]] — no existing electrical service reaches the structure. Powers: 4 air-circulation fans, an irrigation pump, grow lights + ambient lighting, a radio, and louvered vent door actuators.

Constraints

- Location: Maryland/DC area — roughly 4 to 4.5 average peak sun hours/day
- Off-grid, full autonomy needed — fans/pump/lights/radio should work at night and on cloudy days, so battery storage is required (not daytime-only)
- Budget: flexible, not yet fixed — real cost options to come from a solar-cost-optimizer pass
- [[Greenhouse Design]] (dimensions, roof pitch/orientation) isn't filled in yet, so panel mounting location is still open

Rough Load Estimate

Early estimate to sanity-check feasibility — not sourced product specs yet. To be firmed up once actual fan/pump/light models are picked.

| Load | Qty | Est. W each | Runtime | Wh/day |
|---|---|---|---|---|
| Circulation fans | 4 | ~30 W | 8 hr | 960 |
| Irrigation pump (12V diaphragm/demand type) | 1 | ~60 W | 1 hr | 60 |
| Grow lights (supplemental LED) | 1 set | ~150 W | 6 hr | 900 |
| Ambient lighting | 1 | ~20 W | 4 hr | 80 |
| Radio | 1 | ~10 W | 4 hr | 40 |
| Louvered vent door actuators | 2 | ~20 W (only while moving) | ~15 min total | 10 |
| **Total** | | | | **~2,050 Wh/day (~2.05 kWh/day)** |

That's a modest load — comparable to a couple of laptops running all day.

High-Level Options

Grid-tied vs off-grid
- Off-grid is the clear call. No grid service reaches the greenhouse, and trenching/running conduit from the house isn't worth it to interconnect a few-hundred-watt load. Off-grid solar + battery is a good fit at this scale.

Battery vs no battery
- Battery required, per the "anytime" runtime requirement. Recommend LiFePO4 over lead-acid — better cycle life for daily charge/discharge use, safer, no ventilation/off-gassing concerns inside or near a greenhouse.

Roof vs ground mount
- Not settled — depends on the greenhouse's actual roof pitch/orientation, which [[Greenhouse Design]] doesn't have yet. Roof mount is cheaper (no racking/footing) if there's usable south-facing roof area that can carry the load. Ground or pole mount costs more but allows optimal tilt/orientation and keeps the roof clear — worth it if the greenhouse roof is shaded, north-facing, or lightly built. Hand off to solar-architect once dimensions exist.

DIY vs professional install
- Very DIY-approachable at this scale — sub-1kW array, small battery bank, standalone off-grid system with no utility interconnection. Electrical permitting requirements for a detached-structure off-grid system vary by county (Maryland/DC area) — worth a quick local-jurisdiction check before wiring, but this isn't a project that requires a professional installer.

Feasibility Read

**Green light.** ~2 kWh/day is a small, well-bounded load. Rough sizing:
- Panels: 2,050 Wh ÷ (4.5 sun hrs × ~0.75 system efficiency, accounting for charge controller/battery/inverter losses) ≈ 600W minimum → **~800W–1,000W array** gives comfortable cloudy-day margin
- Battery: ~2 days of autonomy (cloudy-day buffer) at 2.05 kWh/day ÷ 0.8 usable depth (LiFePO4) ≈ **~5 kWh battery bank**

Both are small, inexpensive, well-precedented off-grid setups — nothing here is a stretch. No red flags from the load side. The open risks are physical (mounting location, shading) rather than electrical.

Open Questions

- ~~[[Greenhouse Design]] dimensions/orientation~~ — resolved: 12'x8' lean-to greenhouse, 12'x6' matching solar canopy, see [[Solar Power - Site Layout]]
- ~~Shading near the greenhouse~~ — resolved: clear, open sky, no nearby obstructions
- ~~Louvered vent doors motorized or manual~~ — resolved: motorized/automated, kept as a real (small) load in the estimate above
- Real fan/pump/light product specs — current wattages are still estimates, not sourced products — blocks final solar-designer sizing and real solar-cost-optimizer pricing
- Firm budget ceiling — still flexible; real numbers to come from solar-cost-optimizer

Next Steps

Once dimensions and shading are known: **solar-architect** for physical panel placement/mounting. Once loads are firmed up with real product specs: **solar-designer** for panel/battery/inverter sizing and wiring. After the system is designed: **solar-cost-optimizer** for equipment pricing, vendor comparison, and sourcing.
