import React, { useState } from 'react';

interface FormatCategory {
  description: string;
  formats: Record<string, string>;
}

interface SupportedFormats {
  structured_data: FormatCategory;
  documents: FormatCategory;
  images: FormatCategory;
  statistical_software: FormatCategory;
  big_data: FormatCategory;
  models: FormatCategory;
  multimedia: FormatCategory;
}

const SupportedFormatsInfo: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  // Static data - could be fetched from API in the future
  const supportedFormats: SupportedFormats = {
    structured_data: {
      description: 'Spreadsheets, databases, and structured data formats',
      formats: {
        '.csv': 'Comma-separated values',
        '.xlsx': 'Excel workbook',
        '.xls': 'Legacy Excel',
        '.json': 'JSON data',
        '.jsonl': 'JSON Lines',
        '.parquet': 'Apache Parquet',
        '.sql': 'SQL dump files',
        '.sqlite': 'SQLite database',
        '.xml': 'XML data',
        '.yaml': 'YAML configuration',
        '.h5': 'HDF5 files'
      }
    },
    documents: {
      description: 'Text documents and reports',
      formats: {
        '.txt': 'Plain text files',
        '.pdf': 'PDF documents',
        '.docx': 'Word documents',
        '.html': 'HTML documents',
        '.md': 'Markdown files',
        '.ipynb': 'Jupyter notebooks'
      }
    },
    images: {
      description: 'Images with OCR text/table extraction',
      formats: {
        '.png': 'PNG images with OCR',
        '.jpg': 'JPEG images with OCR',
        '.jpeg': 'JPEG images with OCR',
        '.tiff': 'TIFF images with OCR',
        '.bmp': 'Bitmap images with OCR',
        '.webp': 'WebP images with OCR',
        '.heic': 'HEIC images (iPhone photos)',
        '.svg': 'SVG vector graphics'
      }
    },
    statistical_software: {
      description: 'Files from statistical software packages',
      formats: {
        '.sav': 'SPSS files',
        '.dta': 'Stata files',
        '.sas7bdat': 'SAS files',
        '.rda': 'R data files',
        '.rds': 'R serialized data'
      }
    },
    big_data: {
      description: 'Big data and columnar formats',
      formats: {
        '.parquet': 'Apache Parquet',
        '.avro': 'Apache Avro',
        '.orc': 'Apache ORC',
        '.feather': 'Apache Arrow'
      }
    },
    models: {
      description: 'Machine learning models and serialized data',
      formats: {
        '.pkl': 'Pickle files',
        '.pickle': 'Pickle files',
        '.joblib': 'Joblib models',
        '.onnx': 'ONNX models'
      }
    },
    multimedia: {
      description: 'Audio and video files (limited processing)',
      formats: {
        '.wav': 'Audio files',
        '.mp3': 'Audio files',
        '.mp4': 'Video files (frame extraction)'
      }
    }
  };

  const categoryIcons: Record<string, string> = {
    structured_data: '📊',
    documents: '📄',
    images: '🖼️',
    statistical_software: '📈',
    big_data: '🗄️',
    models: '🤖',
    multimedia: '🎵'
  };

  const categoryNames: Record<string, string> = {
    structured_data: 'Structured Data',
    documents: 'Documents',
    images: 'Images',
    statistical_software: 'Statistical Software',
    big_data: 'Big Data',
    models: 'ML Models',
    multimedia: 'Multimedia'
  };

  const getPriorityBadge = (category: string) => {
    const priority1 = ['structured_data', 'documents'];
    const priority2 = ['images'];
    
    if (priority1.includes(category)) {
      return <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">Priority 1</span>;
    } else if (priority2.includes(category)) {
      return <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Priority 2</span>;
    } else {
      return <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full">Priority 3</span>;
    }
  };

  const totalFormats = Object.values(supportedFormats).reduce(
    (total, category) => total + Object.keys(category.formats).length,
    0
  );

  if (!isExpanded) {
    return (
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Comprehensive File Support</h3>
              <p className="text-sm text-gray-600">
                {totalFormats}+ file formats supported across 7 categories
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsExpanded(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <span className="text-sm font-medium">View All Formats</span>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
        
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-white text-gray-700 rounded-full text-sm font-medium border">
            📊 CSV, Excel, JSON
          </span>
          <span className="px-3 py-1 bg-white text-gray-700 rounded-full text-sm font-medium border">
            📄 PDF, Word, Jupyter
          </span>
          <span className="px-3 py-1 bg-white text-gray-700 rounded-full text-sm font-medium border">
            🖼️ Images & Media
          </span>
          <span className="px-3 py-1 bg-white text-gray-500 rounded-full text-sm">
            +{totalFormats - 12} more...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-blue-100 rounded-xl">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">Supported File Formats</h3>
            <p className="text-gray-600">
              DataSoph AI supports {totalFormats}+ file formats for comprehensive data analysis
            </p>
          </div>
        </div>
        <button
          onClick={() => setIsExpanded(false)}
          className="p-2 hover:bg-blue-100 rounded-lg transition-colors"
        >
          <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(supportedFormats).map(([categoryKey, category]) => (
          <div
            key={categoryKey}
            className={`bg-white rounded-lg border-2 transition-all cursor-pointer ${
              activeCategory === categoryKey
                ? 'border-blue-500 shadow-lg'
                : 'border-gray-200 hover:border-blue-300 hover:shadow-md'
            }`}
            onClick={() => setActiveCategory(activeCategory === categoryKey ? null : categoryKey)}
          >
            <div className="p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">{categoryIcons[categoryKey]}</span>
                  <h4 className="font-semibold text-gray-900">{categoryNames[categoryKey]}</h4>
                </div>
                {getPriorityBadge(categoryKey)}
              </div>
              
              <p className="text-sm text-gray-600 mb-3">{category.description}</p>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-blue-600">
                  {Object.keys(category.formats).length} formats
                </span>
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform ${
                    activeCategory === categoryKey ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>

            {activeCategory === categoryKey && (
              <div className="border-t border-gray-200 bg-gray-50 p-4">
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(category.formats).map(([extension, description]) => (
                    <div
                      key={extension}
                      className="flex items-center space-x-2 p-2 bg-white rounded border"
                    >
                      <code className="text-xs font-mono bg-gray-100 px-2 py-1 rounded text-blue-600">
                        {extension}
                      </code>
                      <span className="text-xs text-gray-600 truncate">{description as string}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-100 rounded-lg">
        <div className="flex items-start space-x-3">
          <div className="p-1 bg-blue-200 rounded">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h5 className="font-semibold text-blue-900 mb-2">Processing Priority Levels</h5>
            <div className="space-y-1 text-sm text-blue-800">
              <p><strong>Priority 1:</strong> Immediate processing with full analysis capabilities</p>
              <p><strong>Priority 2:</strong> Standard processing with extended features</p>
              <p><strong>Priority 3:</strong> Specialized processing (may require additional libraries)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SupportedFormatsInfo; 