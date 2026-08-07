"""Fill-in-missing-fields enrichment, on top of canonicalize.py's name
normalization.

canonicalize.py only normalizes spelling of player/set names against what
you've already scanned -- it can't tell you a card's number, team, or
parallel/insert type if the vision model couldn't read them. This module
does that, for card_number / team / parallel_insert_type only (LOOKUP_
FILLABLE_FIELDS below) -- NOT serial_number, which is excluded on purpose:
a print run size ("numbered to 150") is a checklist fact, but which specific
numbered copy you physically own ("45/150") is unique to that card and isn't
something any checklist lookup can know.

At "millions of cards, can't pre-populate anything" scale, this is built as
cache-aside, not a bulk import:

    1. Local first: check checklist_entries (the real source of truth,
       built entirely from your own scans and corrections -- see db.py).
    2. Web fallback: if nothing local and the card's *key* fields (canonical
       player, canonical set, confident year) are solid enough to search on,
       do a live web lookup via a second Claude API call using the same
       ANTHROPIC_API_KEY already configured for extraction.py, with
       Anthropic's server-side web_search tool steered at eBay's current/
       active listings specifically (listing titles reliably include player,
       year, set, card number, and parallel/insert type) -- not a scrape you
       have to maintain. Anything the web lookup finds gets written back into
       checklist_entries, so the *next* card with the same player+set+
       card_number hits the fast local path instead of searching again.
    3. Every unique (player, set, target-field) combo is only ever attempted
       once via the web (see web_lookup_log / has_attempted_web_lookup) --
       duplicate/near-duplicate cards in a big collection don't re-trigger
       paid searches for something already known to be missing.

Trust: a web-sourced value is NOT treated as equivalent to what the vision
model read off the card or what you've personally confirmed. It's written
with confidence held below the review threshold on purpose, so it always
surfaces once in the review UI for a quick human glance -- if you accept it
there, main.py's review-correction flow marks the checklist_entries row
`verified` and it's trusted from then on. This is deliberately conservative:
better to ask you once than to quietly let a bad web guess become "ground
truth" for the rest of the collection.

Caveat: WEB_SEARCH_TOOL_TYPE below reflects the web-search tool version
known at the time this was written -- verify it against the current
Anthropic API docs before relying on this in production; if the API rejects
it, enrichment fails soft (see enrich_fields) and scanning still works,
just without fill-in-missing-fields for that card.

This module also does eBay-sourced price estimation (estimate_price_from_
ebay / PRICE_LOOKUP), searching recently SOLD/completed eBay listings
rather than active ones -- price is fundamentally different from card_
number/team, so it's handled separately, not folded into enrich_fields:
    - It's condition-aware. A raw/played copy and a graded PSA 10 of the
      *same card* can differ 10-100x in sold price, so the query includes
      the vision-extracted `condition` field (see extraction.py) and the
      result should be treated as an estimate for a comparable-condition
      card, not a guaranteed value for your exact copy.
    - It's on-demand only, not automatic per scan and not gated by
      web_lookup_log's "attempt once ever" cache. Unlike a fixed checklist
      fact, a sold price goes stale -- caching it forever the way
      checklist_entries does would be actively wrong. Instead, it's only
      ever run when explicitly requested (see main.py's
      POST /scan/{job_id}/estimate-price), so cost is bounded by how often
      you actually ask, and each estimate is naturally "fresh" as of when
      you asked for it.
    - It's kept in a separate estimated_price/estimated_price_date/
      estimated_price_source set of columns, never touching or overwriting
      the manual price/date_priced fields you enter yourself.
"""
import os

import anthropic

import db

LOOKUP_FILLABLE_FIELDS = ["card_number", "team", "parallel_insert_type"]
KEY_CONFIDENCE_THRESHOLD = 0.85  # player/set/year must be at least this confident to trust as a lookup key
WEB_LOOKUP_CONFIDENCE = 0.6  # deliberately below the review threshold -- see module docstring "Trust"
LOCAL_LOOKUP_CONFIDENCE_VERIFIED = 0.9
LOCAL_LOOKUP_CONFIDENCE_UNVERIFIED = 0.7

ENRICH_MODEL = os.environ.get("CARD_ENRICH_MODEL", os.environ.get("CARD_SCAN_MODEL", "claude-sonnet-5"))
WEB_SEARCH_TOOL_TYPE = os.environ.get("CARD_WEB_SEARCH_TOOL_TYPE", "web_search_20250305")

RECORD_LOOKUP_TOOL = {
    "name": "record_checklist_lookup",
    "description": "Record what was found (or not found) about a specific trading card from web research.",
    "input_schema": {
        "type": "object",
        "properties": {
            "card_number": {"type": "string", "description": "e.g. '#57', or 'unknown' if not found"},
            "team": {"type": "string", "description": "e.g. 'Chicago Bulls', or 'unknown' if not found"},
            "parallel_insert_type": {
                "type": "string",
                "description": "e.g. 'Base', 'Refractor', or 'unknown' if not found",
            },
            "found_anything": {
                "type": "boolean",
                "description": "true if you found real information about this specific card, false if search turned up nothing usable",
            },
        },
        "required": ["card_number", "team", "parallel_insert_type", "found_anything"],
    },
}


class EnrichmentError(RuntimeError):
    pass


def _lookup_key(player_name: str, set_name: str, year: str | None, target_field: str) -> str:
    return f"{player_name.lower()}|{set_name.lower()}|{year or ''}|{target_field}"


def _web_lookup_checklist(
    player_name: str, set_name: str, year: str | None, known_card_number: str | None
) -> dict | None:
    """Two-call pattern: (1) let Claude research with the web_search tool
    and summarize in free text, citations and all; (2) force a second call
    to turn that summary into structured output. Keeps the structured
    result reliable without fighting the server tool for control of the
    first call's tool_choice. Returns a dict of found fields, or None on
    any API failure (never raises -- see enrich_fields, this must fail
    soft)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    client = anthropic.Anthropic(api_key=api_key)

    card_desc = f"{year or ''} {set_name} {player_name}".strip()
    if known_card_number:
        card_desc += f", card number {known_card_number}"

    try:
        research = client.messages.create(
            model=ENRICH_MODEL,
            max_tokens=1024,
            tools=[{"type": WEB_SEARCH_TOOL_TYPE, "name": "web_search", "max_uses": 3}],
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Research this specific trading card: {card_desc}. "
                        "Search eBay.com for CURRENT/active listings of this exact card "
                        "(site:ebay.com or ebay.com search results) -- listing titles for "
                        "this kind of card reliably include the card number, team, and "
                        "parallel/insert type. Cross-reference a few listings rather than "
                        "trusting just one, since individual sellers sometimes mistitle "
                        "listings. Find its card number, the player's team as printed on "
                        "this specific card/set, and its parallel/insert type (e.g. 'Base' "
                        "for a standard card, or the parallel name like 'Refractor'). "
                        "Summarize exactly what you found, and say clearly if you couldn't "
                        "confirm something specific to this card (don't guess)."
                    ),
                }
            ],
        )
        summary = "".join(block.text for block in research.content if block.type == "text")
        if not summary.strip():
            return None

        structured = client.messages.create(
            model=ENRICH_MODEL,
            max_tokens=512,
            tools=[RECORD_LOOKUP_TOOL],
            tool_choice={"type": "tool", "name": "record_checklist_lookup"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Research summary about the card '{card_desc}':\n\n{summary}\n\n"
                        "Record the findings. Use 'unknown' for any field the research "
                        "didn't actually confirm -- don't infer or guess a value."
                    ),
                }
            ],
        )
    except anthropic.APIError:
        return None

    tool_use_block = next((b for b in structured.content if b.type == "tool_use"), None)
    if tool_use_block is None or not tool_use_block.input.get("found_anything"):
        return None

    result = {
        k: v
        for k, v in tool_use_block.input.items()
        if k in ("card_number", "team", "parallel_insert_type") and v and v.lower() != "unknown"
    }
    return result or None


def enrich_fields(fields: dict) -> dict:
    """Fill in low-confidence card_number/team/parallel_insert_type from the
    local checklist_entries table, falling back to a capped live web lookup
    that grows that table for next time. Requires canonicalize.py to have
    already run (uses player/set canonical_id). Never raises -- enrichment
    is best-effort on top of a pipeline that already works without it."""
    try:
        return _enrich_fields_inner(fields)
    except Exception:
        return fields


def _enrich_fields_inner(fields: dict) -> dict:
    result = {name: dict(field) for name, field in fields.items()}

    player_field = result.get("player", {})
    set_field = result.get("set", {})
    year_field = result.get("year", {})

    player_id = player_field.get("canonical_id")
    set_id = set_field.get("canonical_id")
    player_name = player_field.get("canonical_value") or player_field.get("value")
    set_name = set_field.get("canonical_value") or set_field.get("value")
    year_value = year_field.get("value")

    key_ready = (
        player_id is not None
        and set_id is not None
        and player_field.get("confidence", 0) >= KEY_CONFIDENCE_THRESHOLD
        and set_field.get("confidence", 0) >= KEY_CONFIDENCE_THRESHOLD
        and year_field.get("confidence", 0) >= KEY_CONFIDENCE_THRESHOLD
        and year_value
        and year_value != "N/A"
    )
    if not key_ready:
        return result

    known_card_number = result.get("card_number", {}).get("value")
    if result.get("card_number", {}).get("confidence", 0) < KEY_CONFIDENCE_THRESHOLD:
        known_card_number = None

    for target in LOOKUP_FILLABLE_FIELDS:
        target_field = result.get(target)
        if target_field is None or target_field.get("confidence", 0) >= KEY_CONFIDENCE_THRESHOLD:
            continue  # already confident, nothing to fill in

        local_matches = db.find_checklist_entries(player_id, set_id, known_card_number)
        if len(local_matches) == 1:
            entry = local_matches[0]
            value = entry[target] if target != "card_number" else entry["card_number"]
            if value and value != "N/A":
                target_field["value"] = value
                target_field["source"] = "local_lookup"
                target_field["confidence"] = (
                    LOCAL_LOOKUP_CONFIDENCE_VERIFIED
                    if entry["verified"]
                    else LOCAL_LOOKUP_CONFIDENCE_UNVERIFIED
                )
                continue

        lookup_key = _lookup_key(player_name, set_name, year_value, target)
        if db.has_attempted_web_lookup(lookup_key):
            continue  # already tried this exact combo before -- don't re-spend on it

        found = _web_lookup_checklist(player_name, set_name, year_value, known_card_number)
        db.log_web_lookup(lookup_key, found is not None)
        if not found:
            continue

        resolved_card_number = found.get("card_number") or known_card_number
        if not resolved_card_number:
            continue  # can't write a checklist row without a card_number -- it's part of the unique key

        db.upsert_checklist_entry(
            player_id,
            set_id,
            resolved_card_number,
            team=found.get("team"),
            parallel_insert_type=found.get("parallel_insert_type"),
            source="web_lookup",
            verified=False,
        )

        if target in found:
            target_field["value"] = found[target]
            target_field["source"] = "web_lookup"
            target_field["confidence"] = WEB_LOOKUP_CONFIDENCE

    return result


PRICE_ESTIMATE_TOOL = {
    "name": "record_price_estimate",
    "description": "Record an estimated price for a specific trading card based on recently sold eBay listings.",
    "input_schema": {
        "type": "object",
        "properties": {
            "estimated_price": {
                "type": "number",
                "description": "A representative price in USD from recently sold comps, or 0 if no usable sold comps were found",
            },
            "comp_count": {
                "type": "integer",
                "description": "Roughly how many comparable sold listings the estimate is based on",
            },
            "found_anything": {
                "type": "boolean",
                "description": "true if usable sold comps were found for this card in a comparable condition, false otherwise",
            },
            "caveat": {
                "type": "string",
                "description": "Any important caveat, e.g. 'only 2 comps found', 'condition assumed since not specified', 'wide price range observed'",
            },
        },
        "required": ["estimated_price", "comp_count", "found_anything", "caveat"],
    },
}

PRICE_ESTIMATE_SOURCE = "ebay_sold_comps"


def estimate_price_from_ebay(
    player_name: str, set_name: str, year: str | None, card_number: str | None, condition: str | None
) -> dict | None:
    """On-demand only -- see module docstring. Two-call pattern like
    _web_lookup_checklist: research via web_search targeted at eBay sold/
    completed listings, then force structured output. Returns
    {"estimated_price": float, "caveat": str} (caveat includes the comp
    count) or None on failure / no usable comps. Never raises -- callers
    should treat None as "couldn't estimate," not an error."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    client = anthropic.Anthropic(api_key=api_key)

    card_desc = f"{year or ''} {set_name} {player_name}".strip()
    if card_number:
        card_desc += f", card number {card_number}"
    condition_desc = condition if condition and condition != "N/A" else "condition unspecified/unknown"

    try:
        research = client.messages.create(
            model=ENRICH_MODEL,
            max_tokens=1024,
            tools=[{"type": WEB_SEARCH_TOOL_TYPE, "name": "web_search", "max_uses": 3}],
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Research recent SOLD prices on eBay for this specific trading "
                        f"card: {card_desc}, condition: {condition_desc}. Search eBay.com "
                        "sold/completed listings specifically (not active/current "
                        "listings) -- eBay's sold-listings filter is "
                        "'LH_Sold=1&LH_Complete=1' in a search URL, or look for listings "
                        "explicitly marked sold. Only use comps that reasonably match the "
                        "condition given, or note clearly if you had to assume a condition "
                        "because none was specified. Report the range and a representative "
                        "typical price you observed, roughly how many comparable sold "
                        "listings you found, and any caveats (wide price spread, very few "
                        "comps, condition mismatch). If you can't find usable sold comps "
                        "for this specific card, say so plainly rather than estimating from "
                        "a similar-but-different card."
                    ),
                }
            ],
        )
        summary = "".join(block.text for block in research.content if block.type == "text")
        if not summary.strip():
            return None

        structured = client.messages.create(
            model=ENRICH_MODEL,
            max_tokens=512,
            tools=[PRICE_ESTIMATE_TOOL],
            tool_choice={"type": "tool", "name": "record_price_estimate"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Research summary about recent eBay sold prices for "
                        f"'{card_desc}' ({condition_desc}):\n\n{summary}\n\n"
                        "Record the findings. Set found_anything to false and "
                        "estimated_price to 0 if no usable sold comps were actually "
                        "found -- don't invent a number."
                    ),
                }
            ],
        )
    except anthropic.APIError:
        return None

    tool_use_block = next((b for b in structured.content if b.type == "tool_use"), None)
    if tool_use_block is None:
        return None
    result = tool_use_block.input
    if not result.get("found_anything") or not result.get("estimated_price"):
        return None

    caveat = result.get("caveat") or ""
    comp_count = result.get("comp_count")
    if comp_count is not None:
        caveat = f"{caveat} (~{comp_count} comps)".strip()

    return {"estimated_price": float(result["estimated_price"]), "caveat": caveat or None}


def learn_from_correction(field: str, corrected_value: str, current_fields: dict) -> None:
    """Called after a human corrects card_number/team/parallel_insert_type
    in the review UI. Writes a *verified* checklist_entries row so future
    scans of the same player+set+card_number trust the local table
    immediately instead of needing another web lookup."""
    if field not in LOOKUP_FILLABLE_FIELDS:
        return
    player_id = current_fields.get("player", {}).get("canonical_id")
    set_id = current_fields.get("set", {}).get("canonical_id")
    if player_id is None or set_id is None:
        return  # player/set weren't canonicalized -- nothing to key the checklist row on

    card_number = (
        corrected_value if field == "card_number" else current_fields.get("card_number", {}).get("value")
    )
    if not card_number or card_number == "N/A":
        return

    def _clean(value: str | None) -> str | None:
        return value if value and value != "N/A" else None

    team = corrected_value if field == "team" else _clean(current_fields.get("team", {}).get("value"))
    parallel = (
        corrected_value
        if field == "parallel_insert_type"
        else _clean(current_fields.get("parallel_insert_type", {}).get("value"))
    )
    db.upsert_checklist_entry(
        player_id, set_id, card_number, team=team, parallel_insert_type=parallel,
        source="human_review", verified=True,
    )
