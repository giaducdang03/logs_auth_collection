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
        top_success_limit: 5,
        top_failed_limit: 5,
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
        <section className="mb-6 space-y-6">
          <div className="grid grid-cols-1 gap-6 xl:grid-cols-3 xl:items-stretch">
            <div className="xl:col-span-1">
              <UserFrequencyChart
                data={stats?.user_frequency || []}
                isLoading={isLoading}
                className="min-h-[560px]"
              />
            </div>

            <div className="xl:col-span-1">
              <TopIPChart
                data={stats?.top_success_ips || []}
                isLoading={isLoading}
                title="Top Successful IP Addresses"
                datasetLabel="Success Count"
                barColor="rgba(34, 197, 94, 0.8)"
                borderColor="rgba(34, 197, 94, 1)"
                className="min-h-[560px]"
              />
            </div>

            <div className="xl:col-span-1">
              <TopIPChart
                data={stats?.top_failed_ips || []}
                isLoading={isLoading}
                title="Top Failed IP Addresses"
                datasetLabel="Failed Count"
                barColor="rgba(239, 68, 68, 0.8)"
                borderColor="rgba(239, 68, 68, 1)"
                className="min-h-[560px]"
              />
            </div>
          </div>
        </section>

        {/* Recent Activity */}
        <section className="mb-6 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 bg-slate-50 px-4 py-3 sm:px-6">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-700">
              Recent Activity (Top 5)
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Time</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Username</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">IP Address</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Location</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Auth Method</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-100 bg-white">
                {(stats?.recent_activity || []).map((item, idx) => (
                  <tr key={`${item.login_time}-${item.ip_address}-${idx}`} className="transition hover:bg-slate-50">
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-slate-700">{formatRecentTime(item.login_time)}</td>
                    <td className="px-4 py-3 text-sm font-medium text-black">{item.username || '-'}</td>
                    <td className="px-4 py-3 font-mono text-sm text-cyan-700">{item.ip_address || '-'}</td>
                    <td className="px-4 py-3 text-sm text-slate-700">
                      <div className="flex flex-col items-start gap-1">
                        <span>{item.location_label || '-'}</span>
                        {item.org && (
                          <span className="rounded bg-gray-100 px-2 py-0.5 text-[11px] text-gray-600">
                            {item.org}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span
                        className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${
                          item.status === 'success'
                            ? 'bg-emerald-100 text-emerald-800 ring-emerald-600/20'
                            : 'bg-rose-100 text-rose-800 ring-rose-600/20'
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm capitalize text-slate-600">{item.auth_method || 'unknown'}</td>
                  </tr>
                ))}

                {!isLoading && (stats?.recent_activity || []).length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-center text-sm text-slate-500" colSpan={6}>
                      No recent activity in selected range
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Timeline Chart */}
        <div className="mb-6">
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

function formatRecentTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}
