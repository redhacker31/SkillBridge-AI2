import { create } from 'zustand';
import type { User, LoginCredentials, RegisterCredentials } from '../types/auth';
import authService from '../services/authService';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  authError: string | null;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  register: (credentials: RegisterCredentials) => Promise<boolean>;
  logout: () => void;
  initialize: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  authError: null,

  clearError: () => set({ authError: null }),

  login: async (credentials) => {
    set({ isLoading: true, authError: null });
    try {
      const response = await authService.login(credentials);
      localStorage.setItem('token', response.access_token);
      set({ token: response.access_token });
      
      const user = await authService.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
      return true;
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Failed to sign in. Please check your credentials.';
      set({ authError: message, isLoading: false });
      return false;
    }
  },

  register: async (credentials) => {
    set({ isLoading: true, authError: null });
    try {
      await authService.register(credentials);
      // Auto-login after successful registration
      const success = await get().login({
        email: credentials.email,
        password: credentials.password
      });
      return success;
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Failed to create account.';
      set({ authError: message, isLoading: false });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null, isAuthenticated: false, authError: null });
  },

  initialize: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      set({ isLoading: false, isAuthenticated: false });
      return;
    }

    set({ token, isLoading: true });
    try {
      const user = await authService.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error) {
      // Token is invalid/expired, clear it
      localStorage.removeItem('token');
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
