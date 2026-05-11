"""
Train a simple scikit-learn model on the included sample data and save it to backend/models.
Run: python ml/train_model.py
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data", "air_quality_sample.csv")
MODEL_OUT = os.path.join(os.path.dirname(__file__), "..", "backend", "models", "model.joblib")


def main():
    df = pd.read_csv(DATA_PATH)
    # Simple features
    X = df[["temperature", "humidity", "rainfall"]].fillna(0)
    y = df["aqi"]
    model = LinearRegression()
    model.fit(X, y)
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f"Saved model to {MODEL_OUT}")


if __name__ == "__main__":
    main()
