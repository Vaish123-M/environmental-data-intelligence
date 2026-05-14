"""
Comprehensive ML pipeline for AQI prediction.

This training script is intentionally explicit about the data story:
- a small in-repo dataset used as a prototype/demo corpus
- train/validation/test separation
- cross-validation on the training split
- baseline comparison and a feature-engineering ablation study
"""

from datetime import datetime
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .preprocess import get_feature_columns, load_and_preprocess


DATA_PATH = os.path.join(
    os.path.dirname(__file__), "sample_data", "air_quality_real.csv"
)
MODEL_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model.joblib"
)
MODEL_METADATA_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model_metadata.json"
)
MODEL_COMPARISON_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model_comparison.json"
)
SPLITS_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "models", "splits")
RANDOM_STATE = 42


def build_pipeline(regressor):
    """Create a modeling pipeline with consistent preprocessing."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", regressor),
        ]
    )


def metric_bundle(y_true, y_pred):
    """Return common regression metrics in a serializable form."""
    mse = mean_squared_error(y_true, y_pred)
    return {
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def cross_validate_pipeline(pipeline, X_train, y_train, folds=5):
    """Run cross-validation on the training split."""
    n_splits = min(folds, len(X_train))
    if n_splits < 2:
        return {
            "folds": n_splits,
            "r2_mean": None,
            "r2_std": None,
            "mae_mean": None,
            "mae_std": None,
            "rmse_mean": None,
            "rmse_std": None,
        }

    cv = KFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_validate(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring={
            "r2": "r2",
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
        },
        return_train_score=False,
    )

    return {
        "folds": n_splits,
        "r2_mean": float(np.mean(scores["test_r2"])),
        "r2_std": float(np.std(scores["test_r2"])),
        "mae_mean": float(-np.mean(scores["test_mae"])),
        "mae_std": float(np.std(-scores["test_mae"])),
        "rmse_mean": float(-np.mean(scores["test_rmse"])),
        "rmse_std": float(np.std(-scores["test_rmse"])),
    }


def fit_and_evaluate(pipeline, X_train, y_train, X_eval, y_eval, folds=5):
    """Fit a pipeline, compute CV on train, and evaluate on a holdout split."""
    cv_metrics = cross_validate_pipeline(pipeline, X_train, y_train, folds=folds)
    pipeline.fit(X_train, y_train)
    eval_metrics = metric_bundle(y_eval, pipeline.predict(X_eval))
    return pipeline, cv_metrics, eval_metrics


def save_split_csvs(train_features, train_target, val_features, val_target, test_features, test_target):
    """Persist the train/validation/test splits for reproducible evaluation."""
    os.makedirs(SPLITS_DIR, exist_ok=True)

    def attach_target(features, target):
        frame = features.copy().reset_index(drop=True)
        frame["aqi"] = target.reset_index(drop=True)
        return frame

    attach_target(train_features, train_target).to_csv(
        os.path.join(SPLITS_DIR, "train.csv"), index=False
    )
    attach_target(val_features, val_target).to_csv(
        os.path.join(SPLITS_DIR, "val.csv"), index=False
    )
    attach_target(test_features, test_target).to_csv(
        os.path.join(SPLITS_DIR, "test.csv"), index=False
    )


def format_rows(results_by_model):
    """Convert nested model metrics into table rows for JSON/reporting."""
    rows = []
    for model_name, payload in results_by_model.items():
        row = {"model": model_name}
        row.update(payload.get("validation", {}))
        cv = payload.get("cv", {})
        row["cv_r2_mean"] = cv.get("r2_mean")
        row["cv_mae_mean"] = cv.get("mae_mean")
        row["cv_rmse_mean"] = cv.get("rmse_mean")
        rows.append(row)
    return rows


def load_dataset():
    """Load and preprocess the project dataset."""
    print("Loading data...")
    df = load_and_preprocess(DATA_PATH)

    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    return df


def train_model(df):
    """Train and compare multiple ML models with train/val/test separation."""
    print("\nPreparing features...")

    engineered_feature_cols = get_feature_columns(use_engineered_features=True)
    raw_feature_cols = get_feature_columns(use_engineered_features=False)

    X_engineered = df[engineered_feature_cols].fillna(0)
    X_raw = df[raw_feature_cols].fillna(0)
    y = df["aqi"]

    print(f"Engineered features: {engineered_feature_cols}")
    print(f"Raw features: {raw_feature_cols}")
    print("Target variable: AQI")
    print(f"Samples: {len(X_engineered)}")
    print(
        "Dataset scope: small prototype corpus, so evaluation emphasizes methodology over scale."
    )

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X_engineered,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        random_state=RANDOM_STATE,
    )

    raw_train_val, _, raw_y_train_val, _ = train_test_split(
        X_raw,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )
    raw_train, raw_val, raw_y_train, raw_y_val = train_test_split(
        raw_train_val,
        raw_y_train_val,
        test_size=0.25,
        random_state=RANDOM_STATE,
    )

    print(f"\nTrain set size: {len(X_train)}")
    print(f"Validation set size: {len(X_val)}")
    print(f"Test set size: {len(X_test)}")

    candidate_models = {
        "dummy_mean": build_pipeline(DummyRegressor(strategy="mean")),
        "linear_regression": build_pipeline(LinearRegression()),
        "random_forest": build_pipeline(
            RandomForestRegressor(
                n_estimators=200,
                max_depth=6,
                min_samples_split=2,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )
        ),
    }

    candidate_results = {}
    fitted_models = {}

    print("\n" + "=" * 70)
    print("BASELINE COMPARISON TABLE")
    print("=" * 70)
    print(f"{'Model':<20} {'CV R2':<10} {'CV MAE':<10} {'Val R2':<10} {'Val RMSE':<10}")
    print("-" * 70)

    best_model_name = None
    best_selection_score = None

    for model_name, pipeline in candidate_models.items():
        trained_pipeline, cv_metrics, validation_metrics = fit_and_evaluate(
            pipeline,
            X_train,
            y_train,
            X_val,
            y_val,
        )
        candidate_results[model_name] = {
            "cv": cv_metrics,
            "validation": validation_metrics,
        }
        fitted_models[model_name] = trained_pipeline

        print(
            f"{model_name:<20} {cv_metrics['r2_mean']:<10.4f} {cv_metrics['mae_mean']:<10.4f} "
            f"{validation_metrics['r2']:<10.4f} {validation_metrics['rmse']:<10.4f}"
        )

        selection_score = validation_metrics["rmse"] + cv_metrics["rmse_mean"]
        if best_selection_score is None or selection_score < best_selection_score:
            best_selection_score = selection_score
            best_model_name = model_name

    # Fit the best candidate on train + validation, then evaluate on the held-out test split.
    best_pipeline = candidate_models[best_model_name]
    best_pipeline.fit(X_train_val, y_train_val)
    best_test_metrics = metric_bundle(y_test, best_pipeline.predict(X_test))

    best_regressor = best_pipeline.named_steps["regressor"]
    feature_insights = {}
    if hasattr(best_regressor, "coef_"):
        feature_insights = {
            feature: float(coef)
            for feature, coef in zip(engineered_feature_cols, best_regressor.coef_)
        }
    elif hasattr(best_regressor, "feature_importances_"):
        feature_insights = {
            feature: float(importance)
            for feature, importance in zip(
                engineered_feature_cols, best_regressor.feature_importances_
            )
        }

    # Feature-engineering ablation: same model family with and without interaction terms.
    raw_ablation_pipeline = build_pipeline(LinearRegression())
    engineered_ablation_pipeline = build_pipeline(LinearRegression())
    raw_ablation_pipeline.fit(raw_train, raw_y_train)
    engineered_ablation_pipeline.fit(X_train, y_train)

    raw_ablation_metrics = metric_bundle(
        raw_y_val, raw_ablation_pipeline.predict(raw_val)
    )
    engineered_ablation_metrics = metric_bundle(
        y_val, engineered_ablation_pipeline.predict(X_val)
    )
    ablation_results = {
        "raw_features": raw_ablation_metrics,
        "engineered_features": engineered_ablation_metrics,
        "delta_r2": float(
            engineered_ablation_metrics["r2"] - raw_ablation_metrics["r2"]
        ),
        "delta_rmse": float(
            raw_ablation_metrics["rmse"] - engineered_ablation_metrics["rmse"]
        ),
    }

    print("\n" + "=" * 70)
    print("ABLATION STUDY: LINEAR REGRESSION RAW VS ENGINEERED FEATURES")
    print("=" * 70)
    print(f"{'Feature Set':<20} {'Val R2':<10} {'Val RMSE':<10} {'Val MAE':<10}")
    print("-" * 70)
    print(
        f"{'Raw features':<20} {raw_ablation_metrics['r2']:<10.4f} {raw_ablation_metrics['rmse']:<10.4f} {raw_ablation_metrics['mae']:<10.4f}"
    )
    print(
        f"{'Engineered features':<20} {engineered_ablation_metrics['r2']:<10.4f} {engineered_ablation_metrics['rmse']:<10.4f} {engineered_ablation_metrics['mae']:<10.4f}"
    )

    comparison_data = {
        "data_story": {
            "scope": "prototype",
            "dataset_source": os.path.relpath(DATA_PATH, os.path.dirname(__file__)),
            "sample_count": int(len(df)),
            "note": "The project is intentionally scoped as a prototype using a small in-repo dataset; methodology is emphasized over scale.",
        },
        "split": {
            "train": int(len(X_train)),
            "validation": int(len(X_val)),
            "test": int(len(X_test)),
        },
        "cross_validation": {
            model_name: payload["cv"] for model_name, payload in candidate_results.items()
        },
        "comparison_table": format_rows(candidate_results),
        "baseline_table": format_rows(candidate_results),
        "ablation_study": ablation_results,
        "linear_regression": {
            "cv": candidate_results["linear_regression"]["cv"],
            "validation": candidate_results["linear_regression"]["validation"],
        },
        "random_forest": {
            "cv": candidate_results["random_forest"]["cv"],
            "validation": candidate_results["random_forest"]["validation"],
        },
        "dummy_mean": {
            "cv": candidate_results["dummy_mean"]["cv"],
            "validation": candidate_results["dummy_mean"]["validation"],
        },
        "best_model": best_model_name,
        "best_validation_model": best_model_name,
        "selection_criterion": "validation_rmse_plus_cv_rmse",
        "selection_score": float(best_selection_score),
        "best_test_metrics": best_test_metrics,
        "feature_insights": feature_insights,
    }

    save_split_csvs(X_train, y_train, X_val, y_val, X_test, y_test)

    return best_pipeline, comparison_data


def main():
    df = load_dataset()
    model, comparison = train_model(df)

    # Save model.
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f"\n[OK] Model saved to {MODEL_OUT}")

    # Save model metadata for backend consumption.
    metadata = {
        "version": "1.1.0",
        "created_at": datetime.utcnow().isoformat(),
        "scope": comparison["data_story"],
        "split": comparison["split"],
        "features": get_feature_columns(use_engineered_features=True),
        "metrics": comparison.get("best_test_metrics", {}),
        "cv_summary": comparison.get("cross_validation", {}),
        "ablation_study": comparison.get("ablation_study", {}),
    }
    with open(MODEL_METADATA_OUT, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Model metadata saved to {MODEL_METADATA_OUT}")

    # Save model comparison data for backend.
    with open(MODEL_COMPARISON_OUT, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"[OK] Model comparison saved to {MODEL_COMPARISON_OUT}")


if __name__ == "__main__":
    main()