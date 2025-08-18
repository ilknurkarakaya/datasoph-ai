import React from 'react';

interface QuickActionCardProps {
  icon: string;
  title: string;
  description: string;
  onClick: () => void;
}

const QuickActionCard: React.FC<QuickActionCardProps> = ({ 
  icon, 
  title, 
  description, 
  onClick 
}) => {
  return (
    <button
      onClick={onClick}
      className="p-4 text-left bg-[var(--bg-input)] hover:bg-[var(--bg-hover)] border border-[var(--border-light)] rounded-xl transition-all duration-200 hover:shadow-sm group"
    >
      <div className="text-2xl mb-2">{icon}</div>
      <div className="text-sm font-medium text-[var(--text-primary)] mb-1 group-hover:text-[var(--avatar-ai)] transition-colors">
        {title}
      </div>
      <div className="text-xs text-[var(--text-secondary)]">
        {description}
      </div>
    </button>
  );
};

export default QuickActionCard; 