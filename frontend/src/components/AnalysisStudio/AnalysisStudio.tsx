import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Brain,
  Target,
  LineChart,
  PieChart,
  Zap,
  Settings,
  Play,
  Download,
  Eye,
  Code,
  FileText,
  Layers,
  Activity
} from 'lucide-react';

interface AnalysisStudioProps {
  files: any[];
  onAnalysisComplete?: (results: any) => void;
  onNavigate?: (view: string) => void;
}

const AnalysisStudio: React.FC<AnalysisStudioProps> = ({
  files,
  onAnalysisComplete,
  onNavigate = () => {}
}) => {
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [analysisType, setAnalysisType] = useState<string>('overview');
  const [activeTab, setActiveTab] = useState<'analysis' | 'models' | 'visualizations'>('analysis');

  const analysisTypes = [
    {
      id: 'overview',
      name: 'Data Overview',
      description: 'Basic statistics and data profiling',
      icon: BarChart3,
      color: 'bg-blue-500'
    },
    {
      id: 'statistical',
      name: 'Statistical Analysis',
      description: 'Hypothesis testing, correlations, distributions',
      icon: TrendingUp,
      color: 'bg-green-500'
    },
    {
      id: 'ml',
      name: 'Machine Learning',
      description: 'Classification, regression, clustering',
      icon: Brain,
      color: 'bg-purple-500'
    },
    {
      id: 'forecasting',
      name: 'Time Series',
      description: 'Forecasting and trend analysis',
      icon: LineChart,
      color: 'bg-orange-500'
    }
  ];

  const mlModels = [
    {
      id: 'rf_classifier',
      name: 'Random Forest Classifier',
      accuracy: 94.2,
      status: 'trained',
      features: 12,
      dataset: 'Customer Segmentation'
    },
    {
      id: 'xgb_regressor',
      name: 'XGBoost Regressor',
      accuracy: 87.5,
      status: 'training',
      features: 8,
      dataset: 'Sales Forecasting'
    },
    {
      id: 'kmeans_cluster',
      name: 'K-Means Clustering',
      accuracy: null,
      status: 'completed',
      features: 15,
      dataset: 'Market Segmentation'
    }
  ];

  const sampleVisualizations = [
    {
      id: 1,
      title: 'Sales Distribution',
      type: 'histogram',
      description: 'Distribution of sales across regions'
    },
    {
      id: 2,
      title: 'Feature Correlation',
      type: 'heatmap',
      description: 'Correlation matrix of all numeric features'
    },
    {
      id: 3,
      title: 'Time Series Trend',
      type: 'line',
      description: 'Revenue trends over the last 12 months'
    },
    {
      id: 4,
      title: 'Customer Segments',
      type: 'scatter',
      description: 'Customer segmentation visualization'
    }
  ];

  const StatCard = ({ title, value, change, icon: Icon }: any) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className={`text-sm ${change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
              {change}
            </p>
          )}
        </div>
        <Icon className="w-8 h-8 text-gray-400" />
      </div>
    </div>
  );

  return (
    <div className="h-full flex bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Analysis Studio</h2>
          <p className="text-sm text-gray-600">Advanced analytics and machine learning</p>
        </div>

        {/* File Selection */}
        <div className="p-4 border-b border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Dataset
          </label>
          <select
            value={selectedFile?.id || ''}
            onChange={(e) => {
              const file = files.find(f => f.id === parseInt(e.target.value));
              setSelectedFile(file);
            }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Choose a dataset...</option>
            {files.map((file) => (
              <option key={file.id} value={file.id}>
                {file.name}
              </option>
            ))}
          </select>
        </div>

        {/* Analysis Types */}
        <div className="flex-1 p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Analysis Types</h3>
          <div className="space-y-2">
            {analysisTypes.map((type) => {
              const Icon = type.icon;
              return (
                <button
                  key={type.id}
                  onClick={() => setAnalysisType(type.id)}
                  className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-colors ${
                    analysisType === type.id
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'hover:bg-gray-50 text-gray-700'
                  }`}
                >
                  <div className={`p-2 rounded-lg ${type.color}`}>
                    <Icon className="w-4 h-4 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">{type.name}</div>
                    <div className="text-xs text-gray-600">{type.description}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="p-4 border-t border-gray-200">
          <div className="space-y-2">
            <button 
              onClick={() => onNavigate('chat')}
              className="w-full px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              <Brain className="w-4 h-4 inline mr-2" />
              Ask AI Assistant
            </button>
            <button 
              onClick={() => onNavigate('code')}
              className="w-full px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              <Code className="w-4 h-4 inline mr-2" />
              Open Notebook
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Tabs */}
        <div className="bg-white border-b border-gray-200">
          <div className="flex">
            {[
              { id: 'analysis', label: 'Analysis', icon: BarChart3 },
              { id: 'models', label: 'Models', icon: Brain },
              { id: 'visualizations', label: 'Visualizations', icon: PieChart }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-auto p-6">
          {!selectedFile ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Dataset</h3>
                <p className="text-gray-600 mb-6">Choose a dataset from the sidebar to start your analysis</p>
                <button 
                  onClick={() => onNavigate('data')}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Upload Dataset
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {activeTab === 'analysis' && (
                <>
                  {/* Dataset Info */}
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Dataset: {selectedFile.name}
                      </h3>
                      <div className="flex gap-2">
                        <button className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm">
                          <Play className="w-4 h-4 inline mr-1" />
                          Run Analysis
                        </button>
                        <button className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                          <Settings className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <StatCard
                        title="Total Rows"
                        value="12,847"
                        change="+2.3%"
                        icon={Layers}
                      />
                      <StatCard
                        title="Features"
                        value="23"
                        change="+3"
                        icon={BarChart3}
                      />
                      <StatCard
                        title="Missing Values"
                        value="2.1%"
                        change="-0.5%"
                        icon={Activity}
                      />
                      <StatCard
                        title="Quality Score"
                        value="94%"
                        change="+2%"
                        icon={Target}
                      />
                    </div>
                  </div>

                  {/* Analysis Results */}
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      {analysisTypes.find(t => t.id === analysisType)?.name} Results
                    </h3>
                    
                    {analysisType === 'overview' && (
                      <div className="space-y-4">
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <h4 className="font-medium text-gray-900 mb-2">Data Summary</h4>
                          <div className="text-sm text-gray-600 space-y-1">
                            <p>• Numeric columns: 15 (Age, Income, Score, etc.)</p>
                            <p>• Categorical columns: 8 (Gender, Category, Region, etc.)</p>
                            <p>• Date columns: 2 (Registration_Date, Last_Activity)</p>
                            <p>• Target variable: Customer_Segment (3 unique values)</p>
                          </div>
                        </div>
                        
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h4 className="font-medium text-blue-900 mb-2">AI Insights</h4>
                          <div className="text-sm text-blue-800 space-y-1">
                            <p>• Strong correlation detected between Income and Purchase_Amount (r=0.87)</p>
                            <p>• Age distribution appears bimodal with peaks at 25-30 and 45-50</p>
                            <p>• Seasonal patterns identified in purchase data</p>
                            <p>• Potential data quality issues in 3 columns need attention</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {analysisType === 'statistical' && (
                      <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="bg-gray-50 p-4 rounded-lg">
                            <h4 className="font-medium text-gray-900 mb-2">Correlation Analysis</h4>
                            <p className="text-sm text-gray-600 mb-2">Strongest correlations found:</p>
                            <div className="text-sm space-y-1">
                              <div className="flex justify-between">
                                <span>Income ↔ Purchase_Amount</span>
                                <span className="font-medium text-green-600">0.87</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Age ↔ Loyalty_Score</span>
                                <span className="font-medium text-green-600">0.72</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Education ↔ Income</span>
                                <span className="font-medium text-green-600">0.68</span>
                              </div>
                            </div>
                          </div>
                          
                          <div className="bg-gray-50 p-4 rounded-lg">
                            <h4 className="font-medium text-gray-900 mb-2">Distribution Analysis</h4>
                            <p className="text-sm text-gray-600 mb-2">Distribution characteristics:</p>
                            <div className="text-sm space-y-1">
                              <p>• Income: Right-skewed (log-normal)</p>
                              <p>• Age: Bimodal distribution</p>
                              <p>• Purchase_Amount: Normal distribution</p>
                              <p>• Loyalty_Score: Uniform distribution</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {analysisType === 'ml' && (
                      <div className="space-y-4">
                        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg">
                          <h4 className="font-medium text-gray-900 mb-2">ML Recommendations</h4>
                          <div className="text-sm text-gray-700 space-y-2">
                            <p>🎯 <strong>Problem Type:</strong> Multi-class classification (Customer Segmentation)</p>
                            <p>🏆 <strong>Recommended Models:</strong> Random Forest, XGBoost, Neural Network</p>
                            <p>📊 <strong>Expected Accuracy:</strong> 85-92% based on data quality</p>
                            <p>⚙️ <strong>Feature Engineering:</strong> 5 new features recommended</p>
                          </div>
                        </div>
                        
                        <div className="flex gap-3">
                          <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                            <Brain className="w-4 h-4 inline mr-2" />
                            Train Models
                          </button>
                          <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                            <Code className="w-4 h-4 inline mr-2" />
                            Generate Code
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}

              {activeTab === 'models' && (
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-900">Trained Models</h3>
                    <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                      <Brain className="w-4 h-4 inline mr-2" />
                      Train New Model
                    </button>
                  </div>

                  <div className="grid gap-4">
                    {mlModels.map((model) => (
                      <div key={model.id} className="bg-white p-6 rounded-lg border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                          <div>
                            <h4 className="font-medium text-gray-900">{model.name}</h4>
                            <p className="text-sm text-gray-600">Dataset: {model.dataset}</p>
                          </div>
                          <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                            model.status === 'trained' ? 'bg-green-100 text-green-800' :
                            model.status === 'training' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {model.status}
                          </div>
                        </div>

                        <div className="grid grid-cols-3 gap-4 mb-4">
                          {model.accuracy && (
                            <div>
                              <div className="text-xs text-gray-500">Accuracy</div>
                              <div className="text-lg font-bold text-gray-900">{model.accuracy}%</div>
                            </div>
                          )}
                          <div>
                            <div className="text-xs text-gray-500">Features</div>
                            <div className="text-lg font-bold text-gray-900">{model.features}</div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-500">Type</div>
                            <div className="text-sm font-medium text-gray-700">
                              {model.name.includes('Classifier') ? 'Classification' :
                               model.name.includes('Regressor') ? 'Regression' : 'Clustering'}
                            </div>
                          </div>
                        </div>

                        <div className="flex gap-2">
                          <button className="px-3 py-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 text-sm">
                            <Eye className="w-4 h-4 inline mr-1" />
                            View Details
                          </button>
                          <button className="px-3 py-2 bg-green-50 text-green-700 rounded hover:bg-green-100 text-sm">
                            <Download className="w-4 h-4 inline mr-1" />
                            Export
                          </button>
                          <button className="px-3 py-2 bg-gray-50 text-gray-700 rounded hover:bg-gray-100 text-sm">
                            <Target className="w-4 h-4 inline mr-1" />
                            Predict
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'visualizations' && (
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-900">Visualizations</h3>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                      <BarChart3 className="w-4 h-4 inline mr-2" />
                      Create Chart
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {sampleVisualizations.map((viz) => (
                      <div key={viz.id} className="bg-white p-6 rounded-lg border border-gray-200">
                        <div className="h-48 bg-gray-100 rounded-lg mb-4 flex items-center justify-center">
                          <BarChart3 className="w-16 h-16 text-gray-400" />
                        </div>
                        <h4 className="font-medium text-gray-900 mb-1">{viz.title}</h4>
                        <p className="text-sm text-gray-600 mb-4">{viz.description}</p>
                        <div className="flex gap-2">
                          <button className="px-3 py-2 bg-blue-50 text-blue-700 rounded text-sm hover:bg-blue-100">
                            <Eye className="w-4 h-4 inline mr-1" />
                            View
                          </button>
                          <button className="px-3 py-2 bg-gray-50 text-gray-700 rounded text-sm hover:bg-gray-100">
                            <Download className="w-4 h-4 inline mr-1" />
                            Export
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalysisStudio; 