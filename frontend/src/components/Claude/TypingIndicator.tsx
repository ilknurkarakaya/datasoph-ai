import React from 'react';
import DataSophLogo from './DataSophLogo.tsx';

interface TypingIndicatorProps {
  stage?: 'thinking' | 'analyzing' | 'processing' | 'generating';
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ stage = 'thinking' }) => {
  const getAnimationClass = () => {
    switch(stage) {
      case 'thinking': return 'animate-spin';
      case 'analyzing': return 'animate-spin';
      case 'processing': return 'animate-spin';
      case 'generating': return 'animate-spin';
      default: return 'animate-spin';
    }
  };

  return (
    <div className="flex gap-4">
      {/* Spinning DataSoph Spiral Logo - No Background Circle */}
      <div className="w-8 h-8 flex items-center justify-center">
        <DataSophLogo 
          size={24} 
          color="#ffde59"
          className={getAnimationClass()}
        />
      </div>
      
      {/* Message Content */}
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-sm font-medium text-[var(--text-primary)] font-system">Datasoph</span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator; 