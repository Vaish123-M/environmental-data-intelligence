"""
Shared preprocessing utilities for the ML pipeline.
Keep preprocessing logic centralized so training and evaluation use the same steps.
"""

import os
import pandas as pd


def load_and_preprocess(path=None):
    """Load dataset and apply preprocessing used in training.
    If `path` is None the function will default to ml/sample_data/air_quality_real.csv.
    Returns a DataFrame with derived features.
    """
    if path is None:
        path = os.path.join(
            os.path.dirname(__file__), "sample_data", "air_quality_real.csv"
        )

    df = pd.read_csv(path)
    # Handle missing numeric values
    df = df.fillna(df.mean(numeric_only=True))

    # Feature engineering: add derived features used for training
    if (
        "temperature" in df.columns
        and "humidity" in df.columns
        and "rainfall" in df.columns
    ):
        df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
        df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]

    return df
