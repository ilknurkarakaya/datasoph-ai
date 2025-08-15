import React, { useState, useEffect } from 'react';
import { useSidebar, useChat } from '../../App.tsx';
import WelcomeLayout from './WelcomeLayout.tsx';
import ConversationLayout from './ConversationLayout.tsx';
import { chatService } from '../../services/api.ts';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

type TypingStage = 'thinking' | 'analyzing' | 'processing' | 'generating';

const ClaudeChatArea: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(() => {
    try {
      const savedMessages = localStorage.getItem('datasoph-chat-history');
      if (savedMessages) {
        const parsed = JSON.parse(savedMessages);
        return Array.isArray(parsed) ? parsed : [];
      }
    } catch (error) {
      console.error('Error loading initial messages:', error);
    }
    return [];
  });
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [typingStage, setTypingStage] = useState<TypingStage>('thinking');
  const [currentAbortController, setCurrentAbortController] = useState<AbortController | null>(null);
  const { setHasMessages } = useChat();
  
  // Update hasMessages context on mount based on loaded messages
  useEffect(() => {
    setHasMessages(messages.length > 0);
  }, [messages.length, setHasMessages]);
  
  // Load chat history on component mount and when localStorage changes
  useEffect(() => {
    const loadChatHistory = () => {
      const savedMessages = localStorage.getItem('datasoph-chat-history');
      if (savedMessages) {
        try {
          const parsedMessages = JSON.parse(savedMessages);
          setMessages(parsedMessages);
          setHasMessages(parsedMessages.length > 0);
        } catch (error) {
          console.error('Error loading chat history:', error);
        }
      } else {
        setMessages([]);
        setHasMessages(false);
      }
    };
    
    // Load initially
    loadChatHistory();
    
    // Listen for localStorage changes (for chat switching)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'datasoph-chat-history') {
        loadChatHistory();
      }
    };
    
    // Listen for custom events (for same-tab changes)
    const handleChatSwitch = () => {
      loadChatHistory();
    };
    
    // Load initially
    loadChatHistory();
    
    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('chatSwitch', handleChatSwitch);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('chatSwitch', handleChatSwitch);
    };
  }, [setHasMessages]);
  
  // Save messages to localStorage whenever messages change (filter out Base64 images)
  useEffect(() => {
    try {
      const filteredMessages = messages.map(msg => ({
        ...msg,
        content: msg.content.includes('data:image/png;base64') 
          ? msg.content.replace(/data:image\/png;base64,[^"]+/g, '[IMAGE_REMOVED_FOR_STORAGE]')
          : msg.content
      }));
      localStorage.setItem('datasoph-chat-history', JSON.stringify(filteredMessages.slice(-10))); // Keep only last 10 messages
    } catch (error) {
      console.error('Error saving messages to localStorage:', error);
      // If still failing, clear localStorage
      try {
        localStorage.removeItem('datasoph-chat-history');
      } catch {}
    }
  }, [messages]);
  
  // Listen for new chat trigger
  useEffect(() => {
    const handleNewChat = () => {
      setMessages([]);
      setInputValue('');
      setIsTyping(false);
      setHasMessages(false);
      // Cancel any ongoing request
      if (currentAbortController) {
        currentAbortController.abort();
        setCurrentAbortController(null);
      }
    };
    
    // Store the function globally for the context to call
    (window as any).triggerNewChat = handleNewChat;
    
    return () => {
      delete (window as any).triggerNewChat;
    };
  }, [setHasMessages, currentAbortController]);
  
  // Update hasMessages when messages change
  useEffect(() => {
    setHasMessages(messages.length > 0);
  }, [messages, setHasMessages]);
  
  const addMessage = (message: any) => {
    setMessages(prev => [...prev, message]);
  };

  const handleSendMessage = async (message: string, fileId?: string) => {
    // If AI is typing and user clicks send button, stop the current request
    if (isTyping && currentAbortController) {
      currentAbortController.abort();
      setIsTyping(false);
      setCurrentAbortController(null);
      return;
    }

    if (!message.trim() || isTyping) return;
    
    // 🚨 DEBUG: Log file_id
    console.log('🔍 handleSendMessage called with fileId:', fileId);
    
    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: message.trim(),
      timestamp: new Date().toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
      })
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    
    // Create abort controller for this request
    const abortController = new AbortController();
    setCurrentAbortController(abortController);
    
    // Enhanced typing stages with spiral logo animations
    setTypingStage('thinking');
    
    setTimeout(() => setTypingStage('analyzing'), 800);
    setTimeout(() => setTypingStage('processing'), 1600);
    setTimeout(() => setTypingStage('generating'), 2400);
    
    try {
      // If there's a fileId, call the real API for file analysis
      if (fileId) {
        const response = await chatService.sendMessage({
          message: message.trim(),
          user_id: 'web_user',
          file_id: fileId
        });
        
        if (!abortController.signal.aborted) {
          const aiMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: response.response,
            timestamp: new Date().toLocaleTimeString('en-US', { 
              hour: 'numeric', 
              minute: '2-digit',
              hour12: true 
            })
          };
          
          setMessages(prev => [...prev, aiMessage]);
        }
      } else {
        // ALWAYS call the real API for ALL messages - No more mock responses!
        const response = await chatService.sendMessage({
          message: message.trim(),
          user_id: 'web_user',
          file_id: fileId
        });
        
        if (!abortController.signal.aborted) {
          const aiMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: response.response,
            timestamp: new Date().toLocaleTimeString('en-US', { 
              hour: 'numeric', 
              minute: '2-digit',
              hour12: true 
            })
          };
          
          setMessages(prev => [...prev, aiMessage]);
        }
      }
    } catch (error) {
      if (!abortController.signal.aborted) {
        console.error('Chat error:', error);
        
        // Fallback to mock response on error
        setTimeout(() => {
          const aiMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: "I apologize, but I'm having trouble processing your request right now. Please try again or upload your file again.",
            timestamp: new Date().toLocaleTimeString('en-US', { 
              hour: 'numeric', 
              minute: '2-digit',
              hour12: true 
            })
          };
          
          setMessages(prev => [...prev, aiMessage]);
        }, 1000);
      }
    } finally {
      if (!abortController.signal.aborted) {
        setIsTyping(false);
        setCurrentAbortController(null);
      }
    }
  };
  
  return (
    <div className="flex flex-col h-full">
      {/* Clean header without border */}
      <div className="flex items-center p-3 bg-[var(--bg-main)] flex-shrink-0">
        <div className="flex-1" />
      </div>
      
      {/* Main Content Area */}
      <div className="flex-1 min-h-0">
        {messages.length > 0 ? (
          // Conversation Layout (Input at Bottom)
          <ConversationLayout 
            messages={messages}
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            typingStage={typingStage}
            addMessage={addMessage}
          />
        ) : (
          // Welcome Layout (Input Centered)
          <WelcomeLayout
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            addMessage={addMessage}
          />
        )}
      </div>
    </div>
  );
};

export default ClaudeChatArea; 