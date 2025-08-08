import React from 'react';
import CenteredInput from './CenteredInput';
import DataSophLogo from './DataSophLogo';

interface WelcomeLayoutProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string, fileId?: string) => void;
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
              color="#ffde59"
            />
          </div>
        </div>
        
        {/* Welcome Text */}
        <h1 className="text-3xl font-medium text-[var(--text-primary)] mb-4 font-system">
          How can I help you today? {/* Updated v5.0 */}
        </h1>


      </div>

      {/* Centered Input */}
      <div className="w-full max-w-3xl">
        <CenteredInput
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSendMessage={onSendMessage}
          placeholder="Ask like you're working with a data scientist..."
        />
      </div>
    </div>
  );
};

export default WelcomeLayout; 