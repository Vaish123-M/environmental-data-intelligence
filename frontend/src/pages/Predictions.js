import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

function Predictions({ darkMode }) {
  const [formData, setFormData] = useState({
    temperature: 25,
    humidity: 60,
    rainfall: 5,
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-predict on input change
  useEffect(() => {
    const timer = setTimeout(() => {
      handlePredict();
    }, 300);
    return () => clearTimeout(timer);
  }, [formData]);

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
    if (aqi < 50) return { level: 'Good', color: darkMode ? 'text-green-400' : 'text-green-600', bg: darkMode ? 'bg-green-900' : 'bg-green-50', icon: '✨' };
    if (aqi < 100) return { level: 'Moderate', color: darkMode ? 'text-yellow-400' : 'text-yellow-600', bg: darkMode ? 'bg-yellow-900' : 'bg-yellow-50', icon: '⚠️' };
    if (aqi < 150) return { level: 'Unhealthy for Sensitive Groups', color: darkMode ? 'text-orange-400' : 'text-orange-600', bg: darkMode ? 'bg-orange-900' : 'bg-orange-50', icon: '😷' };
    if (aqi < 200) return { level: 'Unhealthy', color: darkMode ? 'text-red-400' : 'text-red-600', bg: darkMode ? 'bg-red-900' : 'bg-red-50', icon: '🚨' };
    return { level: 'Very Unhealthy', color: darkMode ? 'text-red-500' : 'text-red-700', bg: darkMode ? 'bg-red-950' : 'bg-red-50', icon: '⛔' };
  };

  const aqiLevel = prediction ? getAQILevel(prediction.predicted_aqi) : null;

  return (
    <div>
      <h1 className={`text-4xl font-bold mb-2 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
        🎯 Real-Time AQI Prediction
      </h1>
      <p className={`mb-8 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
        Adjust environmental factors below to instantly see the predicted Air Quality Index
      </p>

      <div className={`grid grid-cols-1 lg:grid-cols-2 gap-6`}>
        {/* Input Form */}
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} p-8 rounded-lg shadow-lg transition-colors duration-300`}>
          <h2 className={`text-2xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            📊 Environmental Factors
          </h2>
          
          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <label className={`block font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                🌡️ Temperature
              </label>
              <span className="text-2xl font-bold text-blue-500">{formData.temperature.toFixed(1)}°C</span>
            </div>
            <input
              type="range"
              name="temperature"
              min="-10"
              max="50"
              step="0.1"
              value={formData.temperature}
              onChange={handleChange}
              className={`w-full h-3 rounded-lg appearance-none cursor-pointer ${darkMode ? 'bg-gray-700' : 'bg-gray-300'}`}
            />
            <div className={`flex justify-between text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
              <span>-10°C</span>
              <span>50°C</span>
            </div>
          </div>

          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <label className={`block font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                💧 Humidity
              </label>
              <span className="text-2xl font-bold text-purple-500">{formData.humidity.toFixed(1)}%</span>
            </div>
            <input
              type="range"
              name="humidity"
              min="0"
              max="100"
              step="0.1"
              value={formData.humidity}
              onChange={handleChange}
              className={`w-full h-3 rounded-lg appearance-none cursor-pointer ${darkMode ? 'bg-gray-700' : 'bg-gray-300'}`}
            />
            <div className={`flex justify-between text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
              <span>0%</span>
              <span>100%</span>
            </div>
          </div>

          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <label className={`block font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                🌧️ Rainfall
              </label>
              <span className="text-2xl font-bold text-cyan-500">{formData.rainfall.toFixed(1)}mm</span>
            </div>
            <input
              type="range"
              name="rainfall"
              min="0"
              max="100"
              step="0.1"
              value={formData.rainfall}
              onChange={handleChange}
              className={`w-full h-3 rounded-lg appearance-none cursor-pointer ${darkMode ? 'bg-gray-700' : 'bg-gray-300'}`}
            />
            <div className={`flex justify-between text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
              <span>0mm</span>
              <span>100mm</span>
            </div>
          </div>

          {error && (
            <div className={`p-4 rounded-lg ${darkMode ? 'bg-red-900 text-red-300 border border-red-700' : 'bg-red-100 text-red-700 border border-red-400'}`}>
              ❌ {error}
            </div>
          )}
        </div>

        {/* Prediction Result */}
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} p-8 rounded-lg shadow-lg transition-colors duration-300`}>
          <h2 className={`text-2xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            📈 Prediction Result
          </h2>
          
          {prediction ? (
            <div className={`p-8 rounded-lg ${aqiLevel.bg} transition-all duration-300`}>
              <div className="text-center mb-6">
                <div className="text-6xl mb-2">{aqiLevel.icon}</div>
                <div className={`text-7xl font-bold ${aqiLevel.color} tabular-nums`}>
                  {prediction.predicted_aqi.toFixed(1)}
                </div>
                <div className={`text-2xl font-semibold ${aqiLevel.color} mt-2`}>
                  {aqiLevel.level}
                </div>
              </div>

              <div className={`mt-6 space-y-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                <p className="flex items-center"><span className="mr-2">🌡️</span> <strong>Temperature:</strong> <span className="ml-auto">{formData.temperature.toFixed(1)}°C</span></p>
                <p className="flex items-center"><span className="mr-2">💧</span> <strong>Humidity:</strong> <span className="ml-auto">{formData.humidity.toFixed(1)}%</span></p>
                <p className="flex items-center"><span className="mr-2">🌧️</span> <strong>Rainfall:</strong> <span className="ml-auto">{formData.rainfall.toFixed(1)}mm</span></p>
              </div>

              {loading && (
                <div className="mt-4 text-center">
                  <div className="inline-block animate-spin">⏳</div> Updating prediction...
                </div>
              )}

              {prediction.warning && (
                <div className={`mt-4 p-3 rounded ${darkMode ? 'bg-yellow-900 text-yellow-300 border border-yellow-700' : 'bg-yellow-100 text-yellow-800'}`}>
                  ⚠️ {prediction.warning}
                </div>
              )}

              <div className={`mt-6 p-4 rounded ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-blue-50 text-gray-700'}`}>
                <p className="text-sm">
                  <strong>ℹ️ Note:</strong> Predictions update in real-time as you adjust the sliders. This is a RandomForest model trained on historical air quality data.
                </p>
              </div>

              {prediction.model_version && (
                <div className={`mt-3 text-sm ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
                  🔧 Model version: {prediction.model_version}
                </div>
              )}
            </div>
          ) : loading ? (
            <div className={`p-8 rounded-lg text-center ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'}`}>
              ⏳ Loading initial prediction...
            </div>
          ) : (
            <div className={`p-8 rounded-lg text-center ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'}`}>
              Adjust the sliders to see real-time predictions!
            </div>
          )}
        </div>
      </div>

      {/* AQI Scale Guide */}
      <div className={`mt-12 p-8 rounded-lg shadow-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <h3 className={`text-2xl font-bold mb-6 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
          📚 AQI Scale Reference
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className={`p-4 rounded ${darkMode ? 'bg-green-900' : 'bg-green-50'} border-2 border-green-600`}>
            <div className="text-2xl mb-1">✨</div>
            <div className="text-lg font-bold text-green-600">Good</div>
            <div className={darkMode ? 'text-green-300' : 'text-green-700'}>0-50</div>
          </div>
          <div className={`p-4 rounded ${darkMode ? 'bg-yellow-900' : 'bg-yellow-50'} border-2 border-yellow-600`}>
            <div className="text-2xl mb-1">⚠️</div>
            <div className="text-lg font-bold text-yellow-600">Moderate</div>
            <div className={darkMode ? 'text-yellow-300' : 'text-yellow-700'}>51-100</div>
          </div>
          <div className={`p-4 rounded ${darkMode ? 'bg-orange-900' : 'bg-orange-50'} border-2 border-orange-600`}>
            <div className="text-2xl mb-1">😷</div>
            <div className="text-lg font-bold text-orange-600">Unhealthy-SG</div>
            <div className={darkMode ? 'text-orange-300' : 'text-orange-700'}>101-150</div>
          </div>
          <div className={`p-4 rounded ${darkMode ? 'bg-red-900' : 'bg-red-50'} border-2 border-red-600`}>
            <div className="text-2xl mb-1">🚨</div>
            <div className="text-lg font-bold text-red-600">Unhealthy</div>
            <div className={darkMode ? 'text-red-300' : 'text-red-700'}>151-200</div>
          </div>
          <div className={`p-4 rounded ${darkMode ? 'bg-red-950' : 'bg-red-50'} border-2 border-red-700`}>
            <div className="text-2xl mb-1">⛔</div>
            <div className="text-lg font-bold text-red-700">V. Unhealthy</div>
            <div className={darkMode ? 'text-red-400' : 'text-red-700'}>201+</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Predictions;
