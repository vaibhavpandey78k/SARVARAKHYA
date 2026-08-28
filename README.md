# SARVARAKHYA — Combined Frontend + Backend

This package combines the SARVARAKHYA Precursor Intelligence backend and React frontend into one workspace.

## Architecture

- `backend/` — FastAPI + SQLAlchemy + SQLite + baseline SIF/LSR/extraction/analytics
- `frontend/` — React + TypeScript + Vite HSE dashboard
- Frontend uses the real API by default through `frontend/.env`.

## Run backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Run frontend (second terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally http://localhost:5173).

## Current integrated flow

Analyze page → POST report → POST analysis → display evidence/LSR/context.
Reports page → GET paginated reports with filters.
Dashboard → overview/sites/activities/rules/precursors.

## Important safety/data note

The supplied development corpus has no native SIF ground-truth label. The backend therefore exposes a transparent `baseline` / `baseline-v1` heuristic score, not a calibrated probability. Hospitalization, amputation and loss of eye are retained as source fields and are not used as a SIF ground-truth label.

