from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.report import Report, Prediction
from app.ai.analyzer import analyzer

def analyze_batch(db: Session, limit: int = 1000) -> dict:
    reports = list(db.scalars(select(Report).where(~Report.predictions.any()).order_by(Report.created_at).limit(limit)).all())
    predictions = []
    for report in reports:
        result = analyzer.analyze(report)
        predictions.append(Prediction(report_id=report.id, analysis_type=analyzer.analysis_type, model_version=analyzer.model_version, **result))
    if predictions:
        db.add_all(predictions)
        db.commit()
    return {"requested": limit, "analyzed": len(predictions), "remaining_hint": "Call again until analyzed=0"}
