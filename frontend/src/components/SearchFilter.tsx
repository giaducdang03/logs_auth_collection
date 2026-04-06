import { useState } from 'react';

interface LogFilters {
  username: string;
  ip: string;
  status: string;
  fromTime: string;
  toTime: string;
  sortBy: string;
  sortOrder: string;
}

interface SearchFilterProps {
  filters: LogFilters;
  onFilterChange: (filters: LogFilters) => void;
  isLoading: boolean;
}

export const SearchFilter = ({ filters, onFilterChange, isLoading }: SearchFilterProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleInputChange = (field: keyof LogFilters, value: string) => {
    onFilterChange({ ...filters, [field]: value });
  };

  const handleReset = () => {
    onFilterChange({
      username: '',
      ip: '',
      status: '',
      fromTime: '',
      toTime: '',
      sortBy: 'login_time',
      sortOrder: 'DESC',
    });
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 p-4">
        <button
          className="inline-flex items-center gap-2 text-sm font-semibold text-slate-800 transition hover:text-cyan-700 disabled:cursor-not-allowed disabled:text-slate-400"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <span className="inline-flex h-5 w-5 items-center justify-center rounded border border-slate-300 text-xs">
            {isExpanded ? '-' : '+'}
          </span>
          Search & Filter
        </button>
      </div>

      {isExpanded && (
        <div className="space-y-4 p-4">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div>
              <label htmlFor="username" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">Username</label>
              <input
                id="username"
                type="text"
                value={filters.username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                placeholder="Search by username..."
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              />
            </div>

            <div>
              <label htmlFor="ip" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">IP Address</label>
              <input
                id="ip"
                type="text"
                value={filters.ip}
                onChange={(e) => handleInputChange('ip', e.target.value)}
                placeholder="Search by IP..."
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              />
            </div>

            <div>
              <label htmlFor="status" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">Status</label>
              <select
                id="status"
                value={filters.status}
                onChange={(e) => handleInputChange('status', e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              >
                <option value="">All</option>
                <option value="success">Success</option>
                <option value="failed">Failed</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div>
              <label htmlFor="fromTime" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">From Time</label>
              <input
                id="fromTime"
                type="datetime-local"
                value={filters.fromTime}
                onChange={(e) => handleInputChange('fromTime', e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              />
            </div>

            <div>
              <label htmlFor="toTime" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">To Time</label>
              <input
                id="toTime"
                type="datetime-local"
                value={filters.toTime}
                onChange={(e) => handleInputChange('toTime', e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              />
            </div>

            <div>
              <label htmlFor="sortOrder" className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600">Sort Order</label>
              <select
                id="sortOrder"
                value={filters.sortOrder}
                onChange={(e) => handleInputChange('sortOrder', e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
              >
                <option value="DESC">Newest First</option>
                <option value="ASC">Oldest First</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end border-t border-slate-200 pt-3">
            <button
              className="rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
              onClick={handleReset}
              disabled={isLoading}
            >
              Reset Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
