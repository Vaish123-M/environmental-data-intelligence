import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ darkMode, setDarkMode }) {
  return (
    <nav className={`${darkMode ? 'bg-gray-800' : 'bg-gradient-to-r from-blue-600 to-blue-800'} text-white shadow-lg transition-colors duration-300`}>
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold hover:text-blue-200 transition">
          🌍 EnvDI
        </Link>
        <div className="flex gap-6 items-center">
          <Link to="/" className="hover:text-blue-200 transition font-medium">
            Dashboard
          </Link>
          <Link to="/analytics" className="hover:text-blue-200 transition font-medium">
            Analytics
          </Link>
          <Link to="/evaluation" className="hover:text-blue-200 transition font-medium">
            Evaluation
          </Link>
          <Link to="/predictions" className="hover:text-blue-200 transition font-medium">
            Predictions
          </Link>
          <Link to="/upload" className="hover:text-blue-200 transition font-medium">
            Upload Data
          </Link>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="ml-4 px-3 py-1 rounded-full hover:bg-blue-700 transition font-medium"
            title="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
