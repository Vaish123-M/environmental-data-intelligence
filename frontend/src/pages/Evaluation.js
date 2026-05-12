import React, { useEffect, useState } from 'react';

const API_BASE = 'http://127.0.0.1:8000';

function Evaluation() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/evaluation/summary`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        setSummary(data);
      } catch (err) {
        setError(err.message || 'Failed to load evaluation summary');
      } finally {
        setLoading(false);
      }
    };

    loadSummary();
  }, []);

  if (loading) {
    return <div className="text-center py-12 text-gray-600">Loading evaluation dashboard...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
        Failed to load evaluation dashboard: {error}
      </div>
    );
  }

  const modelInfo = summary?.model_info || {};
  const comparison = summary?.comparison || {};
  const plots = summary?.plots || {};
  const validation = modelInfo?.metrics ? [
    { label: 'Model Version', value: modelInfo.version || 'N/A' },
    { label: 'R²', value: modelInfo.metrics.r2?.toFixed?.(4) ?? 'N/A' },
    { label: 'MSE', value: modelInfo.metrics.mse?.toFixed?.(4) ?? 'N/A' },
    { label: 'RMSE', value: modelInfo.metrics.rmse?.toFixed?.(4) ?? 'N/A' },
  ] : [];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-3 text-gray-800">Model Evaluation</h1>
        <p className="text-gray-600 max-w-3xl">
          A compact checkpoint for deployment readiness: current model metadata, preprocessing validation,
          comparison metrics, and the generated evaluation plots.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {validation.map((item) => (
          <div key={item.label} className="bg-white p-5 rounded-lg shadow">
            <div className="text-sm text-gray-500">{item.label}</div>
            <div className="text-2xl font-bold text-gray-800 mt-1">{item.value}</div>
          </div>
        ))}
      </div>

      {summary?.model_info && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Model Metadata</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div><span className="font-semibold">Created:</span> {modelInfo.created_at || 'N/A'}</div>
            <div><span className="font-semibold">Type:</span> {modelInfo.model_type || 'N/A'}</div>
            <div><span className="font-semibold">Has scaler:</span> {String(modelInfo.has_scaler)}</div>
            <div><span className="font-semibold">Features:</span> {(modelInfo.features || []).join(', ')}</div>
          </div>
        </div>
      )}

      {summary?.comparison && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Comparison Snapshot</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {['linear_regression', 'random_forest'].map((key) => {
              const metrics = comparison[key] || {};
              return (
                <div key={key} className="border rounded-lg p-4 bg-gray-50">
                  <h3 className="font-semibold mb-3 capitalize">{key.replace('_', ' ')}</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span>R²</span><span>{metrics.r2?.toFixed?.(4) ?? 'N/A'}</span></div>
                    <div className="flex justify-between"><span>MSE</span><span>{metrics.mse?.toFixed?.(4) ?? 'N/A'}</span></div>
                    <div className="flex justify-between"><span>RMSE</span><span>{metrics.rmse?.toFixed?.(4) ?? 'N/A'}</span></div>
                    <div className="flex justify-between"><span>MAE</span><span>{metrics.mae?.toFixed?.(4) ?? 'N/A'}</span></div>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-4 text-sm text-gray-600">
            Best model: <span className="font-semibold">{comparison.best_model || summary?.best_model || 'N/A'}</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[
          ['Metrics Comparison', plots.metrics_comparison],
          ['Predictions vs Actual', plots.predictions_vs_actual],
          ['Residuals', plots.residuals],
          ['Feature Importance', plots.feature_importance],
        ].map(([title, src]) => (
          <div key={title} className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-semibold mb-3 text-gray-800">{title}</h3>
            <img src={`${API_BASE}${src}`} alt={title} className="w-full rounded border border-gray-200" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Evaluation;