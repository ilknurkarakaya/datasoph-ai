import React, { useState, useRef } from 'react';
import { 
  Upload, 
  FileText, 
  Database, 
  Eye, 
  BarChart3, 
  Settings,
  Download,
  Trash2,
  Search,
  Filter,
  Grid,
  List,
  CheckCircle,
  AlertTriangle,
  Info,
  Loader2
} from 'lucide-react';
import { ViewType } from '../../types/navigation.ts';

interface DataWorkspaceProps {
  files: any[];
  onFileUpload: (file: any) => void;
  onNavigate: (view: ViewType) => void;
}

const DataWorkspace: React.FC<DataWorkspaceProps> = ({
  files,
  onFileUpload,
  onNavigate
}) => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [showPreview, setShowPreview] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);
  const [dragOver, setDragOver] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (uploadedFiles: FileList) => {
    for (let i = 0; i < uploadedFiles.length; i++) {
      const file = uploadedFiles[i];
      
      // Simulate upload progress
      setUploadProgress(0);
      
      // Create file info object
      const fileInfo = {
        id: Date.now() + i,
        name: file.name,
        size: file.size,
        type: file.type,
        uploadDate: new Date(),
        status: 'processing',
        qualityScore: null as number | null,
        preview: null,
        file: file
      };

      onFileUpload(fileInfo);
      
      // Simulate upload progress
      for (let progress = 0; progress <= 100; progress += 10) {
        await new Promise(resolve => setTimeout(resolve, 100));
        setUploadProgress(progress);
      }
      
      // Simulate quality analysis
      setTimeout(() => {
        fileInfo.status = 'completed';
        fileInfo.qualityScore = Math.floor(Math.random() * 20) + 80; // 80-100%
      }, 1000);
      
      setUploadProgress(null);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    handleFileUpload(e.dataTransfer.files);
  };

  const filteredFiles = files.filter(file => 
    file.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getFileIcon = (type: string) => {
    if (type.includes('csv')) return '📊';
    if (type.includes('excel')) return '📈';
    if (type.includes('json')) return '🗃️';
    if (type.includes('text')) return '📄';
    return '📁';
  };

  const getQualityBadge = (score: number) => {
    if (score >= 90) return { color: 'bg-green-100 text-green-800', label: 'Excellent' };
    if (score >= 70) return { color: 'bg-yellow-100 text-yellow-800', label: 'Good' };
    return { color: 'bg-red-100 text-red-800', label: 'Needs Review' };
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Data Workspace</h1>
            <p className="text-gray-600 mt-1">Upload, explore, and prepare your datasets</p>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Database className="w-4 h-4" />
              <span>{files.length} datasets</span>
            </div>
            
            <button
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Upload Data
            </button>
          </div>
        </div>
      </div>

      {/* Upload Progress */}
      {uploadProgress !== null && (
        <div className="bg-blue-50 border-b border-blue-200 p-4">
          <div className="flex items-center gap-3">
            <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
            <div className="flex-1">
              <div className="text-sm font-medium text-blue-900">Uploading file...</div>
              <div className="w-full bg-blue-200 rounded-full h-2 mt-1">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
            <span className="text-sm text-blue-700">{uploadProgress}%</span>
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between gap-4">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search datasets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* View Toggle */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg ${viewMode === 'grid' ? 'bg-gray-100 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg ${viewMode === 'list' ? 'bg-gray-100 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Drop Zone */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
                      accept=".csv,.xlsx,.xls,.json,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg"
          onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
          className="hidden"
        />

        {files.length === 0 ? (
          <div 
            className={`h-full flex items-center justify-center ${dragOver ? 'bg-blue-50' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
          >
            <div className="text-center max-w-md">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Upload className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No datasets yet</h3>
              <p className="text-gray-600 mb-6">
                Upload your CSV, Excel, or JSON files to get started with data analysis
              </p>
              
              <div className="space-y-4">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto"
                >
                  <Upload className="w-5 h-5" />
                  Choose Files
                </button>
                
                <div className="text-sm text-gray-500">
                  or drag and drop files here
                </div>
              </div>

              <div className="mt-8 text-xs text-gray-500">
                <p>Supported formats: CSV, Excel (.xlsx, .xls), JSON, TXT</p>
                <p>Maximum file size: 100MB</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="p-6">
            {viewMode === 'grid' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredFiles.map((file) => (
                  <div 
                    key={file.id} 
                    className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => {
                      setSelectedFile(file);
                      setShowPreview(true);
                    }}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="text-2xl">{getFileIcon(file.type)}</div>
                      {file.qualityScore && (
                        <div className={`px-2 py-1 rounded-full text-xs font-medium ${getQualityBadge(file.qualityScore).color}`}>
                          {file.qualityScore}%
                        </div>
                      )}
                    </div>

                    <h3 className="font-medium text-gray-900 mb-1 truncate" title={file.name}>
                      {file.name}
                    </h3>
                    
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>Size: {formatFileSize(file.size)}</div>
                      <div>Uploaded: {file.uploadDate.toLocaleDateString()}</div>
                    </div>

                    <div className="flex items-center gap-2 mt-3">
                      {file.status === 'processing' ? (
                        <div className="flex items-center gap-1 text-yellow-600">
                          <Loader2 className="w-3 h-3 animate-spin" />
                          <span className="text-xs">Processing</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-green-600">
                          <CheckCircle className="w-3 h-3" />
                          <span className="text-xs">Ready</span>
                        </div>
                      )}
                    </div>

                    <div className="flex gap-1 mt-3">
                      <button className="flex-1 px-3 py-2 text-xs bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors">
                        <Eye className="w-3 h-3 inline mr-1" />
                        Preview
                      </button>
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          onNavigate('analysis');
                        }}
                        className="flex-1 px-3 py-2 text-xs bg-green-50 text-green-700 rounded hover:bg-green-100 transition-colors"
                      >
                        <BarChart3 className="w-3 h-3 inline mr-1" />
                        Analyze
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200">
                <div className="p-4 border-b border-gray-200">
                  <div className="grid grid-cols-6 gap-4 text-sm font-medium text-gray-700">
                    <div className="col-span-2">Name</div>
                    <div>Size</div>
                    <div>Quality</div>
                    <div>Status</div>
                    <div>Actions</div>
                  </div>
                </div>
                
                <div className="divide-y divide-gray-200">
                  {filteredFiles.map((file) => (
                    <div key={file.id} className="p-4 hover:bg-gray-50">
                      <div className="grid grid-cols-6 gap-4 items-center">
                        <div className="col-span-2 flex items-center gap-3">
                          <span className="text-lg">{getFileIcon(file.type)}</span>
                          <div>
                            <div className="font-medium text-gray-900">{file.name}</div>
                            <div className="text-sm text-gray-500">
                              {file.uploadDate.toLocaleDateString()}
                            </div>
                          </div>
                        </div>
                        
                        <div className="text-sm text-gray-600">
                          {formatFileSize(file.size)}
                        </div>
                        
                        <div>
                          {file.qualityScore && (
                            <div className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getQualityBadge(file.qualityScore).color}`}>
                              {file.qualityScore}%
                            </div>
                          )}
                        </div>
                        
                        <div>
                          {file.status === 'processing' ? (
                            <div className="flex items-center gap-1 text-yellow-600">
                              <Loader2 className="w-3 h-3 animate-spin" />
                              <span className="text-xs">Processing</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-1 text-green-600">
                              <CheckCircle className="w-3 h-3" />
                              <span className="text-xs">Ready</span>
                            </div>
                          )}
                        </div>
                        
                        <div className="flex gap-1">
                          <button className="p-1 text-gray-500 hover:text-blue-600">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button 
                            onClick={() => onNavigate('analysis')}
                            className="p-1 text-gray-500 hover:text-green-600"
                          >
                            <BarChart3 className="w-4 h-4" />
                          </button>
                          <button className="p-1 text-gray-500 hover:text-red-600">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Quick Actions Panel */}
      {files.length > 0 && (
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span>{filteredFiles.length} of {files.length} datasets</span>
              {files.filter(f => f.status === 'processing').length > 0 && (
                <span className="text-yellow-600">
                  {files.filter(f => f.status === 'processing').length} processing
                </span>
              )}
            </div>
            
            <div className="flex gap-2">
              <button 
                onClick={() => onNavigate('analysis')}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
              >
                Start Analysis
              </button>
              <button 
                onClick={() => onNavigate('chat')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              >
                Ask AI
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataWorkspace; 