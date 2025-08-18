import React, { useState, useEffect, createContext, useContext } from 'react';
import ClaudeSidebar from './components/Claude/ClaudeSidebar.tsx';
import ClaudeChatArea from './components/Claude/ClaudeChatArea.tsx';

interface DarkModeContextType {
  darkMode: boolean;
  setDarkMode: (value: boolean) => void;
}

const DarkModeContext = createContext<DarkModeContextType>({
  darkMode: false,
  setDarkMode: () => {}
});

export const useDarkMode = () => useContext(DarkModeContext);

interface UserContextType {
  userName: string;
  userRole: string;
  setUserName: (name: string) => void;
  setUserRole: (role: string) => void;
}

const UserContext = createContext<UserContextType>({
  userName: 'User',
  userRole: 'Data Analyst',
  setUserName: () => {},
  setUserRole: () => {}
});

export const useUser = () => useContext(UserContext);

interface ChatContextType {
  onNewChat: () => void;
  hasMessages: boolean;
  setHasMessages: (value: boolean) => void;
}

const ChatContext = createContext<ChatContextType>({
  onNewChat: () => {},
  hasMessages: false,
  setHasMessages: () => {}
});

export const useChat = () => useContext(ChatContext);

interface SidebarContextType {
  sidebarOpen: boolean;
  setSidebarOpen: (value: boolean) => void;
  toggleSidebar: () => void;
}

const SidebarContext = createContext<SidebarContextType>({
  sidebarOpen: true,
  setSidebarOpen: () => {},
  toggleSidebar: () => {}
});

export const useSidebar = () => useContext(SidebarContext);

function DarkModeProvider({ children }: { children: React.ReactNode }) {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('datasoph-dark-mode');
    return saved ? JSON.parse(saved) : false;
  });
  
  useEffect(() => {
    localStorage.setItem('datasoph-dark-mode', JSON.stringify(darkMode));
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);
  
  return (
    <DarkModeContext.Provider value={{ darkMode, setDarkMode }}>
      <div data-theme={darkMode ? 'dark' : 'light'}>
        {children}
      </div>
    </DarkModeContext.Provider>
  );
}

function UserProvider({ children }: { children: React.ReactNode }) {
  const [userName, setUserName] = useState(() => {
    const saved = localStorage.getItem('datasoph-user-name');
    return saved || 'User';
  });
  
  const [userRole, setUserRole] = useState(() => {
    const saved = localStorage.getItem('datasoph-user-role');
    return saved || 'Data Analyst';
  });
  
  useEffect(() => {
    localStorage.setItem('datasoph-user-name', userName);
  }, [userName]);
  
  useEffect(() => {
    localStorage.setItem('datasoph-user-role', userRole);
  }, [userRole]);
  
  useEffect(() => {
    const hasPrompted = localStorage.getItem('datasoph-name-prompted');
    if (!hasPrompted) {
      const name = prompt('Hello! What is your name?');
      if (name && name.trim()) {
        setUserName(name.trim());
      }
      localStorage.setItem('datasoph-name-prompted', 'true');
    }
  }, []);
  
  return (
    <UserContext.Provider value={{ userName, userRole, setUserName, setUserRole }}>
      {children}
    </UserContext.Provider>
  );
}

function ChatProvider({ children }: { children: React.ReactNode }) {
  const [hasMessages, setHasMessages] = useState(false);
  
  const onNewChat = () => {
    setHasMessages(false);
    
    if ((window as any).triggerNewChat) {
      (window as any).triggerNewChat();
    }
    
    window.history.replaceState(null, '', window.location.pathname);
  };
  
  useEffect(() => {
    const handlePopState = () => {
      if (hasMessages) {
        onNewChat();
      }
    };
    
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [hasMessages]);
  
  useEffect(() => {
    if (hasMessages) {
      window.history.pushState({}, '', '#chat');
    }
  }, [hasMessages]);
  
  return (
    <ChatContext.Provider value={{ onNewChat, hasMessages, setHasMessages }}>
      {children}
    </ChatContext.Provider>
  );
}

function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    const saved = localStorage.getItem('datasoph-sidebar-open');
    if (saved !== null) {
      return JSON.parse(saved);
    }
    return window.innerWidth >= 1024;
  });
  
  const toggleSidebar = () => {
    setSidebarOpen((prev: boolean) => !prev);
  };
  
  useEffect(() => {
    localStorage.setItem('datasoph-sidebar-open', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);
  
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024 && sidebarOpen) {
        setSidebarOpen(false);
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [sidebarOpen]);
  
  return (
    <SidebarContext.Provider value={{ sidebarOpen, setSidebarOpen, toggleSidebar }}>
      {children}
    </SidebarContext.Provider>
  );
}

function DataSophApp() {
  useEffect(() => {
    const handleDragOver = (e: DragEvent) => {
      const target = e.target as HTMLElement;
      const isDropZone = target.closest('[data-drop-zone]');
      if (!isDropZone) {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    const handleDrop = (e: DragEvent) => {
      const target = e.target as HTMLElement;
      const isDropZone = target.closest('[data-drop-zone]');
      if (!isDropZone) {
        e.preventDefault();
        e.stopPropagation();
        // Global drop prevented - not in drop zone
      }
    };

    document.addEventListener('dragover', handleDragOver);
    document.addEventListener('drop', handleDrop);

    return () => {
      document.removeEventListener('dragover', handleDragOver);
      document.removeEventListener('drop', handleDrop);
    };
  }, []);

  return (
    <div className="DataSoph-app font-system">
      <DarkModeProvider>
        <UserProvider>
          <ChatProvider>
            <SidebarProvider>
              <AppContent />
            </SidebarProvider>
          </ChatProvider>
        </UserProvider>
      </DarkModeProvider>
    </div>
  );
}

function AppContent() {
  const { sidebarOpen, setSidebarOpen } = useSidebar();

  return (
    <div className="flex h-screen relative">
      <div className={`transition-all duration-300 ease-in-out ${
        sidebarOpen ? 'w-[260px]' : 'w-12'
      } bg-[var(--bg-sidebar)] flex flex-col ${sidebarOpen ? '' : 'items-center'} lg:relative absolute lg:z-auto z-50 h-full`}>
        {sidebarOpen ? (
          <div className="flex-1 flex flex-col overflow-hidden">
            <ClaudeSidebar />
          </div>
        ) : (
          <div className="p-3 flex-shrink-0">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] rounded-md transition-colors"
              title="Expand sidebar"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        )}
      </div>
      
      <div className="flex-1 bg-[var(--bg-main)] flex flex-col relative">
        <ClaudeChatArea />
      </div>
      
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}

export default DataSophApp; 