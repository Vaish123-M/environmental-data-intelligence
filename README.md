# Environmental Data Intelligence Platform

Concise local-development project that predicts Air Quality Index (AQI) from environmental inputs and provides an interactive analytics dashboard and REST APIs for inference, evaluation, and visualization.

Purpose

- Provide a practical ML engineering pipeline that covers data preprocessing, model training, evaluation (MAE, RMSE, R²), inference APIs, and a React dashboard for visualization.
- Demonstrates end-to-end experience in Machine Learning, Environmental Analytics, and full-stack engineering.

Key Features

- AQI Prediction API: lightweight inference endpoint (`POST /api/predict`) that returns predicted AQI and model metadata.
- Interactive React Dashboard: visualizations, model comparison, and CSV upload for batch predictions.
- Model Evaluation: scripts and plots for MAE, RMSE, and R² with saved artifacts under `ml/plots/`.
- Reproducible ML Pipeline: preprocessing, training, and model serialization using scikit-learn and joblib.
- Dev-ready: tests (`pytest`), formatting (`black`, `ruff`), and simple local workflows.

Tech Stack (high-value keywords)

- Machine Learning: scikit-learn, pandas, numpy, joblib
- Backend & APIs: FastAPI, Uvicorn, SQLAlchemy, SQLite
- Frontend: React, Axios, Recharts, Tailwind CSS
- Dev: pytest, black, ruff

High-level Overview

1. Data preprocessing: `ml/preprocess.py` implements feature engineering (temperature, humidity, rainfall + derived features).
2. Training: `ml/train_model.py` builds a scikit-learn pipeline and saves `backend/models/model.joblib`.
3. Evaluation: `ml/evaluate_model.py` computes MAE, RMSE, R² and writes plots to `ml/plots/`.
4. Inference: `backend/app/main.py` exposes `POST /api/predict`, `GET /api/models/comparison`, and evaluation endpoints.
5. Visualization: `frontend/src/pages/` implements dashboard views and calls the backend at `http://127.0.0.1:8000`.

Machine Learning Workflow (concise)

- Data ingestion: CSV uploads via API or static sample datasets in `ml/sample_data/`.
- Preprocessing: feature construction, scaling, and validation functions in `ml/preprocess.py` and `backend/app/model.py`.
- Model training: pipeline creation (scaler + regressor), hyperparameter tuning (if applied), and serialization to `backend/models/`.
- Evaluation: compute MAE, RMSE, and R²; generate residual and comparison plots saved under `ml/plots/`.
- Runtime: model artifact loaded by FastAPI at startup for low-latency inference.

Project Architecture (folder highlights)

```
environmental-data-intelligence/
├─ backend/
│  ├─ app/            # FastAPI app, model wrapper, database
│  ├─ models/         # serialized model artifacts
│  └─ tests/          # pytest test-suite
├─ frontend/          # React dashboard and UI
├─ ml/                # preprocessing, training, evaluation, plots
└─ README.md, QUICKSTART.md, MODEL_CARD.md, DEMO.md
```

Quickstart (developer)

1) Backend (Windows / PowerShell)

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

API Reference (selected)

- `GET /api/health` — service health and version
- `POST /api/predict` — JSON body: `{temperature, humidity, rainfall}` → returns `{predicted_aqi, model_version, metrics}`
- `POST /api/upload` — upload CSV for batch predictions
- `GET /api/models/comparison` — returns model metrics and plot URLs
- `GET /api/evaluation/summary` — evaluation metrics and plot references

Model & Evaluation

- Model artifact: `backend/models/model.joblib` (scikit-learn pipeline).
- Evaluation metrics recorded: MAE, RMSE, R² (see `ml/evaluate_model.py`).
- Visualization: residual plots and comparison charts saved to `ml/plots/`.

Local execution

- The backend loads a serialized scikit-learn model for low-latency inference.
- Frontend calls the local backend at `http://127.0.0.1:8000`.
- The repo is intentionally kept simple for local development, portfolio review, and internship showcase.

Future improvements

- Add scalable model serving (FastAPI + Gunicorn/Uvicorn workers or cast to a model server).
- Add reproducible training experiments (MLflow or equivalent) and automated model versioning.
- Introduce lightweight async job queue for large/batch processing.
- Add more robust dataset validation and monitoring (data drift alerts).

Reviewer walkthrough (what to inspect quickly)

- `backend/app/model.py`: model wrapper, save/load, and predict contract (good to evaluate engineering quality).
- `ml/train_model.py`: feature engineering, pipeline construction, and training code (shows ML workflow).
- `ml/evaluate_model.py` and `ml/plots/`: how evaluation metrics and visualizations are generated.
- `frontend/src/pages/`: dashboard implementation and how it consumes the API.

Keywords

Machine Learning · Environmental Analytics · AQI Prediction · Data Preprocessing · Model Evaluation · FastAPI · React Dashboard · Scikit-learn · REST APIs · Data Visualization · AI-powered Analytics · Scalable Architecture · Prediction Pipeline

License

Educational use.

Contact

Project owner: see repo owner on GitHub for contact details.

Additional artifacts

- `DEMO.md` — copy-paste API examples for quick verification.
- `MODEL_CARD.md` — model description, inputs/outputs, evaluation notes and limitations.
- `experiments/example_run.json` — example experiment logging format (suggested simple reproducibility pattern).
