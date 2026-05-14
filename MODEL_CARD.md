# Model Card — Environmental Data Intelligence Platform

## Model Overview

- **Model name:** Environmental AQI Predictor
- **Type:** scikit-learn regression pipeline
- **Artifact:** `backend/models/model.joblib`
- **Task:** predict Air Quality Index (AQI) from environmental features

## Intended Use

- Lightweight AQI prediction for dashboards, demos, and student ML projects.
- Useful for environmental analytics workflows that need a simple inference API.
- Not intended for safety-critical or regulatory air-quality decisions.
- Best read as a rigorously engineered prototype built to demonstrate ML workflow quality.

## Dataset Provenance

- **Source in this repo:** `ml/sample_data/air_quality_real.csv`
- **Structure:** 20 rows, 6 columns
- **Columns:** `date`, `region`, `temperature`, `humidity`, `rainfall`, `aqi`
- **Purpose:** compact project dataset used for training, evaluation, and demo outputs
- **Scope note:** the dataset is intentionally small, so the project emphasizes methodology, evaluation discipline, and explainability over raw benchmark performance.

## Training Data Summary

- Numeric features: `temperature`, `humidity`, `rainfall`
- Derived features: `temp_humidity_interaction`, `temp_rainfall_interaction`
- Target: `aqi`
- Preprocessing: missing numeric values are filled with column means, then features are scaled with `StandardScaler`
- Split strategy: train/validation/test separation with cross-validation on the training split

## Model Details

- Training script: `ml/train_model.py`
- Inference contract: `backend/app/model.py`
- Backend API: `backend/app/main.py`
- Model family: scikit-learn pipeline with scaling and regression
- Selected model: random forest regressor chosen by a combined validation/CV RMSE score

## Evaluation Results

Evaluated with `python -m ml.evaluate_model` on the held-out test split:

- **MAE:** 11.1482
- **RMSE:** 12.3148
- **R²:** -13.6570

The training report also includes:

- Baseline comparison table: `backend/models/model_comparison.json`
- Cross-validation summary: `backend/models/model_comparison.json`
- Feature engineering ablation study: `backend/models/model_comparison.json`
- Residual plot: `ml/plots/evaluation_residuals.png`

## Limitations

- The dataset is small, so the model is best suited for demonstration rather than production use.
- The held-out test split contains only 4 samples, so test metrics are highly unstable and should not be over-interpreted.
- Performance may vary outside the observed feature ranges.
- The model does not capture external drivers such as traffic, emissions events, or seasonal policy effects.

## Reproducibility

1. Train or refresh the model: `python ml/train_model.py`
2. Evaluate the model: `python -m ml.evaluate_model`
3. Inspect the backend model artifact: `backend/models/model.joblib`
4. Review the split and comparison artifacts under `backend/models/`

## Versioning

- Track model updates alongside code changes in Git.
- For future experiments, store metrics and configuration in a lightweight JSON file under `experiments/`.
