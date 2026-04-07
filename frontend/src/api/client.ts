import axios, { AxiosInstance } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const APP_BASE_URL = import.meta.env.BASE_URL || '/';
const LOGIN_REDIRECT_PATH = APP_BASE_URL.endsWith('/')
  ? `${APP_BASE_URL}login`
  : `${APP_BASE_URL}/login`;

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface LogRecord {
  id: string;
  username: string | null;
  ip_address: string | null;
  login_time: string;
  status: string;
  auth_method: string | null;
  ssh_key: string | null;
  created_at: string;
}

export interface LogListResponse {
  total: number;
  page: number;
  page_size: number;
  data: LogRecord[];
}

export class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for JWT token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Clear token and redirect to login
          localStorage.removeItem('access_token');
          window.location.href = LOGIN_REDIRECT_PATH;
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.client.post<LoginResponse>('/auth/login', credentials);
    return response.data;
  }

  async register(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.client.post<LoginResponse>('/auth/register', credentials);
    return response.data;
  }

  // Log endpoints
  async getLogs(
    page: number = 1,
    pageSize: number = 20,
    filters?: {
      username?: string;
      ip?: string;
      status?: string;
      from_time?: string;
      to_time?: string;
      sort_by?: string;
      sort_order?: string;
    }
  ): Promise<LogListResponse> {
    const params = {
      page,
      page_size: pageSize,
      ...filters,
    };
    
    const response = await this.client.get<LogListResponse>('/logs', { params });
    return response.data;
  }

  async reloadLogs(): Promise<{ detail: string }> {
    const response = await this.client.post<{ detail: string }>('/logs/reload');
    return response.data;
  }
}

export const apiClient = new ApiClient();
