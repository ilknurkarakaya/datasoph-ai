import React, { useState, useRef, useEffect } from 'react';
import { MoreHorizontal, Trash2, Edit2 } from 'lucide-react';

interface DropdownMenuProps {
  onDelete?: () => void;
  onRename?: () => void;
  isVisible?: boolean;
}

const DropdownMenu: React.FC<DropdownMenuProps> = ({
  onDelete,
  onRename,
  isVisible = true
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsOpen(!isOpen);
  };

  const handleMenuClick = (action: () => void) => {
    return (e: React.MouseEvent) => {
      e.stopPropagation();
      action();
      setIsOpen(false);
    };
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Three-dot trigger button */}
      <button
        ref={buttonRef}
        onClick={handleToggle}
        className={`
          p-1 rounded transition-all duration-200
          ${isOpen ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}
        `}
        style={{ 
          color: 'var(--text-secondary)',
          backgroundColor: isOpen ? 'var(--message-hover)' : 'transparent'
        }}
        onMouseEnter={(e) => {
          if (!isOpen) {
            e.currentTarget.style.color = 'var(--text-primary)';
            e.currentTarget.style.backgroundColor = 'var(--message-hover)';
          }
        }}
        onMouseLeave={(e) => {
          if (!isOpen) {
            e.currentTarget.style.color = 'var(--text-secondary)';
            e.currentTarget.style.backgroundColor = 'transparent';
          }
        }}
      >
        <MoreHorizontal className="w-4 h-4" />
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <div 
          className="absolute right-0 top-full mt-1 py-1 rounded-md shadow-lg border z-50 min-w-[140px]"
          style={{
            backgroundColor: 'var(--main-bg)',
            borderColor: 'var(--sidebar-border)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
          }}
        >
          {onRename && (
            <button
              onClick={handleMenuClick(onRename)}
              className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left transition-colors"
              style={{ color: 'var(--text-primary)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--message-hover)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              <Edit2 className="w-4 h-4" />
              Rename
            </button>
          )}
          
          {onDelete && (
            <button
              onClick={handleMenuClick(onDelete)}
              className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left transition-colors text-red-600 hover:text-red-700"
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--message-hover)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default DropdownMenu; 