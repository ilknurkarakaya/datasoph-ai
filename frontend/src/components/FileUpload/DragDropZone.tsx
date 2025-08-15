import React, { useState, useRef, useCallback } from 'react';
import { Upload, FileText, X, Info } from 'lucide-react';
import SupportedFormatsInfo from './SupportedFormatsInfo.tsx';

interface DragDropZoneProps {
  onFileSelect: (file: File) => void;
  selectedFile?: any;
  onRemoveFile?: () => void;
  accept?: string;
  maxSize?: number; // in MB
  showSupportedFormats?: boolean;
}

const DragDropZone: React.FC<DragDropZoneProps> = ({
  onFileSelect,
  selectedFile,
  onRemoveFile,
  accept = '.csv,.xlsx,.xls,.json,.jsonl,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg,.docx,.html,.md,.ipynb,.sql,.xml,.yaml,.yml,.sqlite,.db,.h5,.hdf5,.sav,.dta,.parquet,.pkl,.onnx,.wav,.mp3,.mp4',
  maxSize = 100,
  showSupportedFormats = true
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [showFormatsInfo, setShowFormatsInfo] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    // Check file size
    if (file.size > maxSize * 1024 * 1024) {
      alert(`File size must be less than ${maxSize}MB`);
      return;
    }

    setIsUploading(true);
    
    // Simulate upload delay (like Claude does)
    await new Promise(resolve => setTimeout(resolve, 500));
    
    onFileSelect(file);
    setIsUploading(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (selectedFile) {
    return (
      <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            <div className="flex flex-col">
              <span className="text-sm font-medium text-blue-900">{selectedFile.name}</span>
              <span className="text-xs text-blue-700">
                {formatFileSize(selectedFile.size)}
              </span>
            </div>
          </div>
          {onRemoveFile && (
            <button
              onClick={onRemoveFile}
              className="p-1 text-blue-600 hover:text-blue-700 hover:bg-blue-100 rounded transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        onChange={handleFileInputChange}
        className="hidden"
      />
      
      <div
        onClick={handleClick}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all
          ${isDragOver 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <Upload className="w-8 h-8 text-gray-400 mx-auto mb-4" />
        <p className="text-sm text-gray-600 mb-2">
          {isUploading ? 'Uploading...' : 'Drag files here or click to upload'}
        </p>
        <div className="flex items-center justify-center space-x-4 text-xs text-gray-500">
          <span>Supports 40+ formats including CSV, Excel, JSON, PDF, images with OCR & more (max {maxSize}MB)</span>
          {showSupportedFormats && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowFormatsInfo(!showFormatsInfo);
              }}
              className="flex items-center space-x-1 text-blue-600 hover:text-blue-700 transition-colors"
            >
              <Info className="w-3 h-3" />
              <span>View all formats</span>
            </button>
          )}
        </div>
      </div>
      
      {showFormatsInfo && showSupportedFormats && (
        <div className="mt-4">
          <SupportedFormatsInfo />
        </div>
      )}
    </div>
  );
};

export default DragDropZone; 