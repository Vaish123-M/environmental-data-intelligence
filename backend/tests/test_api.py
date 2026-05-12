import os
import sys

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


import app.main as main_module
from app.model import EnvironmentalModel


client = TestClient(main_module.app)


def _build_test_wrapper(version="9.9.9"):
    features = pd.DataFrame(
        [
            [20.0, 60.0, 5.0, 1200.0, 100.0],
            [25.0, 70.0, 8.0, 1750.0, 200.0],
            [30.0, 40.0, 1.0, 1200.0, 30.0],
            [35.0, 55.0, 0.0, 1925.0, 0.0],
        ],
        columns=EnvironmentalModel.FEATURE_NAMES,
    )
    target = np.array([60.0, 70.0, 40.0, 35.0])

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", LinearRegression()),
    ])
    pipeline.fit(features, target)
    return EnvironmentalModel(model=pipeline, version=version, metrics={"r2": 0.91, "mse": 1.2, "rmse": 1.1, "mae": 0.8})


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}


def test_model_comparison_endpoint():
    response = client.get("/api/models/comparison")
    assert response.status_code == 200
    payload = response.json()
    assert "models" in payload
    assert "plots" in payload
    assert payload["best_model"] in {"linear_regression", "random_forest"}


def test_predict_endpoint_uses_model(monkeypatch):
    monkeypatch.setattr(main_module, "get_model", lambda: _build_test_wrapper())

    response = client.post(
        "/api/predict",
        json={"temperature": 25, "humidity": 65, "rainfall": 10},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["predicted_aqi"] >= 0
    assert payload["model_version"] == "9.9.9"


def test_model_metadata_endpoint(monkeypatch):
    monkeypatch.setattr(main_module, "get_model", lambda: _build_test_wrapper())

    response = client.get("/api/models/metadata")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_info"]["version"] == "9.9.9"
    assert payload["preprocessing_validation"]["has_scaler"] is True


def test_evaluation_summary_endpoint():
    response = client.get("/api/evaluation/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "plots" in payload
