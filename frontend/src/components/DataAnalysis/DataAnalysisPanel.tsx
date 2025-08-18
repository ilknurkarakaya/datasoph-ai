import React, { useState, useEffect } from 'react';
import { FileAttachment } from '../../types/chat.ts';
import { 
  visualizationService, 
  dataQualityService, 
  mlService, 
  fileService 
} from '../../services/api.ts';

interface DataAnalysisPanelProps {
  fileAttachment: FileAttachment;
  onClose: () => void;
}

const DataAnalysisPanel: React.FC<DataAnalysisPanelProps> = ({ fileAttachment, onClose }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'quality' | 'visualize' | 'ml'>('overview');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [fileInfo, setFileInfo] = useState<any>(null);

  useEffect(() => {
    loadFileInfo();
  }, [fileAttachment.id]);

  const loadFileInfo = async () => {
    try {
      setLoading(true);
      const info = await fileService.getFileInfo(fileAttachment.id);
      setFileInfo(info);
    } catch (error) {
      console.error('Error loading file info:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTabData = async (tab: string) => {
    try {
      setLoading(true);
      let result;
      
      switch (tab) {
        case 'quality':
          result = await dataQualityService.assessQuality(fileAttachment.id, true);
          break;
        case 'visualize':
          result = await visualizationService.createDashboard(fileAttachment.id);
          break;
        case 'ml':
          result = await mlService.analyzeMLPotential(fileAttachment.id);
          break;
        default:
          result = null;
      }
      
      setData(result);
    } catch (error) {
      console.error(`Error loading ${tab} data:`, error);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tab: typeof activeTab) => {
    setActiveTab(tab);
    if (tab !== 'overview') {
      loadTabData(tab);
    }
  };

  const renderOverview = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">📊 File Overview</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">File Name</p>
            <p className="font-medium">{fileAttachment.name}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Size</p>
            <p className="font-medium">{(fileAttachment.size / 1024).toFixed(1)} KB</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Type</p>
            <p className="font-medium">{fileAttachment.type}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Uploaded</p>
            <p className="font-medium">{new Date(fileAttachment.uploadedAt).toLocaleString()}</p>
          </div>
        </div>
      </div>

      {fileInfo && (
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">🔍 Quick Analysis</h3>
          <div className="text-sm text-gray-700 whitespace-pre-line">
            {fileInfo.analysis}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => handleTabChange('quality')}
          className="p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
        >
          <div className="text-green-600 text-2xl mb-2">🛡️</div>
          <h4 className="font-semibold text-green-900">Data Quality</h4>
          <p className="text-sm text-green-700">Assess data quality and get cleaning recommendations</p>
        </button>

        <button
          onClick={() => handleTabChange('visualize')}
          className="p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
        >
          <div className="text-purple-600 text-2xl mb-2">📈</div>
          <h4 className="font-semibold text-purple-900">Visualizations</h4>
          <p className="text-sm text-purple-700">Create interactive charts and dashboards</p>
        </button>

        <button
          onClick={() => handleTabChange('ml')}
          className="p-4 bg-orange-50 border border-orange-200 rounded-lg hover:bg-orange-100 transition-colors"
        >
          <div className="text-orange-600 text-2xl mb-2">🤖</div>
          <h4 className="font-semibold text-orange-900">Machine Learning</h4>
          <p className="text-sm text-orange-700">Train models and make predictions</p>
        </button>
      </div>
    </div>
  );

  const renderDataQuality = () => {
    if (!data) return <div>Loading quality assessment...</div>;

    return (
      <div className="space-y-6">
        <div className={`p-6 rounded-lg border ${
          data.overall_score >= 90 ? 'bg-green-50 border-green-200' :
          data.overall_score >= 70 ? 'bg-yellow-50 border-yellow-200' :
          'bg-red-50 border-red-200'
        }`}>
          <h3 className="text-lg font-semibold mb-2">🛡️ Data Quality Score</h3>
          <div className="text-3xl font-bold mb-2">
            {data.overall_score.toFixed(1)}/100
          </div>
          <p className="text-sm">{data.message}</p>
        </div>

        {data.issues && data.issues.length > 0 && (
          <div className="bg-red-50 p-6 rounded-lg border border-red-200">
            <h4 className="font-semibold text-red-900 mb-3">⚠️ Issues Found</h4>
            <ul className="space-y-2">
              {data.issues.map((issue: any, index: number) => (
                <li key={index} className="text-sm text-red-700">
                  • {issue.description}
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.recommendations && data.recommendations.length > 0 && (
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
            <h4 className="font-semibold text-blue-900 mb-3">💡 Recommendations</h4>
            <ul className="space-y-2">
              {data.recommendations.map((rec: string, index: number) => (
                <li key={index} className="text-sm text-blue-700">
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.cleaning_code && (
          <div className="bg-gray-50 p-6 rounded-lg border">
            <h4 className="font-semibold text-gray-900 mb-3">🛠️ Auto-Generated Cleaning Code</h4>
            <pre className="text-xs text-gray-700 overflow-x-auto bg-white p-4 rounded border">
              {data.cleaning_code}
            </pre>
          </div>
        )}
      </div>
    );
  };

  const renderVisualizations = () => {
    if (!data) return <div>Loading visualizations...</div>;

    return (
      <div className="space-y-6">
        <h3 className="text-lg font-semibold">📈 Interactive Dashboard</h3>
        
        {data.visualizations && data.visualizations.map((viz: any, index: number) => (
          <div key={index} className="bg-white p-6 rounded-lg border">
            <h4 className="font-semibold mb-4">{viz.title}</h4>
            {viz.plotly_json ? (
              <div className="h-96 bg-gray-100 rounded flex items-center justify-center">
                <p className="text-gray-500">📊 Interactive Chart: {viz.title}</p>
                <small className="block text-gray-400 mt-2">
                  (Plotly integration would render here)
                </small>
              </div>
            ) : (
              <div className="h-96 bg-gray-100 rounded flex items-center justify-center">
                <p className="text-gray-500">Chart type: {viz.type}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderMLAnalysis = () => {
    if (!data) return <div>Loading ML analysis...</div>;

    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200">
          <h3 className="text-lg font-semibold text-purple-900 mb-3">🤖 Machine Learning Potential</h3>
          
          {data.data?.suggested_targets && (
            <div className="mb-4">
              <h4 className="font-semibold mb-2">🎯 Suggested Target Variables</h4>
              <div className="space-y-2">
                {data.data.suggested_targets.map((target: any, index: number) => (
                  <div key={index} className="bg-white p-3 rounded border">
                    <div className="flex justify-between items-center">
                      <span className="font-medium">{target.column}</span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        target.task_type === 'classification' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                      }`}>
                        {target.task_type}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{target.reason}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {data.data?.ml_recommendations && (
            <div>
              <h4 className="font-semibold mb-2">📋 ML Recommendations</h4>
              <div className="space-y-2">
                {data.data.ml_recommendations.map((rec: any, index: number) => (
                  <div key={index} className="bg-white p-3 rounded border">
                    <h5 className="font-medium">{rec.type}</h5>
                    <p className="text-sm text-gray-600">{rec.description}</p>
                    {rec.use_cases && (
                      <div className="mt-2">
                        <span className="text-xs text-gray-500">Use cases: </span>
                        <span className="text-xs">{rec.use_cases.join(', ')}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-6xl max-h-[90vh] w-full mx-4 flex flex-col">
        {/* Header */}
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900">
                              🔬 Datasoph Analysis
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          
          {/* Tabs */}
          <div className="flex space-x-4 mt-4">
            {[
              { id: 'overview', label: '📊 Overview', },
              { id: 'quality', label: '🛡️ Quality' },
              { id: 'visualize', label: '📈 Visualize' },
              { id: 'ml', label: '🤖 ML' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab.id as any)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-800 border border-blue-200'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <>
              {activeTab === 'overview' && renderOverview()}
              {activeTab === 'quality' && renderDataQuality()}
              {activeTab === 'visualize' && renderVisualizations()}
              {activeTab === 'ml' && renderMLAnalysis()}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default DataAnalysisPanel; 