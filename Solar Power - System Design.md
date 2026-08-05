#solar

[[Solar Power]] | [[Solar Power - Concept]] | [[Solar Power - Site Layout]]

This is a planning-level electrical design, not a stamped install plan — **a licensed electrician should review and pull any required permit before this gets wired up**, especially the battery, inverter, and grounding work.

Load & Sizing Basis

From [[Solar Power - Concept]]: ~2,050 Wh/day (4 fans, pump, grow+ambient lights, radio, vent actuators — see that note for the per-load breakdown). From [[Solar Power - Site Layout]]: canopy roof is 6' wide x ~9' slope depth (~54 sq ft), fixed tilt ~26.6°, true south, no shading, MD ~4.5 peak sun hours/day.

Panel Array: 2 panels, ~800W — not 3

The site layout's "~2-3 panels" estimate was a flat square-footage calculation. Real panel dimensions change that once you actually try to lay them out:

- Modern ~400W panels run roughly 44.6" x 67.8" (~19-20 W/sq ft is the 2026 residential median).
- The canopy's 6' (72") width is the binding constraint, not total area — a panel's long edge (~68") fits across it with a few inches to spare, but there's no room for a second panel *beside* it (2 panels side-by-side would need ~135"+ of width).
- The fix is orientation: turn the panels so their **long edge runs across the 6' width** and their **short edge (~45") runs up the 9' (108") slope**. Two panels stacked front-to-back down the slope use ~90" of the 108" available depth — comfortably fits, with ~18" left over for mounting rail and edge clearance. A third panel would need ~134" of depth and doesn't fit.

**Result: 2 panels x ~400W = ~800W array** — the low end of the original 800W-1,000W target, not the high end. Worth knowing now rather than after panels are bought.

Generation check: 800W x 4.5 sun hrs x ~0.77 system efficiency (MPPT + battery round-trip + inverter losses combined) ≈ **2,772 Wh/day** generation capacity against a ~2,050 Wh/day load — about 35% headroom for cloudy days, panel aging, and the tilt being a few degrees off the theoretical ideal. Healthy margin without oversizing.

Charge Controller: MPPT, ~50A

- **MPPT over PWM** — MPPT is worth the extra cost here specifically because the panels will be wired in series (see below), producing a string voltage well above the battery voltage; MPPT converts that efficiently, PWM would just waste it.
- Wire the 2 panels **in series**: keeps current low (~9-10A, same as a single panel's Imp) and lets the controller buck a higher input voltage down to the battery — cleaner than paralleling two 24V-adjacent panels into a 24V bank.
- Controller sizing: 800W ÷ 24V x 1.25 (NEC-style safety factor) ≈ 41.7A → **50A MPPT controller**, giving headroom if the array ever grows.

Battery Bank: 24V LiFePO4, ~200Ah (~4.8 kWh)

- **24V system voltage** — the common rule of thumb is 12V under 1,000W, 24V for 1,000-3,000W, 48V above that. This system's ~800W array sits right at the 12V/24V boundary; 24V is the better call because it halves the current (and wire gauge/cost) compared to running the same wattage at 12V, and component availability at 24V is still excellent at this scale.
- **LiFePO4** (as recommended in the concept stage) for cycle life and safety under daily charge/discharge use.
- Target: 2 days of autonomy (cloudy-day buffer) = 2,050 Wh x 2 = 4,100 Wh usable.
- At ~80% practical depth of discharge, that needs ~5,125 Wh nameplate capacity ≈ 213Ah at 24V.
- **Closest standard size: 24V 200Ah (~4.8 kWh nameplate)** — commonly built from two 12V 200Ah LiFePO4 packs in series. This lands slightly under the strict 80%-DoD target (~4.1 kWh usable at 80% DoD vs. the 4.1 kWh goal is close but tight) but LiFePO4 tolerates deeper occasional discharge without much cycle-life penalty, so this is a reasonable practical fit.
- **Flag for solar-cost-optimizer:** a 24V 230-250Ah bank would give more comfortable margin above the 2-day target at a modest cost step up — worth pricing both.

Inverter: ~800W continuous / ~1,500W surge, pure sine wave, 24V input

- Worst-case simultaneous continuous load (everything running at once): 4 fans (120W) + grow lights (150W) + ambient (20W) + radio (10W) + vent actuators (40W) ≈ 340W, plus the pump if it overlaps (60W) ≈ **~400W continuous worst case**.
- Surge: motor starting inrush (fans, pump) can spike 2-3x running watts briefly — sized for ~1,200-1,500W surge capacity.
- **Pure sine wave**, not modified sine — motors (fans, pump) run cooler and more reliably on it, and it's the safer default for mixed/unknown equipment.
- **~800W continuous-rated inverter** gives comfortable headroom above the 400W worst case with room for the surge event, at a 24V DC input to match the battery bank.

Worth reconsidering once real products are picked: if the fans and pump end up being 12V/24V DC-native models rather than AC plug-in ones, running them directly off the DC bus (skipping the inverter entirely for those loads) cuts conversion losses and lets the inverter be downsized further. The pump was already specified as 12V DC — recommend feeding it through a small 24V-to-12V DC-DC converter rather than tapping one battery out of the series pair (that unbalances the pack's charge state over time).

Wiring Plan (high level — sizes/models to be confirmed with real product datasheets)

1. **PV array** (2 panels in series) → PV disconnect/combiner with a fuse sized to ~1.56x the string's short-circuit current (Isc) → **MPPT charge controller** (50A)
2. Charge controller → **battery bank** (24V 200Ah LiFePO4) through a breaker sized to the controller's max output current
3. Battery bank → **main battery disconnect** → busbar, branching to:
   - **Inverter** (24V DC input), its own DC breaker sized to the inverter's rated input current at low-voltage cutoff
   - **DC-DC converter** (24V→12V) for the pump, its own fuse
   - Individual fused branches for any DC-native loads (e.g. DC fans, if chosen over AC)
4. **Grounding**: bond the panel racking/frame, charge controller, inverter chassis, and battery enclosure to a common ground rod — this and all final wire gauges are exactly the kind of thing to have an electrician verify, not something to self-certify from this note.
5. **Disconnects**: accessible PV disconnect and battery disconnect near the array and battery enclosure respectively — good practice for a detached structure even without a formal rapid-shutdown code requirement (that mostly targets grid-tied systems).

Assumptions Used

- 4.5 peak sun hours/day (MD average) — not adjusted for worst-case winter month, since the load is primarily spring-through-fall use
- ~77% combined system efficiency (MPPT + battery round-trip + inverter losses)
- 80% practical LiFePO4 depth of discharge
- 2 days of battery autonomy as the cloudy-day buffer
- All panel/battery/inverter figures are class-level estimates (e.g. "~400W panel," "24V 200Ah pack") pending actual product selection — refine with real datasheets before ordering

Open Questions

- Actual panel/battery/inverter/controller product picks — needed before solar-cost-optimizer can price this
- Exact wire gauges and fuse ratings depend on real cable run lengths — confirm against manufacturer wire-size charts once the physical layout (canopy → battery enclosure location) is set
- Whether fans/pump/lights end up as DC-native or AC plug-in products — changes inverter sizing and whether some loads can skip the inverter entirely
- Licensed electrician review before any real wiring

Next Steps

- **solar-cost-optimizer** — price this spec out (panels, MPPT controller, 24V 200Ah LiFePO4 bank, ~800W pure sine inverter, wiring/fusing hardware) and compare vendors
