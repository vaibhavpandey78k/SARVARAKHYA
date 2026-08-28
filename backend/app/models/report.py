import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str | None] = mapped_column(String(255), index=True, unique=True, nullable=True)
    event_date: Mapped[date | None] = mapped_column(Date, index=True)
    employer: Mapped[str | None] = mapped_column(String(500), index=True)
    address: Mapped[str | None] = mapped_column(String(1000))
    city: Mapped[str | None] = mapped_column(String(255), index=True)
    state: Mapped[str | None] = mapped_column(String(255), index=True)
    zip_code: Mapped[str | None] = mapped_column(String(50))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    primary_naics: Mapped[str | None] = mapped_column(String(100))
    hospitalized: Mapped[str | None] = mapped_column(String(100))
    amputation: Mapped[str | None] = mapped_column(String(100))
    loss_of_eye: Mapped[str | None] = mapped_column(String(100))
    nature: Mapped[str | None] = mapped_column(String(500))
    nature_title: Mapped[str | None] = mapped_column(String(500))
    body_part: Mapped[str | None] = mapped_column(String(500))
    body_part_title: Mapped[str | None] = mapped_column(String(500))
    event: Mapped[str | None] = mapped_column(String(500))
    event_title: Mapped[str | None] = mapped_column(String(500), index=True)
    source: Mapped[str | None] = mapped_column(String(500))
    source_title: Mapped[str | None] = mapped_column(String(500), index=True)
    secondary_source: Mapped[str | None] = mapped_column(String(500))
    final_narrative: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="report", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id: Mapped[str] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), index=True)
    analysis_type: Mapped[str] = mapped_column(String(50), default="baseline")
    model_version: Mapped[str] = mapped_column(String(100), default="baseline-v1")
    sif_prediction: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sif_status: Mapped[str] = mapped_column(String(50), default="uncertain")
    sif_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    sif_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[str] = mapped_column(String(30), default="low")
    activity: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(500))
    barrier_failure: Mapped[str | None] = mapped_column(String(500))
    life_saving_rules: Mapped[list | None] = mapped_column(JSON)
    evidence: Mapped[list | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    report: Mapped[Report] = relationship(back_populates="predictions")

class HumanReview(Base):
    __tablename__ = "human_reviews"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id: Mapped[str] = mapped_column(ForeignKey("predictions.id", ondelete="CASCADE"), index=True)
    reviewer_decision: Mapped[str | None] = mapped_column(String(100))
    reviewer_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
