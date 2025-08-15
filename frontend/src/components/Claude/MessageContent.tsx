import React from 'react';
import CodeBlock from '../UI/CodeBlock.tsx';

interface MessageContentProps {
  content: string;
}

const MessageContent: React.FC<MessageContentProps> = ({ content }) => {
  
  // Check if this is an Expert AI message
  const isExpertMessage = content.includes('🔬 **EXPERT DATA SCIENTIST') || 
                         content.includes('EXPERT DATA SCIENTIST AI') ||
                         content.includes('📊 **ANALYSIS RESULTS:**');
  
  // Check for static chart URLs in content
  const hasChartUrls = /http:\/\/localhost:8000\/static\/figures\/[^\s]+\.png/g.test(content);

  // Check if content has Base64 images - process them with code blocks
  if (content.includes('data:image/png;base64') || content.includes('<div style="position: relative')) {
    return <div dangerouslySetInnerHTML={{ __html: content }} />;
  }

  // Enhanced markdown-like rendering with code block support
  const renderContent = (text: string) => {
    const elements: React.ReactNode[] = [];
    let currentIndex = 0;
    
    // Special handling for Expert AI messages
    if (isExpertMessage) {
      elements.push(
        <div key="expert-badge" className="mb-4 p-3 bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30 rounded-xl">
          <div className="flex items-center gap-2 text-sm font-semibold text-blue-300">
            <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></span>
            🔬 Expert Data Scientist AI Response
          </div>
        </div>
      );
    }
    
    // Split by code blocks first
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let match;
    let lastIndex = 0;
    
    // Process content between code blocks
    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add content before code block
      if (match.index > lastIndex) {
        const beforeContent = text.slice(lastIndex, match.index);
        const beforeElements = parseNonCodeContent(beforeContent, currentIndex, isExpertMessage);
        elements.push(...beforeElements);
        currentIndex += beforeContent.split('\n').length;
      }
      
      // Add code block
      const language = match[1] || 'text';
      const code = match[2].trim();
      
      elements.push(
        <CodeBlock
          key={`code-${currentIndex}`}
          code={code}
          language={language}
          showLineNumbers={true}
        />
      );
      
      lastIndex = codeBlockRegex.lastIndex;
      currentIndex++;
    }
    
    // Add remaining content after last code block
    if (lastIndex < text.length) {
      const remainingContent = text.slice(lastIndex);
      elements.push(...parseNonCodeContent(remainingContent, currentIndex, isExpertMessage));
    }
    
    return elements;
  };
  
  // Parse non-code content with enhanced markdown support
  const parseNonCodeContent = (text: string, startIndex: number, isExpert: boolean = false) => {
    const lines = text.split('\n');
    const elements: React.ReactNode[] = [];
    let listItems: React.ReactNode[] = [];
    let inList = false;
    
    lines.forEach((line, index) => {
      const key = `line-${startIndex}-${index}`;
      
      if (line.trim() === '') {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        elements.push(<div key={key} className="h-2" />);
        return;
      }
      
      // Handle bold text
      if (line.includes('**')) {
        const parts = line.split('**');
        const lineElements: React.ReactNode[] = [];
        parts.forEach((part, partIndex) => {
          if (partIndex % 2 === 1) {
            lineElements.push(<strong key={partIndex} className={isExpert ? "font-semibold text-blue-300" : "font-semibold"}>{part}</strong>);
          } else {
            lineElements.push(part);
          }
        });
        
        elements.push(<p key={key} className="text-gray-300 leading-relaxed mb-2">{lineElements}</p>);
        return;
      }
      
      // Regular paragraph
      elements.push(<p key={key} className="text-gray-300 leading-relaxed mb-2">{line}</p>);
    });
    
    return elements;
  };
  
  return (
    <div className={`space-y-1 max-w-none prose-invert ${isExpertMessage ? 'expert-message' : ''}`}>
      {renderContent(content)}
    </div>
  );
};

export default MessageContent; 