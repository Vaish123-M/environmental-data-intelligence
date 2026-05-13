"""
Comprehensive ML pipeline for AQI prediction.
Includes data preprocessing, feature engineering, model training, and evaluation.
Run: python ml/train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "sample_data", "air_quality_real.csv"
)
MODEL_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model.joblib"
)
MODEL_METADATA_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model_metadata.json"
)


def load_and_preprocess():
    """Load and preprocess data"""
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)

    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))

    # Feature engineering: add derived features
    df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
    df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]

    return df


def train_model(df):
    """Train and compare multiple ML models"""
    print("\nPreparing features...")

    # Features and target
    feature_cols = [
        "temperature",
        "humidity",
        "rainfall",
        "temp_humidity_interaction",
        "temp_rainfall_interaction",
    ]
    X = df[feature_cols].fillna(0)
    y = df["aqi"]

    print(f"Features: {feature_cols}")
    print("Target variable: AQI")
    print(f"Samples: {len(X)}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    # Store results for comparison
    models = {}
    results = {}

    # ===== LINEAR REGRESSION =====
    print("\n" + "=" * 50)
    print("Training Linear Regression model...")
    print("=" * 50)
    lr_model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", LinearRegression()),
        ]
    )
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)

    lr_metrics = {
        "mse": mean_squared_error(y_test, y_pred_lr),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        "mae": mean_absolute_error(y_test, y_pred_lr),
        "r2": r2_score(y_test, y_pred_lr),
    }

    print("\nLinear Regression Performance:")
    print(f"  MSE:  {lr_metrics['mse']:.4f}")
    print(f"  RMSE: {lr_metrics['rmse']:.4f}")
    print(f"  MAE:  {lr_metrics['mae']:.4f}")
    print(f"  R²:   {lr_metrics['r2']:.4f}")

    print("\nLinear Regression Coefficients:")
    linear_regressor = lr_model.named_steps["regressor"]
    for feat, coef in zip(feature_cols, linear_regressor.coef_):
        print(f"  {feat}: {coef:.4f}")
    print(f"  Intercept: {linear_regressor.intercept_:.4f}")

    models["linear_regression"] = lr_model
    results["linear_regression"] = lr_metrics

    # ===== RANDOM FOREST =====
    print("\n" + "=" * 50)
    print("Training Random Forest model...")
    print("=" * 50)
    # Wrap RandomForest in a Pipeline to ensure consistent preprocessing steps
    rf_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=2,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    rf_pipeline.fit(X_train, y_train)
    rf_model = rf_pipeline
    y_pred_rf = rf_model.predict(X_test)

    rf_metrics = {
        "mse": mean_squared_error(y_test, y_pred_rf),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        "mae": mean_absolute_error(y_test, y_pred_rf),
        "r2": r2_score(y_test, y_pred_rf),
    }

    print("\nRandom Forest Performance:")
    print(f"  MSE:  {rf_metrics['mse']:.4f}")
    print(f"  RMSE: {rf_metrics['rmse']:.4f}")
    print(f"  MAE:  {rf_metrics['mae']:.4f}")
    print(f"  R²:   {rf_metrics['r2']:.4f}")

    print("\nRandom Forest Feature Importances:")
    # rf_model is a Pipeline; extract regressor step for importances
    rf_reg = rf_model.named_steps["regressor"]
    for feat, imp in zip(feature_cols, rf_reg.feature_importances_):
        print(f"  {feat}: {imp:.4f}")

    models["random_forest"] = rf_model
    results["random_forest"] = rf_metrics

    # ===== MODEL COMPARISON =====
    print("\n" + "=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)
    print(f"{'Metric':<15} {'Linear Reg':<15} {'Random Forest':<15} {'Winner'}")
    print("-" * 60)

    for metric in ["r2", "mse", "rmse", "mae"]:
        lr_val = lr_metrics[metric]
        rf_val = rf_metrics[metric]
        # For R², higher is better; for others, lower is better
        if metric == "r2":
            winner = "RF" if rf_val > lr_val else "LR"
        else:
            winner = "RF" if rf_val < lr_val else "LR"
        print(f"{metric.upper():<15} {lr_val:<15.4f} {rf_val:<15.4f} {winner}")

    # Determine best model
    best_model_name = (
        "random_forest"
        if results["random_forest"]["r2"] > results["linear_regression"]["r2"]
        else "linear_regression"
    )
    best_model = models[best_model_name]
    best_metrics = results[best_model_name]

    print(f"\n[BEST] Best Model: {best_model_name.replace('_', ' ').title()}")
    print(f"  R2 Score: {best_metrics['r2']:.4f}")

    # Store comparison data
    comparison_data = {
        "linear_regression": lr_metrics,
        "random_forest": rf_metrics,
        "best_model": best_model_name,
    }

    return best_model, comparison_data


def main():
    df = load_and_preprocess()
    model, comparison = train_model(df)

    # Save model
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f"\n[OK] Model saved to {MODEL_OUT}")

    # Save model metadata for backend consumption
    import json

    metadata = {
        "version": "1.0.0",
        "created_at": datetime.utcnow().isoformat(),
        "features": [
            "temperature",
            "humidity",
            "rainfall",
            "temp_humidity_interaction",
            "temp_rainfall_interaction",
        ],
        "metrics": comparison.get(model_name_from_best(comparison), {}),
    }
    with open(MODEL_METADATA_OUT, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Model metadata saved to {MODEL_METADATA_OUT}")

    # Save model comparison data for backend
    comparison_out = os.path.join(os.path.dirname(MODEL_OUT), "model_comparison.json")
    with open(comparison_out, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"[OK] Model comparison saved to {comparison_out}")


def model_name_from_best(comparison: dict) -> str:
    return comparison.get("best_model", "random_forest")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
