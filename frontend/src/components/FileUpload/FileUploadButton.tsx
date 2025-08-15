import React, { useRef } from 'react';

interface FileUploadButtonProps {
  onFileSelect: (files: File[]) => void;
  disabled?: boolean;
}

const FileUploadButton: React.FC<FileUploadButtonProps> = ({ onFileSelect, disabled = false }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length > 0) {
      onFileSelect(files);
    }
    // Reset input value to allow selecting the same file again
    e.target.value = '';
  };

  return (
    <>
      <button
        onClick={handleClick}
        disabled={disabled}
        className={`
          flex-shrink-0
          w-10 h-10
          rounded-xl
          flex items-center justify-center
          transition-all duration-200
          ${disabled 
            ? 'bg-gray-600 cursor-not-allowed text-gray-400'
            : 'bg-claude-surface hover:bg-claude-border text-claude-textMuted hover:text-claude-text'
          }
        `}
        title="Attach file"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
      </button>
      
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".csv,.xlsx,.xls,.json,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg"
        onChange={handleFileChange}
        className="hidden"
      />
    </>
  );
};

export default FileUploadButton; 