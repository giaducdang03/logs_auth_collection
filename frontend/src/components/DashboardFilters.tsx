import React from 'react';
import { DashboardFilters, Granularity } from '../types/dashboard';

interface DashboardFiltersProps {
  filters: DashboardFilters;
  onFilterChange: (filters: DashboardFilters) => void;
  isLoading?: boolean;
}

export const DashboardFiltersComponent: React.FC<DashboardFiltersProps> = ({
  filters,
  onFilterChange,
  isLoading = false,
}) => {
  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilterChange({
      ...filters,
      startDate: e.target.value,
    });
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilterChange({
      ...filters,
      endDate: e.target.value,
    });
  };

  const handleGranularityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onFilterChange({
      ...filters,
      granularity: e.target.value as Granularity,
    });
  };

  const handleQuickSelect = (days: number) => {
    const endDate = new Date();
    const startDate = new Date(endDate);
    startDate.setDate(startDate.getDate() - days);

    onFilterChange({
      ...filters,
      startDate: formatDateForInput(startDate),
      endDate: formatDateForInput(endDate),
    });
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Quick Select Buttons */}
        <div className="col-span-1 md:col-span-2 lg:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quick Select
          </label>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleQuickSelect(7)}
              disabled={isLoading}
              className="px-3 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 transition"
            >
              Last 7 Days
            </button>
            <button
              onClick={() => handleQuickSelect(30)}
              disabled={isLoading}
              className="px-3 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 transition"
            >
              Last 30 Days
            </button>
            <button
              onClick={() => handleQuickSelect(90)}
              disabled={isLoading}
              className="px-3 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 transition"
            >
              Last 90 Days
            </button>
          </div>
        </div>

        {/* Start Date */}
        <div className="col-span-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Start Date
          </label>
          <input
            type="date"
            value={filters.startDate}
            onChange={handleStartDateChange}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
          />
        </div>

        {/* End Date */}
        <div className="col-span-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            End Date
          </label>
          <input
            type="date"
            value={filters.endDate}
            onChange={handleEndDateChange}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
          />
        </div>

        {/* Granularity */}
        <div className="col-span-1 md:col-span-1 lg:col-span-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Granularity
          </label>
          <select
            value={filters.granularity}
            onChange={handleGranularityChange}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
          >
            <option value="day">Daily</option>
            <option value="week">Weekly</option>
            <option value="month">Monthly</option>
          </select>
        </div>
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
