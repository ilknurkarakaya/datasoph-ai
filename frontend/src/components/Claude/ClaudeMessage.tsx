import React from 'react';
import MessageContent from './MessageContent';
import DataSophLogo from './DataSophLogo';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ClaudeMessageProps {
  message: Message;
}

const ClaudeMessage: React.FC<ClaudeMessageProps> = ({ message }) => {
  const isUser = message.type === 'user';
  
  return (
    <div className="flex gap-4">
      {/* Avatar - User or AI with Spiral Logo */}
      <div className={`w-8 h-8 flex items-center justify-center flex-shrink-0 ${
        isUser 
          ? 'bg-[var(--avatar-user)] rounded-full' 
          : ''
      }`}>
        {isUser ? (
          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
          </svg>
        ) : (
          <DataSophLogo size={32} color="#f97316" />
        )}
      </div>
      
      {/* Message Content */}
      <div className="flex-1 min-w-0">
        {/* Header */}
        <div className="flex items-center gap-2 mb-1">
          <span className="text-sm font-medium text-[var(--text-primary)]">
            {isUser ? 'You' : 'DataSoph AI'}
          </span>
          <span className="text-xs text-[var(--text-tertiary)]">
            {message.timestamp}
          </span>
        </div>
        
        {/* Content */}
        <div className="prose prose-sm max-w-none text-[var(--text-primary)] prose-headings:text-[var(--text-primary)] prose-p:text-[var(--text-primary)] prose-code:text-[var(--text-primary)]">
          <MessageContent content={message.content} />
        </div>
      </div>
    </div>
  );
};

export default ClaudeMessage; 