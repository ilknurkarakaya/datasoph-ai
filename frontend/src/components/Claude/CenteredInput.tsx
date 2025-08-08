import React, { useRef } from 'react';

interface CenteredInputProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string) => void;
  placeholder: string;
}

const CenteredInput: React.FC<CenteredInputProps> = ({ 
  inputValue, 
  setInputValue, 
  onSendMessage, 
  placeholder 
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const handleSubmit = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue.trim());
    }
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };
  
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      // Handle file upload logic here
      console.log('Files selected:', Array.from(files));
    }
  };
  
  return (
    <div className="relative">
      {/* Main Input Container */}
      <div className="flex items-end gap-3 bg-[var(--bg-input)] border border-[var(--border-light)] rounded-2xl p-4 shadow-sm hover:shadow-md transition-all duration-200 focus-within:border-[var(--border-focus)] focus-within:shadow-md">
        
        {/* File Upload Button */}
        <button 
          onClick={() => fileInputRef.current?.click()}
          className="flex-shrink-0 p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors"
          title="Upload file"
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
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            placeholder={placeholder}
            rows={1}
            className="w-full resize-none bg-transparent text-[var(--text-primary)] placeholder-[var(--text-placeholder)] border-none outline-none text-base leading-6"
            style={{
              minHeight: '24px',
              maxHeight: '200px'
            }}
          />
        </div>
        
        {/* Send Button */}
        <button
          onClick={handleSubmit}
          disabled={!inputValue.trim()}
          className="flex-shrink-0 p-2 bg-[var(--avatar-ai)] text-white rounded-lg hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 disabled:hover:bg-[var(--avatar-ai)]"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
      
      {/* Footer Text */}
      <p className="text-xs text-[var(--text-tertiary)] text-center mt-3">
        DataSoph AI can make mistakes. Verify important analysis results.
      </p>
      
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

export default CenteredInput; 