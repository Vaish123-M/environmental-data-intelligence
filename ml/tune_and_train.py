"""
Hyperparameter tuning and training script.
Runs a randomized search on RandomForest hyperparameters, fits on training data,
and saves the best pipeline and metadata for serving.

Usage:
    python ml/tune_and_train.py
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

ROOT = os.path.dirname(__file__)
DATA_PATH = os.path.join(ROOT, "sample_data", "air_quality_real.csv")
MODEL_OUT = os.path.join(ROOT, "..", "backend", "models", "model.joblib")
MODEL_METADATA_OUT = os.path.join(
    ROOT, "..", "backend", "models", "model_metadata.json"
)
COMPARISON_OUT = os.path.join(ROOT, "..", "backend", "models", "model_comparison.json")


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df = df.fillna(df.mean(numeric_only=True))
    df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
    df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]
    return df


def build_pipeline():
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", RandomForestRegressor(random_state=42)),
        ]
    )
    return pipeline


def tune_and_train(df):
    feature_cols = [
        "temperature",
        "humidity",
        "rainfall",
        "temp_humidity_interaction",
        "temp_rainfall_interaction",
    ]
    X = df[feature_cols].fillna(0)
    y = df["aqi"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = build_pipeline()

    param_dist = {
        "regressor__n_estimators": [50, 100, 200, 300],
        "regressor__max_depth": [5, 10, 20, None],
        "regressor__min_samples_split": [2, 5, 10],
        "regressor__min_samples_leaf": [1, 2, 4],
    }

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_dist,
        n_iter=12,
        cv=3,
        scoring="r2",
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )

    print("Starting randomized search for best hyperparameters...")
    search.fit(X_train, y_train)

    print(f"Best params: {search.best_params_}")

    best = search.best_estimator_
    y_pred = best.predict(X_test)

    metrics = {
        "mse": float(mean_squared_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
    }

    comparison = {
        "random_forest": metrics,
        "linear_regression": {},
        "best_model": "random_forest",
        "best_params": {k: v for k, v in search.best_params_.items()},
    }

    # Save model and metadata
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(best, MODEL_OUT)
    metadata = {
        "version": "1.0.0",
        "created_at": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "params": {k: v for k, v in search.best_params_.items()},
        "features": feature_cols,
    }
    with open(MODEL_METADATA_OUT, "w") as f:
        json.dump(metadata, f, indent=2)

    with open(COMPARISON_OUT, "w") as f:
        json.dump(comparison, f, indent=2)

    print(f"Saved tuned model to {MODEL_OUT}")
    print(f"Saved metadata to {MODEL_METADATA_OUT}")
    print(f"Saved comparison to {COMPARISON_OUT}")


def main():
    df = load_data()
    tune_and_train(df)


if __name__ == "__main__":
    main()
