import React from 'react';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

const ScatterChart = ({ 
  data, 
  title = 'Scatter Chart',
  height = 300,
  showLegend = true,
  xAxisLabel = 'X Axis',
  yAxisLabel = 'Y Axis',
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
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: color,
        borderWidth: 1,
        callbacks: {
          label: function(context) {
            return `${xAxisLabel}: ${context.parsed.x}, ${yAxisLabel}: ${context.parsed.y}`;
          }
        }
      }
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        display: true,
        title: {
          display: true,
          text: xAxisLabel,
          font: {
            size: 14,
            weight: 'bold'
          }
        },
        grid: {
          color: '#E5E7EB',
        },
        ticks: {
          color: '#6B7280'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: yAxisLabel,
          font: {
            size: 14,
            weight: 'bold'
          }
        },
        grid: {
          color: '#E5E7EB',
        },
        ticks: {
          color: '#6B7280'
        }
      },
    },
    elements: {
      point: {
        radius: 6,
        hoverRadius: 8,
        backgroundColor: color,
        borderColor: '#fff',
        borderWidth: 2
      }
    }
  };

  const chartData = {
    datasets: [
      {
        label: data.label || 'Data Points',
        data: data.points || [],
        backgroundColor: color,
        borderColor: '#fff',
        borderWidth: 2,
        ...data.options
      },
    ],
  };

  return (
    <div style={{ height: `${height}px` }}>
      <Scatter data={chartData} options={options} />
    </div>
  );
};

export default ScatterChart;