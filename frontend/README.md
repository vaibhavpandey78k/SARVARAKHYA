# SARVARAKHYA — SIF Precursor Intelligence Frontend

React + TypeScript frontend for the SIH 2026 SIF (Serious Injury/Fatality) Precursor Intelligence System.

## Development

```bash
npm install
npm run dev
```

The default mode is `mock`, so the UI can be developed without the backend.

## Mock → real API

Copy `.env.example` to `.env` and set:

```env
VITE_API_MODE=real
VITE_API_BASE_URL=http://localhost:8000
```

All HTTP calls are centralized in `src/api/`. Components/pages never call `fetch` directly. The real adapter and mock adapter implement the same `ApiClient` interface.

## Architecture

- `src/api/` — API interface, real HTTP adapter, mock adapter, service factory
- `src/types/` — backend contract types and frontend view types
- `src/components/` — reusable HSE dashboard components
- `src/pages/` — route-level screens
- `src/App.tsx` — page routing and application shell

## Safety UX

The UI deliberately uses language such as **SIF Potential**, **AI Prediction Confidence**, **Requires Review**, and **Supporting Evidence**. Predictions are not presented as final safety decisions; HSE professionals remain responsible for review/action.

## API contract notes / questions for backend approval

1. `GET /api/reports/{id}` can return `analysis` but `POST /api/reports` cannot. Reports therefore show an explicit “Not analyzed” state until analysis exists.
2. `GET /api/reports/{id}` has `report_type: string` while create allows `UA|UC|Near Miss|Incident|null`. The frontend treats the returned value as display data rather than enforcing a narrower enum.
3. No `GET /api/reports` list/search/pagination contract is supplied. The Reports page therefore uses a development mock list. **Backend needs to approve/provide a list endpoint and its pagination/filter contract before production integration.**
4. No review endpoint is supplied. `review_status` and `reviewer_correction` are display-only; the frontend does not mutate review state.
5. Dashboard contracts provide site/activity/rule/precursor aggregates, but no trend endpoint. Trend UI is only shown where `trend_percentage` is explicitly returned by the precursor contract.
6. The contract calls `sif_percentage` a percentage and `sif_density` a density/rate. The frontend displays returned values and does not recompute them.
7. Missing/null analysis fields are tolerated in rendering and shown as `Not available` rather than guessed.

