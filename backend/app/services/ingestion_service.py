from io import BytesIO
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.report import Report

COLUMN_MAP = {
    "ID": "source_id", "EventDate": "event_date", "Employer": "employer", "Address": "address", "City": "city", "State": "state", "ZIP": "zip_code",
    "Latitude": "latitude", "Longitude": "longitude", "Primary NAICS": "primary_naics", "Hospitalized": "hospitalized", "Amputation": "amputation", "Loss of Eye": "loss_of_eye",
    "Nature": "nature", "NatureTitle": "nature_title", "Part of Body": "body_part", "Title": "body_part_title", "Event": "event", "EventTitle": "event_title",
    "Source": "source", "SourceTitle": "source_title", "Secondary Source": "secondary_source", "Final Narrative": "final_narrative",
}

def _clean(v):
    if pd.isna(v): return None
    return str(v).strip()

def _parse_date(v):
    parsed = pd.to_datetime(v, errors="coerce")
    return None if pd.isna(parsed) else parsed.date()

def import_csv(db: Session, file_bytes: bytes, filename: str) -> dict:
    # Chunked ingestion keeps memory predictable for the 105,996-row development corpus.
    stream = BytesIO(file_bytes)
    first = pd.read_csv(stream, nrows=0)
    cols = {c.strip(): c for c in first.columns}
    if "Final Narrative" not in cols:
        raise ValueError("CSV must contain 'Final Narrative'")
    mapped = {internal: cols[expected] for expected, internal in COLUMN_MAP.items() if expected in cols}
    existing_ids = set(db.scalars(select(Report.source_id).where(Report.source_id.is_not(None))).all()) if "source_id" in mapped else set()
    rows_received = imported = skipped = duplicates = 0
    errors = []
    stream.seek(0)
    for df in pd.read_csv(stream, low_memory=False, chunksize=5000):
        rows_received += len(df)
        batch = []
        for idx, row in df.iterrows():
            try:
                source_id = _clean(row[mapped["source_id"]]) if "source_id" in mapped else None
                if source_id and source_id in existing_ids:
                    duplicates += 1
                    continue
                narrative = _clean(row[mapped["final_narrative"]]) or ""
                if len(narrative) < 5:
                    skipped += 1
                    if len(errors) < 20: errors.append({"row": int(idx) + 2, "error": "Final Narrative missing/too short"})
                    continue
                values = {internal: _clean(row[col]) for internal, col in mapped.items()}
                values["event_date"] = _parse_date(row[mapped["event_date"]]) if "event_date" in mapped else None
                for f in ("latitude", "longitude"):
                    if f in values and values[f] is not None:
                        try: values[f] = float(values[f])
                        except (ValueError, TypeError): values[f] = None
                batch.append(Report(**values))
                if source_id: existing_ids.add(source_id)
                imported += 1
            except Exception as exc:
                skipped += 1
                if len(errors) < 20: errors.append({"row": int(idx) + 2, "error": str(exc)[:200]})
        if batch:
            db.add_all(batch)
            db.commit()
    return {"filename": filename, "rows_received": rows_received, "imported": imported, "skipped": skipped, "duplicates": duplicates, "validation_errors": len(errors), "errors": errors}
