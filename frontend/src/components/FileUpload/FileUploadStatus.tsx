import React from 'react';
import { FileText, X } from 'lucide-react';
import { UploadedFileInfo } from '../../types/chat.ts';

interface FileUploadStatusProps {
  uploadedFile: UploadedFileInfo;
  onRemove: () => void;
}

const FileUploadStatus: React.FC<FileUploadStatusProps> = ({ 
  uploadedFile, 
  onRemove 
}) => {
  return (
    <div className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <div>
            <h3 className="text-sm font-medium text-blue-900 dark:text-blue-100">
              ✅ File uploaded: {uploadedFile.filename}
            </h3>
            <p className="text-xs text-blue-600 dark:text-blue-400">
              🔬 Expert Data Scientist AI is analyzing... Ask questions about your data!
            </p>
          </div>
        </div>
        <button
          onClick={onRemove}
          className="p-1 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-800 rounded transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default FileUploadStatus; 