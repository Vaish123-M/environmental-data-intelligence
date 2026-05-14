"""
Shared preprocessing utilities for the ML pipeline.

Keeping preprocessing centralized ensures training, evaluation, and inference
all use the same data transformations.
"""

import os

import pandas as pd


DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data", "air_quality_real.csv")
RAW_FEATURES = ["temperature", "humidity", "rainfall"]
ENGINEERED_FEATURES = RAW_FEATURES + [
    "temp_humidity_interaction",
    "temp_rainfall_interaction",
]


def load_and_preprocess(path=None, add_engineered_features=True):
    """Load dataset and apply the preprocessing used in training and evaluation.

    Args:
        path: Optional CSV path. Defaults to the project sample dataset.
        add_engineered_features: Whether to add interaction terms.

    Returns:
        A DataFrame with missing numeric values filled and optional derived features.
    """
    if path is None:
        path = DATA_PATH

    df = pd.read_csv(path)

    # Use a simple and stable imputation strategy for this prototype dataset.
    df = df.fillna(df.mean(numeric_only=True))

    if add_engineered_features and all(column in df.columns for column in RAW_FEATURES):
        df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
        df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]

    return df


def get_feature_columns(use_engineered_features=True):
    """Return the feature columns for the requested feature set."""
    return ENGINEERED_FEATURES if use_engineered_features else RAW_FEATURES
