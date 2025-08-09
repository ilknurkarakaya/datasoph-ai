import React from 'react';
import CodeBlock from '../UI/CodeBlock';

interface MessageContentProps {
  content: string;
}

const MessageContent: React.FC<MessageContentProps> = ({ content }) => {
  
  // Enhanced markdown-like rendering with code block support
  const renderContent = (text: string) => {
    const elements: React.ReactNode[] = [];
    let currentIndex = 0;
    
    // Split by code blocks first
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let match;
    let lastIndex = 0;
    
    // Process content between code blocks
    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add content before code block
      if (match.index > lastIndex) {
        const beforeContent = text.slice(lastIndex, match.index);
        elements.push(...parseNonCodeContent(beforeContent, currentIndex));
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
      elements.push(...parseNonCodeContent(remainingContent, currentIndex));
    }
    
    return elements;
  };
  
  // Parse non-code content with enhanced markdown support
  const parseNonCodeContent = (text: string, startIndex: number) => {
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
      
      // Handle inline code
      if (line.includes('`') && !line.includes('```')) {
        const parts = line.split('`');
        const lineElements: React.ReactNode[] = [];
        parts.forEach((part, partIndex) => {
          if (partIndex % 2 === 1) {
            lineElements.push(
              <code key={partIndex} className="bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded font-mono text-sm">
                {part}
              </code>
            );
          } else {
            // Handle bold text within non-code parts
            if (part.includes('**')) {
              const boldParts = part.split('**');
              boldParts.forEach((boldPart, boldIndex) => {
                if (boldIndex % 2 === 1) {
                  lineElements.push(<strong key={`bold-${boldIndex}`} className="font-semibold">{boldPart}</strong>);
                } else {
                  lineElements.push(boldPart);
                }
              });
            } else {
              lineElements.push(part);
            }
          }
        });
        
        if (inList && line.trim().startsWith('- ')) {
          const listText = lineElements.slice(1); // Remove the "- " part
          listItems.push(<li key={key} className="text-gray-300 leading-relaxed">{listText}</li>);
        } else {
          if (inList) {
            elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
            listItems = [];
            inList = false;
          }
          elements.push(<p key={key} className="text-gray-300 leading-relaxed mb-2">{lineElements}</p>);
        }
        return;
      }
      
      // Handle bold text
      if (line.includes('**')) {
        const parts = line.split('**');
        const lineElements: React.ReactNode[] = [];
        parts.forEach((part, partIndex) => {
          if (partIndex % 2 === 1) {
                              lineElements.push(<strong key={partIndex} className="font-semibold">{part}</strong>);
          } else {
            lineElements.push(part);
          }
        });
        
        if (inList && line.trim().startsWith('- ')) {
          const listText = lineElements.slice(1); // Remove the "- " part if it exists
          listItems.push(<li key={key} className="text-gray-300 leading-relaxed">{listText}</li>);
        } else {
          if (inList) {
            elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
            listItems = [];
            inList = false;
          }
          elements.push(<p key={key} className="text-gray-300 leading-relaxed mb-2">{lineElements}</p>);
        }
        return;
      }
      
      // Handle list items
      if (line.trim().startsWith('- ')) {
        const listText = line.trim().substring(2);
        listItems.push(<li key={key} className="text-gray-300 leading-relaxed">{listText}</li>);
        inList = true;
        return;
      }
      
      // Handle numbered lists
      if (/^\d+\.\s/.test(line.trim())) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const listText = line.trim().replace(/^\d+\.\s/, '');
        elements.push(<li key={key} className="text-gray-300 leading-relaxed ml-6">{listText}</li>);
        return;
      }
      
      // Handle headers
      if (line.trim().startsWith('#### ')) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const headerText = line.trim().substring(5);
        elements.push(
          <h4 key={key} className="text-sm font-semibold mt-4 mb-2 text-blue-400 border-l-2 border-blue-500 pl-3">
            {headerText}
          </h4>
        );
        return;
      }
      
      if (line.trim().startsWith('### ')) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const headerText = line.trim().substring(4);
        elements.push(
          <h3 key={key} className="text-base font-semibold mt-4 mb-2 text-emerald-400 border-l-3 border-emerald-500 pl-3">
            {headerText}
          </h3>
        );
        return;
      }
      
      if (line.trim().startsWith('## ')) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const headerText = line.trim().substring(3);
        elements.push(
          <h2 key={key} className="text-lg font-bold mt-6 mb-3 border-l-4 border-blue-500 pl-4 bg-gray-800/30 py-2 rounded-r">
            {headerText}
          </h2>
        );
        return;
      }
      
      if (line.trim().startsWith('# ')) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const headerText = line.trim().substring(2);
        elements.push(
          <h1 key={key} className="text-xl font-bold mt-6 mb-4 border-l-4 border-emerald-500 pl-4 bg-gray-800/50 py-3 rounded-r">
            {headerText}
          </h1>
        );
        return;
      }
      
      // Handle blockquotes
      if (line.trim().startsWith('> ')) {
        if (inList) {
          elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
          listItems = [];
          inList = false;
        }
        const quoteText = line.trim().substring(2);
        elements.push(
          <blockquote key={key} className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 py-2 my-3 bg-gray-200 dark:bg-gray-800 italic">
            {quoteText}
          </blockquote>
        );
        return;
      }
      
      // Regular paragraph
      if (inList) {
        elements.push(<ul key={`list-${key}`} className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
        listItems = [];
        inList = false;
      }
      elements.push(<p key={key} className="text-gray-300 leading-relaxed mb-2">{line}</p>);
    });
    
    // Add any remaining list items
    if (inList && listItems.length > 0) {
      elements.push(<ul key="final-list" className="list-disc list-inside space-y-1 my-3 ml-4">{listItems}</ul>);
    }
    
    return elements;
  };
  
  return (
    <div className="space-y-1 max-w-none prose-invert">
      {renderContent(content)}
    </div>
  );
};

export default MessageContent; 