#solar

[[Solar Power]] | [[Solar Power - System Design]]

These are current market estimates from web research (August 2026), not quotes — get real vendor quotes before ordering, and confirm any incentive eligibility with a tax professional or Maryland Energy Administration before counting on it.

Itemized Cost Estimate

| Item | Spec | Est. cost |
|---|---|---|
| Solar panels | 2x ~400W | $700–$950 |
| MPPT charge controller | 50A, 12V/24V auto | $130–$170 |
| Battery bank | 24V 200Ah LiFePO4 (~5.1kWh) | $1,239–$1,600 |
| Inverter | ~800W continuous, pure sine, 24V input | $150–$220 |
| DC-DC converter | 24V→12V, for the pump | $30–$60 |
| Wiring, fusing, disconnects, misc. electrical | PV disconnect, battery disconnect, breakers, cable, lugs | $300–$450 |
| Roof-mount rail/clamp hardware | 2-panel kit, wood-rafter mounting | $150–$250 |
| **Equipment subtotal** | | **~$2,700–$3,700** |

**Not included here** — the canopy's structural build (posts, footings, roof decking, concrete piers) belongs to the greenhouse build budget, not the solar equipment budget. Track that in [[Greenhouse Cost Estimate]] via greenhouse-price-optimizer rather than double-counting it here; this table is the electrical/solar equipment only.

Battery capacity tradeoff (the biggest line item by far): [[Solar Power - System Design]] flagged 230–250Ah as a more comfortable margin than 200Ah. LiFePO4 pricing scales roughly linearly with capacity (~$6/Ah at 24V based on the $1,239 200Ah price point), so:
- **230Ah: ~$1,420** (+~$180)
- **250Ah: ~$1,550** (+~$310)

The opposite lever is also worth knowing: dropping to **1 day of autonomy instead of 2** roughly halves the battery requirement (~100Ah, ~$650–700) — a real ~$550–600 savings if you're comfortable with less cloudy-day buffer. Since the battery is easily the largest single cost, this is the one component where the spec has real room to move either direction depending on how much autonomy actually matters to you.

Incentives — realistically, none apply here

This is worth being direct about rather than hunting for a number that isn't really available:

- **Federal Residential Clean Energy Credit (Section 25D):** eliminated by the One Big Beautiful Bill Act (signed July 2025) for any system placed in service after December 31, 2025. A cash-purchased 2026 system gets **no federal credit** — this used to be the default 30% assumption for solar projects and it no longer applies.
- **Maryland Clean Energy Grant ($1,000):** requires at least 1kW of installed solar. This system is 800W — under the threshold, and [[Solar Power - System Design]] already established that a 3rd panel doesn't physically fit the canopy roof, so crossing 1kW isn't a realistic option here without redesigning the array.
- **Maryland Solar Access Program (MSAP, up to $7,500):** as of April 2026, ~99% of program funding is already reserved for approved projects, with the application window closing June 5, 2026 or whenever funds run out — functionally unavailable by the time this system would be built, and it's generally structured around professionally-installed grid-connected systems, not DIY off-grid.
- **Maryland RCES battery storage grant (30% of battery cost, capped at $5,000):** would be worth ~$370–465 on this battery if eligible, but MD storage incentive programs are generally built around licensed, permitted installations — worth a direct call to MEA if you want to explore it, but don't count on it for a DIY build.

**Bottom line: price this as a straight out-of-pocket equipment cost, no incentive offset.**

Payback — the usual framing doesn't quite fit

A standard solar payback calc (system cost ÷ avoided utility bill) isn't the right lens here, because there's no existing grid connection at the greenhouse being displaced. Per [[Solar Power - Concept]], running grid power out to the greenhouse was already ruled out as impractical for a load this size — solar was chosen as the *only* practical way to power it, not chosen to save money versus an existing electric bill.

Two more honest comparisons:
- **Versus a hypothetical grid run:** trenching and running conduit/service to a detached structure like this commonly runs **$1,500–$5,000+** depending on distance and terrain (rough range, highly site-dependent — not researched in depth here since it was already ruled out). At ~$2,700–$3,700, this solar system is cost-competitive with that alternative while also being fully independent of the utility.
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

Next Steps

This closes out the core design → site → electrical → cost pipeline. From here it's real vendor quotes, then [[greenhouse-builder]] for the actual construction sequence of the combined greenhouse + canopy structure.
