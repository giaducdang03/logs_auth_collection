export type Granularity = "day" | "week" | "month";

export interface DateRange {
  start_date: string;
  end_date: string;
}

export interface TotalStats {
  total_attempts: number;
  success_count: number;
  failed_count: number;
  success_rate: number;
}

export interface UserFrequencyItem {
  username: string | null;
  login_count: number;
}

export interface TopIPItem {
  ip_address: string | null;
  attempt_count: number;
  last_attempt_at?: string | null;
  country?: string | null;
  region?: string | null;
  city?: string | null;
  org?: string | null;
  location_label?: string | null;
}

export interface TimelinePoint {
  time: string;
  timestamp: string;
  success_count: number;
  failed_count: number;
  total_count: number;
}

export interface RecentActivityItem {
  login_time: string;
  username: string | null;
  ip_address: string | null;
  location_label: string | null;
  org: string | null;
  status: string;
  auth_method: string | null;
}

export interface DashboardStats {
  date_range: DateRange;
  granularity: Granularity;
  total_stats: TotalStats;
  user_frequency: UserFrequencyItem[];
  top_ips: TopIPItem[];
  top_success_ips: TopIPItem[];
  top_failed_ips: TopIPItem[];
  recent_activity: RecentActivityItem[];
  timeline: TimelinePoint[];
}

export interface DashboardFilters {
  startDate: string;
  endDate: string;
  granularity: Granularity;
}
