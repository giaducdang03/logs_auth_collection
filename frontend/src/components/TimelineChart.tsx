import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { TimelinePoint, Granularity } from '../types/dashboard';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface TimelineChartProps {
  data: TimelinePoint[];
  granularity: Granularity;
  isLoading?: boolean;
}

export const TimelineChart: React.FC<TimelineChartProps> = ({
  data,
  granularity,
  isLoading = false,
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

  const granularityLabel = {
    day: 'Daily',
    week: 'Weekly',
    month: 'Monthly',
  };

  const chartData = {
    labels: data.map(item => item.time),
    datasets: [
      {
        label: 'Successful Logins',
        data: data.map(item => item.success_count),
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
        pointBorderColor: 'rgba(255, 255, 255, 1)',
        pointBorderWidth: 2,
      },
      {
        label: 'Failed Logins',
        data: data.map(item => item.failed_count),
        borderColor: 'rgba(239, 68, 68, 1)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(239, 68, 68, 1)',
        pointBorderColor: 'rgba(255, 255, 255, 1)',
        pointBorderWidth: 2,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${granularityLabel[granularity]} Login Timeline`,
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <Line data={chartData} options={options} height={80} />
    </div>
  );
};
