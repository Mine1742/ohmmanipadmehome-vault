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


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def create_card(job_id: str, image_path_front: str, image_path_back: str | None) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO cards (job_id, status, image_path_front, image_path_back) "
            "VALUES (?, 'processing', ?, ?)",
            (job_id, image_path_front, image_path_back),
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
