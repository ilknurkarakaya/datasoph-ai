import React from 'react';
import DataSophLogo from './DataSophLogo';

interface TypingIndicatorProps {
  stage?: 'thinking' | 'analyzing' | 'processing' | 'generating';
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ stage = 'thinking' }) => {
  const getTypingMessage = () => {
    switch(stage) {
      case 'thinking': return 'Thinking...';
      case 'analyzing': return 'Analyzing your data...';
      case 'processing': return 'Processing results...';
      case 'generating': return 'Generating insights...';
      default: return 'Working...';
    }
  };

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
          color="#f97316"
          className={getAnimationClass()}
        />
      </div>
      
      {/* Message Content */}
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-sm font-medium text-[var(--text-primary)]">DataSoph AI</span>
          <span className="text-xs text-[var(--text-tertiary)]">{getTypingMessage()}</span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator; 