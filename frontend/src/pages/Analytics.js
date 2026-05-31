import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiUrl } from '../api';

function Analytics({ data, loading }) {
  const [selectedRegion, setSelectedRegion] = useState('All');
  const [modelComparison, setModelComparison] = useState(null);
  const [modelLoading, setModelLoading] = useState(true);

  const formatNumber = (value, digits = 2) => {
    const numericValue = Number(value);
    return Number.isFinite(numericValue) ? numericValue.toFixed(digits) : 'N/A';
  };

  const getModelMetrics = (modelKey) => {
    const model = modelComparison?.models?.[modelKey] || modelComparison?.[modelKey] || {};
    const validation = model.validation || {};
    const cv = model.cv || {};

    return {
      r2: model.r2 ?? validation.r2 ?? cv.r2_mean,
      mse: model.mse ?? validation.mse,
      rmse: model.rmse ?? validation.rmse ?? cv.rmse_mean,
      mae: model.mae ?? validation.mae ?? cv.mae_mean,
    };
  };

  // Fetch model comparison data
  useEffect(() => {
    const fetchModelComparison = async () => {
      try {
        const response = await fetch(apiUrl('/api/models/comparison'));
        const result = await response.json();
        setModelComparison(result);
      } catch (error) {
        console.error('Error fetching model comparison:', error);
      } finally {
        setModelLoading(false);
      }
    };
    fetchModelComparison();
  }, []);

  if (loading) {
    return <div className="text-center py-12">Loading analytics...</div>;
  }

  const regions = ['All', ...new Set(data.map(d => d.region))];
  const filteredData = selectedRegion === 'All' ? data : data.filter(d => d.region === selectedRegion);

  // Calculate correlations
  const divisor = filteredData.length || 1;
  const correlations = {
    tempAqi: formatNumber(filteredData.reduce((sum, d) => sum + d.temperature * d.aqi, 0) / divisor),
    humidityAqi: formatNumber(filteredData.reduce((sum, d) => sum + d.humidity * d.aqi, 0) / divisor),
    rainfallAqi: formatNumber(filteredData.reduce((sum, d) => sum + d.rainfall * d.aqi, 0) / divisor),
  };

  const regionStats = regions.slice(1).map(region => {
    const regionData = data.filter(d => d.region === region);
    return {
      region,
      avgAQI: formatNumber(regionData.reduce((sum, d) => sum + d.aqi, 0) / (regionData.length || 1), 1),
      avgTemp: formatNumber(regionData.reduce((sum, d) => sum + d.temperature, 0) / (regionData.length || 1), 1),
    };
  });

  return (
    <div>
      <h1 className="text-4xl font-bold mb-6 text-gray-800">Advanced Analytics</h1>

      {/* Region Filter */}
      <div className="mb-6 p-4 bg-white rounded-lg shadow">
        <label className="font-semibold mr-4">Filter by Region:</label>
        <select
          value={selectedRegion}
          onChange={(e) => setSelectedRegion(e.target.value)}
          className="px-4 py-2 border rounded-lg"
        >
          {regions.map(region => (
            <option key={region} value={region}>{region}</option>
          ))}
        </select>
      </div>

      {/* Correlation Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Temperature-AQI Correlation</div>
          <div className="text-2xl font-bold text-blue-600">{correlations.tempAqi}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Humidity-AQI Correlation</div>
          <div className="text-2xl font-bold text-purple-600">{correlations.humidityAqi}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Rainfall-AQI Correlation</div>
          <div className="text-2xl font-bold text-cyan-600">{correlations.rainfallAqi}</div>
        </div>
      </div>

      {/* Scatter Plots */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Temperature vs AQI</h2>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="temperature" name="Temperature" />
              <YAxis dataKey="aqi" name="AQI" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={filteredData} fill="#ef4444" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Humidity vs AQI</h2>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="humidity" name="Humidity" />
              <YAxis dataKey="aqi" name="AQI" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={filteredData} fill="#8b5cf6" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ML Model Comparison */}
      {!modelLoading && modelComparison && (
        <div className="mb-6 bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">🤖 Machine Learning Model Comparison</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Linear Regression */}
            <div className="border-l-4 border-blue-500 p-4">
              <h3 className="text-lg font-semibold text-blue-600 mb-3">Linear Regression</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">R² Score:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('linear_regression').r2, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">MSE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('linear_regression').mse, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">RMSE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('linear_regression').rmse, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">MAE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('linear_regression').mae, 4)}</span>
                </div>
              </div>
            </div>

            {/* Random Forest */}
            <div className="border-l-4 border-green-500 p-4">
              <h3 className="text-lg font-semibold text-green-600 mb-3">Random Forest</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">R² Score:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('random_forest').r2, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">MSE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('random_forest').mse, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">RMSE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('random_forest').rmse, 4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">MAE:</span>
                  <span className="font-semibold">{formatNumber(getModelMetrics('random_forest').mae, 4)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Best Model Badge */}
          <div className="mt-4 p-3 bg-amber-50 border-l-4 border-amber-500 rounded">
            <p className="text-amber-900">
              <strong>✓ Best Model in Use:</strong> {(modelComparison.best_model || 'N/A').replace('_', ' ').toUpperCase()}
              <span className="ml-2 text-sm text-amber-700">(Higher R² = Better Predictions)</span>
            </p>
          </div>

          {/* Model Comparison Plots */}
          {modelComparison.plots && (
            <div className="mt-6 pt-6 border-t-2 border-gray-200">
              <h3 className="text-lg font-bold mb-4 text-gray-800">📊 Visual Comparison</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Metrics Comparison */}
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 className="font-semibold mb-3 text-gray-700">Metrics Comparison</h4>
                  <img 
                    src={apiUrl(modelComparison.plots.metrics_comparison)} 
                    alt="Metrics Comparison" 
                    className="w-full rounded border border-gray-300"
                  />
                </div>

                {/* Predictions vs Actual */}
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 className="font-semibold mb-3 text-gray-700">Predictions vs Actual</h4>
                  <img 
                    src={apiUrl(modelComparison.plots.predictions_vs_actual)} 
                    alt="Predictions vs Actual" 
                    className="w-full rounded border border-gray-300"
                  />
                </div>

                {/* Residuals */}
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 className="font-semibold mb-3 text-gray-700">Residuals Analysis</h4>
                  <img 
                    src={apiUrl(modelComparison.plots.residuals)} 
                    alt="Residuals" 
                    className="w-full rounded border border-gray-300"
                  />
                </div>

                {/* Feature Importance */}
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 className="font-semibold mb-3 text-gray-700">Feature Importance</h4>
                  <img 
                    src={apiUrl(modelComparison.plots.feature_importance)} 
                    alt="Feature Importance" 
                    className="w-full rounded border border-gray-300"
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Region Statistics */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Regional Statistics</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Region</th>
                <th className="px-4 py-2 text-left">Avg AQI</th>
                <th className="px-4 py-2 text-left">Avg Temperature</th>
              </tr>
            </thead>
            <tbody>
              {regionStats.map((stat, idx) => (
                <tr key={idx} className="border-b">
                  <td className="px-4 py-2 font-medium">{stat.region}</td>
                  <td className="px-4 py-2">{stat.avgAQI}</td>
                  <td className="px-4 py-2">{stat.avgTemp}°C</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Analytics;
