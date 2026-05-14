# Environmental Data Intelligence

A compact project that predicts Air Quality Index (AQI) from simple environmental inputs and exposes an analytics dashboard and REST APIs for integration and inspection.

What this repo contains
- A FastAPI backend that serves prediction and analytics endpoints and loads a trained scikit-learn model (`backend/models/model.joblib`).
- A React frontend (in `frontend/`) that provides a dashboard, CSV upload, and prediction UI.
- ML utilities and scripts in `ml/` for training, evaluation, and plotting.

Quick summary for readers
- Input: temperature, humidity, rainfall (and derived features).
- Output: predicted AQI value and model metadata (version, metrics).
- Usage: run locally for development, or deploy the frontend and backend to any compatible host.

Getting started (local dev)

1. Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pytest -q
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open API docs at `http://127.0.0.1:8000/docs`.

2. Frontend

```powershell
cd frontend
npm install
npm start
```

Open the UI at `http://localhost:3000` (by default the frontend expects `REACT_APP_API_URL` to point at the backend).

Key API endpoints

- `GET /api/health` — health check
- `POST /api/predict` — request prediction (JSON body with `temperature`, `humidity`, `rainfall`)
- `POST /api/upload` — upload CSV with environmental data
- `GET /api/models/comparison` — model metrics and plots
- `GET /api/evaluation/summary` — evaluation summary for dashboard

Testing & linting

- Run tests: `pytest -q` (backend tests are under `backend/tests/`).
- Formatting: `black .` and `ruff format .` are used in CI.

Notes

- The frontend uses the `REACT_APP_API_URL` environment variable to reach the backend. When deploying (e.g., Vercel), ensure the variable is set or the UI will fail to connect.
- Model artifacts and plots are stored under `backend/models/` and `ml/plots/`.

Where to look next
- Backend code: `backend/app/main.py`, `backend/app/model.py`.
- Frontend entry: `frontend/src/index.js` and `frontend/src/pages/`.
- ML scripts: `ml/train_model.py`, `ml/evaluate_model.py`.

License

Educational use.

