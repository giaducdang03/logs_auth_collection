import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { clearAll } from '../utils/storage';

export const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { username, logout } = useAuth();

  const handleLogout = () => {
    clearAll();
    logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
        {/* Logo */}
        <Link to="/logs" className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
          SSH Auth Log Monitor
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-3 sm:gap-4">
          <Link
            to="/dashboard"
            className="text-sm font-semibold text-slate-700 transition hover:text-slate-900"
          >
            Dashboard
          </Link>
          <Link
            to="/logs"
            className="text-sm font-semibold text-slate-700 transition hover:text-slate-900"
          >
            Logs
          </Link>
          <span className="text-sm text-slate-600">Welcome, {username}!</span>
          <button
            onClick={handleLogout}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
          >
            Logout
          </button>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden flex items-center gap-3">
          <span className="text-xs text-slate-600">{username}</span>
          <button
            onClick={toggleMenu}
            className="inline-flex items-center justify-center p-2 rounded-md text-slate-700 hover:bg-slate-100 focus:outline-none transition"
          >
            <svg
              className={`h-6 w-6 transition-transform ${isMenuOpen ? 'rotate-90' : ''}`}
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-slate-50 px-4 py-3 space-y-2">
          <Link
            to="/logs"
            className="block px-4 py-2 text-slate-700 hover:bg-white rounded-md transition font-semibold"
            onClick={() => setIsMenuOpen(false)}
          >
            Logs
          </Link>
          <Link
            to="/dashboard"
            className="block px-4 py-2 text-slate-700 hover:bg-white rounded-md transition font-semibold"
            onClick={() => setIsMenuOpen(false)}
          >
            Dashboard
          </Link>
          <button
            onClick={() => {
              handleLogout();
              setIsMenuOpen(false);
            }}
            className="w-full text-left rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
};
