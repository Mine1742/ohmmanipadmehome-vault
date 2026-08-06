#personal #jobsearch

[[Food Access Hub]] | [[Job Search Hub]] | build plan for the [[Goals|Build hands-on ArcGIS/GIS experience]] goal, 2026-08-05

Turn the research already done in [[Food Donation Programs]] into a real, published ArcGIS Online web map — genuine GIS experience, not a tutorial exercise, and a direct analog to the "Hunger Heat Map" / "Get Help Map" tools the Capital Area Food Bank posting calls out by name.

## 1. Set up access
- Create a free public account at [arcgis.com](https://www.arcgis.com) — no employer/org sponsor needed.
- Skim 1-2 of Esri's "Learn ArcGIS" lessons on hosted feature layers and web map styling ([learn.arcgis.com](https://learn.arcgis.com)) before touching real data, just enough to know where the buttons are.

## 2. Prep the source data
- Turn [[Food Donation Programs]] into a flat CSV with columns: `name, category, address, city, state, zip, hours, contact, notes`.
- `category` values should match the note's existing section headers so the map can symbolize by type: Grow-and-Donate Program, Local Pantry, Gleaning/Food Rescue, Community Garden, Coordination/Policy Body.
- Most entries already have an address; a few (M-NCPPC plots, PG County DSS pantries) will need a specific address looked up rather than just "6 locations" — geocoding needs a real street address per point.

## 3. Build the layer
- Import the CSV into ArcGIS Online as a hosted feature layer — it geocodes the addresses automatically into point locations.
- Symbolize by `category` (distinct color/icon per type) so grow-and-donate sites read differently from pantries and gleaning orgs at a glance.
- Add pop-ups showing hours/contact/notes per point.

## 4. Optional: show the gap, not just the list
- Layer in USDA's [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas) data (public, free download) for Prince George's County to shade low-access census tracts underneath the point layer — turns "here's a list of pantries" into "here's where the pantries are relative to where the need is," which is the actual analytical move a BI/GIS role is looking for.

## 5. Package it as a StoryMap
- Short intro on food access work in Camp Springs / Prince George's County (reuse framing from [[Food Access Hub]]).
- Embed the web map.
- One section per category with a couple of sentences of context (pulled from the sourcing already done in [[Food Donation Programs]]).

## 6. Publish and close the loop
- Publish the ArcGIS Online item as shareable (public or "anyone with link," your call on privacy).
- Come back and report the link — at that point `Resume - Master.md`, the tailored CAFB resume, and the cover letter all get a real, specific GIS line, replacing the "haven't worked directly in ArcGIS" framing with something you actually built.

Rough effort: a weekend or a few evening sessions — this is a single project, not a multi-week study plan like [[DP-600 Study Guide]].
