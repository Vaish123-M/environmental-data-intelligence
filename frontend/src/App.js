import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Evaluation from './pages/Evaluation';
import Predictions from './pages/Predictions';
import Upload from './pages/Upload';
import { apiUrl } from './api';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(apiUrl('/api/data'));
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50'}`}>
        <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
        <div className="max-w-7xl mx-auto px-4 py-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          <Routes>
            <Route path="/" element={<Dashboard data={data} loading={loading} onRefresh={fetchData} darkMode={darkMode} />} />
            <Route path="/analytics" element={<Analytics data={data} loading={loading} darkMode={darkMode} />} />
            <Route path="/evaluation" element={<Evaluation darkMode={darkMode} />} />
            <Route path="/predictions" element={<Predictions darkMode={darkMode} />} />
            <Route path="/upload" element={<Upload onUpload={fetchData} darkMode={darkMode} />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
