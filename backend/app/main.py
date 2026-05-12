from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from io import BytesIO, StringIO
import pandas as pd
import joblib
import os
import csv
import json
import logging
from datetime import datetime

from .database import SessionLocal, EnvironmentalData, get_db
from .schemas import EnvironmentalDataSchema, PredictRequest, PredictResponse
from .model import EnvironmentalModel

logger = logging.getLogger(__name__)

app = FastAPI(title="Environmental Data Intelligence API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "sample_data", "air_quality_real.csv")
PLOTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "plots")

# Mount plots directory for serving model comparison visualizations
if os.path.exists(PLOTS_PATH):
    app.mount("/api/plots", StaticFiles(directory=PLOTS_PATH), name="plots")

# Global model variable and loader function
model = None

def get_model():
    """Lazy-load model on first access."""
    global model
    if model is None:
        try:
            model_path = os.path.abspath(MODEL_PATH)
            logger.info(f"[LOAD] Trying model path: {model_path}")
            logger.info(f"[LOAD] Path exists: {os.path.exists(model_path)}")
            if os.path.exists(model_path):
                model = EnvironmentalModel.load(model_path)
                logger.info(f"[LOAD] Model v{model.version} loaded")
            else:
                logger.warning(f"[LOAD] Model not found at {model_path}")
        except Exception as e:
            logger.error(f"[LOAD] Error: {type(e).__name__}: {str(e)}")
            model = None
    return model


@app.get("/api/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/models/comparison")
def get_model_comparison():
    """Get ML model comparison metrics (Linear Regression vs Random Forest) with plot URLs"""
    try:
        comparison_file = os.path.join(os.path.dirname(__file__), "..", "models", "model_comparison.json")
        plots = {
            "metrics_comparison": "/api/plots/01_metrics_comparison.png",
            "predictions_vs_actual": "/api/plots/02_predictions_vs_actual.png",
            "residuals": "/api/plots/03_residuals.png",
            "feature_importance": "/api/plots/04_feature_importance.png",
        }
        
        if os.path.exists(comparison_file):
            with open(comparison_file, 'r') as f:
                comparison = json.load(f)
            return {
                "models": comparison,
                "best_model": comparison.get("best_model", "linear_regression"),
                "plots": plots
            }
        else:
            return {
                "models": {
                    "linear_regression": {"r2": 0, "mse": 0, "rmse": 0, "mae": 0},
                    "random_forest": {"r2": 0, "mse": 0, "rmse": 0, "mae": 0}
                },
                "best_model": "linear_regression",
                "plots": plots,
                "warning": "Model comparison data not found; running training..."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/metadata")
def get_model_metadata():
    """Get model versioning, preprocessing, and metadata information"""
    try:
        m = get_model()
        
        if m is not None and isinstance(m, EnvironmentalModel):
            metadata = m.get_metadata()
            checks = m.validate_preprocessing()
            return {
                "model_info": metadata,
                "preprocessing_validation": checks,
                "status": "ok"
            }
        else:
            return {
                "status": "model_not_loaded",
                "warning": "Could not load model for metadata"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/evaluation/summary")
def get_evaluation_summary():
    """Return a compact evaluation summary for the dashboard."""
    try:
        comparison_file = os.path.join(os.path.dirname(__file__), "..", "models", "model_comparison.json")
        metadata_file = os.path.join(os.path.dirname(__file__), "..", "models", "model_metadata.json")
        model_info = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                model_info = json.load(f)

        comparison = {}
        if os.path.exists(comparison_file):
            with open(comparison_file, "r") as f:
                comparison = json.load(f)

        return {
            "status": "ok",
            "model_info": model_info,
            "comparison": comparison,
            "plots": {
                "metrics_comparison": "/api/plots/01_metrics_comparison.png",
                "predictions_vs_actual": "/api/plots/02_predictions_vs_actual.png",
                "residuals": "/api/plots/03_residuals.png",
                "feature_importance": "/api/plots/04_feature_importance.png",
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data")
def get_sample_data(db: Session = Depends(get_db)):
    """Get environmental data from database or sample CSV"""
    try:
        # Try to get from database first
        db_data = db.query(EnvironmentalData).all()
        if db_data:
            return [
                {
                    "date": d.date,
                    "region": d.region,
                    "temperature": d.temperature,
                    "humidity": d.humidity,
                    "rainfall": d.rainfall,
                    "aqi": d.aqi,
                }
                for d in db_data
            ]
        
        # Fall back to sample CSV
        if os.path.exists(SAMPLE_DATA_PATH):
            df = pd.read_csv(SAMPLE_DATA_PATH)
            return df.to_dict(orient="records")
        
        raise HTTPException(status_code=404, detail="No data available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/stats")
def get_data_stats(db: Session = Depends(get_db)):
    """Get statistical summary of environmental data"""
    try:
        data = db.query(EnvironmentalData).all()
        if not data:
            # Try sample data
            if os.path.exists(SAMPLE_DATA_PATH):
                df = pd.read_csv(SAMPLE_DATA_PATH)
            else:
                raise HTTPException(status_code=404, detail="No data available")
        else:
            df = pd.DataFrame([
                {
                    "temperature": d.temperature,
                    "humidity": d.humidity,
                    "rainfall": d.rainfall,
                    "aqi": d.aqi,
                }
                for d in data
            ])

        return {
            "avg_aqi": float(df["aqi"].mean()),
            "max_aqi": float(df["aqi"].max()),
            "min_aqi": float(df["aqi"].min()),
            "avg_temperature": float(df["temperature"].mean()),
            "max_temperature": float(df["temperature"].max()),
            "avg_humidity": float(df["humidity"].mean()),
            "avg_rainfall": float(df["rainfall"].mean()),
            "record_count": len(df),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/regions")
def get_regions(db: Session = Depends(get_db)):
    """Get unique regions in the dataset"""
    try:
        data = db.query(EnvironmentalData.region).distinct().all()
        regions = [d[0] for d in data]
        
        if not regions:
            # Try sample data
            if os.path.exists(SAMPLE_DATA_PATH):
                df = pd.read_csv(SAMPLE_DATA_PATH)
                regions = df["region"].unique().tolist()
            else:
                regions = []
        
        return {"regions": regions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Predict AQI based on environmental factors using wrapped model with versioning"""
    try:
        m = get_model()
        
        # Use wrapped model for prediction (includes preprocessing)
        if m is not None and isinstance(m, EnvironmentalModel):
            result = m.predict(req.temperature, req.humidity, req.rainfall)
            return PredictResponse(
                predicted_aqi=result["predicted_aqi"],
                model_version=result.get("model_version", "1.0.0"),
            )
        
        # Fallback heuristic if model unavailable
        logger.warning("Using fallback heuristic prediction")
        pred = 0.5 * req.temperature + 0.3 * req.humidity + 0.2 * (100 - req.rainfall)
        return PredictResponse(
            predicted_aqi=float(pred),
            warning="Model not found; using heuristic estimate."
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process CSV file with environmental data"""
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        
        # Validate columns
        required_cols = {"date", "region", "temperature", "humidity", "rainfall", "aqi"}
        if not required_cols.issubset(set(df.columns)):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {required_cols - set(df.columns)}"
            )
        
        # Insert into database
        inserted_count = 0
        for _, row in df.iterrows():
            record = EnvironmentalData(
                date=str(row["date"]),
                region=str(row["region"]),
                temperature=float(row["temperature"]),
                humidity=float(row["humidity"]),
                rainfall=float(row["rainfall"]),
                aqi=float(row["aqi"]),
            )
            db.add(record)
            inserted_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {inserted_count} records",
            "records_inserted": inserted_count,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/by-region/{region}")
def get_data_by_region(region: str, db: Session = Depends(get_db)):
    """Get environmental data for a specific region"""
    try:
        data = db.query(EnvironmentalData).filter(EnvironmentalData.region == region).all()
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No data for region: {region}")
        
        return [
            {
                "date": d.date,
                "region": d.region,
                "temperature": d.temperature,
                "humidity": d.humidity,
                "rainfall": d.rainfall,
                "aqi": d.aqi,
            }
            for d in data
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/data")
def clear_data(db: Session = Depends(get_db)):
    """Clear all data from the database"""
    try:
        db.query(EnvironmentalData).delete()
        db.commit()
        return {"message": "All data deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
