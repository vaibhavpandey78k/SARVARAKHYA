# SARVARAKHYA Precursor Intelligence Backend

FastAPI + SQLAlchemy + SQLite MVP implementing the backend contract from the SARVARAKHYA briefs.

## MVP flow

Safety report -> validation -> persistence -> baseline SIF analysis -> Life-Saving Rule mapping -> activity/location/barrier extraction -> prediction persistence -> precursor/dashboard analytics.

## Important safety/data honesty

- The supplied development corpus has no native SIF-potential ground-truth label.
- The included analyzer is a transparent **baseline heuristic**, not a calibrated probability model.
- `sif_score` is a heuristic score; `sif_probability` is `null` for the baseline.
- Hospitalization, amputation and loss of eye are stored as source fields and are **not** used as a SIF ground-truth label.
- Raw narrative is preserved; AI-derived fields live in `predictions`.

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Test

```powershell
pytest -q
```

## API

- GET `/health`
- POST `/api/reports`
- GET `/api/reports?limit=50&offset=0`
- GET `/api/reports/{id}`
- POST `/api/reports/{id}/analyze`
- POST `/api/reports/analyze-batch?limit=1000` (MVP helper for bulk analysis)
- POST `/api/reports/import`
- GET `/api/dashboard/overview`
- GET `/api/dashboard/sites`
- GET `/api/dashboard/activities`
- GET `/api/dashboard/rules`
- GET `/api/dashboard/precursors`

## Example report

```json
{
  "report_text": "Technician entered the maintenance area before electrical isolation was confirmed.",
  "event_date": "2026-08-25",
  "site": "Plant A"
}
```

## CSV

Run the audit before the full import: `python scripts/audit_csv.py path\to\data.csv`. The importer uses 5,000-row chunks to keep memory predictable.

The importer expects `Final Narrative` and recognizes the source fields listed in the SIH brief, including `ID`, `EventDate`, `Employer`, location fields, `EventTitle`, `SourceTitle`, and outcome fields. It reports received/imported/skipped/duplicate/error counts and preserves `ID` as `source_id`.

## Next upgrade

Keep `BaselineAnalyzer.analyze(report)` as the stable interface. Replace its implementation with TF-IDF + Logistic Regression, embeddings, or a validated transformer once expert labels exist; keep the API and prediction schema stable.

