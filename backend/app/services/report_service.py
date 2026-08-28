from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.report import Report, Prediction
from app.ai.analyzer import analyzer


def create_report(db: Session, data) -> Report:
    report = Report(
        source_id=data.source_id,
        event_date=data.event_date,
        employer=data.employer or data.site,
        city=data.city,
        state=data.state,
        latitude=data.latitude,
        longitude=data.longitude,
        source=data.report_type,
        final_narrative=data.report_text,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report(db: Session, report_id: str) -> Report | None:
    return db.get(Report, report_id)


def analyze_report(db: Session, report: Report) -> Prediction:
    result = analyzer.analyze(report)
    prediction = Prediction(
        report_id=report.id,
        analysis_type=analyzer.analysis_type,
        model_version=analyzer.model_version,
        **result,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def list_reports(db: Session, limit: int = 50, offset: int = 0):
    return list(
        db.scalars(
            select(Report).order_by(Report.created_at.desc()).offset(offset).limit(limit)
        ).all()
    )
