import { useState, useCallback } from 'react';
import { FileAttachment } from '../types/chat.ts';
import { fileService } from '../services/api.ts';

// Enhanced file size limits based on file type
const FILE_SIZE_LIMITS = {
  // Small files (fast processing)
  'text/csv': 100 * 1024 * 1024, // 100MB
  'application/json': 50 * 1024 * 1024, // 50MB
  'text/plain': 10 * 1024 * 1024, // 10MB
  'text/markdown': 10 * 1024 * 1024, // 10MB
  
  // Medium files (chunked processing)
  'application/vnd.ms-excel': 200 * 1024 * 1024, // 200MB
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 200 * 1024 * 1024, // 200MB
  'application/pdf': 50 * 1024 * 1024, // 50MB
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 50 * 1024 * 1024, // 50MB
  
  // Images
  'image/png': 50 * 1024 * 1024, // 50MB
  'image/jpeg': 50 * 1024 * 1024, // 50MB
  'image/svg+xml': 10 * 1024 * 1024, // 10MB
  
  // Default fallback
  'default': 50 * 1024 * 1024 // 50MB
};

// Comprehensive list of supported file types organized by priority
const SUPPORTED_FORMATS = {
  // PHASE 1 - CORE DATA FORMATS (Priority 1)
  structured_data: {
    'text/csv': { ext: '.csv', name: 'CSV Files', priority: 1 },
    'application/vnd.ms-excel': { ext: '.xls', name: 'Excel Files (Legacy)', priority: 1 },
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': { ext: '.xlsx', name: 'Excel Files', priority: 1 },
    'application/json': { ext: '.json', name: 'JSON Data', priority: 1 },
    'text/plain': { ext: '.txt', name: 'Text Files', priority: 1 },
  },
  documents: {
    'application/pdf': { ext: '.pdf', name: 'PDF Documents', priority: 1 },
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { ext: '.docx', name: 'Word Documents', priority: 2 },
    'text/html': { ext: '.html', name: 'HTML Documents', priority: 2 },
    'text/markdown': { ext: '.md', name: 'Markdown Files', priority: 2 },
  },
  // PHASE 2 - EXTENDED FORMATS  
  images: {
    'image/png': { ext: '.png', name: 'PNG Images (with OCR)', priority: 2 },
    'image/jpeg': { ext: '.jpg', name: 'JPEG Images (with OCR)', priority: 2 },
    'image/tiff': { ext: '.tiff', name: 'TIFF Images (with OCR)', priority: 2 },
    'image/bmp': { ext: '.bmp', name: 'Bitmap Images (with OCR)', priority: 2 },
    'image/webp': { ext: '.webp', name: 'WebP Images (with OCR)', priority: 2 },
    'image/svg+xml': { ext: '.svg', name: 'SVG Images', priority: 2 },
  },
  // Additional formats by file extension (for files without proper MIME types)
  by_extension: {
    '.jsonl': { name: 'JSON Lines', priority: 1 },
    '.parquet': { name: 'Parquet Files', priority: 1 },
    '.ipynb': { name: 'Jupyter Notebooks', priority: 1 },
    '.sql': { name: 'SQL Scripts', priority: 1 },
    '.xml': { name: 'XML Files', priority: 2 },
    '.yaml': { name: 'YAML Files', priority: 2 },
    '.yml': { name: 'YAML Files', priority: 2 },
    '.sqlite': { name: 'SQLite Database', priority: 2 },
    '.db': { name: 'Database Files', priority: 2 },
    '.h5': { name: 'HDF5 Files', priority: 2 },
    '.hdf5': { name: 'HDF5 Files', priority: 2 },
    // Statistical software formats
    '.sav': { name: 'SPSS Files', priority: 3 },
    '.dta': { name: 'Stata Files', priority: 3 },
    '.sas7bdat': { name: 'SAS Files', priority: 3 },
    '.rda': { name: 'R Data Files', priority: 3 },
    '.rds': { name: 'R Serialized Data', priority: 3 },
    // Big data formats
    '.avro': { name: 'Apache Avro', priority: 3 },
    '.orc': { name: 'Apache ORC', priority: 3 },
    '.feather': { name: 'Apache Arrow', priority: 3 },
    // Model formats
    '.pkl': { name: 'Pickle Files', priority: 3 },
    '.pickle': { name: 'Pickle Files', priority: 3 },
    '.joblib': { name: 'Joblib Models', priority: 3 },
    '.onnx': { name: 'ONNX Models', priority: 3 },
    // Additional image formats for OCR
    '.tiff': { name: 'TIFF Images (with OCR)', priority: 2 },
    '.tif': { name: 'TIFF Images (with OCR)', priority: 2 },
    '.bmp': { name: 'Bitmap Images (with OCR)', priority: 2 },
    '.webp': { name: 'WebP Images (with OCR)', priority: 2 },
    '.heic': { name: 'HEIC Images (iPhone photos with OCR)', priority: 2 },
    // Multimedia (limited support)
    '.wav': { name: 'Audio Files', priority: 3 },
    '.mp3': { name: 'Audio Files', priority: 3 },
    '.mp4': { name: 'Video Files', priority: 3 },
  }
};

// Get all supported types for validation
const getAllSupportedTypes = () => {
  const mimeTypes = new Set<string>();
  const extensions = new Set<string>();
  
  Object.values(SUPPORTED_FORMATS).forEach(category => {
    if (category === SUPPORTED_FORMATS.by_extension) {
      Object.keys(category).forEach(ext => extensions.add(ext));
    } else {
      Object.keys(category).forEach(mime => mimeTypes.add(mime));
    }
  });
  
  return { mimeTypes: Array.from(mimeTypes), extensions: Array.from(extensions) };
};

const { mimeTypes: ALLOWED_MIME_TYPES, extensions: ALLOWED_EXTENSIONS } = getAllSupportedTypes();

export const useFileUpload = () => {
  const [uploadedFiles, setUploadedFiles] = useState<FileAttachment[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const getFileInfo = useCallback((file: File) => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    // Check MIME type first
    for (const [category, formats] of Object.entries(SUPPORTED_FORMATS)) {
      if (category === 'by_extension') continue;
      if (file.type in formats) {
        return (formats as any)[file.type];
      }
    }
    
    // Check by extension
    if (extension in SUPPORTED_FORMATS.by_extension) {
      return (SUPPORTED_FORMATS.by_extension as any)[extension];
    }
    
    return null;
  }, []);

  const validateFile = useCallback((file: File): string | null => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    const fileInfo = getFileInfo(file);
    
    // Check if file type is supported
    if (!fileInfo && !ALLOWED_MIME_TYPES.includes(file.type) && !ALLOWED_EXTENSIONS.includes(extension)) {
      return `❌ File type not supported. 

📁 **Supported formats:**
• **Data:** CSV, Excel (.xlsx, .xls), JSON, Parquet, SQL
• **Documents:** PDF, Word (.docx), HTML, Markdown, Jupyter Notebooks
• **Images with OCR:** PNG, JPEG, TIFF, BMP, WebP, HEIC (text/table extraction)
• **Statistical:** SPSS (.sav), Stata (.dta), R data (.rda, .rds)
• **Databases:** SQLite, HDF5
• **Models:** Pickle, Joblib, ONNX

🔄 Convert your file to one of these formats for the best analysis experience.`;
    }

    // Check file size based on type
    const sizeLimit = (FILE_SIZE_LIMITS as any)[file.type] || FILE_SIZE_LIMITS['default'];
    if (file.size > sizeLimit) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
      const limitMB = (sizeLimit / (1024 * 1024)).toFixed(0);
      
      return `📏 File size exceeds limit for ${fileInfo?.name || extension.toUpperCase()} files.
      
**Current size:** ${sizeMB}MB
**Maximum allowed:** ${limitMB}MB

💡 **Tips:**
• For large datasets, try converting to Parquet format
• For text files, consider splitting into smaller chunks
• For images, compress or resize before uploading`;
    }

    return null;
  }, [getFileInfo]);

  // NEW: Enhanced upload with comprehensive analysis
  const uploadFile = useCallback(async (file: File): Promise<FileAttachment | null> => {
    const validationError = validateFile(file);
    if (validationError) {
      setUploadError(validationError);
      return null;
    }

    setIsUploading(true);
    setUploadError(null);

    try {
      console.log('🚀 Starting comprehensive DataSoph AI analysis...');
      
      // First, try the comprehensive analysis endpoint
      let result;
      try {
        result = await fileService.uploadAndAnalyzeFile(file);
        console.log('✅ Comprehensive analysis completed:', result);
      } catch (comprehensiveError) {
        console.log('⚠️ Comprehensive analysis failed, falling back to basic upload:', comprehensiveError);
        // Fallback to basic upload
        result = await fileService.uploadFile(file);
      }
      
      const fileInfo = getFileInfo(file);
      
      const fileAttachment: FileAttachment = {
        id: result.file_id || result.analysis_result?.file_id,
        name: result.filename || file.name,
        filename: result.filename || file.name,
        size: result.size || file.size,
        type: result.type || file.type,
        uploadedAt: new Date().toISOString(),
        analysisData: result, // Store full analysis data
      };

      setUploadedFiles(prev => [...prev, fileAttachment]);
      
      // Enhanced success message
      const successMessage = result.analysis_result
        ? `🎯 DataSoph AI Analysis Complete! Generated ${result.analysis_result.charts_count || 'multiple'} charts and comprehensive insights.`
        : fileInfo 
        ? `✅ Great! I can analyze this ${fileInfo.name} file. What would you like to know about your data?`
        : `✅ File uploaded successfully. I'll do my best to analyze this format.`;
      
      console.log(successMessage);
      
      return fileAttachment;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Upload failed';
      setUploadError(`❌ Upload failed: ${errorMessage}
      
💡 **Try these solutions:**
• Check your internet connection
• Ensure the file isn't corrupted
• Try a different file format
• Contact support if the issue persists`);
      return null;
    } finally {
      setIsUploading(false);
    }
  }, [validateFile, getFileInfo]);

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

  const getSupportedFormats = useCallback(() => {
    return SUPPORTED_FORMATS;
  }, []);

  const isFileSupported = useCallback((file: File): boolean => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    return getFileInfo(file) !== null || ALLOWED_MIME_TYPES.includes(file.type) || ALLOWED_EXTENSIONS.includes(extension);
  }, [getFileInfo]);

  return {
    uploadedFiles,
    isUploading,
    uploadError,
    uploadFile,
    removeFile,
    clearFiles,
    validateFile,
    formatFileSize,
    getSupportedFormats,
    isFileSupported,
    getFileInfo,
  };
}; 