import React from 'react';
import { useDarkMode, useUser, useChat, useSidebar } from '../../App.tsx';

const ClaudeSidebar: React.FC = () => {
  const { darkMode, setDarkMode } = useDarkMode();
  const { userName, setUserName } = useUser();
  const { onNewChat } = useChat();
  const { setSidebarOpen } = useSidebar();
  
  // State for managing menu and rename
  const [openMenuId, setOpenMenuId] = React.useState<string | null>(null);
  const [renamingChatId, setRenamingChatId] = React.useState<string | null>(null);
  const [renameValue, setRenameValue] = React.useState('');
  
  // Load chat history from localStorage
  const [chatHistory, setChatHistory] = React.useState<{id: string, title: string, messages: any[]}[]>([]);
  
  React.useEffect(() => {
    const savedHistory = localStorage.getItem('datasoph-chat-sessions');
    if (savedHistory) {
      try {
        setChatHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    }
  }, []);
  
  // Update chat history when messages change
  React.useEffect(() => {
    const checkForNewMessages = () => {
      const savedMessages = localStorage.getItem('datasoph-chat-history');
      if (savedMessages) {
        try {
          const messages = JSON.parse(savedMessages);
          if (messages.length > 0) {
            // Check if this is a new session or update to existing
            const sessionId = localStorage.getItem('current-session-id') || 'session-' + Date.now();
            const firstUserMessage = messages.find((msg: any) => msg.type === 'user');
            if (firstUserMessage) {
              const title = firstUserMessage.content.substring(0, 30) + (firstUserMessage.content.length > 30 ? '...' : '');
              
              setChatHistory(prev => {
                const existingIndex = prev.findIndex(chat => chat.id === sessionId);
                let newHistory;
                
                // Filter out Base64 images from messages to save localStorage space
                const cleanMessages = messages.map((msg: any) => {
                  if (msg.type === 'ai' && msg.content) {
                    // Remove Base64 data URLs but keep the HTML structure
                    const cleanContent = msg.content.replace(/data:image\/[^;]+;base64,[^"]+/g, '[IMAGE_REMOVED]');
                    return { ...msg, content: cleanContent };
                  }
                  return msg;
                });
                
                if (existingIndex >= 0) {
                  // Update existing session
                  newHistory = [...prev];
                  newHistory[existingIndex] = { id: sessionId, title, messages: cleanMessages };
                } else {
                  // Create new session - limit to last 5 sessions to save space
                  newHistory = [{ id: sessionId, title, messages: cleanMessages }, ...prev.slice(0, 4)];
                }
                
                try {
                  localStorage.setItem('datasoph-chat-sessions', JSON.stringify(newHistory));
                } catch (error) {
                  console.error('localStorage quota exceeded, clearing old sessions:', error);
                  // If still quota exceeded, keep only current session
                  const currentOnly = [{ id: sessionId, title, messages: cleanMessages }];
                  localStorage.setItem('datasoph-chat-sessions', JSON.stringify(currentOnly));
                  newHistory = currentOnly;
                }
                return newHistory;
              });
            }
          }
        } catch (error) {
          console.error('Error processing chat messages:', error);
        }
      }
    };
    
    // Check immediately and then every 2 seconds
    checkForNewMessages();
    const interval = setInterval(checkForNewMessages, 2000);
    return () => clearInterval(interval);
  }, []);
  
  // Handle chat selection
  const handleChatSelect = (chat: {id: string, title: string, messages: any[]}) => {
    // Save the selected chat as current chat history
    localStorage.setItem('datasoph-chat-history', JSON.stringify(chat.messages));
    // Set current session ID
    localStorage.setItem('current-session-id', chat.id);
    // Dispatch custom event to trigger chat area reload
    window.dispatchEvent(new CustomEvent('chatSwitch'));
  };
  
  // Handle chat rename
  const handleRenameStart = (chat: {id: string, title: string, messages: any[]}) => {
    setRenamingChatId(chat.id);
    setRenameValue(chat.title);
    setOpenMenuId(null);
  };
  
  const handleRenameSubmit = (chatId: string) => {
    if (renameValue.trim()) {
      setChatHistory(prev => {
        const updated = prev.map(chat => 
          chat.id === chatId ? { ...chat, title: renameValue.trim() } : chat
        );
        localStorage.setItem('datasoph-chat-sessions', JSON.stringify(updated));
        return updated;
      });
    }
    setRenamingChatId(null);
    setRenameValue('');
  };
  
  const handleRenameCancel = () => {
    setRenamingChatId(null);
    setRenameValue('');
  };
  
  // Handle chat delete
  const handleChatDelete = (chatId: string) => {
    setChatHistory(prev => {
      const updated = prev.filter(chat => chat.id !== chatId);
      localStorage.setItem('datasoph-chat-sessions', JSON.stringify(updated));
      return updated;
    });
    setOpenMenuId(null);
    
    // If deleted chat was current, clear current chat
    const currentSessionId = localStorage.getItem('current-session-id');
    if (currentSessionId === chatId) {
      localStorage.removeItem('datasoph-chat-history');
      localStorage.removeItem('current-session-id');
      window.dispatchEvent(new CustomEvent('chatSwitch'));
    }
  };
  
  // Handle key press for rename
  const handleKeyPress = (e: React.KeyboardEvent, chatId: string) => {
    if (e.key === 'Enter') {
      handleRenameSubmit(chatId);
    } else if (e.key === 'Escape') {
      handleRenameCancel();
    }
  };
  
  const handleNewChat = () => {
    // Create new session ID for the new chat
    const newSessionId = 'session-' + Date.now();
    localStorage.setItem('current-session-id', newSessionId);
    // Clear current chat history
    localStorage.removeItem('datasoph-chat-history');
    // Dispatch custom event to trigger chat area reload
    window.dispatchEvent(new CustomEvent('chatSwitch'));
    onNewChat();
  };
  
  const handleUserNameClick = () => {
    const newName = window.prompt('Adınızı güncelleyin:', userName);
    if (newName && newName.trim()) {
      setUserName(newName.trim());
    }
  };

  const handleClearDataContext = async () => {
    // eslint-disable-next-line no-restricted-globals
    if (confirm('Bu işlem tüm eski veri bağlamını ve konuşma geçmişini silecek. Devam etmek istiyor musunuz?')) {
      try {
        // Import API dynamically to avoid circular imports
        const api = await import('../../services/api');
        const result = await api.resetConversation();
        console.log('✅ Data context cleared:', result);
        
        // Also clear local storage
        localStorage.removeItem('datasoph-chat-history');
        localStorage.removeItem('datasoph-chat-sessions');
        localStorage.removeItem('current-session-id');
        
        // Trigger chat area reload
        window.dispatchEvent(new CustomEvent('chatSwitch'));
        setChatHistory([]);
        
        window.alert(result.message || 'Veri bağlamı başarıyla temizlendi! 🔄');
      } catch (error) {
        console.error('❌ Error clearing data context:', error);
        window.alert('Veri bağlamı temizlenirken bir hata oluştu. Sayfayı yenilemeyi deneyin.');
      }
    }
  };
  
  return (
    <>
      {/* Top Section - DataSoph Logo, Brand and Toggle */}
      <div className="px-3 py-4">
        <div className="flex items-center justify-between px-0">
          <div 
            className="flex items-center cursor-pointer hover:opacity-80 transition-opacity"
            onClick={handleNewChat}
            title="Go to homepage"
          >
          <span className="text-xl font-medium text-[var(--text-primary)] font-system">Datasoph</span>
          </div>
          {/* Toggle Button - aligned with logo/brand */}
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] rounded-md transition-colors"
            title="Collapse sidebar"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      {/* New Chat Section */}
      <div className="p-3">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center gap-3 px-0 py-2 hover:bg-[var(--bg-hover)] rounded-md transition-colors group text-left"
        >
          <svg className="w-4 h-4 text-[var(--text-secondary)] group-hover:text-[var(--text-primary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-sm font-medium text-[var(--text-primary)] font-system">New chat</span>
        </button>
      </div>
      
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-3">
          {chatHistory.length > 0 ? (
            <div className="space-y-1">
              <div className="text-xs text-[var(--text-tertiary)] font-system mb-2">Recent Chats</div>
              {chatHistory.map((chat, index) => (
                <div key={chat.id} className="group relative">
                  <div
                    className="flex items-center justify-between px-2 py-2 hover:bg-[var(--bg-hover)] rounded-md transition-colors cursor-pointer"
                    onClick={() => renamingChatId !== chat.id && handleChatSelect(chat)}
                  >
                    {/* Title */}
                    <div className="flex items-center flex-1 min-w-0">
                      {/* Title or Rename Input */}
                      {renamingChatId === chat.id ? (
                        <input
                          type="text"
                          value={renameValue}
                          onChange={(e) => setRenameValue(e.target.value)}
                          onKeyPress={(e) => handleKeyPress(e, chat.id)}
                          onBlur={() => handleRenameCancel()}
                          onClick={(e) => e.stopPropagation()}
                          className="flex-1 text-xs bg-[var(--bg-main)] border border-[var(--border-light)] rounded px-1 py-0.5 text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-blue-500"
                          autoFocus
                        />
                      ) : (
                        <span className="text-xs text-[var(--text-primary)] font-system truncate flex-1">
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
                        className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-[var(--bg-hover)] transition-all duration-150"
                      >
                        <svg className="w-3 h-3 text-[var(--text-secondary)]" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                        </svg>
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
                          <div className="absolute right-0 top-full mt-1 w-32 py-1 bg-[var(--bg-main)] rounded-lg shadow-lg border border-[var(--border-light)] z-20">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRenameStart(chat);
                              }}
                              className="w-full flex items-center gap-2 px-3 py-1.5 text-xs text-left text-[var(--text-primary)] hover:bg-[var(--bg-hover)]"
                            >
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                              </svg>
                              Rename
                            </button>
                            
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleChatDelete(chat.id);
                              }}
                              className="w-full flex items-center gap-2 px-3 py-1.5 text-xs text-left text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                            >
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                              Delete
                            </button>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
          <div className="text-xs text-[var(--text-tertiary)] font-system">No previous conversations</div>
          )}
        </div>
      </div>
      
      {/* User Profile Section */}
              <div className="p-3">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-7 h-7 bg-[var(--bg-hover)] rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1 min-w-0 cursor-pointer" onClick={handleUserNameClick}>
            <div className="text-sm font-medium text-[var(--text-primary)] hover:text-[var(--avatar-user)] transition-colors font-system">
              {userName}
            </div>
          </div>
          {/* Clear Data Context Button */}
          <button
            onClick={handleClearDataContext}
            className="p-1 rounded hover:bg-[var(--bg-hover)] transition-colors mr-1"
            title="Clear old data context for fresh analysis"
          >
            <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-1 rounded hover:bg-[var(--bg-hover)] transition-colors"
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? (
              <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            ) : (
              <svg className="w-4 h-4 text-[var(--text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </>
  );
};

export default ClaudeSidebar; 