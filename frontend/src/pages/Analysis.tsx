import { useLocation, useNavigate, Navigate } from 'react-router-dom';
import type { AnalysisResponse } from '../types/analysis';

export default function Analysis() {
  const navigate = useNavigate();
  const location = useLocation();
  const analysisResult = location.state?.analysisResult as AnalysisResponse;

  if (!analysisResult) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            SkillBridge AI
          </span>
          <button onClick={() => navigate('/dashboard')} className="text-sm font-medium text-slate-400 hover:text-white transition-colors cursor-pointer">
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto py-12 px-6">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">Analysis Results</h1>
          <p className="text-sm text-slate-400 mt-2">Here is a comprehensive breakdown of your resume match.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center flex flex-col items-center">
            <h2 className="text-lg font-bold text-slate-350">Overall Resume Score</h2>
            <div className="my-6 inline-flex items-center justify-center h-32 w-32 rounded-full border-4 border-indigo-500/30 bg-indigo-500/5">
              <span className="text-4xl font-extrabold text-indigo-400">{analysisResult.resume_score}</span>
            </div>
            <p className="text-xs text-slate-400">Based on standard formatting, sections, and keyword density.</p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center flex flex-col items-center">
            <h2 className="text-lg font-bold text-slate-350">ATS Score</h2>
            <div className="my-6 inline-flex items-center justify-center h-32 w-32 rounded-full border-4 border-cyan-500/30 bg-cyan-500/5">
              <span className="text-4xl font-extrabold text-cyan-400">{analysisResult.ats_score}%</span>
            </div>
            <p className="text-xs text-slate-400">Compatibility with Applicant Tracking Systems for the target role.</p>
          </div>
        </div>

        <div className="space-y-6">
          {analysisResult.ats_suggestions && analysisResult.ats_suggestions.length > 0 && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-bold text-amber-400 mb-4">ATS Suggestions</h2>
              <ul className="list-disc pl-5 space-y-2 text-sm text-slate-300">
                {analysisResult.ats_suggestions.map((suggestion, idx) => (
                  <li key={idx}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-bold mb-4">Detected Skills</h2>
            <div className="flex flex-wrap gap-2">
              {analysisResult.present_skills.length > 0 ? (
                analysisResult.present_skills.map((skill) => (
                  <span key={skill} className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-450 rounded-full text-xs font-semibold">
                    {skill}
                  </span>
                ))
              ) : (
                <span className="text-sm text-slate-500">No matching skills detected for this role.</span>
              )}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-bold mb-4">Missing Skills (Skill Gaps)</h2>
            <div className="flex flex-wrap gap-2">
              {analysisResult.missing_skills.length > 0 ? (
                analysisResult.missing_skills.map((missingSkill) => (
                  <span key={missingSkill.skill} className="px-3 py-1 bg-rose-500/10 border border-rose-500/20 text-rose-450 rounded-full text-xs font-semibold">
                    {missingSkill.skill}
                  </span>
                ))
              ) : (
                <span className="text-sm text-slate-500">You have all the required skills!</span>
              )}
            </div>
          </div>
        </div>

        <div className="mt-10 text-center">
          <button 
            onClick={() => navigate('/roadmap')}
            className="px-8 py-3 bg-gradient-to-r from-indigo-550 to-cyan-550 hover:from-indigo-650 hover:to-cyan-650 text-white font-semibold rounded-xl shadow-lg transition-transform transform hover:-translate-y-0.5 cursor-pointer"
          >
            View Learning Roadmap & Recs
          </button>
        </div>
      </main>
    </div>
  );
}
