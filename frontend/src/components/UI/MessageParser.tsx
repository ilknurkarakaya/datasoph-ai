import React from 'react';
import CodeBlock from './CodeBlock.tsx';

// Parse inline code in text
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
      <code key={`code-${keyIndex++}`} className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded text-sm font-mono">
        {match[1]}
      </code>
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

// Parse text with code blocks
export const parseMessageWithCode = (content: string) => {
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const codeBlocks: Array<{
    fullMatch: string;
    language: string;
    code: string;
    title?: string;
    fileName?: string;
  }> = [];

  let match;
  while ((match = codeBlockRegex.exec(content)) !== null) {
    const [fullMatch, language = '', code] = match;
    codeBlocks.push({
      fullMatch,
      language,
      code: code.trim(),
    });
  }

  const parts = content.split(codeBlockRegex);
  return { parts, codeBlocks };
};

// Component to render message with code blocks
interface MessageWithCodeBlocksProps {
  message: {
    parts: string[];
    codeBlocks: Array<{
      fullMatch: string;
      language: string;
      code: string;
      title?: string;
      fileName?: string;
    }>;
  };
  executable?: boolean;
}

export const MessageWithCodeBlocks: React.FC<MessageWithCodeBlocksProps> = ({ 
  message, 
  executable = false 
}) => {
  const elements: React.ReactNode[] = [];
  let codeBlockIndex = 0;

  message.parts.forEach((part, index) => {
    if (index % 3 === 0) {
      // Text content
      if (part.trim()) {
        elements.push(
          <div key={`text-${index}`} className="prose prose-sm max-w-none dark:prose-invert" style={{ color: 'inherit' }}>
            {parseTextContent(part)}
          </div>
        );
      }
    } else if (index % 3 === 2) {
      // Code block
      const codeBlock = message.codeBlocks[codeBlockIndex++];
      if (codeBlock) {
        elements.push(
          <CodeBlock
            key={`code-${index}`}
            code={codeBlock.code}
            language={codeBlock.language}
            title={codeBlock.title}
            fileName={codeBlock.fileName}
            executable={executable}
          />
        );
      }
    }
  });

  return <div>{elements}</div>;
};

// Parse and render HTML content safely
const parseHTMLContent = (content: string): React.ReactNode[] => {
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let keyIndex = 0;

  // If content has Base64 images but is not in expected HTML format, handle it specially
  if (content.includes('data:image/png;base64') && !content.includes('<div style="position: relative')) {
    // Split content by Base64 images
    const base64Regex = /(data:image\/png;base64,[^"'\s]+)/g;
    const textParts = content.split(base64Regex);
    
    textParts.forEach((part, index) => {
      if (part.startsWith('data:image/png;base64,')) {
        // This is a Base64 image
        parts.push(
          <div key={`image-${keyIndex++}`} className="my-4 text-center">
            <img 
              src={part} 
              alt="Generated Chart" 
              className="max-w-full h-auto border border-gray-200 dark:border-gray-700 rounded-lg"
              style={{ maxWidth: '600px', margin: '0 auto' }}
            />
          </div>
        );
      } else if (part.trim()) {
        // This is text content
        parts.push(
          <div key={`text-${keyIndex++}`} className="prose prose-sm max-w-none dark:prose-invert">
            {parseTextContent(part)}
          </div>
        );
      }
    });
    
    return parts;
  }

  // Check for Base64 images in HTML divs
  const htmlDivRegex = /<div[^>]*style="[^"]*position:\s*relative[^"]*"[^>]*>([\s\S]*?)<\/div>/g;
  let match;

  while ((match = htmlDivRegex.exec(content)) !== null) {
    // Add content before the HTML div
    if (match.index > lastIndex) {
      const beforeContent = content.slice(lastIndex, match.index);
      if (beforeContent.trim()) {
        parts.push(
          <div key={`text-${keyIndex++}`} className="prose prose-sm max-w-none dark:prose-invert">
            {parseTextContent(beforeContent)}
          </div>
        );
      }
    }

    // Parse the HTML div content
    const divContent = match[1];
    
    // Extract download link
    const downloadLinkMatch = divContent.match(/<a href="([^"]+)"[^>]*download="([^"]+)"[^>]*>([^<]+)<\/a>/);
    
    // Extract image
    const imageMatch = divContent.match(/<img src="([^"]+)"[^>]*alt="([^"]+)"[^>]*\/>/);
    
    // Extract title
    const titleMatch = divContent.match(/<h3[^>]*>([^<]+)<\/h3>/);

    if (imageMatch && downloadLinkMatch) {
      parts.push(
        <div key={`chart-${keyIndex++}`} className="relative my-5 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden bg-white dark:bg-gray-800">
          <div className="absolute top-2 right-2 z-10">
            <a
              href={downloadLinkMatch[1]}
              download={downloadLinkMatch[2]}
              className="bg-black bg-opacity-70 text-white px-3 py-2 rounded-md text-xs flex items-center gap-1 hover:bg-opacity-90 transition-all font-medium"
            >
              📥 Download PNG
            </a>
          </div>
          {titleMatch && (
            <h3 className="m-0 p-4 bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600 font-semibold">
              {titleMatch[1]}
            </h3>
          )}
          <img 
            src={imageMatch[1]} 
            alt={imageMatch[2]} 
            className="w-full h-auto block"
          />
        </div>
      );
    }

    lastIndex = match.index + match[0].length;
  }

  // Add remaining content
  if (lastIndex < content.length) {
    const remainingContent = content.slice(lastIndex);
    if (remainingContent.trim()) {
      parts.push(
        <div key={`text-${keyIndex++}`} className="prose prose-sm max-w-none dark:prose-invert">
          {parseTextContent(remainingContent)}
        </div>
      );
    }
  }

  return parts.length > 0 ? parts : [
    <div key="text-0" className="prose prose-sm max-w-none dark:prose-invert">
      {parseTextContent(content)}
    </div>
  ];
};

// Main AI Message component
interface AIMessageProps {
  content: string;
  executable?: boolean;
}

export const AIMessage: React.FC<AIMessageProps> = ({ 
  content, 
  executable = false 
}) => {
  // First check for HTML content (charts with Base64 images)
  if (content.includes('<div style="position: relative') || content.includes('data:image/png;base64')) {
    const htmlParts = parseHTMLContent(content);
    return <div>{htmlParts}</div>;
  }
  
  // Then check for code blocks
  const parsedMessage = parseMessageWithCode(content);
  if (parsedMessage.codeBlocks.length > 0) {
    return <MessageWithCodeBlocks message={parsedMessage} executable={executable} />;
  }
  
  // No special content, just process as regular text
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert" style={{ color: 'inherit' }}>
      {parseTextContent(content)}
    </div>
  );
};


// Parse regular text content with markdown
const parseTextContent = (content: string): React.ReactNode[] => {
  return content.split('\n').map((line, index) => {
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
  });
};