import React from 'react';

interface DataSophLogoProps {
  variant?: 'default' | 'compact' | 'icon-only';
  className?: string;
}

const DataSophLogo: React.FC<DataSophLogoProps> = ({ 
  variant = 'default', 
  className = '' 
}) => {
  if (variant === 'icon-only') {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <div className="relative">
          {/* Sophisticated geometric icon representing data science expertise */}
          <svg 
            width="32" 
            height="32" 
            viewBox="0 0 32 32" 
            className="text-blue-600"
            fill="currentColor"
          >
            {/* Neural network nodes */}
            <circle cx="8" cy="8" r="2" className="fill-blue-600" />
            <circle cx="24" cy="8" r="2" className="fill-blue-500" />
            <circle cx="8" cy="24" r="2" className="fill-blue-700" />
            <circle cx="24" cy="24" r="2" className="fill-blue-500" />
            <circle cx="16" cy="16" r="3" className="fill-blue-800" />
            
            {/* Connecting lines representing data flow */}
            <line x1="8" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="24" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="8" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="24" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            
            {/* Statistical elements */}
            <path d="M4 28 Q16 20 28 28" stroke="currentColor" strokeWidth="1" fill="none" className="text-blue-300" />
          </svg>
        </div>
      </div>
    );
  }

  if (variant === 'compact') {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="relative">
          <svg 
            width="28" 
            height="28" 
            viewBox="0 0 32 32" 
            className="text-blue-600"
            fill="currentColor"
          >
            <circle cx="8" cy="8" r="2" className="fill-blue-600" />
            <circle cx="24" cy="8" r="2" className="fill-blue-500" />
            <circle cx="8" cy="24" r="2" className="fill-blue-700" />
            <circle cx="24" cy="24" r="2" className="fill-blue-500" />
            <circle cx="16" cy="16" r="3" className="fill-blue-800" />
            <line x1="8" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="24" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="8" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <line x1="24" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
            <path d="M4 28 Q16 20 28 28" stroke="currentColor" strokeWidth="1" fill="none" className="text-blue-300" />
          </svg>
        </div>
        <div>
          <span className="text-xl font-bold text-gray-900 tracking-tight">
            DataSoph
          </span>
          <span className="text-xs text-blue-600 font-medium block leading-tight">
            PhD-Level AI
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <div className="relative">
        <svg 
          width="40" 
          height="40" 
          viewBox="0 0 32 32" 
          className="text-blue-600"
          fill="currentColor"
        >
          {/* Neural network nodes */}
          <circle cx="8" cy="8" r="2" className="fill-blue-600" />
          <circle cx="24" cy="8" r="2" className="fill-blue-500" />
          <circle cx="8" cy="24" r="2" className="fill-blue-700" />
          <circle cx="24" cy="24" r="2" className="fill-blue-500" />
          <circle cx="16" cy="16" r="3" className="fill-blue-800" />
          
          {/* Connecting lines representing data flow */}
          <line x1="8" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
          <line x1="24" y1="8" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
          <line x1="8" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
          <line x1="24" y1="24" x2="16" y2="16" stroke="currentColor" strokeWidth="1.5" className="text-blue-400" />
          
          {/* Statistical curve */}
          <path d="M4 28 Q16 20 28 28" stroke="currentColor" strokeWidth="1" fill="none" className="text-blue-300" />
          
          {/* Expertise indicator */}
          <circle cx="26" cy="6" r="4" className="fill-blue-100 stroke-blue-600" strokeWidth="1" />
          <text x="26" y="7" className="text-xs font-bold fill-blue-600" textAnchor="middle">PhD</text>
        </svg>
      </div>
      
      <div className="flex flex-col">
        <div className="flex items-baseline space-x-1">
          <span className="text-2xl font-bold text-gray-900 tracking-tight">
            DataSoph
          </span>
          <span className="text-lg font-medium text-blue-600">
            .ai
          </span>
        </div>
        
        <div className="flex items-center space-x-2 -mt-1">
          <span className="text-xs text-gray-600 font-medium">
            PhD-Level Data Science AI
          </span>
          <div className="flex items-center space-x-1">
            <div className="w-1 h-1 bg-blue-500 rounded-full"></div>
            <span className="text-xs text-blue-600 font-semibold">
              Fortune 500 Standards
            </span>
          </div>
        </div>
        
        <div className="text-xs text-gray-500 mt-0.5 font-medium">
          Think like a consultant • Communicate like a professor • Deliver like a pro
        </div>
      </div>
    </div>
  );
};

export default DataSophLogo; 