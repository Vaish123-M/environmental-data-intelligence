import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

function Upload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file.' });
      return;
    }

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE}/api/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setMessage({ type: 'success', text: response.data.message });
      setFile(null);
      setTimeout(() => onUpload(), 1000);
    } catch (err) {
      setMessage({ type: 'error', text: 'Upload failed: ' + (err.response?.data?.detail || err.message) });
    } finally {
      setUploading(false);
    }
  };

  const handleClearData = async () => {
    if (!window.confirm('Are you sure you want to delete all uploaded data? This cannot be undone.')) return;
    try {
      setUploading(true);
      await axios.delete(`${API_BASE}/api/data`);
      setMessage({ type: 'success', text: 'All uploaded data deleted.' });
      setTimeout(() => onUpload(), 500);
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to delete data: ' + (err.response?.data?.detail || err.message) });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8 text-gray-800">Upload Environmental Data</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-8 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-6">Upload CSV File</h2>

          <div className="mb-6 p-8 border-2 border-dashed border-blue-300 rounded-lg text-center">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
              id="fileInput"
            />
            <label htmlFor="fileInput" className="cursor-pointer">
              <div className="text-4xl mb-2">📁</div>
              <p className="text-gray-700 font-medium">Click to select a CSV file</p>
              <p className="text-gray-500 text-sm">or drag and drop</p>
            </label>
            {file && <p className="mt-4 text-green-600 font-semibold">✓ {file.name}</p>}
          </div>

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>

          <button
            onClick={handleClearData}
            disabled={uploading}
            className="w-full mt-3 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition disabled:opacity-50"
          >
            {uploading ? 'Working...' : 'Delete All Uploaded Data'}
          </button>

          {message && (
            <div className={`mt-4 p-4 rounded ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {message.text}
            </div>
          )}
        </div>

        <div className="bg-white p-8 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-6">CSV Format Example</h2>
          <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
{`date,region,temperature,humidity,rainfall,aqi
2024-01-01,North,22.1,55,0.0,85
2024-01-02,North,21.8,57,0.0,88
2024-01-03,Central,30.2,40,0.0,120
...`}
          </pre>
          <div className="mt-6 p-4 bg-blue-50 rounded">
            <p className="text-sm text-gray-700">
              <strong>Required columns:</strong> date, region, temperature, humidity, rainfall, aqi
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Upload;
