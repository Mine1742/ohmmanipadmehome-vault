from typing import Optional

from pydantic import BaseModel


class FieldValue(BaseModel):
    value: Optional[str] = None
    confidence: float = 0.0


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


class ReviewSubmission(BaseModel):
    field: str
    new_value: str
    reviewer: str = "owner"
