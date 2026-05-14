"""
Performance Benchmark and Optimization script.
Measures model inference latency, memory usage, and optimizes for serving.

Usage:
    python ml/benchmark_model.py

"""

import os
import time
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Paths
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "model.joblib"
)
DATA_PATH = os.path.join(
    os.path.dirname(__file__), "sample_data", "air_quality_real.csv"
)
BENCHMARK_OUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "models", "benchmark.json"
)

FEATURE_COLS = [
    "temperature",
    "humidity",
    "rainfall",
    "temp_humidity_interaction",
    "temp_rainfall_interaction",
]


def benchmark_inference_latency(model, X, n_samples=1000):
    """Measure inference latency for n predictions."""
    print("\n" + "=" * 60)
    print("INFERENCE LATENCY BENCHMARK")
    print("=" * 60)

    # Single prediction latency
    single_sample = X.iloc[[0]].values
    times = []
    for _ in range(n_samples):
        start = time.perf_counter()
        model.predict(single_sample)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    latencies = {
        "single_prediction_ms": {
            "mean": float(np.mean(times)),
            "median": float(np.median(times)),
            "std": float(np.std(times)),
            "min": float(np.min(times)),
            "max": float(np.max(times)),
        }
    }

    print(f"Single prediction (n={n_samples}):")
    print(f"  Mean latency:   {latencies['single_prediction_ms']['mean']:.4f} ms")
    print(f"  Median latency: {latencies['single_prediction_ms']['median']:.4f} ms")
    print(f"  Std Dev:        {latencies['single_prediction_ms']['std']:.4f} ms")
    print(f"  Min:            {latencies['single_prediction_ms']['min']:.4f} ms")
    print(f"  Max:            {latencies['single_prediction_ms']['max']:.4f} ms")

    # Batch prediction latency
    batch_sizes = [1, 10, 100, 1000]
    batch_times = {}
    for batch_size in batch_sizes:
        if batch_size <= len(X):
            batch = X.iloc[:batch_size].values
            start = time.perf_counter()
            model.predict(batch)
            end = time.perf_counter()
            elapsed_ms = (end - start) * 1000
            batch_times[f"batch_{batch_size}"] = {
                "total_ms": float(elapsed_ms),
                "per_sample_ms": float(elapsed_ms / batch_size),
            }

    print(f"\nBatch Predictions (1 run each):")
    for batch_key, batch_info in batch_times.items():
        print(
            f"  {batch_key:15} | Total: {batch_info['total_ms']:8.2f} ms | Per-sample: {batch_info['per_sample_ms']:.4f} ms"
        )

    latencies.update(batch_times)
    return latencies


def benchmark_model_size(model_path):
    """Measure model file size and memory footprint."""
    print("\n" + "=" * 60)
    print("MODEL SIZE & MEMORY FOOTPRINT")
    print("=" * 60)

    # File size
    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"Model file size: {file_size_mb:.2f} MB")

    # Load and measure memory
    model = joblib.load(model_path)

    # Estimate memory usage (rough)
    import sys

    model_memory_mb = sys.getsizeof(model) / (1024 * 1024)
    print(f"Model memory (loaded): ~{model_memory_mb:.2f} MB")

    return {"file_size_mb": float(file_size_mb), "memory_mb": float(model_memory_mb)}


def throughput_benchmark(model, X, duration_seconds=5):
    """Measure predictions per second (throughput)."""
    print("\n" + "=" * 60)
    print("THROUGHPUT BENCHMARK")
    print("=" * 60)

    single_sample = X.iloc[[0]].values
    count = 0
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration_seconds:
        model.predict(single_sample)
        count += 1

    throughput = count / duration_seconds
    print(f"Throughput (single-sample): {throughput:.1f} predictions/sec")
    print(f"Total predictions in {duration_seconds}s: {count}")

    return {"throughput_pred_per_sec": float(throughput)}


def main():
    print("\n" + "=" * 60)
    print("ENVIRONMENTAL DATA INTELLIGENCE")
    print("MODEL PERFORMANCE BENCHMARK")
    print("=" * 60)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    # Load model and data
    print(f"\nLoading model from {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    print(f"Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df = df.fillna(df.mean(numeric_only=True))
    df["temp_humidity_interaction"] = df["temperature"] * df["humidity"]
    df["temp_rainfall_interaction"] = df["temperature"] * df["rainfall"]

    X = df[FEATURE_COLS]

    # Run benchmarks
    latency_results = benchmark_inference_latency(model, X, n_samples=1000)
    size_results = benchmark_model_size(MODEL_PATH)
    throughput_results = throughput_benchmark(model, X, duration_seconds=5)

    # Combine results
    benchmark_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "model_path": MODEL_PATH,
        "num_samples": len(X),
        "latency": latency_results,
        "size": size_results,
        "throughput": throughput_results,
    }

    # Save results
    os.makedirs(os.path.dirname(BENCHMARK_OUT), exist_ok=True)
    with open(BENCHMARK_OUT, "w") as f:
        json.dump(benchmark_data, f, indent=2)

    print(f"\n✓ Benchmark results saved to {BENCHMARK_OUT}")

    # Summary
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    print(
        f"Mean latency (single):  {latency_results['single_prediction_ms']['mean']:.4f} ms"
    )
    print(
        f"Throughput:             {throughput_results['throughput_pred_per_sec']:.1f} pred/sec"
    )
    print(f"Model file size:        {size_results['file_size_mb']:.2f} MB")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
