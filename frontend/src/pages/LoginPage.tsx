import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export const LoginPage = () => {
  const navigate = useNavigate();
  const { login, register, isLoading, error } = useAuth();
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    if (!username || !password) {
      setFormError('Please fill in all fields');
      return;
    }

    try {
      if (isRegistering) {
        await register(username, password);
      } else {
        await login(username, password);
      }
      navigate('/logs');
    } catch (err: any) {
      setFormError(err.message || 'Authentication failed');
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-amber-50 via-slate-100 to-cyan-50 px-4 py-8">
      <div className="pointer-events-none absolute -left-24 top-[-80px] h-72 w-72 rounded-full bg-amber-300/30 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-24 right-[-100px] h-80 w-80 rounded-full bg-cyan-300/30 blur-3xl" />

      <div className="relative w-full max-w-md rounded-2xl border border-slate-200/70 bg-white/90 p-8 shadow-xl backdrop-blur">
        <h1 className="text-center text-3xl font-bold tracking-tight text-slate-900">SSH Auth Log Monitor</h1>
        <p className="mt-2 text-center text-sm text-slate-600">Sign in to view and filter SSH authentication events.</p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <div>
            <label htmlFor="username" className="mb-2 block text-sm font-semibold text-slate-700">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              disabled={isLoading}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 disabled:cursor-not-allowed disabled:bg-slate-100"
            />
          </div>

          <div>
            <label htmlFor="password" className="mb-2 block text-sm font-semibold text-slate-700">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              disabled={isLoading}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 disabled:cursor-not-allowed disabled:bg-slate-100"
            />
          </div>

          {(formError || error) && (
            <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {formError || error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? 'Loading...' : isRegistering ? 'Register' : 'Login'}
          </button>
        </form>

        <div className="mt-6 border-t border-slate-200 pt-4 text-center text-sm text-slate-600">
          {isRegistering ? 'Already have an account?' : "Don't have an account?"}
          {' '}
          <button
            type="button"
            onClick={() => setIsRegistering(!isRegistering)}
            className="font-semibold text-cyan-700 underline underline-offset-2 transition hover:text-cyan-600"
          >
            {isRegistering ? 'Login' : 'Register'}
          </button>
        </div>

        <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs text-slate-600">
          <p className="font-semibold text-slate-700">Test credentials</p>
          <p className="mt-1">Username: <code className="rounded bg-white px-1.5 py-0.5">admin</code></p>
          <p className="mt-1">Password: <code className="rounded bg-white px-1.5 py-0.5">admin123</code></p>
        </div>
      </div>
    </div>
  );
};
