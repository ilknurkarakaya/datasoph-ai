import React, { useRef } from 'react';

interface ClaudeInputAreaProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSend: () => void;
  isTyping: boolean;
}

const ClaudeInputArea: React.FC<ClaudeInputAreaProps> = ({ 
  inputValue, 
  setInputValue, 
  onSend, 
  isTyping 
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      // Handle file upload logic here
      console.log('Files selected:', Array.from(files));
    }
  };
  
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  };
  
  return (
    <div className="relative">
      {/* Input Container */}
      <div className="flex items-end gap-2">
        {/* File Upload Button */}
        <button 
          onClick={() => fileInputRef.current?.click()}
          className="p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] rounded-md transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
          </svg>
        </button>
        
        {/* Text Input */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Message DataSoph.ai..."
            className="w-full resize-none border-0 bg-transparent text-base text-[var(--text-primary)] placeholder-[var(--text-placeholder)] focus:outline-none font-system"
            rows={1}
            style={{ minHeight: '24px', maxHeight: '120px' }}
          />
          
          {/* Send Button */}
          <button
            onClick={onSend}
            disabled={!inputValue.trim() || isTyping}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 text-[var(--text-secondary)] hover:text-[var(--text-primary)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
      
      {/* Footer Text */}
      <div className="text-xs text-[var(--text-tertiary)] text-center mt-2">
        DataSoph AI can make mistakes. Verify important analysis results.
      </div>
      
      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".csv,.xlsx,.xls,.json,.txt,.pdf"
        onChange={handleFileUpload}
        className="hidden"
      />
    </div>
  );
};

export default ClaudeInputArea; 