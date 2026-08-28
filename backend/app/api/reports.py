from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.report import ReportCreate, ReportOut, AnalyzeResponse
from app.models.report import Report, Prediction
from app.services.report_service import create_report, get_report, analyze_report
from app.services.ingestion_service import import_csv
from app.services.batch_service import analyze_batch

router = APIRouter(prefix="/api/reports", tags=["Reports"])


def _report_payload(report: Report) -> Report:
    # SQLAlchemy relationship is already available; response schema exposes raw source + predictions.
    return report


@router.post("", response_model=ReportOut, status_code=201)
def create(data: ReportCreate, db: Session = Depends(get_db)):
    return create_report(db, data)


@router.get("", response_model=dict)
def list_all(
    search: str | None = None,
    sif: str = "all",
    site: str | None = None,
    activity: str | None = None,
    rule: str | None = None,
    minConfidence: str | None = None,
    date: str | None = None,
    page: int = 1,
    pageSize: int = 5,
    db: Session = Depends(get_db),
):
    page = max(1, page)
    page_size = max(1, min(pageSize, 100))
    reports = list(db.scalars(select(Report).order_by(Report.created_at.desc())).all())
    filtered = []
    for report in reports:
        predictions = sorted(report.predictions, key=lambda p: p.created_at, reverse=True)
        prediction = predictions[0] if predictions else None
        text = report.final_narrative or ""
        report_site = report.employer or ""
        if search and search.lower() not in f"{text} {report_site} {(prediction.activity if prediction else '')}".lower():
            continue
        if site and report_site.lower() != site.lower():
            continue
        if date and str(report.event_date or "") != date:
            continue
        if sif == "sif" and not (prediction and prediction.sif_prediction is True):
            continue
        if sif == "non-sif" and not (prediction and prediction.sif_prediction is False):
            continue
        if activity and not (prediction and (prediction.activity or "").lower() == activity.lower()):
            continue
        if rule and not (prediction and rule in (prediction.life_saving_rules or [])):
            continue
        if minConfidence and not (prediction and (prediction.confidence or "").lower() == minConfidence.lower()):
            continue
        filtered.append(report)

    total = len(filtered)
    start = (page - 1) * page_size
    page_items = [ReportOut.model_validate(r).model_dump(mode="json") for r in filtered[start:start + page_size]]
    return {"items": page_items, "total": total, "page": page, "page_size": page_size}


@router.get("/{report_id}", response_model=ReportOut)
def get(report_id: str, db: Session = Depends(get_db)):
    report = get_report(db, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return report


@router.post("/analyze-batch")
def analyze_many(limit: int = 1000, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 5000))
    return analyze_batch(db, limit)


@router.post("/{report_id}/analyze", response_model=AnalyzeResponse)
def analyze(report_id: str, db: Session = Depends(get_db)):
    report = get_report(db, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return analyze_report(db, report)


@router.post("/import")
async def import_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")
    data = await file.read()
    from app.core.config import settings
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Upload exceeds {settings.max_upload_mb} MB MVP limit")
    try:
        return import_csv(db, data, file.filename)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
