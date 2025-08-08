import React, { useState } from 'react';
import { 
  Download, 
  FileText, 
  Image, 
  Code, 
  Database,
  Presentation,
  Mail,
  Share,
  Settings,
  Calendar,
  Clock,
  Eye,
  CheckCircle,
  Loader2
} from 'lucide-react';

interface ExportCenterProps {
  projects: any[];
  files: any[];
}

const ExportCenter: React.FC<ExportCenterProps> = ({
  projects,
  files
}) => {
  const [selectedProject, setSelectedProject] = useState<any>(null);
  const [exportType, setExportType] = useState('report');
  const [exportFormat, setExportFormat] = useState('pdf');
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);

  const exportTypes = [
    {
      id: 'report',
      name: 'Analysis Report',
      description: 'Comprehensive analysis with insights and visualizations',
      icon: FileText,
      formats: ['pdf', 'docx', 'html']
    },
    {
      id: 'presentation',
      name: 'Presentation',
      description: 'Executive summary for stakeholders',
      icon: Presentation,
      formats: ['pptx', 'pdf']
    },
    {
      id: 'data',
      name: 'Processed Data',
      description: 'Cleaned and transformed datasets',
      icon: Database,
      formats: ['csv', 'xlsx', 'json', 'parquet']
    },
    {
      id: 'code',
      name: 'Analysis Code',
      description: 'Jupyter notebooks and Python scripts',
      icon: Code,
      formats: ['ipynb', 'py', 'r']
    },
    {
      id: 'visualizations',
      name: 'Charts & Graphs',
      description: 'Individual visualizations and dashboards',
      icon: Image,
      formats: ['png', 'svg', 'pdf', 'html']
    }
  ];

  const formatIcons = {
    pdf: '📄',
    docx: '📝',
    html: '🌐',
    pptx: '📊',
    csv: '📋',
    xlsx: '📈',
    json: '🗃️',
    parquet: '📦',
    ipynb: '📓',
    py: '🐍',
    r: '📊',
    png: '🖼️',
    svg: '🎨'
  };

  const recentExports = [
    {
      id: 1,
      name: 'Customer Analysis Report',
      type: 'PDF Report',
      size: '2.4 MB',
      date: new Date(Date.now() - 3600000),
      status: 'completed'
    },
    {
      id: 2,
      name: 'Sales Dashboard',
      type: 'HTML Visualization',
      size: '856 KB',
      date: new Date(Date.now() - 7200000),
      status: 'completed'
    },
    {
      id: 3,
      name: 'ML Model Results',
      type: 'Jupyter Notebook',
      size: '1.2 MB',
      date: new Date(Date.now() - 86400000),
      status: 'completed'
    }
  ];

  const handleExport = async () => {
    setIsExporting(true);
    setExportProgress(0);

    // Simulate export progress
    const progressInterval = setInterval(() => {
      setExportProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsExporting(false);
          return 100;
        }
        return prev + Math.random() * 10;
      });
    }, 200);

    // Simulate export completion
    setTimeout(() => {
      clearInterval(progressInterval);
      setExportProgress(100);
      setTimeout(() => {
        setIsExporting(false);
        setExportProgress(0);
      }, 1000);
    }, 3000);
  };

  const selectedExportType = exportTypes.find(type => type.id === exportType);

  return (
    <div className="h-full flex bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Export Center</h2>
          <p className="text-sm text-gray-600">Generate professional reports and exports</p>
        </div>

        {/* Project Selection */}
        <div className="p-4 border-b border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Project
          </label>
          <select
            value={selectedProject?.id || ''}
            onChange={(e) => {
              const project = projects.find(p => p.id === e.target.value);
              setSelectedProject(project);
            }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Choose a project...</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>

        {/* Export Types */}
        <div className="flex-1 p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Export Type</h3>
          <div className="space-y-2">
            {exportTypes.map((type) => {
              const Icon = type.icon;
              return (
                <button
                  key={type.id}
                  onClick={() => setExportType(type.id)}
                  className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-colors ${
                    exportType === type.id
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'hover:bg-gray-50 text-gray-700 border border-transparent'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <div className="flex-1">
                    <div className="font-medium">{type.name}</div>
                    <div className="text-xs text-gray-600">{type.description}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Recent Exports */}
        <div className="p-4 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Exports</h3>
          <div className="space-y-2">
            {recentExports.slice(0, 3).map((export_) => (
              <div key={export_.id} className="flex items-center gap-2 p-2 bg-gray-50 rounded-lg">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-900 truncate">
                    {export_.name}
                  </div>
                  <div className="text-xs text-gray-500">
                    {export_.type} • {export_.size}
                  </div>
                </div>
                <button className="p-1 text-gray-500 hover:text-blue-600">
                  <Download className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {selectedExportType?.name || 'Select Export Type'}
              </h1>
              {selectedExportType && (
                <p className="text-gray-600 mt-1">{selectedExportType.description}</p>
              )}
            </div>
            
            {selectedProject && selectedExportType && (
              <button
                onClick={handleExport}
                disabled={isExporting}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {isExporting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Exporting...
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    Export
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Export Progress */}
        {isExporting && (
          <div className="bg-blue-50 border-b border-blue-200 p-4">
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
              <div className="flex-1">
                <div className="text-sm font-medium text-blue-900">
                  Generating {selectedExportType?.name.toLowerCase()}...
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2 mt-1">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${exportProgress}%` }}
                  />
                </div>
              </div>
              <span className="text-sm text-blue-700">{Math.round(exportProgress)}%</span>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="flex-1 overflow-auto p-6">
          {!selectedProject ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <Presentation className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Project</h3>
                <p className="text-gray-600">Choose a project from the sidebar to start creating exports</p>
              </div>
            </div>
          ) : !selectedExportType ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <Download className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Choose Export Type</h3>
                <p className="text-gray-600">Select what type of export you'd like to generate</p>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Project Summary */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Project: {selectedProject.name}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <Database className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-gray-900">{selectedProject.files}</div>
                    <div className="text-sm text-gray-600">Datasets</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <FileText className="w-8 h-8 text-green-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-gray-900">{selectedProject.insights}</div>
                    <div className="text-sm text-gray-600">Insights</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <Calendar className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-gray-900">
                      {selectedProject.lastModified.toLocaleDateString()}
                    </div>
                    <div className="text-sm text-gray-600">Last Updated</div>
                  </div>
                </div>
              </div>

              {/* Format Selection */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Output Format</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {selectedExportType.formats.map((format) => (
                    <button
                      key={format}
                      onClick={() => setExportFormat(format)}
                      className={`p-4 rounded-lg border text-center transition-colors ${
                        exportFormat === format
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : 'border-gray-200 hover:border-gray-300 text-gray-700'
                      }`}
                    >
                      <div className="text-2xl mb-2">
                        {formatIcons[format as keyof typeof formatIcons]}
                      </div>
                      <div className="font-medium text-sm">.{format.toUpperCase()}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Export Options */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Export Options</h3>
                
                {exportType === 'report' && (
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="include-code" className="rounded" defaultChecked />
                      <label htmlFor="include-code" className="text-sm text-gray-700">
                        Include source code and methodology
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="include-visualizations" className="rounded" defaultChecked />
                      <label htmlFor="include-visualizations" className="text-sm text-gray-700">
                        Include all visualizations and charts
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="include-raw-data" className="rounded" />
                      <label htmlFor="include-raw-data" className="text-sm text-gray-700">
                        Include raw data appendix
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="executive-summary" className="rounded" defaultChecked />
                      <label htmlFor="executive-summary" className="text-sm text-gray-700">
                        Generate executive summary
                      </label>
                    </div>
                  </div>
                )}

                {exportType === 'presentation' && (
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="key-insights" className="rounded" defaultChecked />
                      <label htmlFor="key-insights" className="text-sm text-gray-700">
                        Focus on key insights and recommendations
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="charts-only" className="rounded" defaultChecked />
                      <label htmlFor="charts-only" className="text-sm text-gray-700">
                        Emphasize charts and visualizations
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="speaker-notes" className="rounded" />
                      <label htmlFor="speaker-notes" className="text-sm text-gray-700">
                        Include speaker notes
                      </label>
                    </div>
                  </div>
                )}

                {exportType === 'data' && (
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="cleaned-data" className="rounded" defaultChecked />
                      <label htmlFor="cleaned-data" className="text-sm text-gray-700">
                        Export cleaned and processed data
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="feature-engineered" className="rounded" />
                      <label htmlFor="feature-engineered" className="text-sm text-gray-700">
                        Include feature-engineered variables
                      </label>
                    </div>
                    <div className="flex items-center gap-3">
                      <input type="checkbox" id="data-dictionary" className="rounded" defaultChecked />
                      <label htmlFor="data-dictionary" className="text-sm text-gray-700">
                        Include data dictionary
                      </label>
                    </div>
                  </div>
                )}
              </div>

              {/* Preview */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Preview</h3>
                  <button className="flex items-center gap-2 px-3 py-2 text-sm text-blue-600 hover:text-blue-700">
                    <Eye className="w-4 h-4" />
                    Full Preview
                  </button>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="text-sm text-gray-600 mb-2">
                    File: {selectedProject.name}_{selectedExportType.name.replace(' ', '_').toLowerCase()}.{exportFormat}
                  </div>
                  <div className="text-sm text-gray-600">
                    Estimated size: {Math.floor(Math.random() * 5) + 1}.{Math.floor(Math.random() * 9) + 1} MB
                  </div>
                </div>
              </div>

              {/* Sharing Options */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Sharing Options</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <button className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <Download className="w-5 h-5 text-blue-600" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Download</div>
                      <div className="text-sm text-gray-600">Save to your device</div>
                    </div>
                  </button>
                  
                  <button className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <Mail className="w-5 h-5 text-green-600" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Email</div>
                      <div className="text-sm text-gray-600">Send via email</div>
                    </div>
                  </button>
                  
                  <button className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <Share className="w-5 h-5 text-purple-600" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Share Link</div>
                      <div className="text-sm text-gray-600">Generate secure link</div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ExportCenter; 