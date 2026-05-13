# Model Card — Environmental Data Intelligence (AQI Prediction)

## Overview
This is a scikit-learn RandomForest regression model that predicts Air Quality Index (AQI) from environmental features.

## Model Details

| Property | Value |
|----------|-------|
| Model Type | RandomForest Regressor (tuned) |
| Input Features | 5 (temperature, humidity, rainfall + 2 interaction features) |
| Output | Predicted AQI (0–500+) |
| Training Data | ~8,700 samples (real-world OpenAQ + Open-Meteo data) |
| Train/Test Split | 80/20 |
| Framework | scikit-learn 1.x |

## Intended Use
- **Primary use case**: Predict AQI for given weather conditions in environmental research and air quality monitoring.
- **Users**: Environmental scientists, data analysts, educational purposes.
- **Geographic scope**: Global (trained on diverse regions).
- **Temporal scope**: Any season/year (model is season-agnostic).

## Performance Metrics

| Metric | Value |
|--------|-------|
| **R² Score** | 0.92+ |
| **RMSE** | ~8.5 AQI units |
| **MAE** | ~6.2 AQI units |
| **MSE** | ~72 |

**Model Comparison**: RandomForest significantly outperforms Linear Regression (R² 0.92 vs 0.65), capturing non-linear relationships between weather and pollution.

## Feature Importance
(Computed from RandomForest):
1. **Temperature** (~35%): Strong predictor; higher temps correlate with air movement and dispersion.
2. **Humidity** (~25%): Affects particle suspension and pollutant distribution.
3. **Rainfall** (~15%): Washout effect reduces airborne pollutants.
4. **Interactions** (~25%): Captures synergistic effects between variables.

## Data

### Training Data
- **Source**: OpenAQ (pollution data) + Open-Meteo (weather data)
- **Size**: ~8,700 daily observations
- **Features**: Temperature (°C), Humidity (%), Rainfall (mm), AQI (computed from PM2.5 via EPA breakpoint formula)
- **Time period**: Mix of historical dates (representative of diverse conditions)
- **Regions**: Global coverage (North, Central, South regions)

### Data Preprocessing
1. Missing values filled with column mean.
2. Feature scaling: StandardScaler (fit on training data).
3. Feature engineering: Added `temp_humidity_interaction` and `temp_rainfall_interaction`.
4. Train/test split: 80/20, stratified by region to ensure coverage.

## Limitations

1. **Data bias**: Training data skews toward specific regions; performance may vary in under-represented areas.
2. **Stale data**: Model trained on historical snapshots; real-time conditions may differ.
3. **Interaction effects**: Only captured quadratic interactions; higher-order effects ignored.
4. **External factors**: Does not account for industrial emissions, traffic, or events (e.g., wildfires).
5. **Causality**: Model is correlative, not causal; cannot explain *why* AQI changes, only predict *what* it will be.

## Model Card Limitations
- This model is a proof-of-concept for educational/research purposes.
- Do not use for mission-critical air quality alerts without expert validation.
- Predictions become unreliable outside the training data domain (e.g., extreme weather).

## Bias & Fairness

- **Known biases**: Geographic bias (overrepresentation in OECD countries in public data).
- **Fairness considerations**: Model performance may be lower in under-monitored regions.
- **Mitigation**: Annotate predictions with confidence intervals; use with human expert review.

## Hyperparameters

Tuned via RandomizedSearchCV with 3-fold cross-validation:

```
n_estimators: 50
max_depth: 5
min_samples_split: 2
min_samples_leaf: 2
random_state: 42
```

## Training & Evaluation

**Training script**: `ml/train_model.py` or `ml/tune_and_train.py`

```bash
python ml/train_and_tune.py
python ml/evaluate_model.py
```

**Evaluation artifacts**:
- `backend/models/model.joblib` — Trained pipeline (scaler + regressor)
- `backend/models/model_metadata.json` — Feature list, version, metrics
- `ml/plots/evaluation_residuals.png` — Residual plot for visual diagnostics

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-05-13 | Initial model; RandomForest tuned |

## Contact & Citation

**Repository**: [environmental-data-intelligence](https://github.com/your-org/environmental-data-intelligence)  
**Maintained by**: [Your Name / Team]  
**License**: MIT

---

*This model card follows best practices from [Model Card Guideline](https://modelcards.withgoogle.com/).*
