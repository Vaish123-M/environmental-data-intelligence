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

Deployment notes

- Frontend API calls are relative by default, so the simplest deployment is to build the React app and serve it behind the same domain as the FastAPI backend.
- If you host the frontend and backend separately, set `REACT_APP_API_BASE_URL` at build time, for example `https://api.example.com`.
- The React dev server also proxies `/api` to `http://127.0.0.1:8000` via `frontend/package.json`, which keeps local development simple.
- A practical low-friction option is one backend host plus a reverse proxy such as Nginx or Caddy in front of both services.

CSV upload format (example rows):

```
date,region,temperature,humidity,rainfall,aqi
2024-01-01,North,22.1,55,0.0,85
```

Troubleshooting
- If backend fails to start, ensure the venv is activated and dependencies installed.
- If `models/model.joblib` is missing, run `python ml/train_model.py`.

See also: [README.md](README.md), [MODEL_CARD.md](MODEL_CARD.md), [DEMO.md](DEMO.md)
