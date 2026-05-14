# Environmental Data Intelligence

Objective

Provide a lightweight, developer-friendly platform that predicts Air Quality Index (AQI) from common environmental inputs, and exposes a small analytics dashboard and REST APIs for exploration and integration.

Brief

This repository contains a FastAPI backend that loads a trained scikit-learn model to predict AQI from inputs (temperature, humidity, rainfall and derived features), plus a React frontend that visualizes predictions, model comparisons, and evaluation plots. It is intended for local development, experimentation, and demonstration.

Tech stack

- Backend: FastAPI, Uvicorn, SQLAlchemy, SQLite
- Frontend: React, Axios, Recharts, Tailwind CSS
- ML: scikit-learn, joblib, pandas, numpy
- Dev & CI: pytest, black, ruff

Quick start (local)

1) Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

2) Frontend

```powershell
cd frontend
npm install
npm start
```

Main endpoints

- `GET /api/health` — health check
- `POST /api/predict` — returns predicted AQI and model metadata
- `POST /api/upload` — upload CSV data for analysis
- `GET /api/models/comparison` — model metrics and plots

Testing & formatting

- Run backend tests: `pytest -q`
- Format: `black .` and `ruff format .`

Notes

- Frontend reads backend URL from `REACT_APP_API_URL`.
- Model artifact: `backend/models/model.joblib`.
- See `QUICKSTART.md` and `DEPLOYMENT.md` for more details.

License

Educational use.

