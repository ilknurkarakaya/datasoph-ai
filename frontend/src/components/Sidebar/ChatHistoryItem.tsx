import React, { useState } from 'react';

interface ChatHistoryItemProps {
  title: string;
  timestamp: Date;
  isActive: boolean;
  onClick: () => void;
  onDelete?: () => void;
}

const ChatHistoryItem: React.FC<ChatHistoryItemProps> = ({
  title,
  timestamp,
  isActive,
  onClick,
  onDelete,
}) => {
  const [showDeleteButton, setShowDeleteButton] = useState(false);

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDelete && window.confirm('Are you sure you want to delete this conversation?')) {
      onDelete();
    }
  };

  const formatDate = (date: Date) => {
    const now = new Date();
    const diffInMs = now.getTime() - date.getTime();
    const diffInHours = diffInMs / (1000 * 60 * 60);
    const diffInDays = diffInMs / (1000 * 60 * 60 * 24);

    if (diffInHours < 1) {
      return 'Just now';
    } else if (diffInHours < 24) {
      return `${Math.floor(diffInHours)}h ago`;
    } else if (diffInDays < 7) {
      return `${Math.floor(diffInDays)}d ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  return (
    <div
      className={`
        group relative px-3 py-2 rounded-md cursor-pointer transition-all duration-200
        ${isActive 
          ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100' 
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'
        }
      `}
      onClick={onClick}
      onMouseEnter={() => setShowDeleteButton(true)}
      onMouseLeave={() => setShowDeleteButton(false)}
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium truncate">
            {title}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            {formatDate(timestamp)}
          </div>
        </div>

        {/* Delete button */}
        {showDeleteButton && onDelete && (
          <button
            onClick={handleDelete}
            className="flex-shrink-0 p-1 rounded-md transition-all duration-200
                     opacity-0 group-hover:opacity-100 hover:bg-red-100 dark:hover:bg-red-900
                     text-gray-400 hover:text-red-600 dark:hover:text-red-400"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" 
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatHistoryItem; 