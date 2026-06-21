import { Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Navbar() {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <Link to="/" className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400 flex items-center space-x-2">
            <span>SkillBridge AI</span>
          </Link>
          
          {isAuthenticated && (
            <div className="hidden md:flex space-x-4">
              <Link 
                to="/dashboard" 
                className={`text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
                  isActive('/dashboard') ? 'bg-indigo-500/10 text-indigo-450' : 'text-slate-300 hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <Link 
                to="/upload" 
                className={`text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
                  isActive('/upload') ? 'bg-indigo-500/10 text-indigo-450' : 'text-slate-300 hover:text-white'
                }`}
              >
                Upload Resume
              </Link>
              <Link 
                to="/roadmap" 
                className={`text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
                  isActive('/roadmap') ? 'bg-indigo-500/10 text-indigo-450' : 'text-slate-300 hover:text-white'
                }`}
              >
                Roadmap
              </Link>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <Link 
            to="/upload" 
            className={`text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
              isActive('/upload') ? 'bg-indigo-500/10 text-indigo-450' : 'text-slate-300 hover:text-white'
            }`}
          >
            Upload Resume
          </Link>
          <Link 
            to="/dashboard" 
            className={`text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
              isActive('/dashboard') ? 'bg-indigo-500/10 text-indigo-450' : 'text-slate-300 hover:text-white'
            }`}
          >
            Dashboard
          </Link>
          <Link 
            to="/upload" 
            className="px-4 py-2 bg-indigo-650 hover:bg-indigo-700 text-sm font-medium rounded-lg transition-colors cursor-pointer text-white shadow-lg shadow-indigo-500/10"
          >
            Analyze Resume
          </Link>

          {/* Original Auth Controls - Hidden for MVP
          {isAuthenticated ? (
            <>
              <span className="text-sm font-medium text-slate-350 hidden sm:inline">
                {user?.full_name}
              </span>
              <button 
                onClick={logout} 
                className="px-4 py-2 border border-slate-700 hover:border-slate-500 hover:bg-slate-800 text-sm font-medium rounded-lg transition-all cursor-pointer text-slate-305 hover:text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-medium text-slate-305 hover:text-white transition-colors">
                Sign In
              </Link>
              <Link to="/register" className="px-4 py-2 bg-indigo-650 hover:bg-indigo-700 text-sm font-medium rounded-lg transition-colors cursor-pointer text-white">
                Register
              </Link>
            </>
          )}
          */}
        </div>
      </div>
    </nav>
  );
}
