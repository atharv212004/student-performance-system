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
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const LineChart = ({ 
  data, 
  title = 'Line Chart',
  height = 300,
  showLegend = true,
  fill = false,
  color = '#3B82F6'
}) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: showLegend,
        position: 'top',
      },
      title: {
        display: !!title,
        text: title,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: color,
        borderWidth: 1,
      }
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          color: '#6B7280'
        }
      },
      y: {
        display: true,
        grid: {
          color: '#E5E7EB',
        },
        ticks: {
          color: '#6B7280'
        }
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
    elements: {
      point: {
        radius: 4,
        hoverRadius: 6,
        backgroundColor: color,
        borderColor: '#fff',
        borderWidth: 2
      },
      line: {
        borderWidth: 3,
        tension: 0.4
      }
    }
  };

  const chartData = {
    labels: data.labels || [],
    datasets: [
      {
        label: data.label || 'Data',
        data: data.values || [],
        borderColor: color,
        backgroundColor: fill ? `${color}20` : color,
        fill: fill,
        ...data.options
      },
    ],
  };

  return (
    <div style={{ height: `${height}px` }}>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default LineChart;