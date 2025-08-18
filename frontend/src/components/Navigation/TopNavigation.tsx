import React, { useState } from 'react';
import { 
  Search, 
  Bell, 
  Settings, 
  User, 
  Menu,
  Sparkles,
  Activity,
  Zap
} from 'lucide-react';
import { ViewType } from '../../types/navigation.ts';

interface TopNavigationProps {
  currentView: ViewType;
  onToggleSidebar: () => void;
  projects: any[];
}

const TopNavigation: React.FC<TopNavigationProps> = ({
  currentView,
  onToggleSidebar,
  projects
}) => {
  const [searchValue, setSearchValue] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);

  const getViewTitle = (view: ViewType) => {
    const titles = {
      dashboard: 'Dashboard',
      chat: 'AI Assistant',
      data: 'Data Workspace', 
      analysis: 'Analysis Studio',
      code: 'Code Environment',
      export: 'Export Center'
    };
    return titles[view] || 'Datasoph';
  };

  const getViewDescription = (view: ViewType) => {
    const descriptions = {
      dashboard: 'Overview of your data science projects and insights',
      chat: 'Intelligent AI assistant for data science questions',
      data: 'Upload, explore, and prepare your datasets',
      analysis: 'Advanced statistical analysis and machine learning',
      code: 'Interactive coding environment with notebooks',
      export: 'Export and share your analyses and reports'
    };
    return descriptions[view] || 'Professional data science platform';
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-xl font-bold text-gray-900">
                {getViewTitle(currentView)}
              </h1>
              {currentView === 'dashboard' && (
                <div className="flex items-center gap-1 px-2 py-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-medium rounded-full">
                  <Sparkles className="w-3 h-3" />
                  AI-Powered
                </div>
              )}
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {getViewDescription(currentView)}
            </p>
          </div>
        </div>

        {/* Center Section - Search */}
        <div className="hidden md:block flex-1 max-w-md mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search projects, files, or ask AI..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
            {searchValue && (
              <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <div className="p-3">
                  <div className="text-xs text-gray-500 mb-2">Quick Actions</div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 p-2 hover:bg-gray-50 rounded cursor-pointer">
                      <Zap className="w-4 h-4 text-blue-500" />
                      <span className="text-sm">Ask AI: "{searchValue}"</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-3">
          {/* Activity Status */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium">
            <Activity className="w-3 h-3" />
            <span>All Systems Operational</span>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 relative"
            >
              <Bell className="w-5 h-5" />
              <div className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></div>
            </button>
            
            {showNotifications && (
              <div className="absolute right-0 top-full mt-2 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <div className="p-4 border-b border-gray-200">
                  <h3 className="font-medium text-gray-900">Notifications</h3>
                </div>
                <div className="p-4 space-y-3">
                  <div className="flex gap-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Model Training Complete</p>
                      <p className="text-xs text-gray-500">Customer segmentation model finished with 94% accuracy</p>
                      <p className="text-xs text-gray-400 mt-1">2 minutes ago</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Data Quality Check</p>
                      <p className="text-xs text-gray-500">Sales data quality score improved to 98%</p>
                      <p className="text-xs text-gray-400 mt-1">1 hour ago</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 border-t border-gray-200">
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    View all notifications
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Settings */}
          <button className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700">
            <Settings className="w-5 h-5" />
          </button>

          {/* User Profile */}
          <div className="flex items-center gap-3 pl-3 border-l border-gray-200">
            <div className="hidden sm:block text-right">
              <p className="text-sm font-medium text-gray-900">Data Scientist</p>
              <p className="text-xs text-gray-500">Professional Plan</p>
            </div>
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopNavigation; 