import React from 'react';
import { useDarkMode, useUser, useChat } from '../../App';
import DataSophLogo from './DataSophLogo';

const ClaudeSidebar: React.FC = () => {
  const { darkMode, setDarkMode } = useDarkMode();
  const { userName, setUserName } = useUser();
  const { onNewChat } = useChat();
  
  const conversations = [
    "Customer Segmentation Analysis",
    "Sales Data Exploration", 
    "Churn Prediction Model",
    "Revenue Forecasting",
    "Market Basket Analysis",
    "A/B Test Results Review",
    "Time Series Anomaly Detection",
    "Regression Model Validation",
    "Data Quality Assessment",
    "Feature Engineering Pipeline"
  ];
  
  const handleNewChat = () => {
    onNewChat();
  };
  
  const handleUserNameClick = () => {
    const newName = prompt('Adınızı güncelleyin:', userName);
    if (newName && newName.trim()) {
      setUserName(newName.trim());
    }
  };
  
  return (
    <>
      {/* Top Section - DataSoph Logo and Brand */}
      <div className="px-3 py-4 border-b border-[var(--border-light)]">
        <div className="flex items-center gap-3 px-0">
          <DataSophLogo size={28} color="#f97316" />
          <span className="text-base font-medium text-[var(--text-primary)] font-system">DataSoph.ai</span>
        </div>
      </div>

      {/* New Chat Section */}
      <div className="p-3">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center gap-3 px-3 py-2 bg-[var(--btn-primary)] hover:bg-[var(--btn-primary-hover)] border border-[var(--border-light)] rounded-md transition-colors group"
        >
          <svg className="w-4 h-4 text-[var(--text-secondary)] group-hover:text-[var(--text-primary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-sm font-medium text-[var(--btn-text)] font-system">New chat</span>
        </button>
      </div>
      
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto">
        {/* Chat history items would go here */}
        <div className="p-3">
          <div className="text-xs text-[var(--text-tertiary)] font-system">No previous conversations</div>
        </div>
      </div>
      
      {/* User Profile Section */}
      <div className="p-3 border-t border-[var(--border-light)]">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-7 h-7 bg-[var(--avatar-user)] rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1 min-w-0 cursor-pointer" onClick={handleUserNameClick}>
            <div className="text-sm font-medium text-[var(--text-primary)] hover:text-[var(--avatar-user)] transition-colors font-system">
              {userName}
            </div>
          </div>
          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-1 rounded hover:bg-[var(--bg-hover)] transition-colors"
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? (
              <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707M16.95 7.05a7 7 0 101.414 1.414l-.707.707A8 8 0 1112 4.001V3z" />
              </svg>
            ) : (
              <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </>
  );
};

export default ClaudeSidebar; 