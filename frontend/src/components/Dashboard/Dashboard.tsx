import React from 'react';
import { 
  Upload, 
  MessageSquare, 
  Database, 
  BarChart3,
  Code2,
  FileText,
  ArrowRight,
  Activity,
  Clock,
  Users,
  Zap
} from 'lucide-react';
import { ViewType } from '../../types/navigation.ts';

interface DashboardProps {
  projects: any[];
  recentFiles: any[];
  onNavigate: (view: ViewType) => void;
}

const Dashboard: React.FC<DashboardProps> = ({
  projects,
  recentFiles,
  onNavigate
}) => {
  const quickActions = [
    {
      id: 'upload',
      title: 'Upload Dataset',
      description: 'Start with your data',
      icon: Upload,
      action: () => onNavigate('data')
    },
    {
      id: 'chat',
      title: 'Ask AI Assistant',
      description: 'Get instant help',
      icon: MessageSquare,
      action: () => onNavigate('chat')
    },
    {
      id: 'analysis',
      title: 'Start Analysis',
      description: 'Explore your data',
      icon: BarChart3,
      action: () => onNavigate('analysis')
    },
    {
      id: 'notebook',
      title: 'Open Notebook',
      description: 'Code interactively',
      icon: Code2,
      action: () => onNavigate('code')
    }
  ];

  return (
    <div className="flex-1 overflow-auto bg-white">
      {/* Main Container */}
      <div className="max-w-6xl mx-auto">
        
        {/* Header Section */}
        <header className="text-center py-16 px-6">
          <h1 className="title-1 mb-4">
            Welcome to Datasoph
          </h1>
          <p className="body-large text-gray-600 max-w-2xl mx-auto mb-8">
            Your intelligent data science assistant. Upload data, ask questions, 
            and get professional insights powered by advanced AI.
          </p>
          
          {/* Status Indicator */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-full text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>All systems operational</span>
          </div>
        </header>

        {/* Quick Actions */}
        <section className="px-6 mb-16">
          <div className="text-center mb-8">
            <h2 className="title-2 mb-2">Quick Actions</h2>
            <p className="body text-gray-600">Get started with these common tasks</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <button
                  key={action.id}
                  onClick={action.action}
                  className="card-minimal text-center group cursor-pointer"
                >
                  <div className="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-100 transition-colors duration-200">
                    <Icon className="w-6 h-6 text-blue-500" />
                  </div>
                  <h3 className="body-small font-medium text-gray-800 mb-1">{action.title}</h3>
                  <p className="caption text-gray-500">{action.description}</p>
                  <ArrowRight className="w-4 h-4 text-gray-400 mx-auto mt-3 group-hover:text-gray-600 group-hover:translate-x-1 transition-all duration-200" />
                </button>
              );
            })}
          </div>
        </section>

        {/* Stats Section */}
        <section className="px-6 mb-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Database className="w-6 h-6 text-blue-500" />
              </div>
              <div className="text-2xl font-semibold text-gray-800">{projects.length}</div>
              <div className="caption text-gray-500">Active Projects</div>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-50 rounded-lg flex items-center justify-center mx-auto mb-3">
                <FileText className="w-6 h-6 text-green-500" />
              </div>
              <div className="text-2xl font-semibold text-gray-800">{recentFiles.length}</div>
              <div className="caption text-gray-500">Datasets</div>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-orange-50 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Activity className="w-6 h-6 text-orange-500" />
              </div>
              <div className="text-2xl font-semibold text-gray-800">156</div>
              <div className="caption text-gray-500">AI Insights</div>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-50 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Zap className="w-6 h-6 text-purple-500" />
              </div>
              <div className="text-2xl font-semibold text-gray-800">94%</div>
              <div className="caption text-gray-500">Quality Score</div>
            </div>
          </div>
        </section>

        {/* Recent Projects */}
        <section className="px-6 mb-16">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="title-2 mb-1">Recent Projects</h2>
                <p className="body text-gray-600">Continue working on your data science projects</p>
              </div>
              {projects.length > 0 && (
                <button 
                  onClick={() => onNavigate('analysis')}
                  className="btn-ghost flex items-center gap-1"
                >
                  View all
                  <ArrowRight className="w-4 h-4" />
                </button>
              )}
            </div>
            
            {projects.length === 0 ? (
              <div className="text-center py-12 border border-gray-200 rounded-lg">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Database className="w-6 h-6 text-gray-400" />
                </div>
                <h3 className="body font-medium text-gray-800 mb-2">No projects yet</h3>
                <p className="body-small text-gray-600 mb-6">Create your first data science project to get started</p>
                <button 
                  onClick={() => onNavigate('data')}
                  className="btn-primary"
                >
                  <Upload className="w-4 h-4" />
                  Upload Dataset
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {projects.slice(0, 3).map((project) => (
                  <div key={project.id} className="card-minimal cursor-pointer group">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-colors duration-200">
                        <BarChart3 className="w-5 h-5 text-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="body font-medium text-gray-800 mb-1 group-hover:text-gray-900 transition-colors duration-200">
                          {project.name}
                        </h3>
                        <div className="flex items-center gap-4 body-small text-gray-500">
                          <span>{project.files} files</span>
                          <span>{project.insights} insights</span>
                          <div className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            <span>{project.lastModified.toLocaleDateString()}</span>
                          </div>
                        </div>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                        project.status === 'active' ? 'bg-green-100 text-green-700' :
                        project.status === 'completed' ? 'bg-blue-100 text-blue-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {project.status}
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all duration-200" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* Recent Activity */}
        {projects.length > 0 && (
          <section className="px-6 mb-16">
            <div className="max-w-4xl mx-auto">
              <h2 className="title-2 mb-6">Recent Activity</h2>
              
              <div className="space-y-4">
                {[
                  {
                    id: 1,
                    action: 'Model training completed',
                    project: 'Customer Segmentation',
                    time: '2 minutes ago',
                    type: 'success'
                  },
                  {
                    id: 2,
                    action: 'Dataset uploaded',
                    project: 'Sales Forecasting',
                    time: '1 hour ago',
                    type: 'info'
                  },
                  {
                    id: 3,
                    action: 'Analysis generated',
                    project: 'Marketing Campaign',
                    time: '2 hours ago',
                    type: 'success'
                  }
                ].map((activity) => (
                  <div key={activity.id} className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      activity.type === 'success' ? 'bg-green-100' :
                      activity.type === 'info' ? 'bg-blue-100' : 'bg-gray-100'
                    }`}>
                      <Activity className={`w-4 h-4 ${
                        activity.type === 'success' ? 'text-green-600' :
                        activity.type === 'info' ? 'text-blue-600' : 'text-gray-600'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <p className="body-small font-medium text-gray-800">{activity.action}</p>
                      <p className="caption text-gray-500">{activity.project} • {activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Footer Spacing */}
        <div className="h-12"></div>
      </div>
    </div>
  );
};

export default Dashboard; 