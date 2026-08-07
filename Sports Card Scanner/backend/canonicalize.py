"""Phase 2 canonicalization & enrichment (sports_card_scanning_recommendations.md §2).

No external reference API (TCG Price Lookup, TCGAPI.net, PSA API) is wired in
here -- none were reachable with credentials at build time. The recommendations
doc explicitly names a self-assembled checklist as the fallback for sports-card
coverage gaps, so that's what this implements:

- players/sets reference tables (see db.py), grown two ways:
    1. auto-learned from extractions the vision model itself was already
       confident about (>= LEARN_CONFIDENCE_THRESHOLD), so the table fills in
       as real cards get scanned, with no manual data entry required
    2. corrected via the existing human-review flow -- a review correction
       both fixes that card's field and teaches the reference table the
       right canonical spelling, recording the original (wrong) extracted
       value as a known alias so future misreads of the same kind normalize
       to the same canonical value automatically
- RapidFuzz fuzzy matching of new extractions against that table

If a real external reference source becomes available later, seed
players/sets from it via db.upsert_player / db.upsert_set instead of (or in
addition to) the auto-learning here -- the matching logic itself doesn't
need to change.
"""
import json

from rapidfuzz import fuzz, process

import db

MATCH_ACCEPT_THRESHOLD = 90  # fuzzy score (0-100) at/above which a match is trusted
LEARN_CONFIDENCE_THRESHOLD = 0.85  # only auto-add unmatched values the model itself trusted


def _player_candidates(rows) -> dict:
    candidates = {}
    for row in rows:
        candidates.setdefault(row["canonical_name"], row)
        for alias in json.loads(row["aliases_json"] or "[]"):
            candidates.setdefault(alias, row)
    return candidates


def _set_candidates(rows) -> dict:
    candidates = {}
    for row in rows:
        candidates.setdefault(f"{row['name']} {row['year'] or ''}".strip(), row)
        for alias in json.loads(row["aliases_json"] or "[]"):
            candidates.setdefault(f"{alias} {row['year'] or ''}".strip(), row)
    return candidates


def match_player(raw_value: str | None) -> tuple[str, int, float] | None:
    """Fuzzy-match raw_value against known players. Returns
    (canonical_name, player_id, score) or None if no players are known yet,
    or nothing scored above MATCH_ACCEPT_THRESHOLD."""
    if not raw_value or raw_value == "N/A":
        return None
    candidates = _player_candidates(db.list_players())
    if not candidates:
        return None
    result = process.extractOne(raw_value, candidates.keys(), scorer=fuzz.WRatio)
    if result is None or result[1] < MATCH_ACCEPT_THRESHOLD:
        return None
    label, score, _ = result
    row = candidates[label]
    return row["canonical_name"], row["id"], score


def match_set(raw_set_value: str | None, raw_year_value: str | None) -> tuple[str, int, float] | None:
    """Fuzzy-match raw_set_value (+ year, if known) against known sets.
    Returns (canonical_name, set_id, score) or None."""
    if not raw_set_value or raw_set_value == "N/A":
        return None
    candidates = _set_candidates(db.list_sets())
    if not candidates:
        return None
    query = f"{raw_set_value} {raw_year_value or ''}".strip()
    result = process.extractOne(query, candidates.keys(), scorer=fuzz.WRatio)
    if result is None or result[1] < MATCH_ACCEPT_THRESHOLD:
        return None
    label, score, _ = result
    row = candidates[label]
    return row["name"], row["id"], score


def canonicalize_fields(fields: dict) -> dict:
    """Given the raw extracted fields dict (player/team/year/set/... ->
    {"value", "confidence"}), return a new dict with canonical_value/
    canonical_id/canonical_score added to the player and set entries where a
    confident reference match exists. Does not touch the model's own
    confidence -- canonicalization is reported alongside it, not blended in.

    Also auto-learns: a field whose value didn't match anything, but which
    the model itself extracted with high confidence, gets added to the
    reference table as a new canonical entry (self-canonicalizing at score
    100, since it becomes the canonical value)."""
    result = {name: dict(field) for name, field in fields.items()}

    player_field = result.get("player")
    if player_field:
        value = player_field.get("value")
        match = match_player(value)
        if match:
            canonical_name, player_id, score = match
            player_field["canonical_value"] = canonical_name
            player_field["canonical_id"] = player_id
            player_field["canonical_score"] = score
        elif value and value != "N/A" and player_field.get("confidence", 0) >= LEARN_CONFIDENCE_THRESHOLD:
            row = db.upsert_player(value)
            player_field["canonical_value"] = row["canonical_name"]
            player_field["canonical_id"] = row["id"]
            player_field["canonical_score"] = 100.0

    set_field = result.get("set")
    if set_field:
        value = set_field.get("value")
        year_value = result.get("year", {}).get("value")
        match = match_set(value, year_value)
        if match:
            canonical_name, set_id, score = match
            set_field["canonical_value"] = canonical_name
            set_field["canonical_id"] = set_id
            set_field["canonical_score"] = score
        elif value and value != "N/A" and set_field.get("confidence", 0) >= LEARN_CONFIDENCE_THRESHOLD:
            row = db.upsert_set(value, year_value)
            set_field["canonical_value"] = row["name"]
            set_field["canonical_id"] = row["id"]
            set_field["canonical_score"] = 100.0

    return result


def learn_from_correction(
    field: str, corrected_value: str, old_value: str | None, year_value: str | None = None
) -> tuple[str, int] | None:
    """Called after a human review correction is applied. Treats the
    correction as ground truth: adds/updates the canonical entry for the
    corrected value, and -- if the original extracted value looks like a
    plausible near-miss rather than just missing/N/A -- records it as a
    known alias, so future misreads of the same kind normalize
    automatically. Returns (canonical_value, canonical_id) for player/set
    corrections so the caller can patch the card's own record, else None."""
    if field == "player" and corrected_value and corrected_value != "N/A":
        row = db.upsert_player(corrected_value)
        if old_value and old_value not in (corrected_value, "N/A"):
            db.add_player_alias(row["id"], old_value)
        return row["canonical_name"], row["id"]
    if field == "set" and corrected_value and corrected_value != "N/A":
        row = db.upsert_set(corrected_value, year_value)
        if old_value and old_value not in (corrected_value, "N/A"):
            db.add_set_alias(row["id"], old_value)
        return row["name"], row["id"]
    return None
