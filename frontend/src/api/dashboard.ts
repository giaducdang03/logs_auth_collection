import axios from 'axios';
import { DashboardStats, Granularity } from '../types/dashboard';
import { getToken } from '../utils/storage';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
client.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface DashboardStatsRequest {
  start_date?: string;
  end_date?: string;
  granularity?: Granularity;
  top_success_limit?: number;
  top_failed_limit?: number;
}

/**
 * Fetch complete dashboard statistics
 */
export async function fetchDashboardStats(
  filters?: DashboardStatsRequest
): Promise<DashboardStats> {
  try {
    const response = await client.get<DashboardStats>('/dashboard/stats', {
      params: filters || {},
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
    throw error;
  }
}

/**
 * Fetch user login frequency
 */
export async function fetchUserFrequency(filters?: DashboardStatsRequest) {
  try {
    const response = await client.get('/dashboard/user-frequency', {
      params: filters || {},
    });
    return response.data.data;
  } catch (error) {
    console.error('Failed to fetch user frequency:', error);
    throw error;
  }
}

/**
 * Fetch top IP addresses
 */
export async function fetchTopIPs(filters?: DashboardStatsRequest) {
  try {
    const response = await client.get('/dashboard/top-ips', {
      params: filters || {},
    });
    return response.data.data;
  } catch (error) {
    console.error('Failed to fetch top IPs:', error);
    throw error;
  }
}

/**
 * Fetch login timeline data
 */
export async function fetchTimeline(filters?: DashboardStatsRequest) {
  try {
    const response = await client.get('/dashboard/timeline', {
      params: filters || {},
    });
    return response.data.data;
  } catch (error) {
    console.error('Failed to fetch timeline:', error);
    throw error;
  }
}
