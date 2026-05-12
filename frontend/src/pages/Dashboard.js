import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_BASE = 'http://127.0.0.1:8000';

function Dashboard({ data, loading, onRefresh }) {
  const [working, setWorking] = useState(false);
  const [message, setMessage] = useState(null);

  const handleClearData = async () => {
    if (!window.confirm('Delete all raw data? This cannot be undone.')) return;
    try {
      setWorking(true);
      await axios.delete(`${API_BASE}/api/data`);
      setMessage({ type: 'success', text: 'All data deleted.' });
      if (onRefresh) onRefresh();
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to delete data: ' + (err.response?.data?.detail || err.message) });
    } finally {
      setWorking(false);
    }
  };
  if (loading) {
    return <div className="text-center py-12 text-lg text-gray-600">Loading dashboard...</div>;
  }

  const stats = {
    avgAQI: data.length ? (data.reduce((sum, d) => sum + d.aqi, 0) / data.length).toFixed(1) : 0,
    maxTemp: data.length ? Math.max(...data.map(d => d.temperature)).toFixed(1) : 0,
    avgRainfall: data.length ? (data.reduce((sum, d) => sum + d.rainfall, 0) / data.length).toFixed(1) : 0,
    regionsCount: data.length ? new Set(data.map(d => d.region)).size : 0,
  };

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8 text-gray-800">Environmental Intelligence Dashboard</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm font-medium">Average AQI</div>
          <div className="text-3xl font-bold text-blue-600">{stats.avgAQI}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm font-medium">Max Temperature</div>
          <div className="text-3xl font-bold text-red-600">{stats.maxTemp}°C</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm font-medium">Avg Rainfall</div>
          <div className="text-3xl font-bold text-cyan-600">{stats.avgRainfall}mm</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm font-medium">Regions Monitored</div>
          <div className="text-3xl font-bold text-green-600">{stats.regionsCount}</div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">AQI Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="aqi" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Temperature by Region</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="temperature" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Humidity Levels</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="humidity" stroke="#8b5cf6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Rainfall Pattern</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="rainfall" fill="#06b6d4" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white p-6 rounded-lg shadow mt-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Raw Data</h2>
          <div>
            <button
              onClick={handleClearData}
              disabled={working}
              className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded"
            >
              {working ? 'Working...' : 'Delete All Data'}
            </button>
          </div>
        </div>
        {message && (
          <div className={`mb-4 p-3 rounded ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            {message.text}
          </div>
        )}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Date</th>
                <th className="px-4 py-2 text-left">Region</th>
                <th className="px-4 py-2 text-left">Temp (°C)</th>
                <th className="px-4 py-2 text-left">Humidity (%)</th>
                <th className="px-4 py-2 text-left">Rainfall (mm)</th>
                <th className="px-4 py-2 text-left">AQI</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2">{row.date}</td>
                  <td className="px-4 py-2">{row.region}</td>
                  <td className="px-4 py-2">{row.temperature}</td>
                  <td className="px-4 py-2">{row.humidity}</td>
                  <td className="px-4 py-2">{row.rainfall}</td>
                  <td className="px-4 py-2 font-bold">{row.aqi}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
