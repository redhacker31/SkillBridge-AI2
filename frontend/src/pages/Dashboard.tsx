import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dashboardService } from '../services/dashboardService';
import type { AnalysisResponse } from '../types/analysis';
import { AlertCircle, FileText, CheckCircle, Target, Award, Map, Briefcase, Activity, TrendingUp, TrendingDown, BookOpen, ChevronDown, ChevronUp, PieChart, Bug } from 'lucide-react';

export default function Dashboard() {
  const [summary, setSummary] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showDebug, setShowDebug] = useState(false);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await dashboardService.getSummary();
        setSummary(data);
      } catch (err: any) {
        if (err.response?.status === 404) {
          setSummary(null);
        } else {
          setError('Failed to load dashboard data.');
        }
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-300 font-sans p-8 space-y-8 animate-pulse">
        <div className="max-w-7xl mx-auto h-16 bg-slate-900/50 rounded-xl mb-8 border border-slate-800"></div>
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="col-span-2 h-64 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
          <div className="h-64 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
        </div>
        <div className="max-w-7xl mx-auto h-32 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="h-96 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
          <div className="h-96 bg-slate-900/50 rounded-2xl border border-slate-800"></div>
        </div>
      </div>
    );
  }

  if (!summary && !error) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center">
        <FileText className="h-16 w-16 text-indigo-400 mb-4" />
        <h2 className="text-3xl font-bold mb-4">No Active Analysis Found</h2>
        <Link to="/upload" className="px-8 py-4 bg-indigo-600 rounded-xl">Upload Resume</Link>
      </div>
    );
  }

  if (!summary) return null;

  // Null-safe helpers
  const pi = summary.personal_info || {} as any;
  const sc = summary.skill_categories || { core: [], preferred: [], bonus: [], unrelated: [] };
  const rc = summary.resume_completeness || { score: 0, breakdown: {} };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 font-sans selection:bg-indigo-500/30">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            SkillBridge AI
          </span>
          <div className="flex items-center gap-3">
            {summary.domain && (
              <span className="text-xs px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                {summary.domain}
              </span>
            )}
            <Link to="/upload" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm font-medium rounded-lg transition-colors cursor-pointer border border-slate-700">
              New Analysis
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* 1. Candidate Profile & AI Summary */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl"></div>
          <div className="flex flex-col md:flex-row justify-between gap-8 relative z-10">
            <div className="flex-1">
              <h1 className="text-4xl font-black text-white mb-2">{pi.name || 'Candidate Name Not Detected'}</h1>
              <div className="text-sm text-slate-400 flex flex-wrap gap-4 mb-6">
                {pi.email && <span>📧 {pi.email}</span>}
                {pi.phone && <span>📱 {pi.phone}</span>}
                {pi.github && <a href={pi.github} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline">GitHub</a>}
                {pi.linkedin && <a href={pi.linkedin} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline">LinkedIn</a>}
              </div>
              <div className="text-sm text-slate-300 space-y-1 mb-6 border-l-2 border-indigo-500 pl-4">
                <p><strong>Education:</strong> {pi.degree || 'Not detected'} {pi.college && pi.college !== 'Not Specified' ? `at ${pi.college}` : ''}</p>
                <p><strong>Class of:</strong> {pi.graduation_year || 'Not detected'}</p>
              </div>
              {summary.resume_summary && (
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs uppercase tracking-wider text-indigo-400 font-bold mb-2">AI Generated Summary</h3>
                  <p className="text-sm leading-relaxed">{summary.resume_summary}</p>
                </div>
              )}
            </div>

            {/* Top Level Analytics */}
            <div className="w-full md:w-1/3 space-y-4">
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500 uppercase font-bold">Resume Score</p>
                  <p className="text-3xl font-black text-white">{summary.resume_score}<span className="text-sm text-slate-500 font-normal">/100</span></p>
                </div>
                <Award className="w-10 h-10 text-amber-400 opacity-50" />
              </div>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500 uppercase font-bold">ATS Match</p>
                  <p className="text-3xl font-black text-white">{summary.ats_score}<span className="text-sm text-slate-500 font-normal">%</span></p>
                </div>
                <CheckCircle className="w-10 h-10 text-emerald-400 opacity-50" />
              </div>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500 uppercase font-bold">Interview Ready</p>
                  <p className="text-3xl font-black text-white">{summary.interview_readiness?.overall || 0}<span className="text-sm text-slate-500 font-normal">%</span></p>
                </div>
                <Activity className="w-10 h-10 text-cyan-400 opacity-50" />
              </div>
            </div>
          </div>
        </section>

        {/* Resume Completeness */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
          <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center">
            <PieChart className="w-5 h-5 mr-2 text-violet-400"/>
            Resume Completeness — {rc.score}%
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
            {Object.entries(rc.breakdown || {}).map(([key, val]) => (
              <div key={key} className={`p-3 rounded-lg border text-center ${val ? 'bg-emerald-950/30 border-emerald-500/30' : 'bg-rose-950/30 border-rose-500/30'}`}>
                <div className="mb-1">
                  {val ? <CheckCircle className="w-5 h-5 mx-auto text-emerald-400" /> : <AlertCircle className="w-5 h-5 mx-auto text-rose-400" />}
                </div>
                <p className={`text-xs font-bold ${val ? 'text-emerald-300' : 'text-rose-300'}`}>{key}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Skill Gap Chart */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
          <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center">
            <Target className="w-5 h-5 mr-2 text-rose-400"/>
            Skill Gap Analysis — {summary.skill_coverage_percentage}% Match
          </h3>
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <div>
                <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-400 bg-indigo-200/10">
                  Skills Found: {summary.skills_found_count}
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-rose-400 bg-rose-200/10">
                  Total Required: {summary.total_required_skills}
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-4 mb-4 text-xs flex rounded-full bg-slate-800">
              <div style={{ width: `${summary.skill_coverage_percentage}%` }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500 transition-all duration-1000 ease-out"></div>
            </div>
          </div>
        </section>

        {/* 2. Score Breakdowns */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><Award className="w-5 h-5 mr-2 text-indigo-400"/> Resume Score Breakdown</h3>
            <div className="space-y-3">
              {(summary.resume_score_breakdown || []).map((item, idx) => (
                <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-sm">{item.category}</span>
                    <span className={`text-sm font-bold ${item.score === item.max_score ? 'text-emerald-400' : 'text-amber-400'}`}>{item.score} / {item.max_score}</span>
                  </div>
                  {item.deduction_reason && <p className="text-xs text-rose-400 mt-1">↳ {item.deduction_reason}</p>}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><CheckCircle className="w-5 h-5 mr-2 text-emerald-400"/> ATS Score Breakdown</h3>
            <div className="space-y-3">
              {(summary.ats_score_breakdown || []).map((item, idx) => (
                <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex items-start">
                  <div className="mt-0.5 mr-3">
                    {item.passed ? <CheckCircle className="w-4 h-4 text-emerald-500" /> : <AlertCircle className="w-4 h-4 text-rose-500" />}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-200">{item.metric}</h4>
                    <p className={`text-xs mt-1 ${item.passed ? 'text-slate-400' : 'text-rose-400'}`}>{item.details}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 3. Strengths & Weaknesses */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
           <div className="bg-emerald-950/20 border border-emerald-900/30 rounded-2xl p-6">
             <h3 className="text-lg font-bold text-emerald-400 mb-4 flex items-center"><TrendingUp className="w-5 h-5 mr-2"/> Top Strengths</h3>
             <ul className="space-y-2">
               {(summary.strengths || []).map((s, i) => (
                 <li key={i} className="text-sm flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-emerald-500 flex-shrink-0"/> {s}</li>
               ))}
               {(!summary.strengths || summary.strengths.length === 0) && <li className="text-sm text-slate-500 italic">No standout strengths detected yet.</li>}
             </ul>
           </div>
           <div className="bg-rose-950/20 border border-rose-900/30 rounded-2xl p-6">
             <h3 className="text-lg font-bold text-rose-400 mb-4 flex items-center"><TrendingDown className="w-5 h-5 mr-2"/> Key Weaknesses</h3>
             <ul className="space-y-2">
               {(summary.weaknesses || []).map((w, i) => (
                 <li key={i} className="text-sm flex items-start"><AlertCircle className="w-4 h-4 mr-2 mt-0.5 text-rose-500 flex-shrink-0"/> {w}</li>
               ))}
               {(!summary.weaknesses || summary.weaknesses.length === 0) && <li className="text-sm text-slate-500 italic">No weaknesses detected.</li>}
             </ul>
           </div>
        </section>

        {/* 4. Skill Analysis */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-white mb-6 border-b border-slate-800 pb-2">Skill Intelligence Matrix</h3>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-slate-950 p-4 rounded-xl border border-indigo-500/30">
              <h4 className="text-sm font-bold text-indigo-400 mb-3">Core Required</h4>
              <div className="flex flex-wrap gap-2">
                {sc.core.map(s => <span key={s} className="px-2 py-1 bg-indigo-500/10 text-indigo-300 text-xs rounded border border-indigo-500/20">{s}</span>)}
                {sc.core.length === 0 && <span className="text-xs text-slate-500">None detected</span>}
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-cyan-500/30">
              <h4 className="text-sm font-bold text-cyan-400 mb-3">Preferred</h4>
              <div className="flex flex-wrap gap-2">
                {sc.preferred.map(s => <span key={s} className="px-2 py-1 bg-cyan-500/10 text-cyan-300 text-xs rounded border border-cyan-500/20">{s}</span>)}
                {sc.preferred.length === 0 && <span className="text-xs text-slate-500">None detected</span>}
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-emerald-500/30">
              <h4 className="text-sm font-bold text-emerald-400 mb-3">Bonus / Other Tech</h4>
              <div className="flex flex-wrap gap-2">
                {sc.bonus.map(s => <span key={s} className="px-2 py-1 bg-emerald-500/10 text-emerald-300 text-xs rounded border border-emerald-500/20">{s}</span>)}
                {sc.bonus.length === 0 && <span className="text-xs text-slate-500">None detected</span>}
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-700">
              <h4 className="text-sm font-bold text-slate-400 mb-3">Unrelated</h4>
              <div className="flex flex-wrap gap-2">
                {sc.unrelated.map(s => <span key={s} className="px-2 py-1 bg-slate-800 text-slate-400 text-xs rounded border border-slate-700">{s}</span>)}
                {sc.unrelated.length === 0 && <span className="text-xs text-slate-500">None detected</span>}
              </div>
              <p className="text-[10px] text-slate-500 mt-2">These do not affect your score.</p>
            </div>
          </div>

          {/* Missing Skills */}
          <div className="mt-8">
            <h4 className="text-md font-bold text-white mb-4">Critical Skill Gaps ({summary.skill_coverage_percentage || 0}% Coverage)</h4>
            <div className="flex flex-wrap gap-2">
              {(summary.missing_skills || []).map((item, idx) => {
                let bgColor = 'bg-slate-500/10 border-slate-500/20 text-slate-400';
                if (item.priority === 'Critical') bgColor = 'bg-rose-500/10 border-rose-500/30 text-rose-400 shadow-[0_0_10px_rgba(244,63,94,0.1)]';
                else if (item.priority === 'High') bgColor = 'bg-orange-500/10 border-orange-500/30 text-orange-400';
                else if (item.priority === 'Medium') bgColor = 'bg-amber-500/10 border-amber-500/20 text-amber-400';

                return (
                  <div key={idx} className={`px-3 py-1.5 border rounded-lg text-sm font-medium flex flex-col ${bgColor} max-w-sm`}>
                    <div className="flex justify-between items-center gap-4">
                      <span>{item.skill}</span>
                      <span className="opacity-60 text-[10px] uppercase tracking-wider">{item.priority}</span>
                    </div>
                    {item.reason && <span className="text-[10px] opacity-80 mt-1 italic leading-tight">{item.reason}</span>}
                  </div>
                );
              })}
              {(!summary.missing_skills || summary.missing_skills.length === 0) && <p className="text-sm text-emerald-400">No missing skills detected! Perfect match.</p>}
            </div>
          </div>
        </section>

        {/* 5. Experience & Projects */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><Briefcase className="w-5 h-5 mr-2 text-cyan-400"/> Experience Analysis</h3>
            <div className="space-y-4">
              {(summary.experience_analysis || []).map((exp, i) => (
                <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <h4 className="font-bold text-slate-200">{exp.role || 'Role not detected'} @ {exp.company || 'Company not detected'}</h4>
                  <p className="text-xs text-slate-500 mb-2">{exp.duration || ''}</p>
                  <p className="text-sm text-indigo-300">{exp.evaluation}</p>
                </div>
              ))}
              {(!summary.experience_analysis || summary.experience_analysis.length === 0) && (
                <p className="text-sm text-slate-500 italic p-4 text-center">No professional experience found. Consider internships or open-source contributions.</p>
              )}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><FileText className="w-5 h-5 mr-2 text-indigo-400"/> Project Analysis</h3>
            <div className="space-y-4 overflow-y-auto max-h-[500px] pr-2 custom-scrollbar">
              {(summary.project_analysis || []).map((proj, i) => (
                <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-800 relative">
                  <span className={`absolute top-4 right-4 text-[10px] uppercase px-2 py-0.5 rounded font-bold ${proj.complexity === 'Advanced' ? 'bg-emerald-500/20 text-emerald-400' : proj.complexity === 'Intermediate' ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-800 text-slate-400'}`}>{proj.complexity}</span>
                  <h4 className="font-bold text-slate-200 w-3/4">{proj.name}</h4>
                  <p className="text-xs text-slate-500 mb-3">{proj.technologies || 'No technologies detected'}</p>
                  <p className="text-sm text-slate-300 mb-3">{proj.evaluation}</p>
                  <div className="bg-rose-950/10 rounded-lg p-2 border border-rose-900/20">
                    <p className="text-xs font-bold text-rose-400 mb-1">AI Suggestions to Improve:</p>
                    <ul className="text-xs text-slate-400 list-disc list-inside">
                      {(proj.suggestions || []).map((s, idx) => <li key={idx}>{s}</li>)}
                    </ul>
                  </div>
                </div>
              ))}
              {(!summary.project_analysis || summary.project_analysis.length === 0) && (
                <p className="text-sm text-slate-500 italic p-4 text-center">No projects detected. Add portfolio projects to strengthen your profile.</p>
              )}
            </div>
          </div>
        </section>

        {/* 6. Career & Interview Probability */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><Target className="w-5 h-5 mr-2 text-indigo-400"/> Top 5 Career Matches</h3>
            <div className="space-y-3">
              {(summary.career_readiness || []).map((c, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-sm font-semibold text-slate-200">{c.career}</span>
                  <div className="flex items-center w-1/3">
                    <div className="w-full bg-slate-800 rounded-full h-2 mr-3">
                      <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${c.match_percentage}%` }}></div>
                    </div>
                    <span className="text-xs font-bold text-indigo-400 w-8">{c.match_percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-800 pb-2 flex items-center"><Activity className="w-5 h-5 mr-2 text-rose-400"/> Interview Probability</h3>
            <div className="space-y-3">
              {(summary.interview_probability || []).map((ip, i) => (
                <div key={i} className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-sm text-slate-200">{ip.company}</span>
                    <span className={`text-sm font-black ${ip.probability > 80 ? 'text-emerald-400' : ip.probability > 50 ? 'text-amber-400' : 'text-rose-400'}`}>{ip.probability}%</span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{ip.reason}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 7. Visual Learning Roadmap */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-lg">
          <h3 className="text-xl font-bold text-white mb-8 border-b border-slate-800 pb-2 flex items-center"><Map className="w-5 h-5 mr-2 text-emerald-400"/> AI Generated Visual Learning Path</h3>
          <div className="relative border-l border-slate-700 ml-3 md:ml-6 space-y-8">
            {(summary.visual_roadmap || []).map((step, idx) => (
              <div key={idx} className="relative pl-8 md:pl-12">
                <div className="absolute w-6 h-6 bg-slate-900 border-2 border-emerald-500 rounded-full -left-3 flex items-center justify-center">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full"></div>
                </div>
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 hover:border-emerald-500/50 transition-colors">
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-2">
                    <h4 className="text-lg font-bold text-emerald-400">Step {step.step_number}: {step.title}</h4>
                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded mt-2 md:mt-0">Takes ~{step.estimated_duration}</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-1">Recommended Resource</p>
                      <p className="text-sm text-slate-300 flex items-center"><BookOpen className="w-3 h-3 mr-1 text-indigo-400"/> {step.resource}</p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-1">Validation Mini-Project</p>
                      <p className="text-sm text-slate-300 flex items-center"><Target className="w-3 h-3 mr-1 text-rose-400"/> {step.mini_project}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Module 17: Parser Debug Panel */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl shadow-lg overflow-hidden">
          <button
            onClick={() => setShowDebug(!showDebug)}
            className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-800/50 transition-colors"
          >
            <span className="flex items-center text-sm font-bold text-slate-400">
              <Bug className="w-4 h-4 mr-2 text-amber-400" />
              Parser Debug Panel (Development Mode)
            </span>
            {showDebug ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
          </button>
          {showDebug && summary.debug_info && (
            <div className="p-6 border-t border-slate-800 bg-slate-950">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-500 uppercase font-bold">Domain Detected</p>
                  <p className="text-sm text-white font-bold">{summary.debug_info.domain_detected || 'N/A'}</p>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-500 uppercase font-bold">Parsing Confidence</p>
                  <p className="text-sm text-white font-bold">{summary.debug_info.parsing_confidence || 0}%</p>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-500 uppercase font-bold">Skills Detected</p>
                  <p className="text-sm text-white font-bold">
                    {(summary.debug_info.skill_intelligence?.technical?.length || 0)} Tech / {(summary.debug_info.skill_intelligence?.professional?.length || 0)} Prof / {(summary.debug_info.skill_intelligence?.domain?.length || 0)} Domain
                  </p>
                </div>
              </div>
              <details className="group">
                <summary className="text-xs text-slate-500 cursor-pointer hover:text-slate-300 transition-colors">Show Raw Parsed Data JSON</summary>
                <pre className="mt-2 text-xs bg-slate-900 p-4 rounded-lg border border-slate-800 overflow-x-auto max-h-96 text-slate-400">
                  {JSON.stringify(summary.debug_info.raw_parsed_data, null, 2)}
                </pre>
              </details>
              <details className="group mt-3">
                <summary className="text-xs text-slate-500 cursor-pointer hover:text-slate-300 transition-colors">Show Skill Intelligence JSON</summary>
                <pre className="mt-2 text-xs bg-slate-900 p-4 rounded-lg border border-slate-800 overflow-x-auto max-h-96 text-slate-400">
                  {JSON.stringify(summary.debug_info.skill_intelligence, null, 2)}
                </pre>
              </details>
            </div>
          )}
        </section>

      </main>
    </div>
  );
}
