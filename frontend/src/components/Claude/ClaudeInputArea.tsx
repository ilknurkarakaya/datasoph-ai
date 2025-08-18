import React, { useRef, useState } from 'react';
import { useFileUpload } from '../../hooks/useFileUpload.ts';
import { useDragAndDrop } from '../../hooks/useDragAndDrop.ts';
import { UploadedFileInfo } from '../../types/chat.ts';
import InlineFileStatus from '../FileUpload/InlineFileStatus.tsx';


interface ClaudeInputAreaProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSend: (fileId?: string) => void;
  isTyping: boolean;
  onFileUploaded?: (fileId: string, fileName: string) => void;
  addMessage?: (message: any) => void;
}

const ClaudeInputArea: React.FC<ClaudeInputAreaProps> = ({ 
  inputValue, 
  setInputValue, 
  onSend, 
  isTyping,
  onFileUploaded,
  addMessage
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
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendClick();
    }
  };

  const handleSendClick = () => {
    // If AI is typing, we need to call onSend to trigger stop functionality
    if (isTyping) {
      onSend(); // This will trigger the stop functionality in handleSendMessage
      return;
    }

    // 🔧 FIXED: Chat only - no file processing here
    if (inputValue.trim()) {
      // Sending chat message
      onSend(); // Pure chat message
    }
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
          
          // Send analysis results directly to chat if available
          if (uploadResult.analysisData && addMessage) {
            const analysisMessage = formatAnalysisForChat(uploadResult.analysisData, uploadResult.name);
            addMessage({
              id: Date.now(),
              type: 'assistant',
              content: analysisMessage,
              timestamp: new Date().toISOString()
            });
          }
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
          
          // Send analysis results directly to chat if available
          if (uploadResult.analysisData && addMessage) {
            const analysisMessage = formatAnalysisForChat(uploadResult.analysisData, uploadResult.name);
            addMessage({
              id: Date.now(),
              type: 'assistant',
              content: analysisMessage,
              timestamp: new Date().toISOString()
            });
          }
        }
      } catch (error) {
        console.error('File drop upload error:', error);
      }
    }
  };

  const handleRemoveFile = () => {
    setUploadedFileInfo(null);
  };

  const formatAnalysisForChat = (analysisData: any, fileName: string): string => {
    if (!analysisData) return `📊 **${fileName}** analizi tamamlandı.`;
    
    let message = `📊 **${fileName} - Analiz Sonuçları**\n\n`;
    
    if (analysisData.summary) {
      message += `**📋 Özet:**\n${analysisData.summary}\n\n`;
    }
    
    if (analysisData.insights && analysisData.insights.length > 0) {
      message += `**💡 Önemli Bulgular:**\n`;
      analysisData.insights.slice(0, 5).forEach((insight: string, index: number) => {
        message += `${index + 1}. ${insight}\n`;
      });
      message += `\n`;
    }
    
    if (analysisData.statistics) {
      message += `**📈 İstatistikler:**\n`;
      Object.entries(analysisData.statistics).slice(0, 4).forEach(([key, value]) => {
        message += `• **${key}:** ${value}\n`;
      });
      message += `\n`;
    }
    
    if (analysisData.charts && analysisData.charts.length > 0) {
      message += `**📊 Grafikler Oluşturuldu:**\n`;
      analysisData.charts.forEach((chart: string) => {
        message += `• ${chart}\n`;
      });
      message += `\n`;
    }
    
    message += `✅ **Analiz tamamlandı!** Detaylı sorular sorabilir veya daha fazla analiz isteyebilirsiniz.`;
    
    return message;
  };

  const canSend = (inputValue.trim() || uploadedFileInfo || isTyping) && !isUploading;
  
  return (
    <div className="relative">
      {/* Input Container with Drag & Drop */}
      <div 
        data-drop-zone="true"
        className="flex flex-col gap-2 relative p-3 border-[0.5px] border-[var(--border-light)] rounded-xl bg-[var(--bg-input)] shadow-sm hover:border-[var(--border-medium)] transition-colors"
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
            className="absolute inset-0 z-10 rounded-xl flex items-center justify-center transition-colors duration-200"
          >
            <div className="px-2 py-1 text-xs text-[#656d76] dark:text-[#8b949e] font-medium">
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
        <div className="flex items-end gap-2">
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
              placeholder={uploadedFileInfo ? "Ask questions about your data or send empty to analyze..." : "Ask like you're working with a data scientist..."}
              className="w-full resize-none border-0 bg-transparent text-base text-[var(--text-primary)] placeholder-[var(--text-placeholder)] focus:outline-none font-system pr-8"
              rows={1}
              style={{ minHeight: '24px', maxHeight: '120px' }}
            />
            
            {/* Send Button */}
            <button
              onClick={handleSendClick}
              disabled={!canSend}
              className="absolute right-0 top-1/2 transform -translate-y-1/2 p-1 text-[var(--text-secondary)] hover:text-[var(--text-primary)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {(() => {
                return isTyping ? (
                  // Stop icon when AI is typing
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="6" y="6" width="12" height="12" rx="2" strokeWidth="2" />
                  </svg>
                ) : (
                  // Send icon when ready to send
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                );
              })()}
            </button>
          </div>
        </div>
      </div>
      
      {/* Upload Error */}
      {uploadError && (
        <div className="text-xs text-red-500 text-center mt-2 px-2 py-1 bg-red-50 dark:bg-red-900/20 rounded">
          {uploadError}
        </div>
      )}
      
      {/* Footer Text */}
      <div className="text-[10px] text-[var(--text-tertiary)] text-center mt-2 opacity-70 flex items-center justify-center gap-2">
        <span>Datasoph can make mistakes. Verify important analysis results.</span>
        {uploadedFileInfo && (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-[9px] font-medium">
            🔬 Expert AI Active
          </span>
        )}
      </div>
      
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

export default ClaudeInputArea; 