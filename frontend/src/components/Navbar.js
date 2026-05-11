import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold hover:text-blue-200 transition">
          🌍 EnvDI
        </Link>
        <div className="flex gap-6">
          <Link to="/" className="hover:text-blue-200 transition font-medium">
            Dashboard
          </Link>
          <Link to="/analytics" className="hover:text-blue-200 transition font-medium">
            Analytics
          </Link>
          <Link to="/predictions" className="hover:text-blue-200 transition font-medium">
            Predictions
          </Link>
          <Link to="/upload" className="hover:text-blue-200 transition font-medium">
            Upload Data
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
