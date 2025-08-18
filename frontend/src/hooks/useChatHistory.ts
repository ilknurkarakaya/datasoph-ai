import { useState, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ChatHistory, Message } from '../types/chat.ts';

const STORAGE_KEY = 'datasoph-chats';

export const useChatHistory = () => {
  const [chats, setChats] = useState<ChatHistory[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    const savedChats = localStorage.getItem(STORAGE_KEY);
    if (savedChats) {
      try {
        const parsedChats = JSON.parse(savedChats).map((chat: any) => ({
          ...chat,
          createdAt: new Date(chat.createdAt),
          lastUpdated: new Date(chat.lastUpdated),
          messages: chat.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }))
        }));
        setChats(parsedChats);
        
        // Set the most recent chat as current if no current chat
        if (parsedChats.length > 0 && !currentChatId) {
          setCurrentChatId(parsedChats[0].id);
        }
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    }
  }, [currentChatId]);

  // Save chats to localStorage whenever chats change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
  }, [chats]);

  const createNewChat = useCallback(() => {
    const newChat: ChatHistory = {
      id: uuidv4(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      lastUpdated: new Date()
    };

    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
    return newChat.id;
  }, []);

  const deleteChat = useCallback((chatId: string) => {
    setChats(prev => prev.filter(chat => chat.id !== chatId));
    
    // If deleting current chat, switch to another or create new
    if (currentChatId === chatId) {
      const remainingChats = chats.filter(chat => chat.id !== chatId);
      if (remainingChats.length > 0) {
        setCurrentChatId(remainingChats[0].id);
      } else {
        const newChatId = createNewChat();
        setCurrentChatId(newChatId);
      }
    }
  }, [chats, currentChatId, createNewChat]);

  const renameChat = useCallback((chatId: string, newTitle: string) => {
    if (!newTitle.trim()) {
      return; // Don't allow empty titles
    }

    setChats(prev => prev.map(chat => {
      if (chat.id === chatId) {
        return {
          ...chat,
          title: newTitle.trim(),
          lastUpdated: new Date()
        };
      }
      return chat;
    }));
  }, []);

  const addMessageToChat = useCallback((chatId: string, message: Message) => {
    setChats(prev => prev.map(chat => {
      if (chat.id === chatId) {
        const updatedMessages = [...chat.messages, message];
        
        // Update title based on first user message if still "New Chat"
        let title = chat.title;
        if (title === 'New Chat' && message.isUser) {
          title = message.content.length > 50 
            ? message.content.substring(0, 50) + '...'
            : message.content;
        }

        return {
          ...chat,
          title,
          messages: updatedMessages,
          lastUpdated: new Date()
        };
      }
      return chat;
    }));
  }, []);

  const updateChatMessages = useCallback((chatId: string, messages: Message[]) => {
    setChats(prev => prev.map(chat => {
      if (chat.id === chatId) {
        // Update title based on first user message if still "New Chat"
        let title = chat.title;
        if (title === 'New Chat' && messages.length > 0) {
          const firstUserMessage = messages.find(msg => msg.isUser);
          if (firstUserMessage) {
            title = firstUserMessage.content.length > 50 
              ? firstUserMessage.content.substring(0, 50) + '...'
              : firstUserMessage.content;
          }
        }

        return {
          ...chat,
          title,
          messages,
          lastUpdated: new Date()
        };
      }
      return chat;
    }));
  }, []);

  const getCurrentChat = useCallback(() => {
    return chats.find(chat => chat.id === currentChatId) || null;
  }, [chats, currentChatId]);

  const switchToChat = useCallback((chatId: string) => {
    setCurrentChatId(chatId);
  }, []);

  return {
    chats,
    currentChatId,
    currentChat: getCurrentChat(),
    createNewChat,
    deleteChat,
    renameChat,
    addMessageToChat,
    updateChatMessages,
    switchToChat,
  };
}; 