import React from 'react';
import { FileAttachment } from '../../types/chat.ts';

interface FilePreviewProps {
  files: FileAttachment[];
  onRemoveFile: (fileId: string) => void;
  formatFileSize: (bytes: number) => string;
}

const FilePreview: React.FC<FilePreviewProps> = ({ files, onRemoveFile, formatFileSize }) => {
  if (files.length === 0) return null;

  const getFileIcon = (type: string) => {
    if (type.includes('csv')) {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
        </svg>
      );
    } else if (type.includes('json')) {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M5,3H7V5H5V10A2,2 0 0,1 3,8V5A2,2 0 0,1 5,3M19,3A2,2 0 0,1 21,5V8A2,2 0 0,1 19,10V5H17V3H19M5,13H7V15H5V20A2,2 0 0,0 7,22H5A2,2 0 0,0 3,20V15A2,2 0 0,0 5,13M19,13A2,2 0 0,0 21,15V20A2,2 0 0,0 19,22H17V20H19V15H17V13H19Z" />
        </svg>
      );
    } else if (type.includes('excel') || type.includes('spreadsheet')) {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M15.5,15L13.5,17L15.5,19L14.09,20.41L12.09,18.41L10.09,20.41L8.68,19L10.68,17L8.68,15L10.09,13.59L12.09,15.59L14.09,13.59L15.5,15Z" />
        </svg>
      );
    } else {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
        </svg>
      );
    }
  };

  return (
    <div className="mb-3 space-y-2">
      {files.map((file) => (
        <div
          key={file.id}
          className="
            flex items-center gap-3
            p-2 rounded-lg
            bg-claude-input border border-claude-border
            text-sm
          "
        >
          <div className="flex-shrink-0 text-claude-textMuted">
            {getFileIcon(file.type)}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="text-claude-text font-medium truncate">
              {file.filename}
            </div>
            <div className="text-claude-textMuted text-xs">
              {formatFileSize(file.size)}
            </div>
          </div>
          
          <button
            onClick={() => onRemoveFile(file.id)}
            className="
              flex-shrink-0
              p-1 rounded-md
              text-claude-textMuted hover:text-red-400
              hover:bg-red-900 hover:bg-opacity-20
              transition-all duration-200
            "
            title="Remove file"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      ))}
    </div>
  );
};

export default FilePreview; 