import React from 'react';
import CenteredInput from './CenteredInput.tsx';
import DataSophLogo from './DataSophLogo.tsx';

interface WelcomeLayoutProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string, fileId?: string) => void;
  isTyping?: boolean;
  addMessage?: (message: any) => void;
}

const WelcomeLayout: React.FC<WelcomeLayoutProps> = ({ 
  inputValue, 
  setInputValue, 
  onSendMessage,
  isTyping = false,
  addMessage
}) => {
  return (
    <div className="relative min-h-screen px-6">
      {/* Logo positioned at top */}
      <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 flex flex-col items-center text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="w-20 h-20 flex items-center justify-center">
            <DataSophLogo 
              size={72} 
              className="drop-shadow-sm" 
              color="#ffde59"
            />
          </div>
        </div>
        
        <h1 className="text-4xl font-medium text-[var(--text-primary)] font-system">
          How can I help you today? {/* Updated v8.2 - Bigger Font */}
        </h1>
      </div>

      {/* Chat Input - EXACTLY in the center of viewport */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-3xl px-6">
        <CenteredInput
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSendMessage={onSendMessage}
          placeholder="Ask like you're working with a data scientist..."
          isTyping={isTyping}
          addMessage={addMessage}
        />
      </div>
    </div>
  );
};

export default WelcomeLayout; 