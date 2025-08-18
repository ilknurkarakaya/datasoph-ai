import React from 'react';

interface NewChatButtonProps {
  onClick?: () => void;
}

const NewChatButton: React.FC<NewChatButtonProps> = ({ onClick }) => {
  return (
    <button 
      onClick={onClick}
      className="w-full flex items-center gap-3 px-3 py-2.5 text-sm 
               text-gray-700 dark:text-gray-300 hover:bg-gray-100 
               dark:hover:bg-gray-800 rounded-md transition-colors
               border border-gray-200 dark:border-gray-700"
    >
      <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 5l7 7-7 7M5 5l7 7-7 7" />
      </svg>
      New chat
    </button>
  );
};

export default NewChatButton; 