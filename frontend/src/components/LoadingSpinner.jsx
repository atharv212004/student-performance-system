import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ 
  size = 'md', 
  text = 'Loading...', 
  className = '',
  fullScreen = false 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  };

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-80 flex items-center justify-center z-50">
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className={`${sizeClasses.xl} animate-spin text-primary-600`} />
          <p className={`${textSizeClasses.lg} text-gray-600 font-medium`}>
            {text}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center justify-center space-x-2 ${className}`}>
      <Loader2 className={`${sizeClasses[size]} animate-spin text-primary-600`} />
      {text && (
        <span className={`${textSizeClasses[size]} text-gray-600`}>
          {text}
        </span>
      )}
    </div>
  );
};

export default LoadingSpinner;