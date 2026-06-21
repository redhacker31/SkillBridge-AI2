import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { resumeService } from '../services/resumeService';

export default function ResumeUpload() {
  const navigate = useNavigate();
  const [careerGoal, setCareerGoal] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'analyzing' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const validateFile = (selectedFile: File) => {
    if (selectedFile.type !== 'application/pdf') {
      setErrorMessage('Please upload a PDF file.');
      setStatus('error');
      return false;
    }
    if (selectedFile.size > MAX_FILE_SIZE) {
      setErrorMessage('File size exceeds the 5MB limit.');
      setStatus('error');
      return false;
    }
    return true;
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    setStatus('idle');
    setErrorMessage('');

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const selectedFile = e.dataTransfer.files[0];
      if (validateFile(selectedFile)) {
        setFile(selectedFile);
      }
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setStatus('idle');
    setErrorMessage('');
    
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      if (validateFile(selectedFile)) {
        setFile(selectedFile);
      }
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !careerGoal) return;

    setStatus('uploading');
    setUploadProgress(0);
    setErrorMessage('');

    try {
      let uploadResponse;
      try {
        uploadResponse = await resumeService.uploadResume(file, (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(progress);
          }
        });
      } catch (uploadError) {
        throw new Error('UPLOAD_FAILED');
      }

      setStatus('analyzing');
      
      let analysisInit;
      try {
        analysisInit = await resumeService.analyzeResume(uploadResponse.id, careerGoal);
      } catch (analyzeError) {
        throw new Error('ANALYSIS_FAILED');
      }

      let isComplete = false;
      let attempt = 0;
      
      while (!isComplete && attempt < 30) {
        await new Promise((resolve) => setTimeout(resolve, 3000));
        let statusResponse;
        try {
          statusResponse = await resumeService.getAnalysisStatus(analysisInit.analysis_id);
        } catch (statusError) {
          throw new Error('ANALYSIS_FAILED');
        }
        
        if (statusResponse.status === 'completed') {
          isComplete = true;
        } else if (statusResponse.status === 'failed') {
          throw new Error('ANALYSIS_FAILED');
        }
        attempt++;
      }
      
      if (!isComplete) {
         throw new Error('ANALYSIS_FAILED');
      }

      setStatus('success');
      setSuccessMessage('Analysis complete! Redirecting...');
      setFile(null);
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (error: any) {
      console.error('Process failed:', error);
      setStatus('error');
      if (error.message === 'UPLOAD_FAILED') {
        setErrorMessage('Upload failed. Please try again.');
      } else if (error.message === 'ANALYSIS_FAILED') {
        setErrorMessage('Analysis failed. Please try again.');
      } else {
        setErrorMessage(error.message || error.response?.data?.detail || 'Failed to process resume. Please try again.');
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      <main className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
          <h2 className="text-2xl font-bold text-white mb-2">Analyze Your Resume</h2>
          <p className="text-sm text-slate-400 mb-6">
            Select your target career goal and upload your resume in PDF format to detect skills, score your profile, and build a learning roadmap.
          </p>
          
          <form onSubmit={handleUpload} className="space-y-6">
            <div>
              <label className="block text-xs font-semibold text-slate-350 uppercase tracking-wider mb-2">
                Select Career Goal
              </label>
              <select 
                value={careerGoal} 
                onChange={(e) => setCareerGoal(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
                required
                disabled={status === 'uploading'}
              >
                <option value="" className="bg-slate-950">Choose a path...</option>
                {[
                  { k: "frontend_developer_react", n: "Frontend Developer (React)" },
                  { k: "backend_developer_python", n: "Backend Developer (Python)" },
                  { k: "data_scientist", n: "Data Scientist" },
                  { k: "devops_engineer", n: "DevOps Engineer" },
                  { k: "fullstack_developer", n: "Full Stack Developer" },
                  { k: "machine_learning_engineer", n: "Machine Learning Engineer" },
                  { k: "ios_developer", n: "iOS Developer" },
                  { k: "android_developer", n: "Android Developer" },
                  { k: "ui_ux_designer", n: "UI/UX Designer" },
                  { k: "cloud_architect_aws", n: "Cloud Architect (AWS)" },
                  { k: "cybersecurity_analyst", n: "Cybersecurity Analyst" },
                  { k: "data_analyst", n: "Data Analyst" },
                  { k: "database_administrator", n: "Database Administrator" },
                  { k: "blockchain_developer", n: "Blockchain Developer" },
                  { k: "game_developer_unity", n: "Game Developer (Unity)" },
                  { k: "game_developer_unreal", n: "Game Developer (Unreal)" },
                  { k: "site_reliability_engineer", n: "Site Reliability Engineer" },
                  { k: "product_manager", n: "Product Manager" },
                  { k: "quality_assurance_engineer", n: "Quality Assurance Engineer" },
                  { k: "data_engineer", n: "Data Engineer" },
                  { k: "cloud_engineer_azure", n: "Cloud Engineer (Azure)" },
                  { k: "cloud_engineer_gcp", n: "Cloud Engineer (GCP)" },
                  { k: "frontend_developer_angular", n: "Frontend Developer (Angular)" },
                  { k: "frontend_developer_vue", n: "Frontend Developer (Vue)" },
                  { k: "backend_developer_java", n: "Backend Developer (Java)" },
                  { k: "backend_developer_go", n: "Backend Developer (Go)" },
                  { k: "backend_developer_node", n: "Backend Developer (Node.js)" },
                  { k: "backend_developer_csharp", n: "Backend Developer (C# .NET)" },
                  { k: "embedded_systems_engineer", n: "Embedded Systems Engineer" },
                  { k: "ar_vr_developer", n: "AR/VR Developer" },
                  { k: "big_data_engineer", n: "Big Data Engineer" },
                  { k: "computer_vision_engineer", n: "Computer Vision Engineer" },
                  { k: "nlp_engineer", n: "NLP Engineer" },
                  { k: "robotics_engineer", n: "Robotics Engineer" },
                  { k: "bi_analyst", n: "Business Intelligence Analyst" },
                  { k: "it_support_specialist", n: "IT Support Specialist" }
                ].map((c) => (
                  <option key={c.k} value={c.k} className="bg-slate-950">{c.n}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-350 uppercase tracking-wider mb-2">
                Upload Resume (PDF)
              </label>
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors relative ${
                  isDragging
                    ? 'border-indigo-500 bg-indigo-950/20'
                    : 'border-slate-700 hover:border-indigo-500 bg-slate-850/50'
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <input 
                  type="file" 
                  accept=".pdf" 
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  onChange={handleFileChange}
                  disabled={status === 'uploading' || status === 'analyzing'}
                />
                <div className="space-y-2 pointer-events-none">
                  <UploadCloud className={`mx-auto h-12 w-12 ${isDragging ? 'text-indigo-400' : 'text-slate-400'}`} />
                  <p className="text-sm font-semibold">
                    {file ? 'Selected: ' + file.name : 'Drag & drop your resume PDF here or click to browse'}
                  </p>
                  <p className="text-xs text-slate-500">PDF documents only, up to 5MB</p>
                </div>
              </div>
            </div>

            {file && status !== 'success' && (
              <div className="flex items-center justify-between p-3 bg-slate-800 rounded-lg border border-slate-700">
                <div className="flex items-center space-x-3 truncate">
                  <FileText className="h-6 w-6 text-indigo-400 flex-shrink-0" />
                  <div className="truncate">
                    <p className="text-xs font-medium text-slate-200 truncate">{file.name}</p>
                    <p className="text-[10px] text-slate-450">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setFile(null)}
                  className="text-xs font-semibold text-red-400 hover:text-red-300 transition-colors"
                  disabled={status === 'uploading' || status === 'analyzing'}
                >
                  Remove
                </button>
              </div>
            )}

            {status === 'uploading' && (
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-medium text-slate-350">
                  <span>Uploading...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className="bg-indigo-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              </div>
            )}

            {status === 'analyzing' && (
              <div className="space-y-3">
                <div className="flex justify-between text-xs font-medium text-indigo-300">
                  <span className="flex items-center"><Loader2 className="animate-spin h-3 w-3 mr-2" /> AI is analyzing your resume...</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-indigo-500 h-2 rounded-full animate-pulse w-full" />
                </div>
              </div>
            )}

            {status === 'error' && (
              <div className="p-4 bg-red-950/20 border border-red-800/50 rounded-lg flex items-start space-x-2">
                <AlertCircle className="h-5 w-5 text-red-450 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-red-200">{errorMessage}</span>
              </div>
            )}

            {status === 'success' && (
              <div className="p-4 bg-emerald-950/20 border border-emerald-800/50 rounded-lg flex items-start space-x-2">
                <CheckCircle className="h-5 w-5 text-emerald-450 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-emerald-200">{successMessage}</span>
              </div>
            )}

            <button 
              type="submit"
              disabled={!file || !careerGoal || status === 'uploading' || status === 'analyzing'}
              className={`w-full py-3 text-white font-semibold rounded-lg shadow-lg flex items-center justify-center space-x-2 transition-all ${
                file && careerGoal && status !== 'uploading' && status !== 'analyzing'
                  ? 'bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 cursor-pointer' 
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed'
              }`}
            >
              {status === 'uploading' || status === 'analyzing' ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5 mr-2" />
                  <span>{status === 'uploading' ? 'Uploading...' : 'Analyzing...'}</span>
                </>
              ) : (
                <span>Analyze Resume</span>
              )}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
