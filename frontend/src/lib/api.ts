import axios from 'axios';
import { AnalysisResult } from '@/types/analysis'; // Ensure you have this type imported

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  googleAuth: async (code: string) => {
    const response = await api.post('/api/auth/google', { code });
    return response.data;
  },
};

export const analysisApi = {
  analyze: async (repoUrl: string) => {
    // FIX 1: Changed 'repo_url' to 'github_url' to match Python Pydantic model
    const response = await api.post('/api/analyze/', { github_url: repoUrl });
    return response.data;
  },
  
  // FIX 2: Now accepts the analysis result to send to the backend
  sendReport: async (analysisData: AnalysisResult) => {
    const response = await api.post('/api/analyze/send-report', { 
      analysis_data: analysisData 
    });
    return response.data;
  },
};

export const paymentApi = {
  generateLink: async (amount: number, message: string) => {
    const response = await api.post('/api/payment/generate-link', { amount, message });
    return response.data;
  },
};