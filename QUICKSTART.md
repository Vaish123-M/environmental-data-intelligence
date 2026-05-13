# 🚀 Quick Start Guide — Run locally in ~5 minutes

Prerequisites
- Python 3.8+ and PowerShell (Windows) or a POSIX shell
- Node.js 16+ (for the frontend)

1) Backend — install and run

```powershell
# From project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pytest -q
python ml/train_model.py    # optional: create models/model.joblib
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open: `http://127.0.0.1:8000` (API docs: `http://127.0.0.1:8000/docs`)

2) Frontend — optional (run in separate terminal)

```bash
cd frontend
npm install
npm start
```

Open: `http://localhost:3000`

3) Quick API checks

Use the OpenAPI docs or these curl examples:

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/data

curl -X POST http://127.0.0.1:8000/api/predict -H "Content-Type: application/json" -d '{"temperature":25,"humidity":60,"rainfall":5}'
```

CSV upload format (example rows):

```
date,region,temperature,humidity,rainfall,aqi
2024-01-01,North,22.1,55,0.0,85
```

Troubleshooting
- If backend fails to start, ensure the venv is activated and dependencies installed.
- If `models/model.joblib` is missing, run `python ml/train_model.py`.

Next steps (recommended for internship polish)
- Add `requirements-dev.txt` and dev tools (`black`, `ruff`, `mypy`).
- Add GitHub Actions to run tests and linters on PRs.
- Create `MODEL_CARD.md` and an evaluation notebook under `ml/`.

See also: [DEPLOYMENT.md](DEPLOYMENT.md), [BUILD_SUMMARY.md](BUILD_SUMMARY.md)
