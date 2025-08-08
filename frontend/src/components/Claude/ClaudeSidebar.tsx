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
      {/* Top Section - New Chat Button with DataSoph Logo */}
      <div className="p-3 border-b border-[var(--border-light)]">
        <div className="flex items-center gap-2 mb-3">
          <DataSophLogo size={20} color="#f97316" />
          <span className="text-sm font-semibold text-[var(--text-primary)]">DataSoph AI</span>
        </div>
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center gap-3 px-3 py-2 bg-[var(--btn-primary)] hover:bg-[var(--btn-primary-hover)] border border-[var(--border-light)] rounded-md transition-colors group"
        >
          <svg className="w-4 h-4 text-[var(--text-secondary)] group-hover:text-[var(--text-primary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-sm font-medium text-[var(--btn-text)]">New chat</span>
        </button>
      </div>
      
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-1">
          {conversations.map((title, index) => (
            <div 
              key={index}
              className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[var(--bg-hover)] cursor-pointer transition-colors group"
            >
              <svg className="w-4 h-4 text-[var(--text-tertiary)] group-hover:text-[var(--text-secondary)] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <span className="text-sm text-[var(--text-primary)] truncate group-hover:text-[var(--text-primary)]">
                {title}
              </span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Bottom Section - User Profile */}
      <div className="p-3 border-t border-[var(--border-light)]">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-7 h-7 bg-[var(--avatar-user)] rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1 min-w-0 cursor-pointer" onClick={handleUserNameClick}>
            <div className="text-sm font-medium text-[var(--text-primary)] hover:text-[var(--avatar-user)] transition-colors">
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
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
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