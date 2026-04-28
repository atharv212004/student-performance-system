import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import Card from './Card';

const StatCard = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendValue,
  color = 'primary',
  loading = false
}) => {
  const colorClasses = {
    primary: {
      bg: 'bg-primary-50',
      icon: 'text-primary-600',
      text: 'text-primary-600'
    },
    success: {
      bg: 'bg-success-50',
      icon: 'text-success-600',
      text: 'text-success-600'
    },
    warning: {
      bg: 'bg-warning-50',
      icon: 'text-warning-600',
      text: 'text-warning-600'
    },
    danger: {
      bg: 'bg-danger-50',
      icon: 'text-danger-600',
      text: 'text-danger-600'
    }
  };

  const getTrendIcon = () => {
    if (trend === 'up') return TrendingUp;
    if (trend === 'down') return TrendingDown;
    return Minus;
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-success-600';
    if (trend === 'down') return 'text-danger-600';
    return 'text-gray-500';
  };

  const TrendIcon = getTrendIcon();

  if (loading) {
    return (
      <Card className="animate-pulse">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
          </div>
          <div className="ml-4 flex-1">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className={`w-12 h-12 ${colorClasses[color].bg} rounded-lg flex items-center justify-center`}>
            {Icon && <Icon className={`w-6 h-6 ${colorClasses[color].icon}`} />}
          </div>
        </div>
        
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          
          {(subtitle || (trend && trendValue)) && (
            <div className="flex items-center mt-1">
              {trend && trendValue && (
                <div className={`flex items-center ${getTrendColor()}`}>
                  <TrendIcon className="w-4 h-4 mr-1" />
                  <span className="text-sm font-medium">{trendValue}</span>
                </div>
              )}
              
              {subtitle && (
                <span className={`text-sm ${trend && trendValue ? 'ml-2' : ''} text-gray-500`}>
                  {subtitle}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};

export default StatCard;