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

## Dataset Provenance

- **Source in this repo:** `ml/sample_data/air_quality_real.csv`
- **Structure:** 20 rows, 6 columns
- **Columns:** `date`, `region`, `temperature`, `humidity`, `rainfall`, `aqi`
- **Purpose:** compact project dataset used for training, evaluation, and demo outputs

## Training Data Summary

- Numeric features: `temperature`, `humidity`, `rainfall`
- Derived features: `temp_humidity_interaction`, `temp_rainfall_interaction`
- Target: `aqi`
- Preprocessing: missing numeric values are filled with column means, then features are scaled with `StandardScaler`
- Split strategy: 80/20 train-test split with `random_state=42`

## Model Details

- Training script: `ml/train_model.py`
- Inference contract: `backend/app/model.py`
- Backend API: `backend/app/main.py`
- Model family: scikit-learn pipeline with scaling and regression

## Evaluation Results

Evaluated with `python -m ml.evaluate_model`:

- **MAE:** 6.5889
- **RMSE:** 7.9677
- **R²:** 0.6275

Residual plots are saved to `ml/plots/evaluation_residuals.png`.

## Limitations

- The dataset is small, so the model is best suited for demonstration rather than production use.
- Performance may vary outside the observed feature ranges.
- The model does not capture external drivers such as traffic, emissions events, or seasonal policy effects.

## Reproducibility

1. Train or refresh the model: `python ml/train_model.py`
2. Evaluate the model: `python -m ml.evaluate_model`
3. Inspect the backend model artifact: `backend/models/model.joblib`

## Versioning

- Track model updates alongside code changes in Git.
- For future experiments, store metrics and configuration in a lightweight JSON file under `experiments/`.
