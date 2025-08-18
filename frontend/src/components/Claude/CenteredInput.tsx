import React, { useRef, useState } from 'react';
import { useFileUpload } from '../../hooks/useFileUpload.ts';
import { useDragAndDrop } from '../../hooks/useDragAndDrop.ts';
import { UploadedFileInfo } from '../../types/chat.ts';
import InlineFileStatus from '../FileUpload/InlineFileStatus.tsx';

interface CenteredInputProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string, fileId?: string) => void;
  placeholder: string;
  isTyping?: boolean;
}

const CenteredInput: React.FC<CenteredInputProps> = ({ 
  inputValue, 
  setInputValue, 
  onSendMessage, 
  placeholder,
  isTyping = false
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadedFileInfo, setUploadedFileInfo] = useState<UploadedFileInfo | null>(null);
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
    
    // If AI is typing, send an empty message to trigger stop functionality
    if (isTyping) {
      onSendMessage('', undefined); // This will trigger the stop functionality in handleSendMessage
      return;
    }

    // Normal message sending when AI is not typing
    if (uploadedFileInfo) {
      // If there's an uploaded file, send message with file context
      const message = inputValue.trim() || `Please analyze my uploaded file: ${uploadedFileInfo.filename}`;
      onSendMessage(message, uploadedFileInfo.file_id);
      // Keep the file info for continued context
    } else if (inputValue.trim()) {
      // Normal message without file
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
        const uploadResult = await uploadFile(file);
        if (uploadResult) {
          // Only show upload confirmation - NO automatic analysis
          setUploadedFileInfo({
            file_id: uploadResult.id,
            filename: uploadResult.name,
            uploaded_at: new Date().toISOString(),
            analysis_done: false,
            size: uploadResult.size
          });
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
        const uploadResult = await uploadFile(file);
        if (uploadResult) {
          // Only show upload confirmation - NO automatic analysis
          setUploadedFileInfo({
            file_id: uploadResult.id,
            filename: uploadResult.name,
            uploaded_at: new Date().toISOString(),
            analysis_done: false,
            size: uploadResult.size
          });
        }
      } catch (error) {
        console.error('File drop upload error:', error);
      }
    }
  };

  const handleRemoveFile = () => {
    setUploadedFileInfo(null);
  };

  const canSend = (inputValue.trim() || uploadedFileInfo || isTyping) && !isUploading;
  
  return (
    <div className="relative">
      {/* Main Input Container with Drag & Drop */}
      <div 
        data-drop-zone="true"
        className="flex flex-col gap-2 bg-[var(--bg-input)] border border-[var(--border-light)] rounded-2xl px-4 py-3 shadow-sm hover:shadow-md transition-all duration-200 relative"
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={(e) => handleDrop(e, handleFilesDropped)}
      >
        {/* Drag & Drop Overlay */}
        {isDragging && (
          <div 
            style={{
              backgroundColor: isOver 
                ? 'var(--bg-hover)' 
                : 'var(--bg-sidebar)',
              opacity: isOver ? 0.95 : 0.90,
              border: isOver ? '2px solid var(--border-medium)' : '1px solid var(--border-light)'
            }} 
            className="absolute inset-0 z-10 rounded-2xl flex items-center justify-center transition-colors duration-200"
          >
            <div className="px-3 py-2 text-sm text-[#656d76] dark:text-[#8b949e] font-medium">
              {isOver ? 'Drop files here' : 'Drag files here'}
            </div>
          </div>
        )}

        {/* Inline File Status - Elegant and thin */}
        {uploadedFileInfo && (
          <div className="pb-1">
            <InlineFileStatus 
              uploadedFile={uploadedFileInfo}
              onRemove={handleRemoveFile}
            />
          </div>
        )}
        
        {/* Input Row */}
        <div className="flex items-end gap-3">
          {/* File Upload Button */}
          <button 
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading || isTyping}
            className={`flex-shrink-0 p-2 rounded-lg transition-colors ${
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
              onChange={handleInputChange}
              onKeyDown={handleKeyPress}
              placeholder={uploadedFileInfo ? "Ask questions about your data or send empty to analyze..." : placeholder}
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
            disabled={!canSend}
            className="flex-shrink-0 p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {(() => {
              return isTyping ? (
                // Stop icon when AI is typing
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <rect x="6" y="6" width="12" height="12" rx="2" strokeWidth="2" />
                </svg>
              ) : (
                // Send icon when ready to send
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              );
            })()}
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
      <p className="text-[10px] text-[var(--text-tertiary)] text-center mt-3 opacity-70">
        Datasoph can make mistakes. Verify important analysis results.
      </p>
      
      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".csv,.xlsx,.xls,.json,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg"
        onChange={handleFileUpload}
        className="hidden"
      />
    </div>
  );
};

export default CenteredInput; 