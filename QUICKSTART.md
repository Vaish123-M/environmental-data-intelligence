# 🚀 Quick Start Guide — 5 Minutes to Running

## Prerequisites
- Python 3.8+ (`python --version`)
- Node.js 16+ (`node --version`)

---

## Step 1: Backend Setup (2 minutes)

```bash
# Open PowerShell in project root
cd environmental-data-intelligence

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Train ML model
python ml/train_model.py

# Start backend
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ **Backend running:** `http://127.0.0.1:8000`  
✅ **API Docs:** `http://127.0.0.1:8000/docs`

---

## Step 2: Frontend Setup (3 minutes) — *In a new terminal*

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

✅ **Frontend opens automatically at:** `http://localhost:3000`

---

## What You'll See

### Dashboard Page (`/`)
- 4 statistic cards (AQI, Temperature, Humidity, Rainfall)
- 4 interactive charts showing environmental trends
- Raw data table with all records

### Analytics Page (`/analytics`)
- Correlation analysis
- Scatter plots for pattern analysis
- Regional statistics
- Dynamic region filtering

### Predictions Page (`/predictions`)
- Interactive sliders for weather factors
- Real-time AQI prediction
- Color-coded risk levels

### Upload Page (`/upload`)
- CSV file upload
- Auto-validation
- Database integration

---

## Test the API

Open `http://127.0.0.1:8000/docs` and try:
- `GET /api/health` → Health check
- `GET /api/data` → All environmental data
- `GET /api/data/stats` → Statistics
- `POST /api/predict` → Predict AQI

**Try prediction with:**
```json
{
  "temperature": 25,
  "humidity": 60,
  "rainfall": 5
}
```

---

## Sample CSV Upload Format

Save as `.csv` and upload via `/upload` page:
```
date,region,temperature,humidity,rainfall,aqi
2024-01-01,North,22.1,55,0.0,85
2024-01-02,Central,30.2,40,0.0,120
```

---

## Troubleshooting

**Backend won't start?**
```bash
# Ensure port 8000 is free
# Verify Python: python --version
# Reinstall: pip install -r backend/requirements.txt
```

**Frontend won't connect?**
- Check backend is running
- Browser console (F12) for errors
- Check `http://127.0.0.1:8000/docs` loads

**ML model not found?**
```bash
python ml/train_model.py
```

---

## Deployment

### Frontend → Vercel
```bash
cd frontend
npm run build
# Connect to Vercel, deploy `build/` folder
```

### Backend → Render/Railway
- Connect GitHub repo
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python 3.11+

---

## Next: Customize!

- Add real data (OpenAQ, NASA, NOAA)
- Train better models (Random Forest, Neural Networks)
- Add user authentication
- Integrate weather APIs
- Deploy to production

---

**Documentation:** See [DEPLOYMENT.md](DEPLOYMENT.md) and [BUILD_SUMMARY.md](BUILD_SUMMARY.md)
