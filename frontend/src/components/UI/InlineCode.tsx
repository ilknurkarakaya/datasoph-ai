import React from 'react';

interface InlineCodeProps {
  children: string;
  language?: string;
  className?: string;
}

const InlineCode: React.FC<InlineCodeProps> = ({ 
  children, 
  language,
  className = '' 
}) => {
  return (
    <code 
      className={`bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-2 py-1 rounded text-sm font-mono border border-gray-200 dark:border-gray-600 ${className}`}
      title={language ? `${language} code` : 'Code'}
    >
      {children}
    </code>
  );
};

export default InlineCode; 