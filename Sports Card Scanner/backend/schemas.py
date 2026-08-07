from typing import Optional

from pydantic import BaseModel, Field


class FieldValue(BaseModel):
    value: Optional[str] = None
    confidence: float = 0.0
    canonical_value: Optional[str] = None
    canonical_id: Optional[int] = None
    canonical_score: Optional[float] = None
    # None = read directly off the card by the vision model. 'local_lookup' /
    # 'web_lookup' = filled in by enrich.py from checklist_entries or a live
    # web search. 'human_review' = confirmed/corrected by a person.
    source: Optional[str] = None


class CardFields(BaseModel):
    player: FieldValue
    team: FieldValue
    year: FieldValue
    set: FieldValue
    card_number: FieldValue
    serial_number: FieldValue
    parallel_insert_type: FieldValue
    notable_flags: FieldValue


class UploadResponse(BaseModel):
    status: str
    job_id: str


class ScanResult(BaseModel):
    job_id: str
    status: str
    extraction_method: Optional[str] = None
    model_used: Optional[str] = None
    fields: Optional[CardFields] = None
    needs_review: bool = False
    error: Optional[str] = None
    price: Optional[float] = None
    date_priced: Optional[str] = None


class ReviewSubmission(BaseModel):
    field: str
    new_value: str
    reviewer: str = "owner"


class PriceSubmission(BaseModel):
    price: float = Field(ge=0)
    # ISO date string (YYYY-MM-DD), e.g. when you looked the price up. Defaults
    # to today (server-side) if omitted -- see main.py's /scan/{job_id}/price.
    date_priced: Optional[str] = None
