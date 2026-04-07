import React, { useState, useEffect, type ReactNode } from 'react';
import {
  ChartBarSquareIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline';
import { DashboardStats, DashboardFilters } from '../types/dashboard';
import { fetchDashboardStats } from '../api/dashboard';
import { DashboardFiltersComponent } from '../components/DashboardFilters';
import { UserFrequencyChart } from '../components/UserFrequencyChart';
import { TopIPChart } from '../components/TopIPChart';
import { TimelineChart } from '../components/TimelineChart';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize filters with default date range (last 7 days)
  const [filters, setFilters] = useState<DashboardFilters>(() => {
    const endDate = new Date();
    const startDate = new Date(endDate);
    startDate.setDate(startDate.getDate() - 7);

    return {
      startDate: formatDateForInput(startDate),
      endDate: formatDateForInput(endDate),
      granularity: 'day',
    };
  });

  // Fetch data when filters change
  useEffect(() => {
    loadDashboardData();
  }, [filters]);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetchDashboardStats({
        start_date: filters.startDate,
        end_date: filters.endDate,
        granularity: filters.granularity,
      });

      setStats(response);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (newFilters: DashboardFilters) => {
    setFilters(newFilters);
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <main className="mx-auto w-full max-w-7xl space-y-6 px-4 py-6 sm:px-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            SSH authentication log analytics and statistics
          </p>
        </div>

        {/* Filters */}
        <DashboardFiltersComponent
          filters={filters}
          onFilterChange={handleFilterChange}
          isLoading={isLoading}
        />

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Stats Cards */}
        {stats && !isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <StatCard
              title="Total Attempts"
              value={stats.total_stats.total_attempts}
              icon={<ChartBarSquareIcon className="h-8 w-8 text-slate-500" />}
            />
            <StatCard
              title="Successful"
              value={stats.total_stats.success_count}
              icon={<CheckCircleIcon className="h-8 w-8 text-green-600" />}
              color="green"
            />
            <StatCard
              title="Failed"
              value={stats.total_stats.failed_count}
              icon={<XCircleIcon className="h-8 w-8 text-red-600" />}
              color="red"
            />
            <StatCard
              title="Success Rate"
              value={`${stats.total_stats.success_rate.toFixed(1)}%`}
              icon={<ArrowTrendingUpIcon className="h-8 w-8 text-blue-600" />}
              color="blue"
            />
          </div>
        )}

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* User Frequency Chart */}
          <div>
            <UserFrequencyChart
              data={stats?.user_frequency || []}
              isLoading={isLoading}
            />
          </div>

          {/* Top IP Chart */}
          <div>
            <TopIPChart data={stats?.top_ips || []} isLoading={isLoading} />
          </div>
        </div>

        {/* Timeline Chart */}
        <div>
          <TimelineChart
            data={stats?.timeline || []}
            granularity={filters.granularity}
            isLoading={isLoading}
          />
        </div>
      </main>
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: ReactNode;
  color?: 'green' | 'red' | 'blue' | 'gray';
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  color = 'gray',
}) => {
  const colorClasses = {
    green: 'bg-green-50 border-green-200',
    red: 'bg-red-50 border-red-200',
    blue: 'bg-blue-50 border-blue-200',
    gray: 'bg-gray-50 border-gray-200',
  };

  return (
    <div className={`${colorClasses[color]} border rounded-lg p-4`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        {icon}
      </div>
    </div>
  );
};

function formatDateForInput(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
