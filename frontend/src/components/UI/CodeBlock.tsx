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
  
  // Copy to clipboard with smooth animation
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

  // Get authentic programming language colors
  const getLanguageColor = (lang: string): string => {
    const colors: Record<string, string> = {
      python: 'text-[#3776ab]',          // Python blue
      javascript: 'text-[#f7df1e]',     // JavaScript yellow
      typescript: 'text-[#3178c6]',     // TypeScript blue
      sql: 'text-[#e38c00]',            // SQL orange
      r: 'text-[#276dc3]',              // R blue
      bash: 'text-[#4eaa25]',           // Bash green
      shell: 'text-[#4eaa25]',          // Shell green
      json: 'text-[#292929]',           // JSON dark gray
      yaml: 'text-[#cb171e]',           // YAML red
      xml: 'text-[#0060ac]',            // XML blue
      html: 'text-[#e34c26]',           // HTML orange-red
      css: 'text-[#1572b6]',            // CSS blue
      markdown: 'text-[#083fa1]',       // Markdown blue
      java: 'text-[#ed8b00]',           // Java orange
      cpp: 'text-[#00599c]',            // C++ blue
      csharp: 'text-[#239120]',         // C# green
      php: 'text-[#777bb4]',            // PHP purple
      ruby: 'text-[#cc342d]',           // Ruby red
      go: 'text-[#00add8]',             // Go cyan
      rust: 'text-[#dea584]',           // Rust orange
      swift: 'text-[#fa7343]'           // Swift orange
    };
    return colors[lang.toLowerCase()] || 'text-gray-400';
  };

  // Check if language supports execution
  const isExecutableLanguage = (lang: string): boolean => {
    const executableLanguages = ['python', 'javascript', 'sql', 'r', 'bash', 'shell'];
    return executableLanguages.includes(lang.toLowerCase());
  };

  return (
    <div className={`group relative bg-[#0d1117] rounded-lg overflow-hidden border border-[#30363d] shadow-lg my-4 ${className}`}>
      {/* Professional Header */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#161b22] border-b border-[#30363d]">
        <div className="flex items-center gap-3">
          {/* Language icon and info */}
          <div className="flex items-center gap-2">
            <div className="flex flex-col">
              <span className={`text-sm font-medium ${getLanguageColor(language)}`}>
                {getLanguageDisplayName(language)}
              </span>
              {fileName && (
                <span className="text-xs text-[#8b949e] font-mono">{fileName}</span>
              )}
            </div>
          </div>
          
          {/* Title */}
          {title && (
            <div className="flex items-center gap-2 ml-1">
              <div className="w-1 h-3 bg-[#0969da] rounded-full"></div>
              <span className="text-sm text-[#f0f6fc] font-medium">{title}</span>
            </div>
          )}
        </div>
        
        {/* Action buttons */}
        <div className="flex items-center gap-1">
          {/* Execute button for supported languages */}
          {executable && isExecutableLanguage(language) && (
            <button
              onClick={executeCode}
              disabled={isRunning}
              className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-[#238636] hover:text-[#2ea043] hover:bg-[#238636]/10 rounded-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed border border-[#238636]/30 hover:border-[#2ea043]/40"
              title={`Run ${getLanguageDisplayName(language)} code`}
            >
              <Play className={`w-3 h-3 ${isRunning ? 'animate-pulse' : ''}`} />
              {isRunning ? 'Running...' : 'Run'}
            </button>
          )}
          
          {/* Download button */}
          <button
            onClick={downloadCode}
            className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-[#0969da] hover:text-[#1f6feb] hover:bg-[#0969da]/10 rounded-md transition-all duration-200 border border-[#0969da]/30 hover:border-[#1f6feb]/40"
            title="Download as file"
          >
            <Download className="w-3 h-3" />
            Download
          </button>
          
          {/* Copy button with enhanced styling */}
          <button
            onClick={copyCode}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium rounded-md transition-all duration-200 border ${
              copied 
                ? 'text-[#238636] bg-[#238636]/10 border-[#238636]/30' 
                : 'text-[#8b949e] hover:text-[#f0f6fc] hover:bg-[#30363d] border-[#30363d] hover:border-[#8b949e]/30'
            }`}
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-3 h-3 text-[#238636]" />
                <span className="text-[#238636] font-medium">Copied!</span>
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

      {/* Code content with proper alignment */}
      <div className="relative bg-[#0d1117]">
        <SyntaxHighlighter
          language={language.toLowerCase()}
          style={oneDark}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            padding: '16px 20px',
            background: 'transparent',
            fontSize: '13px',
            lineHeight: '1.5',
            fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Monaco, Consolas, "Liberation Mono", Menlo, monospace',
            borderRadius: '0',
            overflow: 'auto',
            whiteSpace: 'pre' as const,
            tabSize: 4
          }}
          lineNumberStyle={{
            color: '#6e7681',
            fontSize: '12px',
            minWidth: '45px',
            paddingRight: '20px',
            borderRight: '1px solid #21262d',
            marginRight: '20px',
            userSelect: 'none',
            textAlign: 'right',
            fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Monaco, Consolas, "Liberation Mono", Menlo, monospace'
          }}
          wrapLines={false}
          wrapLongLines={false}
          codeTagProps={{
            style: {
              fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Monaco, Consolas, "Liberation Mono", Menlo, monospace',
              fontSize: '13px',
              fontWeight: '400',
              whiteSpace: 'pre' as const,
              tabSize: 4
            }
          }}
          preTag={({ children, ...props }: { children: React.ReactNode; [key: string]: any }) => (
            <pre 
              {...props} 
              style={{
                ...props.style,
                whiteSpace: 'pre' as const,
                tabSize: 4,
                fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Monaco, Consolas, "Liberation Mono", Menlo, monospace'
              }}
            >
              {children}
            </pre>
          )}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeBlock; 