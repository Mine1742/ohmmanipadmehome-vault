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
    # default_factory=FieldValue (not a bare required field) on every
    # attribute here on purpose: cards scanned before a field existed (e.g.
    # `condition`, added 2026-08-07) have no key for it at all in their
    # stored fields_json. A required field with no default makes Pydantic
    # reject ANY pre-existing card the moment a new field is added --
    # exactly the bug that broke /scan/list and /scan/{job_id}/review for
    # every already-scanned card here. Defaulting to an empty FieldValue
    # means an old card just shows that field as unset instead of the
    # whole card failing to load.
    player: FieldValue = Field(default_factory=FieldValue)
    team: FieldValue = Field(default_factory=FieldValue)
    year: FieldValue = Field(default_factory=FieldValue)
    set: FieldValue = Field(default_factory=FieldValue)
    card_number: FieldValue = Field(default_factory=FieldValue)
    serial_number: FieldValue = Field(default_factory=FieldValue)
    parallel_insert_type: FieldValue = Field(default_factory=FieldValue)
    notable_flags: FieldValue = Field(default_factory=FieldValue)
    condition: FieldValue = Field(default_factory=FieldValue)


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
    # Your own entry -- what you paid, or what you believe it's worth. Never
    # auto-filled. See PriceSubmission / POST /scan/{job_id}/price.
    price: Optional[float] = None
    date_priced: Optional[str] = None
    # An eBay-sourced estimate, kept deliberately separate from the manual
    # price above and never overwrites it. Only set when you explicitly
    # request it -- see POST /scan/{job_id}/estimate-price -- since it costs
    # a web-search call each time and isn't run automatically per scan.
    estimated_price: Optional[float] = None
    estimated_price_date: Optional[str] = None
    estimated_price_source: Optional[str] = None
    estimated_price_caveat: Optional[str] = None


class ReviewSubmission(BaseModel):
    field: str
    new_value: str
    reviewer: str = "owner"


class PriceSubmission(BaseModel):
    price: float = Field(ge=0)
    # ISO date string (YYYY-MM-DD), e.g. when you looked the price up. Defaults
    # to today (server-side) if omitted -- see main.py's /scan/{job_id}/price.
    date_priced: Optional[str] = None
