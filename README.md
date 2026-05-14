# Environmental Data Intelligence

Air quality prediction and environmental analytics platform built with FastAPI, React, and scikit-learn. The project provides real-time AQI prediction, data analysis, and model evaluation through a simple web interface.

Repository
- GitHub: https://github.com/Vaish123-M/environmental-data-intelligence

## Project Summary

This project predicts AQI from environmental inputs such as temperature, humidity, and rainfall. It also includes a dashboard for exploring trends, comparing model performance, and reviewing generated plots.

## Key Features

- Real-time AQI prediction from environmental inputs.
- Analytics dashboard with scatter plots and regional statistics.
- Model comparison view with evaluation metrics and visual outputs.
- CSV upload support for adding environmental data.
- REST APIs for health, data, prediction, upload, and evaluation.

## Tech Stack

Frontend: React, Axios, Recharts, Tailwind CSS

Backend: FastAPI, Uvicorn, SQLAlchemy, SQLite

Machine Learning: scikit-learn, joblib, pandas, numpy

## Architecture

```text
User Browser
    -> React Frontend
    -> FastAPI Backend
    -> ML Model / Data Layer
    -> Prediction + Analytics Response
```

Backend responsibilities:
- Serve REST APIs for prediction, data, uploads, and evaluation.
- Load the trained model artifact from `backend/models/model.joblib`.
- Expose plot images and model comparison metadata.

Frontend responsibilities:
- Render dashboard, analytics, upload, and prediction screens.
- Call backend APIs through `REACT_APP_API_URL`.
- Display model outputs and charts in a clean UI.

## Project Structure

```text
environmental-data-intelligence/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── model.py
│   │   └── schemas.py
│   ├── models/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── components/
│   └── public/
├── ml/
│   ├── train_model.py
│   ├── train_with_plots.py
│   ├── evaluate_model.py
│   └── plots/
├── QUICKSTART.md
├── DEPLOYMENT.md
└── README.md
```

## Local Setup

### Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pytest -q
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

### Frontend

```powershell
cd frontend
npm install
npm start
```

Open:
- `http://localhost:3000`

## Useful API Endpoints

- `GET /api/health` - Backend health check.
- `GET /api/data` - Environmental dataset.
- `GET /api/data/stats` - Summary statistics.
- `POST /api/predict` - AQI prediction endpoint.
- `POST /api/upload` - CSV upload endpoint.
- `GET /api/models/comparison` - Model metrics and plot links.
- `GET /api/evaluation/summary` - Evaluation summary for the dashboard.

## Deployment Notes

- Frontend expects `REACT_APP_API_URL` to point to the deployed backend.
- Backend can run on Render, Railway, or any platform that supports Python web services.
- See `DEPLOYMENT.md` for deployment steps.

## Project Highlights

- Practical ML pipeline for AQI prediction and analysis.
- Clear frontend-backend separation with API-driven communication.
- Visual model evaluation that makes results easy to review.
- Ready for local development and cloud deployment.

## Notes for Reviewers

- Use `QUICKSTART.md` for setup steps.
- Use `DEPLOYMENT.md` for deployment configuration.
- Model artifacts and plots are stored under `backend/models/` and `ml/plots/`.

## License

Educational use.

