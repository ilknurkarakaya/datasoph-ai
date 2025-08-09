import React, { useState, useEffect } from 'react';
import { useSidebar, useChat } from '../../App';
import WelcomeLayout from './WelcomeLayout';
import ConversationLayout from './ConversationLayout';
import { chatService } from '../../services/api';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

type TypingStage = 'thinking' | 'analyzing' | 'processing' | 'generating';

const ClaudeChatArea: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [typingStage, setTypingStage] = useState<TypingStage>('thinking');
  const { toggleSidebar } = useSidebar();
  const { hasMessages, setHasMessages, onNewChat } = useChat();
  
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
    
    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('chatSwitch', handleChatSwitch);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('chatSwitch', handleChatSwitch);
    };
  }, [setHasMessages]);
  
  // Save messages to localStorage whenever messages change
  useEffect(() => {
    localStorage.setItem('datasoph-chat-history', JSON.stringify(messages));
  }, [messages]);
  
  // Listen for new chat trigger
  useEffect(() => {
    const handleNewChat = () => {
      setMessages([]);
      setInputValue('');
      setIsTyping(false);
      setHasMessages(false);
    };
    
    // Store the function globally for the context to call
    (window as any).triggerNewChat = handleNewChat;
    
    return () => {
      delete (window as any).triggerNewChat;
    };
  }, [setHasMessages]);
  
  // Update hasMessages when messages change
  useEffect(() => {
    setHasMessages(messages.length > 0);
  }, [messages, setHasMessages]);
  
  // Template responses removed - now using GENIUS AI for ALL messages!
  
  const handleSendMessage = async (message: string, fileId?: string) => {
    if (!message.trim() || isTyping) return;
    
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
          user_id: 'user-' + Date.now(),
          file_id: fileId
        });
        
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
        setIsTyping(false);
      } else {
        // ALWAYS call the real API for ALL messages - No more mock responses!
        const response = await chatService.sendMessage({
          message: message.trim(),
          user_id: 'user-' + Date.now()
        });
        
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
        setIsTyping(false);
      }
    } catch (error) {
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
        setIsTyping(false);
      }, 3200);
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
        {hasMessages ? (
          // Conversation Layout (Input at Bottom)
          <ConversationLayout 
            messages={messages}
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            typingStage={typingStage}
          />
        ) : (
          // Welcome Layout (Input Centered)
          <WelcomeLayout
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
          />
        )}
      </div>
    </div>
  );
};

export default ClaudeChatArea; 