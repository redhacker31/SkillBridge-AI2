import Navbar from '../components/Navbar';
import { Outlet } from 'react-router-dom';

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      <Navbar />
      <div className="flex-1">
        <Outlet />
      </div>
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-505">
        <div className="max-w-7xl mx-auto px-4">
          &copy; {new Date().getFullYear()} SkillBridge AI. Portfolio Edition.
        </div>
      </footer>
    </div>
  );
}
