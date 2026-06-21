import axios from 'axios';
import type { User, LoginCredentials, RegisterCredentials, TokenResponse } from '../types/auth';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Axios Request Interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  async register(credentials: RegisterCredentials): Promise<User> {
    const response = await api.post<User>('/auth/register', credentials);
    return response.data;
  },

  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', credentials);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },
};
export default authService;
