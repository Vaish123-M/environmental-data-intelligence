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

---

For interviewers: quick walkthrough

- What this project demonstrates: a complete ML application lifecycle — preprocessing and training scripts (`ml/`), a serialised model artifact (`backend/models/model.joblib`), a REST API for inference (`backend/app/main.py`), and a React dashboard for visualization (`frontend/src/pages/`).
- How to validate: run backend tests (`pytest -q`) and use `POST /api/predict` to verify predictions. Example curl:

```bash
curl -s -X POST http://127.0.0.1:8000/api/predict -H "Content-Type: application/json" -d '{"temperature":25,"humidity":65,"rainfall":10}' | jq
```

- Model details: feature inputs are `temperature`, `humidity`, `rainfall` plus derived features (see `ml/preprocess.py`); model artifact path: `backend/models/model.joblib`; model evaluation metrics are produced by `ml/evaluate_model.py` and saved plots under `ml/plots/`.

- Reproducible steps for results:
	1. Prepare Python env and install dependencies: `pip install -r backend/requirements.txt`.
	2. (Optional) Retrain: `python ml/train_model.py` will produce `backend/models/model.joblib`.
	3. Run evaluation: `python ml/evaluate_model.py` to print MAE/RMSE/R2 and write plots.

- What to look for in code during an interview:
	- `backend/app/model.py`: model wrapper, save/load, predict API contract.
	- `backend/app/main.py`: API endpoints and router structure.
	- `ml/train_model.py`: feature engineering and training pipeline.
	- `frontend/src/pages/`: how UI obtains and displays model outputs.

If you'd like, I can also add a short `DEMO.md` with sample requests and example responses (JSON) for quick copy-paste during interviews.

