import { useState, useCallback } from 'react';
import { apiClient } from '../api/client';
import * as storage from '../utils/storage';

export interface UseAuthReturn {
  username: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = (): UseAuthReturn => {
  const [username, setUsername] = useState<string | null>(storage.getUser());
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.login({ username, password });
      storage.setToken(response.access_token);
      storage.setUser(username);
      setUsername(username);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Login failed';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.register({ username, password });
      storage.setToken(response.access_token);
      storage.setUser(username);
      setUsername(username);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Registration failed';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    storage.clearAll();
    setUsername(null);
    setError(null);
  }, []);

  return {
    username,
    isAuthenticated: !!username && !!storage.getToken(),
    isLoading,
    error,
    login,
    register,
    logout,
  };
};
