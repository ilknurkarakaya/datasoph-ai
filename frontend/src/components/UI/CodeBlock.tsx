import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check, Play, Download } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language: string;
  title?: string;
  fileName?: string;
  executable?: boolean;
  showLineNumbers?: boolean;
  className?: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language,
  title,
  fileName,
  executable = false,
  showLineNumbers = true,
  className = ''
}) => {
  const [copied, setCopied] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  
  // Copy to clipboard
  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = code;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Execute code (for supported languages)
  const executeCode = async () => {
    setIsRunning(true);
    // TODO: Implement actual code execution
    console.log(`Executing ${language} code:`, code);
    setTimeout(() => setIsRunning(false), 2000);
  };

  // Download as file
  const downloadCode = () => {
    const fileExtensions: Record<string, string> = {
      python: 'py',
      javascript: 'js',
      typescript: 'ts',
      sql: 'sql',
      r: 'R',
      bash: 'sh',
      shell: 'sh',
      json: 'json',
      yaml: 'yml',
      xml: 'xml',
      html: 'html',
      css: 'css',
      markdown: 'md'
    };
    
    const extension = fileExtensions[language.toLowerCase()] || 'txt';
    const filename = fileName || `datasoph_code.${extension}`;
    
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Language icon mapping
  const getLanguageIcon = (lang: string): string => {
    const icons: Record<string, string> = {
      python: '🐍',
      javascript: '🟨',
      typescript: '🔷',
      sql: '🗄️',
      r: '📊',
      bash: '⚡',
      shell: '⚡',
      json: '📋',
      yaml: '⚙️',
      xml: '📄',
      html: '🌐',
      css: '🎨',
      markdown: '📝',
      java: '☕',
      cpp: '⚙️',
      csharp: '🟣',
      php: '🟪',
      ruby: '💎',
      go: '🐹',
      rust: '🦀',
      swift: '🍎'
    };
    return icons[lang.toLowerCase()] || '📄';
  };

  // Get language display name
  const getLanguageDisplayName = (lang: string): string => {
    const displayNames: Record<string, string> = {
      javascript: 'JavaScript',
      typescript: 'TypeScript',
      python: 'Python',
      sql: 'SQL',
      r: 'R',
      bash: 'Bash',
      shell: 'Shell',
      json: 'JSON',
      yaml: 'YAML',
      xml: 'XML',
      html: 'HTML',
      css: 'CSS',
      markdown: 'Markdown',
      java: 'Java',
      cpp: 'C++',
      csharp: 'C#',
      php: 'PHP',
      ruby: 'Ruby',
      go: 'Go',
      rust: 'Rust',
      swift: 'Swift'
    };
    return displayNames[lang.toLowerCase()] || lang.charAt(0).toUpperCase() + lang.slice(1);
  };

  // Check if language supports execution
  const isExecutableLanguage = (lang: string): boolean => {
    const executableLanguages = ['python', 'javascript', 'sql', 'r', 'bash', 'shell'];
    return executableLanguages.includes(lang.toLowerCase());
  };

  return (
    <div className={`bg-gray-900 rounded-lg overflow-hidden border border-gray-700 my-4 ${className}`}>
      {/* Header with language, title, and actions */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-2">
          <span className="text-lg" title={getLanguageDisplayName(language)}>
            {getLanguageIcon(language)}
          </span>
          <span className="text-sm font-medium text-gray-300">
            {getLanguageDisplayName(language)}
          </span>
          {title && (
            <>
              <span className="text-gray-500">•</span>
              <span className="text-sm text-gray-400">{title}</span>
            </>
          )}
          {fileName && (
            <>
              <span className="text-gray-500">•</span>
              <span className="text-sm text-gray-400 font-mono">{fileName}</span>
            </>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          {/* Execute button for supported languages */}
          {executable && isExecutableLanguage(language) && (
            <button
              onClick={executeCode}
              disabled={isRunning}
              className="flex items-center gap-1 px-2 py-1 text-xs text-green-400 hover:text-green-300 hover:bg-gray-700 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title={`Run ${getLanguageDisplayName(language)} code`}
            >
              <Play className="w-3 h-3" />
              {isRunning ? 'Running...' : 'Run'}
            </button>
          )}
          
          {/* Download button */}
          <button
            onClick={downloadCode}
            className="flex items-center gap-1 px-2 py-1 text-xs text-blue-400 hover:text-blue-300 hover:bg-gray-700 rounded transition-colors"
            title="Download as file"
          >
            <Download className="w-3 h-3" />
            Download
          </button>
          
          {/* Copy button */}
          <button
            onClick={copyCode}
            className="flex items-center gap-1 px-2 py-1 text-xs text-gray-400 hover:text-gray-300 hover:bg-gray-700 rounded transition-colors"
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-3 h-3 text-green-400" />
                <span className="text-green-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" />
                Copy
              </>
            )}
          </button>
        </div>
      </div>

      {/* Code content with syntax highlighting */}
      <div className="relative">
        <SyntaxHighlighter
          language={language.toLowerCase()}
          style={oneDark}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            padding: '1rem',
            background: 'transparent',
            fontSize: '14px',
            lineHeight: '1.5',
            fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace'
          }}
          lineNumberStyle={{
            color: '#6b7280',
            fontSize: '12px',
            minWidth: '2.5rem',
            paddingRight: '1rem'
          }}
          wrapLines={true}
          wrapLongLines={true}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeBlock; 