# Environmental Data Intelligence — Full-Stack Research Platform

This repository is a compact, internship-ready scaffold for an Environmental Data Intelligence project. It includes a FastAPI backend, a simple scikit-learn ML pipeline, sample datasets, and a demo frontend. The goal is reproducible experiments, clear APIs, and a presentable demo you can show in interviews.

Key highlights
- FastAPI backend serving model inference and dataset endpoints.
- Example ML pipeline (`ml/train_model.py`) and saved model artifact (`models/model.joblib`).
- Demo frontend + static dashboard for quick visualization.

Getting started (developer quick commands)

1) Create and activate a Python virtual environment, install backend dependencies, and run tests:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pip install -r backend/requirements.txt --upgrade
pytest -q
```

2) Train (optional) and run the backend locally:

```powershell
python ml/train_model.py
uvicorn backend.app.main:app --reload --port 8000
```

3) Open the demo UI:

- Open `frontend/static_dashboard.html` in your browser, or run the React frontend in `frontend/`:

```bash
cd frontend
npm install
npm start
```

Tests & quality
- Run tests: `pytest -q` (tests are under `backend/tests/`).
- Add coverage: `pytest --cov=backend --cov-report=term-missing`.
- Lint/format: add `black`, `ruff`, and `mypy` to `requirements-dev.txt` and run in CI.

Packaging & CI
- Add `pyproject.toml` or `setup.cfg` for packaging and pin dependencies.
- Add a GitHub Actions workflow to run tests, lint, and build on PRs.

Model & metadata
- Model artifact: `models/model.joblib` and `models/model_metadata.json` describe input features and version.
- Add a `MODEL_CARD.md` describing model intended use, limitations, and evaluation metrics.

Development notes
- Database: SQLite is used for local prototyping; swap to PostgreSQL in production.
- Warnings in tests: address SQLAlchemy and timezone-aware datetime deprecations.

Contributing
- Add a `CONTRIBUTING.md` with dev setup, testing, and commit guidelines.

Contact
- Use repository issues for questions or reach out with the contact info in the project header.

This README is intentionally concise — see `QUICKSTART.md` for copy-paste commands and `DEPLOYMENT.md` for production deployment notes.

Docker
- Backend Dockerfile: `backend/Dockerfile`
- Start locally with: `docker-compose up --build`

