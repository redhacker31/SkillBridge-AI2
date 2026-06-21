import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardService } from '../services/dashboardService';
import type { AnalysisResponse } from '../types/analysis';
import { BookOpen, Award, Clock, Star, Map } from 'lucide-react';

export default function Roadmap() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await dashboardService.getSummary();
        setSummary(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col p-8 space-y-8 animate-pulse">
        <div className="h-16 bg-slate-900/50 rounded-xl mb-8 border border-slate-800"></div>
        <div className="h-32 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
        <div className="h-64 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center">
        <h2 className="text-3xl font-bold mb-4">No Active Roadmap Found</h2>
        <button onClick={() => navigate('/dashboard')} className="px-8 py-4 bg-indigo-600 rounded-xl">Back to Dashboard</button>
      </div>
    );
  }

  const roadmapSteps = summary.visual_roadmap || [];
  const courses = summary.courses || [];
  const projects = summary.projects || [];
  const internships = summary.internships || [];

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col font-sans selection:bg-indigo-500/30">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            SkillBridge AI
          </span>
          <button onClick={() => navigate('/dashboard')} className="text-sm font-medium px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors cursor-pointer border border-slate-700">
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto py-12 px-6 w-full space-y-16 animate-fade-in">
        <div className="text-center">
          <h1 className="text-4xl font-black bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            Your Personal Learning Roadmap
          </h1>
          <p className="text-slate-400 mt-4 max-w-2xl mx-auto text-lg">
            Structured phases to acquire your missing skills for <span className="font-bold text-white">{summary.career_readiness?.[0]?.career || 'your target role'}</span>.
          </p>
        </div>

        {/* Roadmap steps timeline */}
        <section>
          <h2 className="text-2xl font-bold mb-8 flex items-center border-b border-slate-800 pb-2">
            <Map className="w-6 h-6 mr-3 text-indigo-400" /> Learning Timeline
          </h2>
          
          {roadmapSteps.length > 0 ? (
            <div className="relative border-l-2 border-indigo-900/50 ml-4 md:ml-8 space-y-12">
              {roadmapSteps.map((step, idx) => (
                <div key={idx} className="relative pl-8 transition-all duration-300 hover:translate-x-2">
                  <div className="absolute -left-3 top-1 bg-indigo-500 h-6 w-6 rounded-full border-4 border-slate-950 flex items-center justify-center shadow-[0_0_15px_rgba(99,102,241,0.5)]"></div>
                  <h3 className="text-lg font-bold text-slate-100 flex items-center">
                    Phase {step.step_number}: {step.title}
                  </h3>
                  <div className="flex items-center gap-4 mt-2">
                    <span className="text-xs font-semibold px-2 py-1 bg-slate-800 text-slate-300 rounded border border-slate-700 flex items-center"><Clock className="w-3 h-3 mr-1"/> {step.estimated_duration}</span>
                  </div>
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-indigo-500/30 transition-colors">
                      <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wide flex items-center"><BookOpen className="w-3 h-3 mr-1"/> Primary Resource</h4>
                      <p className="text-sm font-medium text-slate-300 mt-2">{step.resource}</p>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-cyan-500/30 transition-colors">
                      <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wide flex items-center"><Award className="w-3 h-3 mr-1"/> Validation Project</h4>
                      <p className="text-sm font-medium text-slate-300 mt-2">{step.mini_project}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
              No roadmap steps generated.
            </div>
          )}
        </section>

        {/* AI Recommendations */}
        <section className="space-y-12">
          <h2 className="text-2xl font-bold mb-8 flex items-center border-b border-slate-800 pb-2">
            <Star className="w-6 h-6 mr-3 text-amber-400" /> Curated Recommendations
          </h2>

          {/* Courses */}
          {courses.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-4 text-indigo-300">Recommended Courses</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {courses.map((c, i) => (
                  <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col hover:border-indigo-500/50 transition-colors">
                    <h4 className="text-lg font-bold text-white">{c.title}</h4>
                    <p className="text-sm text-slate-400 mt-2 italic flex-1">"{c.reason}"</p>
                    <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-800">
                      <span className="text-[10px] uppercase font-bold px-2 py-1 bg-slate-800 rounded text-slate-300">Diff: {c.difficulty}</span>
                      <span className="text-[10px] uppercase font-bold px-2 py-1 bg-slate-800 rounded text-slate-300">Time: {c.estimated_time}</span>
                      {c.addressed_skills?.map(s => <span key={s} className="text-[10px] uppercase font-bold px-2 py-1 bg-indigo-500/10 border border-indigo-500/20 rounded text-indigo-300">Skill: {s}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Projects */}
          {projects.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-4 text-emerald-300">Portfolio Projects</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {projects.map((p, i) => (
                  <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col hover:border-emerald-500/50 transition-colors">
                    <h4 className="text-lg font-bold text-white">{p.title}</h4>
                    <p className="text-sm text-slate-400 mt-2 italic flex-1">"{p.reason}"</p>
                    <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-800">
                      <span className="text-[10px] uppercase font-bold px-2 py-1 bg-slate-800 rounded text-slate-300">Diff: {p.difficulty}</span>
                      <span className="text-[10px] uppercase font-bold px-2 py-1 bg-slate-800 rounded text-slate-300">Time: {p.estimated_time}</span>
                      {p.addressed_skills?.map(s => <span key={s} className="text-[10px] uppercase font-bold px-2 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded text-emerald-300">Skill: {s}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Internships */}
          {internships.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-4 text-cyan-300">Target Internships</h3>
              <div className="space-y-4">
                {internships.map((i, idx) => (
                  <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/50 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                      <h4 className="text-lg font-bold text-white">{i.title}</h4>
                      <p className="text-sm text-slate-400 mt-1">{i.reason}</p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="text-[10px] uppercase font-bold px-2 py-1 bg-slate-800 rounded text-slate-300">{i.estimated_time}</span>
                      {i.addressed_skills?.map(s => <span key={s} className="text-[10px] uppercase font-bold px-2 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded text-cyan-300">{s}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </section>
      </main>
    </div>
  );
}

// Ensure lucide icon Map is imported. Oh wait, I didn't import Map above. I need to fix imports.
