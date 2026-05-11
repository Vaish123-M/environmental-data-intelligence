# Environmental Data Intelligence Platform - Setup & Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+ (backend)
- Node.js 16+ (frontend)
- Git

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train ML model:
```bash
python ../ml/train_model.py
```

4. Start backend server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at `http://127.0.0.1:8000`
API docs available at `http://127.0.0.1:8000/docs`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm start
```

Frontend will open at `http://localhost:3000`

3. Build for production:
```bash
npm run build
```

## API Endpoints

### Health & Data
- `GET /api/health` - Health check
- `GET /api/data` - Get all environmental data
- `GET /api/data/stats` - Get data statistics
- `GET /api/data/regions` - Get unique regions
- `GET /api/data/by-region/{region}` - Get data for specific region

### Predictions
- `POST /api/predict` - Predict AQI (requires: temperature, humidity, rainfall)

### Data Management
- `POST /api/upload` - Upload CSV file
- `DELETE /api/data` - Clear all data

## Database

Uses SQLite (`environmental_data.db`) for local development.
Automatically created on first run.

To use PostgreSQL in production:
1. Install PostgreSQL
2. Update `DATABASE_URL` in `backend/app/database.py`
3. Ensure connection details are correct

## Deployment

### Vercel (Frontend)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variable: `REACT_APP_API_URL=<your-backend-url>`
4. Deploy

### Render or Railway (Backend)

1. Create new Web Service
2. Connect GitHub repository
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Configure environment (Python 3.11)
5. Deploy

## Project Structure

```
environmental-data-intelligence/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── Analytics.js
│   │   │   ├── Predictions.js
│   │   │   └── Upload.js
│   │   ├── components/
│   │   │   └── Navbar.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   └── __init__.py
│   ├── models/
│   └── requirements.txt
├── ml/
│   ├── sample_data/
│   │   └── air_quality_sample.csv
│   └── train_model.py
└── README.md
```

## Features

### Dashboard
- Real-time environmental statistics
- Interactive charts (AQI, Temperature, Humidity, Rainfall)
- Regional analysis
- Raw data table

### Analytics
- Correlation analysis
- Scatter plots
- Regional statistics
- Customizable filters

### Predictions
- Interactive sliders for environmental factors
- Real-time AQI prediction
- AQI level indicators

### Data Upload
- CSV file upload
- Automatic data validation
- Database integration

## Technologies Used

**Frontend:**
- React 18
- React Router
- Recharts (visualizations)
- Axios (API calls)
- Tailwind CSS

**Backend:**
- FastAPI
- SQLAlchemy ORM
- Pandas
- Scikit-learn
- SQLite/PostgreSQL

**ML/AI:**
- Linear Regression
- Data preprocessing
- Feature engineering
- Model evaluation

## Future Enhancements

1. User authentication and authorization
2. Advanced ML models (Random Forest, Neural Networks)
3. Real-time data integration (weather APIs, satellite data)
4. Geospatial visualizations (Mapbox/Leaflet)
5. LLM-powered insights and report generation
6. Automated alerts for anomalies
7. Data export to multiple formats
8. Multi-language support

## Troubleshooting

**Backend won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check port 8000 is not in use
- Verify Python path: `which python` (or `where python` on Windows)

**Frontend connection issues:**
- Ensure backend is running on `http://127.0.0.1:8000`
- Check CORS is enabled (should be by default)
- Open browser developer console for error details

**Database issues:**
- Delete `environmental_data.db` and restart backend to reset
- Ensure SQLite is installed (usually bundled with Python)

## Support & Documentation

- API Swagger Docs: `http://127.0.0.1:8000/docs`
- API ReDoc: `http://127.0.0.1:8000/redoc`

## License

Educational and research use.
