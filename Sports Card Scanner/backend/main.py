import datetime
import json
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # picks up Sports Card Scanner/.env before extraction.py reads env vars

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import canonicalize
import db
import enrich
import extraction
from schemas import CardFields, FieldValue, PriceSubmission, ReviewSubmission, ScanResult, UploadResponse

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
IMAGES_DIR = DATA_DIR / "images"
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

CONFIDENCE_REVIEW_THRESHOLD = 0.85

app = FastAPI(title="Sports Card Scanner")


@app.on_event("startup")
def on_startup() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    db.init_db()


def _save_upload(job_id: str, side: str, upload: UploadFile) -> str:
    suffix = Path(upload.filename or "").suffix or ".jpg"
    dest = IMAGES_DIR / f"{job_id}_{side}{suffix}"
    dest.write_bytes(upload.file.read())
    return str(dest)


def _run_extraction(job_id: str, image_path_front: str, image_path_back: str | None) -> None:
    try:
        fields, raw_response = extraction.extract_card_fields(image_path_front, image_path_back)
    except extraction.ExtractionError as exc:
        db.save_extraction_error(job_id, str(exc))
        return

    fields = canonicalize.canonicalize_fields(fields)
    fields = enrich.enrich_fields(fields)

    needs_review = any(
        f.get("confidence", 0) < CONFIDENCE_REVIEW_THRESHOLD for f in fields.values()
    )
    db.save_extraction_result(
        job_id=job_id,
        extraction_method="llm_primary",
        model_used=extraction.DEFAULT_MODEL,
        raw_response=raw_response,
        fields=fields,
        needs_review=needs_review,
    )


@app.post("/scan/upload", response_model=UploadResponse)
def upload_scan(
    background_tasks: BackgroundTasks,
    front: UploadFile = File(...),
    back: UploadFile | None = File(None),
) -> UploadResponse:
    job_id = str(uuid.uuid4())
    front_path = _save_upload(job_id, "front", front)
    back_path = _save_upload(job_id, "back", back) if back is not None else None

    db.create_card(job_id, front_path, back_path)
    background_tasks.add_task(_run_extraction, job_id, front_path, back_path)

    return UploadResponse(status="received", job_id=job_id)


def _row_to_result(row) -> ScanResult:
    fields = None
    if row["fields_json"]:
        raw_fields = json.loads(row["fields_json"])
        fields = CardFields(**{k: FieldValue(**v) for k, v in raw_fields.items()})
    return ScanResult(
        job_id=row["job_id"],
        status=row["status"],
        extraction_method=row["extraction_method"],
        model_used=row["model_used"],
        fields=fields,
        needs_review=bool(row["needs_review"]),
        error=row["error"],
        price=row["price"],
        date_priced=row["date_priced"],
        estimated_price=row["estimated_price"],
        estimated_price_date=row["estimated_price_date"],
        estimated_price_source=row["estimated_price_source"],
        estimated_price_caveat=row["estimated_price_caveat"],
    )


@app.get("/scan/result/{job_id}", response_model=ScanResult)
def get_scan_result(job_id: str) -> ScanResult:
    row = db.get_card(job_id)
    if row is None:
        raise HTTPException(status_code=404, detail="job not found")
    return _row_to_result(row)


@app.get("/scan/list")
def list_scans(needs_review: bool = False) -> list[ScanResult]:
    return [_row_to_result(row) for row in db.list_cards(needs_review_only=needs_review)]


@app.post("/scan/{job_id}/review")
def submit_review(job_id: str, submission: ReviewSubmission) -> ScanResult:
    row = db.get_card(job_id)
    if row is None:
        raise HTTPException(status_code=404, detail="job not found")
    old_fields = json.loads(row["fields_json"]) if row["fields_json"] else {}
    old_value = old_fields.get(submission.field, {}).get("value")
    try:
        db.apply_review_correction(
            job_id, submission.field, old_value, submission.new_value, submission.reviewer
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    year_value = old_fields.get("year", {}).get("value")
    learned = canonicalize.learn_from_correction(
        submission.field, submission.new_value, old_value, year_value
    )
    if learned:
        canonical_value, canonical_id = learned
        db.set_field_canonical(job_id, submission.field, canonical_value, canonical_id, 100.0)

    enrich.learn_from_correction(submission.field, submission.new_value, old_fields)

    return _row_to_result(db.get_card(job_id))


@app.post("/scan/{job_id}/price")
def submit_price(job_id: str, submission: PriceSubmission) -> ScanResult:
    row = db.get_card(job_id)
    if row is None:
        raise HTTPException(status_code=404, detail="job not found")
    date_priced = submission.date_priced or datetime.date.today().isoformat()
    db.set_price(job_id, submission.price, date_priced)
    return _row_to_result(db.get_card(job_id))


@app.post("/scan/{job_id}/estimate-price")
def estimate_price(job_id: str) -> ScanResult:
    """On-demand only -- see enrich.py's module docstring for why this isn't
    run automatically per scan. Costs one eBay-targeted web-search call each
    time it's invoked."""
    row = db.get_card(job_id)
    if row is None:
        raise HTTPException(status_code=404, detail="job not found")
    fields = json.loads(row["fields_json"]) if row["fields_json"] else {}

    player_field = fields.get("player", {})
    set_field = fields.get("set", {})
    year_field = fields.get("year", {})
    player_name = player_field.get("canonical_value") or player_field.get("value")
    set_name = set_field.get("canonical_value") or set_field.get("value")
    year_value = year_field.get("value")

    key_ready = (
        player_name
        and set_name
        and year_value
        and year_value != "N/A"
        and player_field.get("confidence", 0) >= enrich.KEY_CONFIDENCE_THRESHOLD
        and set_field.get("confidence", 0) >= enrich.KEY_CONFIDENCE_THRESHOLD
        and year_field.get("confidence", 0) >= enrich.KEY_CONFIDENCE_THRESHOLD
    )
    if not key_ready:
        raise HTTPException(
            status_code=400,
            detail=(
                "Player, set, and year all need to be confidently known before a "
                "price can be estimated -- review/correct them first."
            ),
        )

    card_number = fields.get("card_number", {}).get("value")
    condition = fields.get("condition", {}).get("value")

    result = enrich.estimate_price_from_ebay(player_name, set_name, year_value, card_number, condition)
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="Couldn't find a usable price estimate (no sold comps found, or the lookup failed).",
        )

    today = datetime.date.today().isoformat()
    db.set_estimated_price(
        job_id, result["estimated_price"], today, enrich.PRICE_ESTIMATE_SOURCE, result.get("caveat")
    )
    return _row_to_result(db.get_card(job_id))


@app.get("/images/{filename}")
def get_image(filename: str) -> FileResponse:
    path = IMAGES_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="image not found")
    return FileResponse(path)


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
