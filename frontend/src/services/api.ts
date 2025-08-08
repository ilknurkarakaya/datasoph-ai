import axios from 'axios';
import { ChatRequest, ChatResponse, FileUploadResponse } from '../types/chat';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat Service
export const chatService = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat', request);
    return response.data;
  },

  sendSimpleMessage: async (message: string, fileId?: string): Promise<ChatResponse> => {
    const request: ChatRequest = {
      message,
      user_id: 'default_user',
      ...(fileId && { file_id: fileId }),
    };

    const response = await api.post('/chat', request);
    return response.data;
  },
};

// File Service
export const fileService = {
  uploadFile: async (file: File): Promise<FileUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  getFileInfo: async (fileId: string) => {
    const response = await api.get(`/data/${fileId}/info`);
    return response.data;
  },

  getFileColumns: async (fileId: string) => {
    const response = await api.get(`/data/${fileId}/columns`);
    return response.data;
  },

  getCleaningCode: async (fileId: string) => {
    const response = await api.get(`/data/${fileId}/clean-code`);
    return response.data;
  },
};

// Data Visualization Service
export const visualizationService = {
  createDashboard: async (fileId: string) => {
    const response = await api.post('/visualize', {
      file_id: fileId,
      chart_type: 'dashboard'
    });
    return response.data;
  },

  createCustomChart: async (fileId: string, chartConfig: {
    chart_type: string;
    x_column?: string;
    y_column?: string;
    color_column?: string;
    title?: string;
  }) => {
    const response = await api.post('/visualize', {
      file_id: fileId,
      ...chartConfig
    });
    return response.data;
  },
};

// Data Quality Service
export const dataQualityService = {
  assessQuality: async (fileId: string, generateCode: boolean = false) => {
    const response = await api.post('/data-quality', {
      file_id: fileId,
      generate_code: generateCode
    });
    return response.data;
  },
};

// Machine Learning Service
export const mlService = {
  analyzeMLPotential: async (fileId: string) => {
    const response = await api.post('/ml/analyze', {
      file_id: fileId
    });
    return response.data;
  },

  trainModel: async (fileId: string, config: {
    target_column: string;
    model_type?: string;
    task_type?: string;
    test_size?: number;
    cross_validation?: boolean;
  }) => {
    const response = await api.post('/ml/train', {
      file_id: fileId,
      ...config
    });
    return response.data;
  },

  makePredictions: async (modelId: string, fileId: string) => {
    const response = await api.post('/ml/predict', {
      model_id: modelId,
      file_id: fileId
    });
    return response.data;
  },

  listModels: async () => {
    const response = await api.get('/ml/models');
    return response.data;
  },

  getModelInfo: async (modelId: string) => {
    const response = await api.get(`/ml/models/${modelId}`);
    return response.data;
  },
};

// System Service
export const systemService = {
  getHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  getSystemInfo: async () => {
    const response = await api.get('/');
    return response.data;
  },
};

// Chat history management (localStorage for now)
export const chatHistoryService = {
  getChats: async () => {
    return [];
  },
  
  createChat: async (title: string) => {
    return { id: Date.now().toString(), title };
  },
  
  deleteChat: async (chatId: string) => {
    return { success: true };
  },
  
  getChat: async (chatId: string) => {
    return null;
  },
  
  updateChat: async (chatId: string, messages: any[]) => {
    return { success: true };
  },
};

export default api; 