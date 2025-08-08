import { useState, useCallback } from 'react';
import { FileAttachment } from '../types/chat';
import { fileService } from '../services/api';

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const ALLOWED_TYPES = [
  'text/csv',
  'application/json',
  'text/plain',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
];

export const useFileUpload = () => {
  const [uploadedFiles, setUploadedFiles] = useState<FileAttachment[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const validateFile = useCallback((file: File): string | null => {
    if (file.size > MAX_FILE_SIZE) {
      return `File size exceeds 50MB limit. Current size: ${(file.size / (1024 * 1024)).toFixed(2)}MB`;
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      return `File type not supported. Allowed types: CSV, Excel, JSON, TXT`;
    }

    return null;
  }, []);

  const uploadFile = useCallback(async (file: File): Promise<FileAttachment | null> => {
    const validationError = validateFile(file);
    if (validationError) {
      setUploadError(validationError);
      return null;
    }

    setIsUploading(true);
    setUploadError(null);

    try {
      const result = await fileService.uploadFile(file);
      
      const fileAttachment: FileAttachment = {
        id: result.file_id,
        name: result.filename,
        filename: result.filename,
        size: result.size,
        type: result.type,
        uploadedAt: new Date().toISOString(),
      };

      setUploadedFiles(prev => [...prev, fileAttachment]);
      return fileAttachment;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Upload failed';
      setUploadError(errorMessage);
      return null;
    } finally {
      setIsUploading(false);
    }
  }, [validateFile]);

  const removeFile = useCallback((fileId: string) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  }, []);

  const clearFiles = useCallback(() => {
    setUploadedFiles([]);
    setUploadError(null);
  }, []);

  const formatFileSize = useCallback((bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }, []);

  return {
    uploadedFiles,
    isUploading,
    uploadError,
    uploadFile,
    removeFile,
    clearFiles,
    validateFile,
    formatFileSize,
  };
}; 