import React, { useRef } from 'react';
import { useFileUpload } from '../../hooks/useFileUpload';
import { useDragAndDrop } from '../../hooks/useDragAndDrop';

interface ClaudeInputAreaProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSend: () => void;
  isTyping: boolean;
  onFileUploaded?: (fileId: string, fileName: string) => void;
}

const ClaudeInputArea: React.FC<ClaudeInputAreaProps> = ({ 
  inputValue, 
  setInputValue, 
  onSend, 
  isTyping,
  onFileUploaded 
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { uploadFile, isUploading, uploadError, validateFile } = useFileUpload();
  const { 
    isDragging, 
    isOver, 
    handleDragEnter, 
    handleDragLeave, 
    handleDragOver, 
    handleDrop 
  } = useDragAndDrop();
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };
  
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0]; // Handle first file
      try {
        const uploadedFile = await uploadFile(file);
        if (uploadedFile && onFileUploaded) {
          // Automatically trigger AI analysis with a standard message
          onFileUploaded(uploadedFile.id, uploadedFile.name);
        }
      } catch (error) {
        console.error('File upload error:', error);
      }
    }
    // Reset input value to allow uploading the same file again
    e.target.value = '';
  };

  const handleFilesDropped = async (files: File[]) => {
    if (files.length > 0) {
      const file = files[0]; // Handle first file
      
      // Validate file before uploading
      const validationError = validateFile(file);
      if (validationError) {
        console.error('File validation error:', validationError);
        return;
      }

      try {
        const uploadedFile = await uploadFile(file);
        if (uploadedFile && onFileUploaded) {
          // Automatically trigger AI analysis with a standard message
          onFileUploaded(uploadedFile.id, uploadedFile.name);
        }
      } catch (error) {
        console.error('File drop upload error:', error);
      }
    }
  };
  
  return (
    <div className="relative">
      {/* Input Container with Drag & Drop */}
      <div 
        data-drop-zone="true"
        className="flex items-end gap-2 relative"
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={(e) => handleDrop(e, handleFilesDropped)}
      >
        {/* Drag & Drop Overlay */}
        {isDragging && (
          <div className={`absolute inset-0 z-10 rounded-xl transition-all duration-200 flex items-center justify-center ${
            isOver 
              ? 'bg-blue-500/10 border border-blue-400' 
              : 'bg-gray-100/50 dark:bg-gray-800/50 border border-gray-300 dark:border-gray-600'
          }`}>
            <div className="flex items-center gap-1 px-2 py-1 bg-white/90 dark:bg-gray-900/90 rounded-md shadow-sm">
              <svg className={`w-3 h-3 ${isOver ? 'text-blue-500' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 12l3 3m0 0l3-3m-3 3V9" />
              </svg>
              <span className={`text-xs ${isOver ? 'text-blue-600' : 'text-gray-600'}`}>
                {isOver ? 'Bırak' : 'Sürükle'}
              </span>
            </div>
          </div>
        )}

        {/* File Upload Button */}
        <button 
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading || isTyping}
          className={`p-2 rounded-md transition-colors ${
            isUploading || isTyping 
              ? 'text-[var(--text-secondary)] opacity-50 cursor-not-allowed' 
              : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)]'
          }`}
          title={isUploading ? 'Uploading...' : 'Upload file for analysis'}
        >
          {isUploading ? (
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
          )}
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
      
      {/* Upload Error */}
      {uploadError && (
        <div className="text-xs text-red-500 text-center mt-2 px-2 py-1 bg-red-50 dark:bg-red-900/20 rounded">
          {uploadError}
        </div>
      )}
      
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