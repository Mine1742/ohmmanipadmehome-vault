import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "cards.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS cards (
    job_id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'processing',
    extraction_method TEXT,
    model_used TEXT,
    raw_llm_response_json TEXT,
    fields_json TEXT,
    needs_review INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    image_path_front TEXT NOT NULL,
    image_path_back TEXT,
    price REAL,
    date_priced TEXT,
    estimated_price REAL,
    estimated_price_date TEXT,
    estimated_price_source TEXT,
    estimated_price_caveat TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL REFERENCES cards(job_id),
    corrected_field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_name TEXT NOT NULL UNIQUE,
    aliases_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    year TEXT,
    manufacturer TEXT,
    aliases_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(name, year)
);

CREATE TABLE IF NOT EXISTS checklist_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(id),
    set_id INTEGER NOT NULL REFERENCES sets(id),
    card_number TEXT NOT NULL,
    team TEXT,
    parallel_insert_type TEXT,
    source TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(player_id, set_id, card_number)
);

CREATE TABLE IF NOT EXISTS web_lookup_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lookup_key TEXT NOT NULL,
    found INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, coltype: str) -> None:
    """Idempotent ALTER TABLE, so an already-existing cards.db from before a
    schema change (like adding price/date_priced) picks up the new column
    without needing to be deleted/recreated. No-op on a fresh DB, since
    SCHEMA's CREATE TABLE already includes the column."""
    existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        _ensure_column(conn, "cards", "price", "REAL")
        _ensure_column(conn, "cards", "date_priced", "TEXT")
        _ensure_column(conn, "cards", "estimated_price", "REAL")
        _ensure_column(conn, "cards", "estimated_price_date", "TEXT")
        _ensure_column(conn, "cards", "estimated_price_source", "TEXT")
        _ensure_column(conn, "cards", "estimated_price_caveat", "TEXT")


def create_card(job_id: str, image_path_front: str, image_path_back: str | None) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO cards (job_id, status, image_path_front, image_path_back) "
            "VALUES (?, 'processing', ?, ?)",
            (job_id, image_path_front, image_path_back),
        )


def set_price(job_id: str, price: float, date_priced: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE cards SET price = ?, date_priced = ? WHERE job_id = ?",
            (price, date_priced, job_id),
        )


def set_estimated_price(
    job_id: str, price: float, date: str, source: str, caveat: str | None = None
) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE cards SET estimated_price = ?, estimated_price_date = ?, "
            "estimated_price_source = ?, estimated_price_caveat = ? WHERE job_id = ?",
            (price, date, source, caveat, job_id),
        )


def save_extraction_result(
    job_id: str,
    extraction_method: str,
    model_used: str,
    raw_response: dict,
    fields: dict,
    needs_review: bool,
) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE cards SET status = 'complete', extraction_method = ?, model_used = ?, "
            "raw_llm_response_json = ?, fields_json = ?, needs_review = ? WHERE job_id = ?",
            (
                extraction_method,
                model_used,
                json.dumps(raw_response),
                json.dumps(fields),
                int(needs_review),
                job_id,
            ),
        )


def save_extraction_error(job_id: str, error: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE cards SET status = 'error', error = ? WHERE job_id = ?",
            (error, job_id),
        )


def get_card(job_id: str) -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM cards WHERE job_id = ?", (job_id,)).fetchone()


def list_cards(needs_review_only: bool = False) -> list[sqlite3.Row]:
    with get_conn() as conn:
        if needs_review_only:
            return conn.execute(
                "SELECT * FROM cards WHERE needs_review = 1 AND status = 'complete' "
                "ORDER BY created_at DESC"
            ).fetchall()
        return conn.execute("SELECT * FROM cards ORDER BY created_at DESC").fetchall()


def set_field_canonical(
    job_id: str, field: str, canonical_value: str, canonical_id: int, canonical_score: float
) -> None:
    """Patch canonical_value/canonical_id/canonical_score onto an already-saved
    field, without touching its value/confidence. Used after a review
    correction teaches the reference table a new canonical spelling, so the
    corrected card reflects that it's now a confident canonical match too."""
    with get_conn() as conn:
        row = conn.execute("SELECT fields_json FROM cards WHERE job_id = ?", (job_id,)).fetchone()
        if row is None or not row["fields_json"]:
            return
        fields = json.loads(row["fields_json"])
        if field not in fields:
            return
        fields[field]["canonical_value"] = canonical_value
        fields[field]["canonical_id"] = canonical_id
        fields[field]["canonical_score"] = canonical_score
        conn.execute(
            "UPDATE cards SET fields_json = ? WHERE job_id = ?",
            (json.dumps(fields), job_id),
        )


def list_players() -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM players").fetchall()


def list_sets() -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM sets").fetchall()


def upsert_player(canonical_name: str) -> sqlite3.Row:
    """Return the player row with this exact canonical_name, creating it
    first if it doesn't exist yet."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM players WHERE canonical_name = ?", (canonical_name,)
        ).fetchone()
        if row is not None:
            return row
        conn.execute("INSERT INTO players (canonical_name) VALUES (?)", (canonical_name,))
        return conn.execute(
            "SELECT * FROM players WHERE canonical_name = ?", (canonical_name,)
        ).fetchone()


def add_player_alias(player_id: int, alias: str) -> None:
    with get_conn() as conn:
        row = conn.execute("SELECT aliases_json FROM players WHERE id = ?", (player_id,)).fetchone()
        if row is None:
            raise ValueError(f"no player with id {player_id}")
        aliases = json.loads(row["aliases_json"] or "[]")
        if alias not in aliases:
            aliases.append(alias)
            conn.execute(
                "UPDATE players SET aliases_json = ? WHERE id = ?", (json.dumps(aliases), player_id)
            )


def upsert_set(name: str, year: str | None, manufacturer: str | None = None) -> sqlite3.Row:
    """Return the set row matching this exact (name, year), creating it
    first if it doesn't exist yet."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sets WHERE name = ? AND year IS ?", (name, year)
        ).fetchone()
        if row is not None:
            return row
        conn.execute(
            "INSERT INTO sets (name, year, manufacturer) VALUES (?, ?, ?)", (name, year, manufacturer)
        )
        return conn.execute(
            "SELECT * FROM sets WHERE name = ? AND year IS ?", (name, year)
        ).fetchone()


def add_set_alias(set_id: int, alias: str) -> None:
    with get_conn() as conn:
        row = conn.execute("SELECT aliases_json FROM sets WHERE id = ?", (set_id,)).fetchone()
        if row is None:
            raise ValueError(f"no set with id {set_id}")
        aliases = json.loads(row["aliases_json"] or "[]")
        if alias not in aliases:
            aliases.append(alias)
            conn.execute(
                "UPDATE sets SET aliases_json = ? WHERE id = ?", (json.dumps(aliases), set_id)
            )


def find_checklist_entries(
    player_id: int, set_id: int, card_number: str | None = None
) -> list[sqlite3.Row]:
    """Look up known checklist rows for this player+set (the real source of
    truth for enrichment), optionally narrowed to an exact card_number. With
    no card_number this can return more than one row (e.g. a base card and
    an insert for the same player in the same set) -- callers should only
    auto-fill from the result when it's unambiguous (exactly one row)."""
    with get_conn() as conn:
        if card_number:
            return conn.execute(
                "SELECT * FROM checklist_entries WHERE player_id = ? AND set_id = ? AND card_number = ?",
                (player_id, set_id, card_number),
            ).fetchall()
        return conn.execute(
            "SELECT * FROM checklist_entries WHERE player_id = ? AND set_id = ?",
            (player_id, set_id),
        ).fetchall()


def upsert_checklist_entry(
    player_id: int,
    set_id: int,
    card_number: str,
    team: str | None = None,
    parallel_insert_type: str | None = None,
    source: str = "web_lookup",
    verified: bool = False,
) -> sqlite3.Row:
    """Add or update the checklist row for this exact (player, set,
    card_number). A verified=True write (from a human review correction)
    always wins over an existing unverified one; an unverified write never
    overwrites an already-verified row."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT * FROM checklist_entries WHERE player_id = ? AND set_id = ? AND card_number = ?",
            (player_id, set_id, card_number),
        ).fetchone()
        if existing is not None and existing["verified"] and not verified:
            return existing
        if existing is not None:
            conn.execute(
                "UPDATE checklist_entries SET team = COALESCE(?, team), "
                "parallel_insert_type = COALESCE(?, parallel_insert_type), "
                "source = ?, verified = ? WHERE id = ?",
                (team, parallel_insert_type, source, int(verified), existing["id"]),
            )
            return conn.execute(
                "SELECT * FROM checklist_entries WHERE id = ?", (existing["id"],)
            ).fetchone()
        conn.execute(
            "INSERT INTO checklist_entries "
            "(player_id, set_id, card_number, team, parallel_insert_type, source, verified) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (player_id, set_id, card_number, team, parallel_insert_type, source, int(verified)),
        )
        return conn.execute(
            "SELECT * FROM checklist_entries WHERE player_id = ? AND set_id = ? AND card_number = ?",
            (player_id, set_id, card_number),
        ).fetchone()


def has_attempted_web_lookup(lookup_key: str) -> bool:
    """True if a web lookup for this exact key was already attempted
    (found or not) -- caps repeat web-search spend on the same missing
    combo across duplicate/near-duplicate cards."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM web_lookup_log WHERE lookup_key = ? LIMIT 1", (lookup_key,)
        ).fetchone()
        return row is not None


def log_web_lookup(lookup_key: str, found: bool) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO web_lookup_log (lookup_key, found) VALUES (?, ?)",
            (lookup_key, int(found)),
        )


def apply_review_correction(job_id: str, field: str, old_value: str | None, new_value: str, reviewer: str) -> None:
    with get_conn() as conn:
        row = conn.execute("SELECT fields_json FROM cards WHERE job_id = ?", (job_id,)).fetchone()
        if row is None:
            raise ValueError(f"no card with job_id {job_id}")
        fields = json.loads(row["fields_json"]) if row["fields_json"] else {}
        if field not in fields:
            raise ValueError(f"unknown field {field}")
        fields[field]["value"] = new_value
        fields[field]["confidence"] = 1.0

        still_needs_review = any(f.get("confidence", 0) < 0.85 for f in fields.values())

        conn.execute(
            "UPDATE cards SET fields_json = ?, needs_review = ? WHERE job_id = ?",
            (json.dumps(fields), int(still_needs_review), job_id),
        )
        conn.execute(
            "INSERT INTO audit (job_id, corrected_field, old_value, new_value, reviewer) "
            "VALUES (?, ?, ?, ?, ?)",
            (job_id, field, old_value, new_value, reviewer),
        )
