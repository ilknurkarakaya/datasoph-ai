export interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isTyping?: boolean;
  fileAttachment?: FileAttachment;
}

export interface FileAttachment {
  id: string;
  name: string;  // Changed from filename to name for consistency
  filename: string;
  size: number;
  type: string;
  url?: string;
  uploadedAt: string;  // Add upload timestamp
  analysisData?: any;  // Store comprehensive analysis results
}

export interface ChatHistory {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  lastUpdated: Date;
}

export interface ChatRequest {
  message: string;
  user_id?: string;
  file_id?: string;
  context?: string;
}

export interface ChatResponse {
  response: string;
  status?: string;
  timestamp: string;
}

export interface ApiError {
  message: string;
  status: number;
}

export interface FileUploadResponse {
  file_id: string;
  filename: string;
  size?: number;
  type?: string;
  message: string;
}

export interface UploadedFileInfo {
  file_id: string;
  filename: string;
  uploaded_at: string;
  analysis_done: boolean;
  size?: number;
}

// New types for DataSoph AI features
export interface DataQualityResponse {
  status: string;
  overall_score: number;
  issues: Array<{
    type: string;
    severity: string;
    description: string;
    column?: string;
  }>;
  recommendations: string[];
  cleaning_code?: string;
  message: string;
}

export interface VisualizationResponse {
  status: string;
  visualizations: Array<{
    id: string;
    title: string;
    type: string;
    plotly_json?: any;
  }>;
  message: string;
}

export interface MLAnalysisResponse {
  status: string;
  message: string;
  data: {
    data_summary: any;
    ml_recommendations: Array<{
      type: string;
      description: string;
      methods?: string[];
      use_cases?: string[];
    }>;
    suggested_targets: Array<{
      column: string;
      task_type: string;
      reason: string;
      confidence: string;
    }>;
    preprocessing_needed: Array<{
      type: string;
      description: string;
      priority: string;
    }>;
    model_suggestions: any;
  };
} 