import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Login() {
  const navigate = useNavigate();
  const { login, isLoading, authError, clearError, isAuthenticated } = useAuthStore();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  useEffect(() => {
    clearError();
    setLocalError(null);
    
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate, clearError]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (!email.trim() || !password) {
      setLocalError('Please fill in all fields.');
      return;
    }

    const success = await login({ email, password });
    if (success) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-tr from-slate-950 via-slate-900 to-indigo-950 px-4">
      <div className="w-full max-w-md bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-8 shadow-2xl transition duration-300 hover:border-indigo-500/25">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-white tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            SkillBridge AI
          </h2>
          <p className="mt-2 text-sm text-slate-450">Bridge the gap between your resume and career goals</p>
        </div>

        {/* Error Panels */}
        {(localError || authError) && (
          <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/25 rounded-lg text-rose-400 text-sm">
            {localError || authError}
          </div>
        )}

        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@university.edu"
              disabled={isLoading}
              className="w-full px-4 py-3 bg-slate-950/50 border border-slate-800 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all disabled:opacity-50"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={isLoading}
              className="w-full px-4 py-3 bg-slate-950/50 border border-slate-800 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all disabled:opacity-50"
              required
            />
          </div>
          <button 
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-indigo-500/20 transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:transform-none cursor-pointer flex items-center justify-center"
          >
            {isLoading ? (
              <div className="h-5 w-5 border-2 border-t-transparent border-white rounded-full animate-spin"></div>
            ) : (
              'Sign In'
            )}
          </button>
        </form>
        <p className="mt-6 text-center text-xs text-slate-400">
          New to SkillBridge?{' '}
          <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}
