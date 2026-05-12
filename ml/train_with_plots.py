"""Enhanced ML pipeline with model comparison plots and detailed metrics.

Generates:
- model_comparison.json with metrics
- plots/ folder with comparison charts (metrics, residuals, feature importance)
- Detailed stdout report
- Wrapped model with versioning and preprocessing consistency

Run: python ml/train_with_plots.py
"""

import os
import json
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

# Add backend to path for model wrapper import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.model import EnvironmentalModel, create_model_from_pipeline

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Note: matplotlib not installed; skipping plots")

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data", "air_quality_real.csv")
MODEL_OUT = os.path.join(os.path.dirname(__file__), "..", "backend", "models", "model.joblib")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")


def load_and_preprocess():
    """Load and preprocess data."""
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    df = df.fillna(df.mean(numeric_only=True))
    df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
    df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]
    return df


def train_model(df):
    """Train and compare multiple ML models."""
    print("\nPreparing features...")

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
    print(f"Target variable: AQI")
    print(f"Samples: {len(X)}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    models = {}
    results = {}
    y_predictions = {}

    # ===== LINEAR REGRESSION =====
    print("\n" + "=" * 50)
    print("Training Linear Regression model...")
    print("=" * 50)
    lr_model = Pipeline([("scaler", StandardScaler()), ("regressor", LinearRegression())])
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)

    lr_metrics = {
        "mse": mean_squared_error(y_test, y_pred_lr),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        "mae": mean_absolute_error(y_test, y_pred_lr),
        "r2": r2_score(y_test, y_pred_lr),
    }

    print(f"\nLinear Regression Performance:")
    print(f"  MSE:  {lr_metrics['mse']:.4f}")
    print(f"  RMSE: {lr_metrics['rmse']:.4f}")
    print(f"  MAE:  {lr_metrics['mae']:.4f}")
    print(f"  R2:   {lr_metrics['r2']:.4f}")

    models["linear_regression"] = lr_model
    results["linear_regression"] = lr_metrics
    y_predictions["linear_regression"] = y_pred_lr

    # ===== RANDOM FOREST =====
    print("\n" + "=" * 50)
    print("Training Random Forest model...")
    print("=" * 50)
    rf_model = RandomForestRegressor(
        n_estimators=100, max_depth=10, min_samples_split=2, random_state=42, n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    rf_metrics = {
        "mse": mean_squared_error(y_test, y_pred_rf),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        "mae": mean_absolute_error(y_test, y_pred_rf),
        "r2": r2_score(y_test, y_pred_rf),
    }

    print(f"\nRandom Forest Performance:")
    print(f"  MSE:  {rf_metrics['mse']:.4f}")
    print(f"  RMSE: {rf_metrics['rmse']:.4f}")
    print(f"  MAE:  {rf_metrics['mae']:.4f}")
    print(f"  R2:   {rf_metrics['r2']:.4f}")

    models["random_forest"] = rf_model
    results["random_forest"] = rf_metrics
    y_predictions["random_forest"] = y_pred_rf

    # ===== COMPARISON TABLE =====
    print("\n" + "=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)
    print(f"{'Metric':<15} {'Linear Reg':<15} {'Random Forest':<15} {'Winner'}")
    print("-" * 60)

    for metric in ["r2", "mse", "rmse", "mae"]:
        lr_val = results["linear_regression"][metric]
        rf_val = results["random_forest"][metric]
        winner = "RF" if (metric == "r2" and rf_val > lr_val) or (metric != "r2" and rf_val < lr_val) else "LR"
        print(f"{metric.upper():<15} {lr_val:<15.4f} {rf_val:<15.4f} {winner}")

    best_model_name = (
        "random_forest"
        if results["random_forest"]["r2"] > results["linear_regression"]["r2"]
        else "linear_regression"
    )
    best_model = models[best_model_name]
    best_metrics = results[best_model_name]

    print(f"\n[BEST] Best Model: {best_model_name.replace('_', ' ').title()}")
    print(f"  R2 Score: {best_metrics['r2']:.4f}")

    # Generate plots if matplotlib available
    if MATPLOTLIB_AVAILABLE:
        generate_plots(
            X_test, y_test, y_predictions, feature_cols, models, results, best_model_name
        )

    comparison_data = {
        "linear_regression": results["linear_regression"],
        "random_forest": results["random_forest"],
        "best_model": best_model_name,
    }

    return best_model, comparison_data


def generate_plots(X_test, y_test, y_predictions, feature_cols, models, results, best_model_name):
    """Generate comparison plots."""
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # 1. Metrics Comparison Bar Chart
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Model Comparison: Metrics", fontsize=14, fontweight="bold")

    metrics = ["r2", "mse", "rmse", "mae"]
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for metric, pos in zip(metrics, positions):
        ax = axes[pos]
        lr_val = results["linear_regression"][metric]
        rf_val = results["random_forest"][metric]
        bars = ax.bar(["Linear Reg", "Random Forest"], [lr_val, rf_val], color=["#3498db", "#e74c3c"])
        ax.set_ylabel(metric.upper())
        ax.set_title(f"{metric.upper()}")
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
            )

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "01_metrics_comparison.png"), dpi=100, bbox_inches="tight")
    print(f"\n[PLOT] Saved metrics_comparison.png")
    plt.close()

    # 2. Predictions vs Actual
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Actual vs Predicted AQI", fontsize=14, fontweight="bold")

    models_to_plot = ["linear_regression", "random_forest"]
    for ax, model_name in zip(axes, models_to_plot):
        y_pred = y_predictions[model_name]
        ax.scatter(y_test, y_pred, alpha=0.6, s=100)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
        ax.set_xlabel("Actual AQI")
        ax.set_ylabel("Predicted AQI")
        ax.set_title(f"{model_name.replace('_', ' ').title()} (R2={results[model_name]['r2']:.3f})")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "02_predictions_vs_actual.png"), dpi=100, bbox_inches="tight")
    print(f"[PLOT] Saved predictions_vs_actual.png")
    plt.close()

    # 3. Residuals Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Residuals (Prediction Errors)", fontsize=14, fontweight="bold")

    for ax, model_name in zip(axes, models_to_plot):
        y_pred = y_predictions[model_name]
        residuals = y_test - y_pred
        ax.scatter(y_pred, residuals, alpha=0.6, s=100)
        ax.axhline(y=0, color="r", linestyle="--", lw=2)
        ax.set_xlabel("Predicted AQI")
        ax.set_ylabel("Residuals")
        ax.set_title(f"{model_name.replace('_', ' ').title()}")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "03_residuals.png"), dpi=100, bbox_inches="tight")
    print(f"[PLOT] Saved residuals.png")
    plt.close()

    # 4. Feature Importance (Random Forest)
    rf_model = models["random_forest"]
    fig, ax = plt.subplots(figsize=(10, 6))
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]

    ax.bar(range(len(importances)), importances[indices])
    ax.set_xlabel("Feature")
    ax.set_ylabel("Importance")
    ax.set_title("Random Forest Feature Importance")
    ax.set_xticks(range(len(importances)))
    ax.set_xticklabels([feature_cols[i] for i in indices], rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "04_feature_importance.png"), dpi=100, bbox_inches="tight")
    print(f"[PLOT] Saved feature_importance.png")
    plt.close()


def main():
    df = load_and_preprocess()
    model, comparison = train_model(df)

    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    
    # Wrap model with versioning and preprocessing consistency
    best_model_name = comparison.get("best_model", "linear_regression")
    best_metrics = comparison[best_model_name]
    
    wrapped_model = create_model_from_pipeline(
        pipeline=model,
        metrics=best_metrics,
        version="1.0.0",
    )
    
    # Save wrapped model (includes metadata)
    wrapped_model.save(MODEL_OUT)
    print(f"\n[OK] Wrapped model saved to {MODEL_OUT}")
    print(f"[OK] Model metadata includes: version, metrics, preprocessing info")
    
    # Validate preprocessing
    checks = wrapped_model.validate_preprocessing()
    print(f"[OK] Preprocessing validation: {checks}")

    # Save model comparison separately
    comparison_out = os.path.join(os.path.dirname(MODEL_OUT), "model_comparison.json")
    with open(comparison_out, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"[OK] Model comparison saved to {comparison_out}")
    print(f"\n[NOTE] Plots saved to {PLOTS_DIR}/" if MATPLOTLIB_AVAILABLE else "")


if __name__ == "__main__":
    main()
