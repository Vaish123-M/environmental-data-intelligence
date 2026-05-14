# Demo — Quick Requests

This file contains ready-to-run example requests to exercise the API locally.

1) Predict (single sample)

```bash
curl -s -X POST http://127.0.0.1:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature":25,"humidity":65,"rainfall":10}' | jq
```

Example response (JSON):

```json
{
  "predicted_aqi": 72.3,
  "model_version": "1.2.0",
  "metrics": {"mae": 3.5, "rmse": 5.0, "r2": 0.78}
}
```

2) Batch upload (CSV)

```bash
curl -s -X POST http://127.0.0.1:8000/api/upload \
  -F "file=@sample.csv" | jq
```

3) Health check

```bash
curl -s http://127.0.0.1:8000/api/health | jq
```

Notes
- Replace `127.0.0.1:8000` with your `REACT_APP_API_URL` or deployed backend URL.
- The example response values are illustrative. Run `python ml/evaluate_model.py` to compute actual MAE/RMSE/R² for the current model.
