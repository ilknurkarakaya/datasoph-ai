import React from 'react';

interface MessageContentProps {
  content: string;
}

const MessageContent: React.FC<MessageContentProps> = ({ content }) => {
  // Simple markdown-like rendering for basic formatting
  const renderContent = (text: string) => {
    // Split by lines and process each one
    const lines = text.split('\n');
    const elements: React.ReactNode[] = [];
    
    lines.forEach((line, index) => {
      if (line.trim() === '') {
        elements.push(<br key={index} />);
        return;
      }
      
      // Handle bold text
      if (line.includes('**')) {
        const parts = line.split('**');
        const lineElements: React.ReactNode[] = [];
        parts.forEach((part, partIndex) => {
          if (partIndex % 2 === 1) {
            lineElements.push(<strong key={partIndex}>{part}</strong>);
          } else {
            lineElements.push(part);
          }
        });
        elements.push(<p key={index}>{lineElements}</p>);
      }
      // Handle list items
      else if (line.trim().startsWith('- ')) {
        const listText = line.trim().substring(2);
        elements.push(
          <li key={index} className="ml-4">
            {listText}
          </li>
        );
      }
      // Handle headers
      else if (line.trim().startsWith('## ')) {
        const headerText = line.trim().substring(3);
        elements.push(
          <h2 key={index} className="text-lg font-semibold mt-4 mb-2">
            {headerText}
          </h2>
        );
      }
      else if (line.trim().startsWith('### ')) {
        const headerText = line.trim().substring(4);
        elements.push(
          <h3 key={index} className="text-base font-medium mt-3 mb-2">
            {headerText}
          </h3>
        );
      }
      // Regular paragraph
      else {
        elements.push(<p key={index}>{line}</p>);
      }
    });
    
    return elements;
  };
  
  return <div className="space-y-2">{renderContent(content)}</div>;
};

export default MessageContent; 