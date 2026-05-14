import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.model import EnvironmentalModel  # noqa: E402


def _make_pipeline():
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

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", LinearRegression()),
        ]
    )
    pipeline.fit(features, target)
    return pipeline


def test_model_wrapper_round_trip(tmp_path):
    pipeline = _make_pipeline()
    wrapper = EnvironmentalModel(
        model=pipeline,
        version="2.1.0",
        metrics={"r2": 0.88, "mse": 2.1, "rmse": 1.45, "mae": 1.05},
    )

    model_path = tmp_path / "model.joblib"
    wrapper.save(str(model_path))

    loaded = EnvironmentalModel.load(str(model_path))
    assert loaded.version == "2.1.0"
    assert loaded.scaler is not None
    assert loaded.validate_preprocessing()["has_scaler"] is True

    result = loaded.predict(25.0, 65.0, 10.0)
    assert "predicted_aqi" in result
    assert result["model_version"] == "2.1.0"


def test_model_wrapper_input_validation():
    pipeline = _make_pipeline()
    wrapper = EnvironmentalModel(model=pipeline)

    try:
        wrapper.build_features(25.0, 120.0, 10.0)
        assert False, "Expected validation to fail for humidity > 100"
    except ValueError as exc:
        assert "Humidity must be 0-100" in str(exc)
