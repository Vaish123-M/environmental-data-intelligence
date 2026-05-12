import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

function Predictions() {
  const [formData, setFormData] = useState({
    temperature: 25,
    humidity: 60,
    rainfall: 5,
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value),
    });
  };

  const handlePredict = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_BASE}/api/predict`, formData);
      setPrediction(response.data);
    } catch (err) {
      setError('Failed to get prediction. ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const getAQILevel = (aqi) => {
    if (aqi < 50) return { level: 'Good', color: 'text-green-600', bg: 'bg-green-50' };
    if (aqi < 100) return { level: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-50' };
    if (aqi < 150) return { level: 'Unhealthy', color: 'text-orange-600', bg: 'bg-orange-50' };
    return { level: 'Very Unhealthy', color: 'text-red-600', bg: 'bg-red-50' };
  };

  const aqiLevel = prediction ? getAQILevel(prediction.predicted_aqi) : null;

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8 text-gray-800">AQI Prediction Model</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="bg-white p-8 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-6">Environmental Factors</h2>
          
          <div className="mb-6">
            <label className="block text-gray-700 font-semibold mb-2">Temperature (°C)</label>
            <input
              type="range"
              name="temperature"
              min="-10"
              max="50"
              step="0.1"
              value={formData.temperature}
              onChange={handleChange}
              className="w-full"
            />
            <div className="text-2xl font-bold text-blue-600">{formData.temperature}°C</div>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-semibold mb-2">Humidity (%)</label>
            <input
              type="range"
              name="humidity"
              min="0"
              max="100"
              step="0.1"
              value={formData.humidity}
              onChange={handleChange}
              className="w-full"
            />
            <div className="text-2xl font-bold text-purple-600">{formData.humidity}%</div>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-semibold mb-2">Rainfall (mm)</label>
            <input
              type="range"
              name="rainfall"
              min="0"
              max="100"
              step="0.1"
              value={formData.rainfall}
              onChange={handleChange}
              className="w-full"
            />
            <div className="text-2xl font-bold text-cyan-600">{formData.rainfall}mm</div>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Predicting...' : 'Predict AQI'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
        </div>

        {/* Prediction Result */}
        <div className="bg-white p-8 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-6">Prediction Result</h2>
          
          {prediction ? (
            <div className={`p-8 rounded-lg ${aqiLevel.bg}`}>
              <div className="text-center mb-4">
                <div className={`text-6xl font-bold ${aqiLevel.color}`}>
                  {prediction.predicted_aqi.toFixed(1)}
                </div>
                <div className={`text-2xl font-semibold ${aqiLevel.color}`}>
                  {aqiLevel.level}
                </div>
              </div>

              <div className="mt-6 space-y-3 text-gray-700">
                <p><strong>Temperature:</strong> {formData.temperature}°C</p>
                <p><strong>Humidity:</strong> {formData.humidity}%</p>
                <p><strong>Rainfall:</strong> {formData.rainfall}mm</p>
              </div>

              {prediction.warning && (
                <div className="mt-4 p-3 bg-yellow-100 text-yellow-800 rounded">
                  ⚠️ {prediction.warning}
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded">
                <p className="text-sm text-gray-700">
                  <strong>Note:</strong> This prediction is based on a linear regression model trained on the sample dataset. For production use, integrate with a more sophisticated ML model.
                </p>
              </div>

              {prediction.model_version && (
                <div className="mt-3 text-sm text-gray-500">
                  Model version: {prediction.model_version}
                </div>
              )}
            </div>
          ) : (
            <div className="p-8 bg-gray-100 rounded-lg text-center text-gray-600">
              Enter environmental factors and click "Predict AQI" to see the model's prediction.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Predictions;
