#solar

[[Solar Power]] | [[Solar Power - System Design]]

These are current market estimates from web research (August 2026), not quotes — get real vendor quotes before ordering, and confirm any incentive eligibility with a tax professional or Maryland Energy Administration before counting on it.

**Revision note:** the design changed after this was first written — one west canopy became two smaller canopies (east + west), each holding 1 panel instead of 2 stacked on the west side alone (see [[Solar Power - Site Layout]]). Total panel count/wattage is unchanged (still 2x ~400W, ~800W), so the panel/battery/controller/inverter cost lines below are still accurate. Two things below did change: mounting hardware (now two separate single-panel rail kits) and permitting — the build now confirmedly requires a Prince George's County building permit plus a rooftop PV permit (previously this was an open, likely-exempt question; now it's confirmed required, see [[Greenhouse Design]]).

Itemized Cost Estimate

| Item | Spec | Est. cost |
|---|---|---|
| Solar panels | 2x ~400W | $700–$950 |
| MPPT charge controller | 50A, 12V/24V auto | $130–$170 |
| Battery bank | 24V 200Ah LiFePO4 (~5.1kWh) | $1,239–$1,600 |
| Inverter | ~800W continuous, pure sine, 24V input | $150–$220 |
| DC-DC converter | 24V→12V, for the pump | $30–$60 |
| Wiring, fusing, disconnects, misc. electrical | PV disconnect, battery disconnect, breakers, cable — now with longer/split runs to two canopies instead of one | $350–$500 |
| Roof-mount rail/clamp hardware | **2 separate single-panel kits** (east + west canopy), wood-rafter mounting | $200–$350 |
| Permit fees | Prince George's County building permit + rooftop PV permit — now confirmed required, not researched in detail here | *not yet priced — check DPIE fee schedule* |
| **Equipment subtotal (excl. permit fees)** | | **~$2,800–$3,900** |

**Not included here** — the canopy's structural build (posts, footings, roof decking, concrete piers) belongs to the greenhouse build budget, not the solar equipment budget. Track that in [[Greenhouse Cost Estimate]] via greenhouse-price-optimizer rather than double-counting it here; this table is the electrical/solar equipment only.

Battery capacity tradeoff (the biggest line item by far): [[Solar Power - System Design]] flagged 230–250Ah as a more comfortable margin than 200Ah. LiFePO4 pricing scales roughly linearly with capacity (~$6/Ah at 24V based on the $1,239 200Ah price point), so:
- **230Ah: ~$1,420** (+~$180)
- **250Ah: ~$1,550** (+~$310)

The opposite lever is also worth knowing: dropping to **1 day of autonomy instead of 2** roughly halves the battery requirement (~100Ah, ~$650–700) — a real ~$550–600 savings if you're comfortable with less cloudy-day buffer. Since the battery is easily the largest single cost, this is the one component where the spec has real room to move either direction depending on how much autonomy actually matters to you.

Vendor Sourcing — specific real products

System is finalized at 800W (2 panels, one per canopy). Confidence varies by line — flagged below. Get real quotes before ordering regardless.

| Item | Specific product | Vendor | Price | Confidence |
|---|---|---|---|---|
| Solar panel (need 2x) | **RICH SOLAR MEGA 400** — 400W, 67.8" x 44.7" x 1.2", 45.2 lbs | richsolar.com | ~$350–450 (class estimate, exact current price not confirmed) | Dimensions confirmed as a match for the ~68"x45" envelope both canopies need; price is a class estimate, not pulled from the live listing |
| MPPT charge controller | **EPEVER 50A MPPT** (12V/24V auto, 150V max PV input) — or equivalent from VEVOR/KFFKFF at similar spec | Amazon / EPEVER direct | ~$130–$170 | Good — matches the 50A target directly, several brands at this exact rating and price band |
| Battery | **LiTime 24V 200Ah LiFePO4** (5,120Wh, 200A BMS, 4,000+ cycles) | litime.com / Amazon | **$1,239** | High — specific price confirmed |
| Battery (230Ah alternative) | **LiTime 24V 230Ah LiFePO4** (5,888Wh) — real product exists in this exact line | litime.com / Walmart | ~$1,420 (scaled from the 200Ah price; exact listing price not confirmed) | Medium — product confirmed real, price estimated by linear Ah scaling |
| Inverter | **Renogy 2000W 24V Pure Sine Wave Inverter** | renogy.com | $339.99 | Medium — Renogy doesn't make an 800W-class 24V unit (their line jumps from smaller 12V models to 2000W at 24V), so this is oversized for the ~400W worst-case load, but it's a real, confirmed-price option with headroom if the load ever grows. A closer-sized 24V unit from another brand is worth a further look before buying — don't default to this without checking |
| DC-DC converter (pump) | **Victron Orion 24/12-25A** (or the non-isolated buck converter family generally) | Victron dealers (NAZ Solar Electric, SanTan Solar, Amazon) | ~$100–$125 (confirmed price point is the 70A version at $124.10; the pump only needs ~5A so a smaller-rated Orion, typically similarly priced or less, is the better fit) | Medium — Victron Orion family confirmed real and available at this general price band; exact SKU/amperage to buy needs a final check against the pump's actual current draw |
| Roof-mount hardware | **Standard pitched-roof rail-and-clamp kit** (Z-brackets/L-feet + rails + end/mid clamps) — correction from earlier research | Multiple (Amazon, AltE, ShopSolarKits) | ~$150–$250 per single-panel kit | **Correction:** the canopy roof is already built at a fixed ~20.56° pitch, so this needs a standard flush/rail-mount kit for a pitched roof — not an "adjustable tilt mount" bracket (those are a different product, meant to create tilt on a flat roof/ground, and would be the wrong thing to order here) |

Two things worth doing before ordering: (1) confirm the exact panel model's current price and availability directly, since panel pricing shifts often and this table used a dimension-matched product as a stand-in rather than a live quote; (2) size the DC-DC converter to the pump's actual nameplate current once a specific pump model is picked, rather than defaulting to whichever Orion SKU turned up first in search.

Incentives — realistically, none apply here

This is worth being direct about rather than hunting for a number that isn't really available:

- **Federal Residential Clean Energy Credit (Section 25D):** eliminated by the One Big Beautiful Bill Act (signed July 2025) for any system placed in service after December 31, 2025. A cash-purchased 2026 system gets **no federal credit** — this used to be the default 30% assumption for solar projects and it no longer applies.
- **~~Maryland Clean Energy Grant ($1,000, ≥1kW)~~ — correction: this program ended.** Earlier research here conflated it with the current MSAP program; on closer check, the $1,000 grant was from the separate Maryland Clean Energy Rebate program, which **concluded at the end of FY2025 (~June 2025)** and is not available in 2026. It also required a NABCEP-certified professional installer (DIY excluded) and that the property be the applicant's primary residence — so it wouldn't have fit this build even while it existed. Not worth redesigning around, and not available regardless.
- Separately: even setting the (nonexistent) incentive aside, reaching 1kW isn't a simple component swap. Each canopy fits exactly 1 panel at ~38.4 sq ft (6' x 6.408' slope) — a ~400-450W panel is close to the physical ceiling for that footprint; a 500-600W panel needed to clear 1kW with 2 panels typically runs ~90"+ on its long edge and doesn't fit the ~77" slope depth. Getting there would mean deepening both canopies to ~7.5', a real structural redesign (more framing, bigger footprint, cascading changes through [[Greenhouse Build Plan]]) — likely costing more than $1,000 on its own even if there were still a grant to chase.
- **Maryland Solar Access Program (MSAP, up to $7,500):** as of April 2026, ~99% of program funding is already reserved for approved projects, with the application window closing June 5, 2026 or whenever funds run out — functionally unavailable by the time this system would be built, and it's generally structured around professionally-installed grid-connected systems, not DIY off-grid.
- **Maryland RCES battery storage grant (30% of battery cost, capped at $5,000):** would be worth ~$370–465 on this battery if eligible, but MD storage incentive programs are generally built around licensed, permitted installations — worth a direct call to MEA if you want to explore it, but don't count on it for a DIY build.

**Bottom line: price this as a straight out-of-pocket equipment cost, no incentive offset.**

Payback — the usual framing doesn't quite fit

A standard solar payback calc (system cost ÷ avoided utility bill) isn't the right lens here, because there's no existing grid connection at the greenhouse being displaced. Per [[Solar Power - Concept]], running grid power out to the greenhouse was already ruled out as impractical for a load this size — solar was chosen as the *only* practical way to power it, not chosen to save money versus an existing electric bill.

Two more honest comparisons:
- **Versus a hypothetical grid run:** trenching and running conduit/service to a detached structure like this commonly runs **$1,500–$5,000+** depending on distance and terrain (rough range, highly site-dependent — not researched in depth here since it was already ruled out). At ~$2,800–$3,900 (excluding permit fees), this solar system is still cost-competitive with that alternative while also being fully independent of the utility.
- **Versus MD utility electricity rates**, if you tried to value the ~748 kWh/year this system produces at typical residential rates (~$0.17–$0.20/kWh): that's only **~$130–$150/year** of avoided cost, which would put a pure bill-offset payback north of 20 years. That's not a flattering number, but it's the wrong comparison for this project — the system isn't offsetting an existing bill, it's enabling a load that otherwise couldn't be powered at all.

Assumptions & Caveats

- Equipment prices are current-market estimates from web search (August 2026), not vendor quotes — get real quotes before ordering
- Battery pricing based on LiTime/Redodo-tier budget-to-midrange brands; premium brands (e.g. Battle Born) would cost meaningfully more
- Excludes sales tax, shipping (partially reflected in some listed prices, inconsistently), and any electrician review/labor
- Excludes the canopy's structural build cost (framing, footings) — see [[Greenhouse Cost Estimate]]
- Incentive eligibility should be confirmed directly with a tax professional or MEA before assuming any of the above applies

Sources:
- [How Much Does A 400 Watt Solar Panel Cost? [Updated: August 2026]](https://shineofsolar.com/how-much-does-a-400-watt-solar-panel-cost/)
- [LiTime 24V 200Ah Lithium 8D Battery](https://www.litime.com/products/24v-200ah-lifepo4-lithium-battery)
- [Federal 25D Battery Storage Tax Credit](https://homes.rewiringamerica.org/federal-incentives/25d-battery-storage-tax-credit)
- [Solar Battery Tax Credit 2026: What Changed After the OBBBA](https://www.solarpermitsolutions.com/blog/solar-battery-tax-credit-2026)
- [Solar Battery Storage Maryland 2026 — Costs, Brands & Incentives](https://marylandsolarguide.com/solar-battery-storage-maryland/)
- [MEGA 400 Solar Panel | RICH SOLAR](https://richsolar.com/products/mega-400-400-watt-24-volt-solar-panel)
- [LiTime 24V 230Ah Lithium Battery](https://www.litime.com/products/24v-230ah-lithium-battery)
- [2000W 24V Pure Sine Wave Inverter | Renogy US](https://www.renogy.com/products/2000w-24v-pure-sine-wave-inverter)
- [Victron Energy Orion DC-DC Converters](https://www.victronenergy.com/dc-dc-converters)

Next Steps

This closes out the core design → site → electrical → cost pipeline. From here it's real vendor quotes, then [[greenhouse-builder]] for the actual construction sequence of the combined greenhouse + canopy structure.
