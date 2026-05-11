from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Environmental Data Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    temperature: float
    humidity: float
    rainfall: float


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/data")
def get_sample_data():
    # Return the sample CSV bundled in the repo
    sample = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "sample_data", "air_quality_sample.csv")
    if not os.path.exists(sample):
        raise HTTPException(status_code=404, detail="Sample data not found")
    df = pd.read_csv(sample)
    return df.to_dict(orient="records")


@app.post("/api/predict")
def predict(req: PredictRequest):
    # Try to load model, else fallback to a simple heuristic
    model_file = os.path.abspath(MODEL_PATH)
    if os.path.exists(model_file):
        model = joblib.load(model_file)
        X = [[req.temperature, req.humidity, req.rainfall]]
        pred = model.predict(X)[0]
        return {"predicted_aqi": float(pred)}
    # fallback heuristic
    pred = 0.5 * req.temperature + 0.3 * req.humidity + 0.2 * (100 - req.rainfall)
    return {"predicted_aqi": float(pred), "warning": "Model not found; returned heuristic estimate."}
