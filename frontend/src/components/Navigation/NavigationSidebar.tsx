import React from 'react';
import DataSophLogo from '../DataSophLogo';

interface NavigationSidebarProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

const NavigationSidebar: React.FC<NavigationSidebarProps> = ({ isCollapsed, onToggle }) => {
  const navigationItems = [
    { icon: '🏠', label: 'Ana Sayfa', path: '/' },
    { icon: '📊', label: 'Analiz Stüdyosu', path: '/analysis' },
    { icon: '🤖', label: 'AI Asistan', path: '/chat' },
    { icon: '📈', label: 'Veri Görselleştirme', path: '/visualization' },
    { icon: '📁', label: 'Projeler', path: '/projects' },
    { icon: '⚙️', label: 'Ayarlar', path: '/settings' },
  ];

  return (
    <nav className={`
      fixed left-0 top-0 h-full bg-white border-r border-gray-200 
      transition-all duration-300 ease-in-out z-40
      ${isCollapsed ? 'w-16' : 'w-64'}
    `}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {!isCollapsed && (
          <div className="flex items-center space-x-3">
            <DataSophLogo variant="compact" />
          </div>
        )}
        
        {isCollapsed && (
          <div className="flex justify-center w-full">
            <DataSophLogo variant="icon-only" />
          </div>
        )}
        
        <button
          onClick={onToggle}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg 
            className="w-4 h-4 text-gray-600" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d={isCollapsed ? "M9 5l7 7-7 7" : "M15 19l-7-7 7-7"} 
            />
          </svg>
        </button>
      </div>

      {/* Navigation Items */}
      <div className="py-4">
        {navigationItems.map((item) => (
          <a
            key={item.path}
            href={item.path}
            className={`
              flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600
              transition-colors duration-200
              ${isCollapsed ? 'justify-center' : 'space-x-3'}
            `}
          >
            <span className="text-xl">{item.icon}</span>
            {!isCollapsed && (
              <span className="font-medium">{item.label}</span>
            )}
          </a>
        ))}
      </div>

      {/* Professional Stats */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-gray-50">
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-xs text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>PhD-Level AI Active</span>
            </div>
            
            <div className="flex justify-between text-xs text-gray-500">
              <span>Accuracy</span>
              <span className="font-medium text-blue-600">98.7%</span>
            </div>
            
            <div className="flex justify-between text-xs text-gray-500">
              <span>Processing</span>
              <span className="font-medium text-green-600">Real-time</span>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default NavigationSidebar; 