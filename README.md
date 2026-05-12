# Environmental Data Intelligence — Full-Stack Research Platform

This repository contains a scaffold for an AI-powered Environmental Data Intelligence platform focused on research, sustainability, and practical environmental analysis. It includes a backend API, a lightweight ML workflow, sample datasets, and a simple interactive dashboard demo.

Goals:
- Collect, analyze, visualize, and predict environmental trends (AQI, temperature, rainfall, etc.).
- Provide interpretable analytics and dashboard visualizations for research and internships.
- Ship a clean, modular architecture ready for extension and deployment.

Project structure (high-level):

- `backend/` — FastAPI backend exposing REST endpoints for data and predictions.
- `ml/` — Sample datasets and training scripts (scikit-learn example).
- `frontend/` — A static interactive dashboard demo (`static_dashboard.html`) using Chart.js and Tailwind CDN. Replaceable with a React + Tailwind frontend for production.
- `README.md` — This file (project overview, setup, deployment, resume blurb).

Quick Start (local prototype):

1. Create a Python virtual environment and install backend dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

2. (Optional) Train the example ML model:

```powershell
python ml/train_model.py
```

3. Run the FastAPI backend:

```powershell
uvicorn backend.app.main:app --reload --port 8000
```

4. Open the demo dashboard: `frontend/static_dashboard.html` in your browser (or serve it via a static server).

Architecture

- Frontend: interactive charts and filters (Chart.js/Tailwind demo). Replace with React + Tailwind + Chart.js for production.
- Backend: FastAPI application with endpoints for health, sample data, and prediction. ML model can be trained offline and loaded at runtime.
- ML: `ml/train_model.py` shows a simple scikit-learn pipeline (preprocessing, train, save model). Use TensorFlow for advanced models.
- Database: SQLite recommended for prototyping; PostgreSQL for production-scale.

Folder Structure

- `backend/`
	- `app/main.py` — API endpoints
	- `requirements.txt` — Python deps
	- `models/` — stored model artifacts
- `ml/`
	- `sample_data/air_quality_sample.csv` — sample dataset
	- `train_model.py` — example training script (scikit-learn)
- `frontend/`
	- `static_dashboard.html` — quick demo dashboard (Chart.js + Tailwind CDN)
- `README.md` — project overview & instructions

Resume-worthy Project Description (one-liner):

"Built a modular full-stack Environmental Data Intelligence platform integrating FastAPI, scikit-learn, and interactive Chart.js visualizations to analyze and predict air quality and climate trends — includes data pipelines, model training, and deployment-ready APIs."

What I implemented (this scaffold):

- Clean, modular folder structure suitable for internships and research projects.
- Example ML pipeline to predict AQI from environmental features with saved model artifact.
- FastAPI backend with endpoints for data retrieval and model inference.
- Interactive demo dashboard showing trends and visualizations.
- Detailed README with setup, usage, and deployment notes.

Suggested Next Steps / Improvements:

- Replace `frontend/static_dashboard.html` with a React + Tailwind app (Create React App or Vite).
- Add user authentication and role-based access for research collaborators.
- Integrate PostgreSQL and background workers for large-scale ingestion.
- Add scheduled ETL jobs and CI/CD deployment pipelines.
- Integrate satellite/weather APIs and geospatial mapping (Leaflet / Mapbox).
- Add an LLM-based report generator and RAG knowledge assistant for summarization.

Sample Dataset & Attribution

The default training/data file is a real merged dataset built from two public sources:
- **OpenAQ public S3 archive** for pollution observations (`openaq-data-archive`)
- **Open-Meteo archive API** for matched daily weather (`temperature`, `humidity`, `rainfall`)

The build script at `ml/build_real_dataset.py` downloads archive slices, combines them into the app schema, and writes `ml/sample_data/air_quality_real.csv`. AQI is derived from PM2.5 using the US EPA breakpoint formula.

Step 4 deliverables:
- Automated backend tests live in `backend/tests/`
- Evaluation dashboard is available at `/evaluation` in the React app
- The deployment guide includes the exact test and verification commands

Contact / License

This scaffold is permissively licensed for educational/research use. Modify as needed for your project."
