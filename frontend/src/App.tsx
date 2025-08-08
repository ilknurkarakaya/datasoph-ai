import React, { useState, useEffect, createContext, useContext } from 'react';
import './index.css';
import ClaudeSidebar from './components/Claude/ClaudeSidebar';
import ClaudeChatArea from './components/Claude/ClaudeChatArea';

// Dark mode context
interface DarkModeContextType {
  darkMode: boolean;
  setDarkMode: (value: boolean) => void;
}

const DarkModeContext = createContext<DarkModeContextType>({
  darkMode: false,
  setDarkMode: () => {}
});

export const useDarkMode = () => useContext(DarkModeContext);

// User context
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

// Chat context
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

// Sidebar context
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

// Dark mode provider
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

// User provider
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
  
  // Prompt for user name on first visit
  useEffect(() => {
    const hasPrompted = localStorage.getItem('datasoph-name-prompted');
    if (!hasPrompted) {
      const name = prompt('Merhaba! Adınız nedir?');
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

// Chat provider
function ChatProvider({ children }: { children: React.ReactNode }) {
  const [hasMessages, setHasMessages] = useState(false);
  
  const onNewChat = () => {
    setHasMessages(false);
    
    // Call the triggerNewChat function if it exists
    if ((window as any).triggerNewChat) {
      (window as any).triggerNewChat();
    }
    
    // Update URL to home state without adding to history
    window.history.replaceState(null, '', window.location.pathname);
  };
  
  // Handle browser back button
  useEffect(() => {
    const handlePopState = () => {
      if (hasMessages) {
        onNewChat();
      }
    };
    
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [hasMessages]);
  
  // Update URL when chat starts
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

// Sidebar provider
function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    // Default to open on desktop, closed on mobile
    const saved = localStorage.getItem('datasoph-sidebar-open');
    if (saved !== null) {
      return JSON.parse(saved);
    }
    return window.innerWidth >= 1024; // Default open on desktop
  });
  
  const toggleSidebar = () => {
    setSidebarOpen((prev: boolean) => !prev);
  };
  
  useEffect(() => {
    localStorage.setItem('datasoph-sidebar-open', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);
  
  // Handle window resize
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

// Main DataSoph App - Exact Claude Layout with Collapsible Sidebar
function DataSophApp() {
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
      {/* Sidebar - Collapsible */}
      <div className={`transition-all duration-300 ease-in-out ${
        sidebarOpen ? 'w-[260px]' : 'w-0'
      } bg-[var(--bg-sidebar)] border-r border-[var(--border-light)] flex flex-col overflow-hidden lg:relative absolute lg:z-auto z-50 h-full`}>
        <ClaudeSidebar />
      </div>
      
      {/* Main Chat Area - Adjusts to sidebar state */}
      <div className="flex-1 bg-[var(--bg-main)] flex flex-col relative">
        <ClaudeChatArea />
      </div>
      
      {/* Mobile Overlay */}
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