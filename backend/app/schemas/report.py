from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReportCreate(BaseModel):
    report_text: str = Field(min_length=5, max_length=100_000)
    event_date: date | None = None
    site: str | None = Field(default=None, max_length=500)
    report_type: str | None = Field(default=None, max_length=50)
    source_id: str | None = Field(default=None, max_length=255)
    employer: str | None = Field(default=None, max_length=500)
    city: str | None = None
    state: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("report_text")
    @classmethod
    def clean_text(cls, v: str) -> str:
        v = " ".join(v.split())
        if len(v) < 5:
            raise ValueError("report_text is too short")
        return v


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    report_id: str
    analysis_type: str
    model_version: str
    sif_prediction: bool | None
    sif_status: str
    sif_score: float | None
    sif_probability: float | None
    confidence: str
    life_saving_rules: list[str]
    activity: str | None
    location: str | None
    barrier_failure: str | None
    evidence: list[str]
    review_status: str = "Pending"
    reviewer_correction: bool | None = None
    created_at: datetime


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    source_id: str | None
    event_date: date | None
    employer: str | None
    city: str | None
    state: str | None
    final_narrative: str
    source: str | None = None
    created_at: datetime
    predictions: list[PredictionOut] = []


class AnalyzeResponse(PredictionOut):
    pass
