// 🚀 FIXED API SERVICE - Uses Smart AI System
import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 🔧 FIXED: Added missing api instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatResponse {
  response: string;
  language?: 'turkish' | 'english';
  user_id?: string;
  conversation_turn?: number;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  user_id: string;
  file_id?: string | null;
}

export interface FileUploadResponse {
  success: boolean;
  analysis_completed?: boolean;
  dataset_loaded?: boolean;
  charts_generated?: number;
  response: string;
  processing_time?: number;
  session_id?: string;
  file_id?: string;
  filename?: string;
  size?: number;
  type?: string;
  message?: string;
}

// ENHANCED CHAT FUNCTION THAT USES NEW SMART AI
export const sendChatMessage = async (message: string, userId: string, fileId?: string): Promise<ChatResponse> => {
  try {
    // Debug: Sending message to Smart AI
    
    const response = await fetch(`${API_BASE}/api/v1/ai/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        user_id: userId || `user_${Date.now()}`,
        file_id: fileId || null
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    // Debug: Smart AI response received
    
    return {
      response: data.response,
      language: data.language || 'english',
      user_id: data.user_id,
      conversation_turn: data.conversation_turn || 1,
      timestamp: data.timestamp || new Date().toISOString()
    };
  } catch (error) {
    console.error('❌ Chat API error:', error);
    throw error;
  }
};

// Chat Service (backward compatibility)
export const chatService = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    return sendChatMessage(request.message, request.user_id, request.file_id);
  },

  sendSimpleMessage: async (message: string, fileId?: string): Promise<ChatResponse> => {
    return sendChatMessage(message, 'web_user', fileId);
  },

  clearDataContext: async (userId?: string): Promise<any> => {
    const response = await api.post('/ai/clear-data-context', {
      message: '',
      user_id: userId || 'web_user'
    });
    return response.data;
  }
};

// Expert Data Scientist Service
export const expertService = {
  runExpertAnalysis: async (fileId: string, userId?: string): Promise<ChatResponse> => {
    const response = await api.post('/expert-analysis', {
      file_id: fileId,
      user_id: userId || 'web_user'
    });
    return response.data;
  },

  askExpertQuestion: async (message: string, fileId?: string): Promise<ChatResponse> => {
    // Use the regular chat endpoint but with expert keywords to trigger expert mode
    const expertMessage = `🔬 EXPERT MODE: ${message}`;
    const backendRequest = {
      message: expertMessage,
      user_id: 'web_user',
      file_id: fileId || undefined
    };

    const response = await api.post('/ai/chat', backendRequest);
    return response.data;
  },
};

// Enhanced File Service with Comprehensive Analysis
export const fileService = {
  uploadFile: async (file: File): Promise<FileUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    // CLEAR OLD DATA CONTEXT before uploading new file
    try {
      // Clearing old data context before upload
      await chatService.clearDataContext();
    } catch (clearError) {
      console.warn('⚠️ Could not clear old context:', clearError);
      // Continue with upload even if context clearing fails
    }

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // NEW: Comprehensive file upload and analysis
  uploadAndAnalyzeFile: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);

    // CLEAR OLD DATA CONTEXT before comprehensive analysis
    try {
      // Clearing old data context before comprehensive analysis
      await chatService.clearDataContext();
    } catch (clearError) {
      console.warn('⚠️ Could not clear old context:', clearError);
      // Continue with analysis even if context clearing fails
    }

    // Uploading to comprehensive DataSoph AI analysis
    
    const response = await api.post('/v2/datasoph/analyze-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // NEW: Get available charts
  getAvailableCharts: async (): Promise<string[]> => {
    try {
      // Check common chart names that are generated
      const chartNames = [
        'correlation_heatmap.png',
        'distributions.png',
        'boxplots.png',
        'missing_values_analysis.png',
        'outlier_analysis.png',
        'business_revenue_by_date.png',
        'business_revenue_by_product_category.png',
        'business_revenue_by_region.png',
        'timeseries_date_analysis.png'
      ];
      
      // Generate chart URLs
      const chartUrls = chartNames.map(name => 
        `${API_BASE}/static/figures/${name}`
      );
      
      console.log('📈 Chart URLs generated:', chartUrls.length);
      
      return chartUrls;
    } catch (error) {
      console.error('❌ Error getting charts:', error);
      return [];
    }
  },

  // NEW: Get analysis report
  getAnalysisReport: async (): Promise<string | null> => {
    try {
      const response = await fetch(`${API_BASE}/static/reports/REPORT.md`);
      if (response.ok) {
        return await response.text();
      }
      return null;
    } catch (error) {
      console.error('❌ Error getting report:', error);
      return null;
    }
  }
};

// RESET CONVERSATION
export const resetConversation = async (userId: string): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE}/api/v1/ai/reset-conversation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: '',
        user_id: userId
      }),
    });

    const data = await response.json();
    return data.success || false;
  } catch (error) {
    console.error('❌ Reset conversation error:', error);
    return false;
  }
};

// TEST LANGUAGE DETECTION
export const testLanguageDetection = async (message: string, userId: string): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE}/api/v1/ai/test-language`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        user_id: userId
      }),
    });

    return await response.json();
  } catch (error) {
    console.error('❌ Language test error:', error);
    return null;
  }
};

const apiService = {
  sendChatMessage,
  uploadAndAnalyzeFile: fileService.uploadAndAnalyzeFile,
  getGeneratedCharts: fileService.getAvailableCharts,
  resetConversation,
  testLanguageDetection
};

export default apiService; 