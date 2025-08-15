import React, { useState } from 'react';
import { Plus, Moon, Sun, MoreHorizontal, Trash2, Edit2, ChevronDown } from 'lucide-react';
import { ChatHistory } from '../../types/chat.ts';
import { useDarkMode } from '../../hooks/useDarkMode.ts';

interface UserProfile {
  name: string;
  email?: string;
  plan: string;
  avatar?: string;
  initials: string;
}

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  chats: ChatHistory[];
  currentChatId: string | null;
  onNewChat: () => void;
  onSelectChat: (chatId: string) => void;
  onDeleteChat: (chatId: string) => void;
  onRenameChat: (chatId: string, newTitle: string) => void;
  user?: UserProfile;
}

const Sidebar: React.FC<SidebarProps> = ({ 
  isOpen, 
  onToggle, 
  chats,
  currentChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  onRenameChat,
  user = {
    name: 'Guest User',
    plan: 'Free plan',
    initials: 'GU'
  }
}) => {
  const { isDarkMode, toggleDarkMode } = useDarkMode();
  const [renamingChatId, setRenamingChatId] = useState<string | null>(null);
  const [renameValue, setRenameValue] = useState('');
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);

  const handleRenameStart = (chat: ChatHistory) => {
    setRenamingChatId(chat.id);
    setRenameValue(chat.title);
    setOpenMenuId(null);
  };

  const handleRenameCancel = () => {
    setRenamingChatId(null);
    setRenameValue('');
  };

  const handleRenameSubmit = (chatId: string) => {
    if (renameValue.trim()) {
      onRenameChat(chatId, renameValue.trim());
    }
    setRenamingChatId(null);
    setRenameValue('');
  };

  const handleKeyPress = (e: React.KeyboardEvent, chatId: string) => {
    if (e.key === 'Enter') {
      handleRenameSubmit(chatId);
    } else if (e.key === 'Escape') {
      handleRenameCancel();
    }
  };

  return (
    <>
      {/* Claude's New Sidebar Design */}
      <div className={`
        w-[280px] flex flex-col h-full 
        bg-gray-50 dark:bg-gray-800
        transform transition-transform duration-300 ease-in-out z-50
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 fixed lg:relative
      `}>
        
        {/* Header with New Chat Button */}
        <div className="p-4">
          {/* Mobile close button */}
          <button
            onClick={() => {
              console.log('Sidebar close button clicked');
              onToggle();
            }}
            className="lg:hidden absolute top-4 right-4 p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          {/* New Chat Button - Claude's Blue Style */}
          <button
            onClick={onNewChat}
            className="w-full flex items-center gap-3 px-3 py-3 mb-6 bg-blue-600 dark:bg-orange-600 hover:bg-blue-700 dark:hover:bg-orange-700 rounded-lg transition-colors text-left"
          >
            <div className="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
              <Plus className="w-4 h-4 text-white" />
            </div>
            <span className="text-white font-medium">New chat</span>
          </button>
        </div>

        {/* Recents Section */}
        <div className="flex-1 overflow-y-auto px-4">
          <div className="mb-4">
            <h3 className="text-gray-600 dark:text-gray-400 text-sm font-medium mb-3">Recents</h3>
            
            <div className="space-y-1">
              {chats.length > 0 ? (
                chats.map((chat) => (
                  <div key={chat.id} className="group relative">
                    <div
                      className={`
                        flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-all duration-150
                        ${currentChatId === chat.id 
                          ? 'bg-blue-100 dark:bg-gray-700 text-blue-900 dark:text-white' 
                          : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700'
                        }
                      `}
                      onClick={() => onSelectChat(chat.id)}
                    >
                      {/* Chat Title */}
                      <div className="flex-1 min-w-0">
                        {renamingChatId === chat.id ? (
                          <input
                            type="text"
                            value={renameValue}
                            onChange={(e) => setRenameValue(e.target.value)}
                            onKeyPress={(e) => handleKeyPress(e, chat.id)}
                            onBlur={() => handleRenameCancel()}
                            onClick={(e) => e.stopPropagation()}
                            className="w-full text-sm bg-white dark:bg-gray-600 border border-gray-300 dark:border-gray-500 rounded px-2 py-1 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-blue-500 dark:focus:ring-orange-500"
                            autoFocus
                          />
                        ) : (
                          <span className="text-sm truncate block">
                            {chat.title}
                          </span>
                        )}
                      </div>
                      
                      {/* Three-dot menu */}
                      <div className="relative">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setOpenMenuId(openMenuId === chat.id ? null : chat.id);
                          }}
                          className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-150"
                        >
                          <MoreHorizontal className="w-4 h-4 text-gray-400" />
                        </button>

                        {/* Dropdown menu */}
                        {openMenuId === chat.id && (
                          <>
                            {/* Click outside overlay */}
                            <div 
                              className="fixed inset-0 z-10"
                              onClick={() => setOpenMenuId(null)}
                            />
                            
                            {/* Menu */}
                            <div className="absolute right-0 top-full mt-1 w-48 py-1 bg-white dark:bg-gray-700 rounded-lg shadow-lg z-20">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleRenameStart(chat);
                                }}
                                className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-600"
                              >
                                <Edit2 className="w-4 h-4" />
                                Rename
                              </button>
                              
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onDeleteChat(chat.id);
                                  setOpenMenuId(null);
                                }}
                                className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 hover:bg-gray-100 dark:hover:bg-gray-600"
                              >
                                <Trash2 className="w-4 h-4" />
                                Delete chat
                              </button>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="px-3 py-8 text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Your conversations will appear here
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* User Profile Section - Bottom */}
        <div className="p-4">
          {/* Dark Mode Toggle */}
          <button
            onClick={toggleDarkMode}
            className="w-full flex items-center gap-3 px-3 py-2 mb-3 rounded-lg transition-colors text-left text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {isDarkMode ? (
              <Sun className="w-4 h-4" />
            ) : (
              <Moon className="w-4 h-4" />
            )}
            <span className="text-sm text-gray-700 dark:text-gray-300">{isDarkMode ? 'Light mode' : 'Dark mode'}</span>
          </button>

          {/* Dynamic User Profile */}
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer">
            {user.avatar ? (
              <img 
                src={user.avatar} 
                alt={user.name}
                className="w-8 h-8 rounded-full object-cover"
              />
            ) : (
              <div className="w-8 h-8 rounded-full bg-orange-600 flex items-center justify-center">
                <span className="text-white text-sm font-medium">{user.initials}</span>
              </div>
            )}
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium text-gray-900 dark:text-white truncate">{user.name}</div>
              <div className="text-xs text-gray-600 dark:text-gray-400">{user.plan}</div>
            </div>
            <ChevronDown className="w-4 h-4 text-gray-600 dark:text-gray-400" />
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar; 