import React from 'react';
import { FileText, X } from 'lucide-react';
import { UploadedFileInfo } from '../../types/chat.ts';

interface InlineFileStatusProps {
  uploadedFile: UploadedFileInfo;
  onRemove: () => void;
}

const InlineFileStatus: React.FC<InlineFileStatusProps> = ({ 
  uploadedFile, 
  onRemove 
}) => {
  const formatFileSize = (size?: number): string => {
    if (!size) return '';
    if (size === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(size) / Math.log(k));
    return parseFloat((size / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="flex items-center gap-2 px-2 py-1 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-md text-xs">
      <FileText className="w-3 h-3 text-blue-600 dark:text-blue-400 flex-shrink-0" />
      <span className="text-blue-700 dark:text-blue-300 font-medium truncate max-w-[120px]">
        {uploadedFile.filename}
      </span>
      {uploadedFile.size && (
        <span className="text-blue-500 dark:text-blue-400 text-[10px]">
          ({formatFileSize(uploadedFile.size)})
        </span>
      )}
      <button
        onClick={onRemove}
        className="p-0.5 text-blue-500 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-800 rounded transition-colors flex-shrink-0"
        title="Remove file"
      >
        <X className="w-3 h-3" />
      </button>
    </div>
  );
};

export default InlineFileStatus; 