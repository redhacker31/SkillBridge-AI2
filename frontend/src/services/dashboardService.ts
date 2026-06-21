import { api } from './authService';
import type { AnalysisResponse } from '../types/analysis';

export const dashboardService = {
  getSummary: async (): Promise<AnalysisResponse> => {
    const response = await api.get<AnalysisResponse>('/dashboard/summary');
    return response.data;
  },
};
export default dashboardService;
