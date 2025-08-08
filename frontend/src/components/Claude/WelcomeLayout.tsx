import React from 'react';
import CenteredInput from './CenteredInput';
import DataSophLogo from './DataSophLogo';

interface WelcomeLayoutProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string) => void;
}

const WelcomeLayout: React.FC<WelcomeLayoutProps> = ({ 
  inputValue, 
  setInputValue, 
  onSendMessage 
}) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-full px-6 py-8 overflow-y-auto">
      {/* Hero Section */}
      <div className="text-center mb-8 max-w-2xl">
        {/* DataSoph Spiral Logo */}
        <div className="flex items-center justify-center mb-6">
          <div className="w-20 h-20 flex items-center justify-center">
            <DataSophLogo 
              size={64} 
              className="drop-shadow-sm" 
              color="#f97316"
            />
          </div>
        </div>
        
        {/* Welcome Text */}
        <h1 className="text-3xl font-medium text-[var(--text-primary)] mb-4 font-system">
          How can I help you today?
        </h1>

        <p className="text-lg text-[var(--text-secondary)] leading-relaxed font-system">
          I'm DataSoph.ai, your professional data science assistant. Upload a dataset or ask me any data-related question to get started.
        </p>
      </div>

      {/* Centered Input */}
      <div className="w-full max-w-3xl">
        <CenteredInput
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSendMessage={onSendMessage}
          placeholder="Ask DataSoph AI anything about data science..."
        />
      </div>
    </div>
  );
};

export default WelcomeLayout; 