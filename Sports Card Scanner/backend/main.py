import json
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # picks up Sports Card Scanner/.env before extraction.py reads env vars

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import db
import extraction
from schemas import CardFields, FieldValue, ReviewSubmission, ScanResult, UploadResponse

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
    return _row_to_result(db.get_card(job_id))


@app.get("/images/{filename}")
def get_image(filename: str) -> FileResponse:
    path = IMAGES_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="image not found")
    return FileResponse(path)


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
