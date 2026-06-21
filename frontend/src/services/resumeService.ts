import { api } from './authService';
import type { AnalysisRequest } from '../types/analysis';

export interface ResumeResponse {
  id: number;
  user_id: number;
  filename: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
}

export const resumeService = {
  uploadResume: async (file: File, onUploadProgress?: (progressEvent: any) => void): Promise<ResumeResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<ResumeResponse>('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    return response.data;
  },

  analyzeResume: async (resumeId: number, careerGoal: string): Promise<{message: string, analysis_id: number, status: string}> => {
    const payload: AnalysisRequest = { career_goal: careerGoal };
    const response = await api.post<{message: string, analysis_id: number, status: string}>(`/resume/${resumeId}/analyze`, payload);
    return response.data;
  },

  getAnalysisStatus: async (analysisId: number): Promise<{id: number, status: string}> => {
    const response = await api.get<{id: number, status: string}>(`/resume/analysis/${analysisId}/status`);
    return response.data;
  },
};
export default resumeService;
