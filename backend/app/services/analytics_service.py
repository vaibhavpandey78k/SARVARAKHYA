from collections import Counter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.report import Report, Prediction


def _predictions(db: Session):
    return list(db.scalars(select(Prediction).order_by(Prediction.created_at.desc())).all())


def _reports(db: Session):
    return list(db.scalars(select(Report)).all())


def _latest_predictions(db: Session):
    latest = {}
    for p in _predictions(db):
        latest.setdefault(p.report_id, p)
    return latest


def overview(db: Session):
    reports = _reports(db)
    latest = _latest_predictions(db)
    analyzed = list(latest.values())
    sif = [p for p in analyzed if p.sif_status == "sif-potential"]
    return {
        "total_reports": len(reports),
        "sif_reports": len(sif),
        "sif_percentage": round((len(sif) / len(analyzed) * 100), 2) if analyzed else 0.0,
        "critical_precursors": sum(bool(p.barrier_failure) for p in sif),
        "analyzed_reports": len(analyzed),
        "uncertain_reports": sum(p.sif_status == "uncertain" for p in analyzed),
    }


def rankings(db: Session, dimension: str):
    reports = {r.id: r for r in _reports(db)}
    counts = Counter()
    sif_counts = Counter()
    for p in _latest_predictions(db).values():
        r = reports.get(p.report_id)
        if not r:
            continue
        key = (r.employer if dimension == "site" else p.activity) or "Unknown"
        counts[key] += 1
        if p.sif_status == "sif-potential":
            sif_counts[key] += 1
    items = []
    for key, count in counts.items():
        items.append({
            "site" if dimension == "site" else "activity": key,
            "report_count": count,
            "sif_count": sif_counts[key],
            "sif_density": round(sif_counts[key] / count, 4) if count else 0.0,
        })
    return {"items": sorted(items, key=lambda x: (x["sif_density"], x["sif_count"]), reverse=True)}


def rules(db: Session):
    counter = Counter()
    for p in _latest_predictions(db).values():
        for rule in p.life_saving_rules or []:
            counter[rule] += 1
    total = sum(counter.values())
    return {"items": [
        {"rule": rule, "count": count, "percentage": round(count / total * 100, 2) if total else 0.0}
        for rule, count in counter.most_common()
    ]}


def precursors(db: Session):
    reports = {r.id: r for r in _reports(db)}
    counter = Counter()
    sif_counter = Counter()
    sites = {}
    for p in _latest_predictions(db).values():
        r = reports.get(p.report_id)
        if not r:
            continue
        key = (p.activity or "Unknown", p.location or "Unknown", p.barrier_failure or "Unknown")
        counter[key] += 1
        sites.setdefault(key, set())
        if r.employer:
            sites[key].add(r.employer)
        if p.sif_status == "sif-potential":
            sif_counter[key] += 1

    items = []
    for key, occurrence in counter.items():
        sif_count = sif_counter[key]
        items.append({
            "id": "|".join(key),
            "activity": key[0],
            "location": key[1],
            "barrier_failure": key[2],
            "occurrence_count": occurrence,
            "sif_count": sif_count,
            "sif_density": round(sif_count / occurrence, 4) if occurrence else 0.0,
            "trend_percentage": 0.0,
            "affected_sites": sorted(sites.get(key, set())),
        })
    return {"items": sorted(items, key=lambda x: (x["sif_density"], x["occurrence_count"]), reverse=True)}
