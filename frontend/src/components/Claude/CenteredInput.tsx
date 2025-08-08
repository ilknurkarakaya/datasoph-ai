import React, { useRef } from 'react';
import { useFileUpload } from '../../hooks/useFileUpload';
import { useDragAndDrop } from '../../hooks/useDragAndDrop';

interface CenteredInputProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string, fileId?: string) => void;
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
  const { uploadFile, isUploading, uploadError, validateFile } = useFileUpload();
  const { 
    isDragging, 
    isOver, 
    handleDragEnter, 
    handleDragLeave, 
    handleDragOver, 
    handleDrop 
  } = useDragAndDrop();
  
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
  
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0]; // Handle first file
      try {
        const uploadedFile = await uploadFile(file);
        if (uploadedFile) {
          // Automatically send a message to analyze the uploaded file
          const analysisMessage = `Analyze the uploaded file: ${uploadedFile.name}`;
          onSendMessage(analysisMessage, uploadedFile.id);
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
        if (uploadedFile) {
          // Automatically send a message to analyze the uploaded file
          const analysisMessage = `Analyze the uploaded file: ${uploadedFile.name}`;
          onSendMessage(analysisMessage, uploadedFile.id);
        }
      } catch (error) {
        console.error('File drop upload error:', error);
      }
    }
  };
  
  return (
    <div className="relative">
      {/* Main Input Container with Drag & Drop */}
      <div 
        data-drop-zone="true"
        className="flex items-end gap-3 bg-[var(--bg-input)] border border-[var(--border-light)] rounded-2xl p-4 shadow-sm hover:shadow-md transition-all duration-200 relative"
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={(e) => handleDrop(e, handleFilesDropped)}
      >
        {/* Drag & Drop Overlay */}
        {isDragging && (
          <div className={`absolute inset-0 z-10 rounded-2xl transition-all duration-300 ease-out flex items-center justify-center backdrop-blur-sm ${
            isOver 
              ? 'bg-[var(--bg-main)]/95 border-2 border-dashed border-[#ffde59]/70' 
              : 'bg-[var(--bg-main)]/90 border-2 border-dashed border-[var(--border-light)]'
          }`}>
            <div className="text-center px-6 py-4">
              <div className={`w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center transition-all duration-300 ${
                isOver 
                  ? 'bg-[#ffde59]/15 scale-105' 
                  : 'bg-[var(--bg-hover)] scale-100'
              }`}>
                <svg className={`w-6 h-6 transition-colors duration-300 ${
                  isOver ? 'text-[#ffde59]' : 'text-[var(--text-secondary)]'
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 12l3 3m0 0l3-3m-3 3V9" />
                </svg>
              </div>
              <h3 className={`text-base font-medium mb-1 transition-colors duration-300 font-system ${
                isOver ? 'text-[#ffde59]' : 'text-[var(--text-primary)]'
              }`}>
                {isOver ? 'Dosyayı bırak' : 'Dosya yükle'}
              </h3>
              <p className="text-sm text-[var(--text-secondary)] font-system">
                {isOver 
                  ? 'AI analizi başlayacak' 
                  : 'CSV, Excel, JSON desteklenir'}
              </p>
            </div>
          </div>
        )}
        
        {/* File Upload Button */}
        <button 
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className={`flex-shrink-0 p-2 rounded-lg transition-colors ${
            isUploading 
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
          disabled={!inputValue.trim() || isUploading}
          className="flex-shrink-0 p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
      
      {/* Upload Error */}
      {uploadError && (
        <div className="text-xs text-red-500 text-center mt-2 px-2 py-1 bg-red-50 dark:bg-red-900/20 rounded">
          {uploadError}
        </div>
      )}
      
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