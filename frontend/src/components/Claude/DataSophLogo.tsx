import React from 'react';

interface DataSophLogoProps {
  size?: number;
  className?: string;
  animate?: boolean;
  color?: string;
}

const DataSophLogo: React.FC<DataSophLogoProps> = ({ 
  size = 32, 
  className = '',
  animate = false,
  color = '#ffde59'
}) => {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 200 200" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={`${className} ${animate ? 'animate-spin' : ''}`}
    >
      {/* Outermost spiral - Main spiral path */}
      <path
        d="M100 20 C145 20, 180 45, 180 100 C180 155, 145 180, 100 180 C55 180, 20 155, 20 100 C20 60, 45 35, 85 35 C115 35, 135 55, 135 85 C135 110, 120 125, 95 125 C80 125, 65 110, 65 95 C65 85, 72 78, 82 78 C88 78, 94 84, 94 90 C94 93, 92.5 94.5, 90.5 94.5 C89.2 94.5, 88.1 93.4, 88.1 92.1"
        stroke={color}
        strokeWidth="8"
        strokeLinecap="round"
        fill="none"
      />
      
      {/* Inner spiral layer for depth */}
      <path
        d="M100 25 C140 25, 175 50, 175 100 C175 150, 140 175, 100 175 C60 175, 25 150, 25 100 C25 65, 50 40, 85 40 C110 40, 130 60, 130 85 C130 105, 115 120, 95 120 C82 120, 70 108, 70 95 C70 87, 75 82, 83 82"
        stroke={color}
        strokeWidth="5"
        strokeLinecap="round"
        fill="none"
        opacity="0.7"
      />
      
      {/* Innermost spiral for fine detail */}
      <path
        d="M100 30 C135 30, 170 55, 170 100 C170 145, 135 170, 100 170 C65 170, 30 145, 30 100 C30 70, 50 50, 80 50 C100 50, 120 70, 120 90 C120 105, 110 115, 95 115 C85 115, 75 105, 75 95"
        stroke={color}
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
        opacity="0.6"
      />
    </svg>
  );
};

export default DataSophLogo; 