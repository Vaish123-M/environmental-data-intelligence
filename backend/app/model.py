"""
Model wrapper with versioning, preprocessing consistency, and metadata.

This module provides a unified interface for loading, versioning, and serving
the trained ML model with guaranteed preprocessing consistency.
"""

import os
import json
import joblib
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


logger = logging.getLogger(__name__)


class EnvironmentalModel:
    """
    Wrapper for environmental data ML model with versioning and preprocessing.
    
    Attributes:
        model: Trained sklearn pipeline or model
        version: Model version string
        created_at: Timestamp of model creation
        metrics: Dict of model performance metrics
        features: List of feature names expected by model
        scaler: StandardScaler for consistent preprocessing
    """

    # Expected feature names (must match training pipeline)
    FEATURE_NAMES = [
        "temperature",
        "humidity", 
        "rainfall",
        "temp_humidity_interaction",
        "temp_rainfall_interaction",
    ]
    
    # Valid input features for interaction calculation
    BASE_FEATURES = ["temperature", "humidity", "rainfall"]
    
    def __init__(
        self,
        model: Pipeline,
        version: str = "1.0.0",
        metrics: Dict[str, float] = None,
        created_at: str = None,
    ):
        """
        Initialize model wrapper.
        
        Args:
            model: Trained sklearn Pipeline with preprocessing
            version: Semantic version string
            metrics: Dict with keys: r2, mse, rmse, mae
            created_at: ISO format timestamp
        """
        self.model = model
        self.version = version
        self.metrics = metrics or {}
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.features = self.FEATURE_NAMES.copy()
        
        # Extract scaler if available (for consistent preprocessing)
        self.scaler = None
        if isinstance(model, Pipeline) and "scaler" in model.named_steps:
            self.scaler = model.named_steps["scaler"]
    
    def build_features(self, temperature: float, humidity: float, rainfall: float) -> np.ndarray:
        """
        Build complete feature vector with interactions.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity as percentage (0-100)
            rainfall: Rainfall in mm
            
        Returns:
            numpy array of shape (1, 5) with interaction features
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        if not all(isinstance(x, (int, float)) for x in [temperature, humidity, rainfall]):
            raise ValueError("All inputs must be numeric")
        
        if not (-50 <= temperature <= 60):
            logger.warning(f"Temperature {temperature} outside typical range [-50, 60]")
        if not (0 <= humidity <= 100):
            raise ValueError(f"Humidity must be 0-100, got {humidity}")
        if rainfall < 0:
            raise ValueError(f"Rainfall cannot be negative, got {rainfall}")
        
        # Compute interaction features
        temp_humidity = temperature * humidity
        temp_rainfall = temperature * rainfall
        
        # Return as 2D array (1, 5) for sklearn compatibility
        return np.array([[
            temperature,
            humidity,
            rainfall,
            temp_humidity,
            temp_rainfall,
        ]])
    
    def predict(self, temperature: float, humidity: float, rainfall: float) -> Dict[str, Any]:
        """
        Predict AQI from environmental parameters.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity as percentage (0-100)
            rainfall: Rainfall in mm
            
        Returns:
            Dict with predicted_aqi, model_version, confidence
            
        Raises:
            ValueError: If inputs are invalid
        """
        try:
            # Build and validate features
            features = self.build_features(temperature, humidity, rainfall)
            
            # Predict using pipeline (includes scaler)
            prediction = self.model.predict(features)[0]
            
            # Ensure AQI is valid (0-500+ typical range)
            if prediction < 0:
                logger.warning(f"Negative AQI prediction {prediction}; clamping to 0")
                prediction = max(0, prediction)
            
            return {
                "predicted_aqi": float(prediction),
                "model_version": self.version,
                "features_used": {
                    "temperature": temperature,
                    "humidity": humidity,
                    "rainfall": rainfall,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get model metadata for logging/auditing."""
        return {
            "version": self.version,
            "created_at": self.created_at,
            "model_type": type(self.model).__name__,
            "features": self.features,
            "metrics": self.metrics,
            "has_scaler": self.scaler is not None,
        }
    
    def save(self, path: str) -> None:
        """
        Save model and metadata to file.
        Saves pipeline and metadata separately to avoid pickling class references.
        
        Args:
            path: Path to save model.joblib file
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the underlying pipeline model (not the wrapper)
        joblib.dump(self.model, path)
        logger.info(f"Model pipeline saved to {path}")
        
        # Save metadata as JSON
        metadata = self.get_metadata()
        metadata_path = path.replace(".joblib", "_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Model metadata saved to {metadata_path}")
        
        # Save version and metrics for quick reference
        version_path = path.replace(".joblib", "_version.txt")
        with open(version_path, "w") as f:
            f.write(self.version)
    
    @classmethod
    def load(cls, path: str) -> "EnvironmentalModel":
        """
        Load model wrapper from file.
        Reconstructs wrapper from saved pipeline and metadata.
        
        Args:
            path: Path to model.joblib file
            
        Returns:
            EnvironmentalModel instance
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found at {path}")
        
        try:
            # Load the pipeline (not a class reference)
            pipeline = joblib.load(path)
            logger.info(f"Pipeline loaded from {path}")
            
            # Try to load metadata
            metadata_path = path.replace(".joblib", "_metadata.json")
            metrics = {}
            version = "1.0.0"
            created_at = datetime.utcnow().isoformat()
            
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    version = metadata.get("version", "1.0.0")
                    metrics = metadata.get("metrics", {})
                    created_at = metadata.get("created_at", created_at)
                logger.info(f"Metadata loaded from {metadata_path}")
            
            # Reconstruct the wrapper
            wrapper = cls(
                model=pipeline,
                version=version,
                metrics=metrics,
                created_at=created_at,
            )
            logger.info(f"Model wrapper reconstructed: v{wrapper.version}")
            return wrapper
            
        except Exception as e:
            logger.error(f"Failed to load model: {type(e).__name__}: {str(e)}")
            raise
    
    def validate_preprocessing(self) -> Dict[str, bool]:
        """
        Validate that preprocessing pipeline is correctly configured.
        
        Returns:
            Dict with validation status for each component
        """
        checks = {
            "is_pipeline": isinstance(self.model, Pipeline),
            "has_scaler": self.scaler is not None,
            "has_regressor": False,
            "feature_count_correct": len(self.features) == 5,
        }
        
        if checks["is_pipeline"]:
            checks["has_regressor"] = "regressor" in self.model.named_steps or "randomforestregressor" in self.model.named_steps
        
        return checks


def create_model_from_pipeline(
    pipeline: Pipeline,
    metrics: Dict[str, float] = None,
    version: str = "1.0.0",
) -> EnvironmentalModel:
    """
    Wrap a trained sklearn Pipeline in EnvironmentalModel.
    
    Args:
        pipeline: Trained Pipeline with StandardScaler + Regressor
        metrics: Model performance metrics (optional)
        version: Semantic version string
        
    Returns:
        EnvironmentalModel instance
    """
    return EnvironmentalModel(
        model=pipeline,
        version=version,
        metrics=metrics or {},
        created_at=datetime.utcnow().isoformat(),
    )


def load_or_create_model(model_path: str, fallback_pipeline: Pipeline = None) -> EnvironmentalModel:
    """
    Load model from disk or create from fallback pipeline.
    
    Args:
        model_path: Path to saved model
        fallback_pipeline: Sklearn Pipeline to wrap if model_path doesn't exist
        
    Returns:
        EnvironmentalModel instance
    """
    # Try to load saved model first
    if os.path.exists(model_path):
        try:
            return EnvironmentalModel.load(model_path)
        except Exception as e:
            logger.warning(f"Failed to load model from {model_path}: {e}")
    
    # Fallback to creating wrapper around pipeline
    if fallback_pipeline is not None:
        logger.warning("Creating model wrapper from fallback pipeline")
        return create_model_from_pipeline(fallback_pipeline)
    
    raise RuntimeError(f"No model available at {model_path} and no fallback provided")
