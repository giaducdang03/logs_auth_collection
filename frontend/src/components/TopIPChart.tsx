import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartOptions } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { TopIPItem } from '../types/dashboard';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface TopIPChartProps {
  data: TopIPItem[];
  isLoading?: boolean;
  title?: string;
  datasetLabel?: string;
  barColor?: string;
  borderColor?: string;
  className?: string;
}

export const TopIPChart: React.FC<TopIPChartProps> = ({
  data,
  isLoading = false,
  title = 'Top IP Addresses by Login Attempts',
  datasetLabel = 'Attempt Count',
  barColor = 'rgba(239, 68, 68, 0.8)',
  borderColor = 'rgba(239, 68, 68, 1)',
  className = '',
}) => {
  if (isLoading) {
    return (
      <div className="bg-white shadow rounded-lg p-6 flex items-center justify-center h-96">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg p-6 flex items-center justify-center h-96">
        <div className="text-gray-500">No data available</div>
      </div>
    );
  }

  const chartData = {
    labels: data.map(item => item.ip_address || 'Unknown'),
    datasets: [
      {
        label: datasetLabel,
        data: data.map(item => item.attempt_count),
        backgroundColor: barColor,
        borderColor: borderColor,
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: title,
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className={`h-full bg-white shadow rounded-lg p-6 flex flex-col ${className}`}>
      <Bar data={chartData} options={options} height={data.length * 30 + 100} />

      <div className="mt-4 space-y-2 border-t border-gray-100 pt-3">
        {data.slice(0, 3).map((item) => (
          <div key={`${item.ip_address}-${item.last_attempt_at}`} className="rounded-md border border-gray-100 px-3 py-2 text-xs text-gray-600">
            <div className="flex items-center justify-between gap-4">
              <span className="truncate font-medium text-gray-700">{item.ip_address || 'Unknown'}</span>
              <span>
                {item.last_attempt_at
                  ? `Latest: ${new Date(item.last_attempt_at).toLocaleString()}`
                  : 'Latest: N/A'}
              </span>
            </div>
            <div className="mt-1 flex flex-wrap items-center gap-2 text-[11px] text-gray-500">
              <span>{item.location_label || 'Location: Unknown'}</span>
              {item.org && <span className="rounded bg-gray-100 px-2 py-0.5">{item.org}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
