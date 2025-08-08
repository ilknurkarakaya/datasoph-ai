import React from 'react';
import CodeBlock from './CodeBlock';
import InlineCode from './InlineCode';

interface CodeBlockMatch {
  fullMatch: string;
  language: string;
  title?: string | null;
  code: string;
  fileName?: string | null;
}

interface ParsedMessage {
  text: string;
  codeBlocks: CodeBlockMatch[];
}

interface MessageWithCodeBlocksProps {
  message: ParsedMessage;
  executable?: boolean;
}

interface AIMessageProps {
  content: string;
  executable?: boolean;
}

// Parse message and extract code blocks
export const parseMessageWithCode = (message: string): ParsedMessage => {
  // Enhanced regex to detect code blocks with optional title and filename
  const codeBlockRegex = /```(\w+)(?:\s+([^\n]+))?\n([\s\S]*?)\n```/g;
  
  const codeBlocks: CodeBlockMatch[] = [];
  let match;
  
  // Extract code blocks
  while ((match = codeBlockRegex.exec(message)) !== null) {
    const [fullMatch, language, titleOrFilename, code] = match;
    
    // Try to determine if the second capture group is a filename or title
    let title: string | null = null;
    let fileName: string | null = null;
    
    if (titleOrFilename) {
      // If it has an extension, treat as filename
      if (titleOrFilename.includes('.') && /\.\w+$/.test(titleOrFilename)) {
        fileName = titleOrFilename;
      } else {
        title = titleOrFilename;
      }
    }
    
    codeBlocks.push({
      fullMatch,
      language: language.toLowerCase(),
      title,
      fileName,
      code: code.trim()
    });
  }
  
  return {
    text: message,
    codeBlocks
  };
};

// Process inline code in text
export const processInlineCode = (text: string): React.ReactNode[] => {
  const inlineCodeRegex = /`([^`\n]+)`/g;
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match;
  let keyIndex = 0;

  while ((match = inlineCodeRegex.exec(text)) !== null) {
    // Add text before the inline code
    if (match.index > lastIndex) {
      const beforeText = text.slice(lastIndex, match.index);
      if (beforeText) {
        parts.push(<span key={`text-${keyIndex++}`}>{beforeText}</span>);
      }
    }

    // Add the inline code
    parts.push(
      <InlineCode key={`inline-${keyIndex++}`}>
        {match[1]}
      </InlineCode>
    );

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    const remainingText = text.slice(lastIndex);
    if (remainingText) {
      parts.push(<span key={`text-${keyIndex++}`}>{remainingText}</span>);
    }
  }

  return parts.length > 0 ? parts : [<span key="text-0">{text}</span>];
};

// Component for rendering messages with code blocks
export const MessageWithCodeBlocks: React.FC<MessageWithCodeBlocksProps> = ({ 
  message, 
  executable = false 
}) => {
  let processedContent = message.text;
  
  // Replace code blocks with placeholder components
  message.codeBlocks.forEach((block, index) => {
    processedContent = processedContent.replace(
      block.fullMatch,
      `<CODEBLOCK_${index}>`
    );
  });
  
  // Split content by code block placeholders
  const parts = processedContent.split(/(<CODEBLOCK_\d+>)/);
  
  return (
    <div className="space-y-4">
      {parts.map((part, index) => {
        const codeBlockMatch = part.match(/^<CODEBLOCK_(\d+)>$/);
        if (codeBlockMatch) {
          const blockIndex = parseInt(codeBlockMatch[1]);
          const block = message.codeBlocks[blockIndex];
          return (
            <CodeBlock
              key={`codeblock-${index}`}
              code={block.code}
              language={block.language}
              title={block.title || undefined}
              fileName={block.fileName || undefined}
              executable={executable}
              showLineNumbers={true}
            />
          );
        }
        
        // Regular text content - process inline code
        if (part.trim()) {
          return (
            <div key={`text-${index}`} className="prose prose-sm max-w-none dark:prose-invert" style={{ color: 'inherit' }}>
              {part.split('\n').map((line, lineIndex) => {
                if (!line.trim()) {
                  return <br key={`br-${lineIndex}`} />;
                }
                
                // Process different markdown-style formatting
                if (line.startsWith('**') && line.endsWith('**')) {
                  return (
                    <p key={lineIndex} className="font-semibold mb-2" style={{ color: 'inherit' }}>
                      {processInlineCode(line.slice(2, -2))}
                    </p>
                  );
                } else if (line.startsWith('### ')) {
                  return (
                    <h3 key={lineIndex} className="text-lg font-semibold mb-2 mt-4" style={{ color: 'inherit' }}>
                      {processInlineCode(line.slice(4))}
                    </h3>
                  );
                } else if (line.startsWith('## ')) {
                  return (
                    <h2 key={lineIndex} className="text-xl font-semibold mb-3 mt-5" style={{ color: 'inherit' }}>
                      {processInlineCode(line.slice(3))}
                    </h2>
                  );
                } else if (line.startsWith('# ')) {
                  return (
                    <h1 key={lineIndex} className="text-2xl font-bold mb-4 mt-6" style={{ color: 'inherit' }}>
                      {processInlineCode(line.slice(2))}
                    </h1>
                  );
                } else if (line.startsWith('• ') || line.startsWith('- ')) {
                  return (
                    <p key={lineIndex} className="ml-4 mb-1" style={{ color: 'inherit' }}>
                      {processInlineCode(line.slice(2))}
                    </p>
                  );
                } else if (line.match(/^\d+\.\s/)) {
                  return (
                    <p key={lineIndex} className="ml-4 mb-1" style={{ color: 'inherit' }}>
                      {processInlineCode(line)}
                    </p>
                  );
                } else {
                  return (
                    <p key={lineIndex} className="mb-4 last:mb-0" style={{ color: 'inherit' }}>
                      {processInlineCode(line)}
                    </p>
                  );
                }
              })}
            </div>
          );
        }
        
        return null;
      })}
    </div>
  );
};

// Main AI Message component
export const AIMessage: React.FC<AIMessageProps> = ({ 
  content, 
  executable = false 
}) => {
  const parsedMessage = parseMessageWithCode(content);
  
  if (parsedMessage.codeBlocks.length > 0) {
    return <MessageWithCodeBlocks message={parsedMessage} executable={executable} />;
  }
  
  // No code blocks, just process inline code
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert" style={{ color: 'inherit' }}>
      {content.split('\n').map((line, index) => {
        if (!line.trim()) {
          return <br key={`br-${index}`} />;
        }
        
        // Process different markdown-style formatting
        if (line.startsWith('**') && line.endsWith('**')) {
          return (
            <p key={index} className="font-semibold mb-2" style={{ color: 'inherit' }}>
              {processInlineCode(line.slice(2, -2))}
            </p>
          );
        } else if (line.startsWith('### ')) {
          return (
            <h3 key={index} className="text-lg font-semibold mb-2 mt-4" style={{ color: 'inherit' }}>
              {processInlineCode(line.slice(4))}
            </h3>
          );
        } else if (line.startsWith('## ')) {
          return (
            <h2 key={index} className="text-xl font-semibold mb-3 mt-5" style={{ color: 'inherit' }}>
              {processInlineCode(line.slice(3))}
            </h2>
          );
        } else if (line.startsWith('# ')) {
          return (
            <h1 key={index} className="text-2xl font-bold mb-4 mt-6" style={{ color: 'inherit' }}>
              {processInlineCode(line.slice(2))}
            </h1>
          );
        } else if (line.startsWith('• ') || line.startsWith('- ')) {
          return (
            <p key={index} className="ml-4 mb-1" style={{ color: 'inherit' }}>
              {processInlineCode(line.slice(2))}
            </p>
          );
        } else if (line.match(/^\d+\.\s/)) {
          return (
            <p key={index} className="ml-4 mb-1" style={{ color: 'inherit' }}>
              {processInlineCode(line)}
            </p>
          );
        } else {
          return (
            <p key={index} className="mb-4 last:mb-0" style={{ color: 'inherit' }}>
              {processInlineCode(line)}
            </p>
          );
        }
      })}
    </div>
  );
}; 