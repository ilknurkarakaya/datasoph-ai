import { useState, useCallback } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  id: string;
}

interface FileAnalysisResult {
  status: string;
  analysis: any;
  type: string;
}

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Generate unique user ID for session persistence
  const generateUserId = useCallback(() => {
    let userId = localStorage.getItem('datasoph_user_id');
    if (!userId) {
      userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('datasoph_user_id', userId);
    }
    return userId;
  }, []);

  const addMessage = useCallback((message: Omit<Message, 'timestamp' | 'id'>) => {
    const newMessage: Message = {
      ...message,
      timestamp: new Date(),
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9)
    };
    setMessages(prev => [...prev, newMessage]);
  }, []);

  // 🔧 CHAT ONLY - No file processing
  const sendChatMessage = useCallback(async (content: string) => {
    // Add user message
    addMessage({ role: 'user', content });
    
    setIsLoading(true);
    try {
      const userId = generateUserId();
      
      console.log('🗨️ Sending CHAT message (no files):', content);
      
      const response = await axios.post('/api/v1/ai/chat', {
        message: content,
        user_id: userId
      });
      
      // Add assistant response
      addMessage({ 
        role: 'assistant', 
        content: response.data.response 
      });
      
      console.log('✅ Chat response received');
      
    } catch (error) {
      console.error('❌ Chat error:', error);
      addMessage({ 
        role: 'assistant', 
        content: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin. / Sorry, an error occurred. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  }, [addMessage, generateUserId]);

  // 🔧 FILE ANALYSIS ONLY - Separate from chat
  const analyzeFile = useCallback(async (file: File): Promise<FileAnalysisResult | null> => {
    try {
      console.log('📊 Starting FILE ANALYSIS (not chat):', file.name);
      
      const formData = new FormData();
      formData.append('files', file);
      
      const response = await axios.post('/api/v2/datasoph/analyze-file', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      console.log('✅ File analysis completed');
      return response.data;
      
    } catch (error) {
      console.error('❌ File analysis error:', error);
      
      // Fallback to basic upload if comprehensive analysis fails
      try {
        console.log('⚠️ Falling back to basic upload...');
        const formData = new FormData();
        formData.append('file', file);
        
        const fallbackResponse = await axios.post('/api/v1/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        return {
          status: 'basic_upload',
          analysis: fallbackResponse.data,
          type: 'file_upload'
        };
        
      } catch (fallbackError) {
        console.error('❌ Basic upload also failed:', fallbackError);
        return null;
      }
    }
  }, []);

  // Combined handler for messages with or without files
  const handleSubmit = useCallback(async (
    message: string, 
    files?: File[]
  ): Promise<{ type: 'chat' | 'file_analysis', data?: any }> => {
    
    if (files && files.length > 0) {
      // FILE ANALYSIS ROUTE - No chat message
      console.log('🔀 Routing to FILE ANALYSIS');
      const analysisResult = await analyzeFile(files[0]);
      return { 
        type: 'file_analysis', 
        data: analysisResult 
      };
      
    } else if (message.trim()) {
      // CHAT ONLY ROUTE - No files
      console.log('🔀 Routing to CHAT');
      await sendChatMessage(message);
      return { type: 'chat' };
      
    } else {
      console.log('⚠️ No message or files provided');
      return { type: 'chat' };
    }
  }, [sendChatMessage, analyzeFile]);

  const clearChat = useCallback(() => {
    setMessages([]);
    localStorage.removeItem('datasoph_user_id');
    console.log('🔄 Chat cleared and session reset');
  }, []);

  // Reset conversation on server
  const resetConversation = useCallback(async () => {
    try {
      const userId = generateUserId();
      await axios.post('/api/v1/ai/reset-conversation', {
        message: '',
        user_id: userId
      });
      
      clearChat();
      console.log('🔄 Server conversation reset');
      
    } catch (error) {
      console.error('❌ Reset conversation error:', error);
      // Clear local anyway
      clearChat();
    }
  }, [generateUserId, clearChat]);

  return {
    messages,
    isLoading,
    sendChatMessage,
    analyzeFile,
    handleSubmit,
    clearChat,
    resetConversation,
    addMessage
  };
}; 