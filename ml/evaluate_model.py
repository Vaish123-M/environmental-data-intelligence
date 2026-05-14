"""
Evaluation script for the saved model.
Computes MAE, RMSE, and R² on the sample dataset and writes a residuals plot to `ml/plots/evaluation_residuals.png`.
Run from project root:

    python ml/evaluate_model.py

"""

import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Use shared preprocessing utilities
from .preprocess import load_and_preprocess

ROOT = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(ROOT, "backend", "models", "model.joblib")
DATA_PATH = os.path.join(
    os.path.dirname(__file__), "sample_data", "air_quality_real.csv"
)
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")

# Feature columns used in training
FEATURE_COLS = [
    "temperature",
    "humidity",
    "rainfall",
    "temp_humidity_interaction",
    "temp_rainfall_interaction",
]


def evaluate():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run `python ml/train_model.py` first."
        )

    print(f"Loading model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    print(f"Reading data from: {DATA_PATH}")
    df = load_and_preprocess(DATA_PATH)

    if "aqi" not in df.columns:
        raise ValueError(
            "`aqi` column not found in data; cannot evaluate without true labels."
        )

    X = df[FEATURE_COLS].fillna(0)
    y_true = df["aqi"]

    print(f"Predicting on {len(X)} samples...")
    y_pred = model.predict(X)

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    print("Evaluation results:")
    print(f"  MAE:  {mae:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R2:   {r2:.4f}")

    # Save residuals plot
    os.makedirs(PLOTS_DIR, exist_ok=True)
    resid = y_true - y_pred
    plt.figure(figsize=(8, 5))
    plt.scatter(y_pred, resid, alpha=0.5)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Predicted AQI")
    plt.ylabel("Residual (True - Predicted)")
    plt.title("Residuals vs Predicted")
    out_png = os.path.join(PLOTS_DIR, "evaluation_residuals.png")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    print(f"Saved residuals plot to: {out_png}")

    # return metrics for programmatic use
    return {"mae": mae, "rmse": rmse, "r2": r2}


if __name__ == "__main__":
    evaluate()
