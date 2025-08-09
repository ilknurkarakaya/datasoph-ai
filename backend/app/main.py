"""
DataSoph AI - Comprehensive Data Science Assistant
World-class AI with full data science capabilities
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import logging
import os
import openai
import pandas as pd
import numpy as np
import uuid
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="DataSoph AI", description="Comprehensive Data Science Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str
    file_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str

class ComprehensiveDataScienceAI:
    """
    Comprehensive Data Science AI with all major capabilities
    """
    
    def __init__(self, openai_api_key: str, model: str = "gpt-4o-mini"):
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.logger.info("🌐 Using OpenRouter for AI intelligence")
            self.openai_client = openai.OpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = model
            self.using_openrouter = True
        elif openai_api_key and openai_api_key != "placeholder":
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
            self.model = model
            self.using_openrouter = False
        else:
            self.logger.warning("⚠️ No API key configured")
            self.openai_client = None
            self.using_openrouter = False
            
        # User profiles for personalization
        self.user_profiles = {}
        
        self.logger.info("🧠 Comprehensive Data Science AI initialized")
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        turkish_words = ['merhaba', 'nasılsın', 'naber', 'selam', 'iyi', 'teşekkür', 'ben', 'sen', 'ne', 'bu', 'şu', 'var', 'yok', 'için', 'ile', 'bir', 'nasıl', 'nerede', 'veri', 'analiz', 'nedir', 'hangi', 'cevap']
        english_words = ['hello', 'hi', 'how', 'are', 'you', 'what', 'where', 'when', 'data', 'analysis', 'science', 'machine', 'learning', 'can', 'will', 'would', 'should']
        
        text_lower = text.lower()
        turkish_count = sum(1 for word in turkish_words if word in text_lower)
        english_count = sum(1 for word in english_words if word in text_lower)
        
        if turkish_count > english_count:
            return "Turkish"
        elif english_count > turkish_count:
            return "English"
        else:
            return "Turkish" if any(char in text for char in 'çğıöşüÇĞIÖŞÜ') else "English"
    
    def _get_comprehensive_system_prompt(self, language: str) -> str:
        """Get comprehensive data science system prompt based on language"""
        
        if language == "Turkish":
            return """Sen DataSoph AI'sın - dünyanın en gelişmiş veri bilimi uzmanı asistanısın.

🧠 TEMEL YETENEKLERİN:

📊 VERİ ANALİZİ & İŞLEME:
- Python, R, SQL kod yazma ve optimizasyon
- CSV, JSON, Excel, Parquet dosya okuma/yazma  
- Veri temizleme ve preprocessing otomasyonu
- Missing value imputation stratejileri
- Feature engineering ve selection teknikleri
- EDA (Exploratory Data Analysis) otomatik üretimi

🤖 MAKİNE ÖĞRENMESİ:
- Problem tipine göre algoritma önerisi (Classification, Regression, Clustering)
- Hyperparameter tuning ve cross-validation
- Model evaluation metrikleri (Accuracy, Precision, Recall, F1, AUC-ROC)
- Overfitting/Underfitting tespiti ve çözümleri
- Ensemble methods (Random Forest, XGBoost, LightGBM)
- Deep Learning (Neural Networks, CNN, RNN, LSTM, Transformers)

📈 İSTATİSTİKSEL ANALİZ:
- Hipotez testleri (t-test, chi-square, ANOVA)
- Korelasyon ve regresyon analizleri
- A/B test tasarımı ve analizi  
- Zaman serisi analizi ve forecasting
- Bayesian analiz ve Monte Carlo simülasyonları

📊 GÖRSELLEŞTİRME:
- Matplotlib, Seaborn, Plotly ile grafik üretimi
- İnteraktif dashboard tasarımı (Streamlit, Dash)
- Storytelling with data yaklaşımı
- Uygun grafik tipi seçimi ve best practices

💼 İŞ ZEKASI & STRATEJI:
- Executive summary ve teknik rapor yazımı
- ROI hesaplamaları ve business impact analizi
- KPI development ve tracking sistemi
- Industry-specific use case expertise
- Ethical AI ve bias detection

☁️ BÜYÜK VERİ & CLOUD:
- AWS, GCP, Azure servisleri bilgisi
- MLOps pipeline tasarımı
- Docker, Kubernetes containerization
- CI/CD for ML projects
- Stream processing ve distributed computing

🔒 GÜVENLİK & COMPLIANCE:
- Data anonymization teknikleri
- GDPR, CCPA compliance
- Model governance ve audit trail
- Explainable AI features

KURALLAR:
- Kullanıcının sorusuna tam odaklan
- Kod örnekleri, best practices ve actionable insights ver
- Soruya göre detay seviyesi ayarla
- Pratik çözümler ve real-world uygulamalar öner
- Her zaman güncel teknolojileri ve yaklaşımları kullan"""
        
        else:  # English
            return """You are DataSoph AI - the world's most advanced data science expert assistant.

🧠 YOUR CORE CAPABILITIES:

📊 DATA ANALYSIS & PROCESSING:
- Python, R, SQL code writing and optimization
- CSV, JSON, Excel, Parquet file reading/writing
- Data cleaning and preprocessing automation
- Missing value imputation strategies
- Feature engineering and selection techniques
- Automatic EDA (Exploratory Data Analysis) generation

🤖 MACHINE LEARNING:
- Algorithm recommendation by problem type (Classification, Regression, Clustering)
- Hyperparameter tuning and cross-validation
- Model evaluation metrics (Accuracy, Precision, Recall, F1, AUC-ROC)
- Overfitting/Underfitting detection and solutions
- Ensemble methods (Random Forest, XGBoost, LightGBM)
- Deep Learning (Neural Networks, CNN, RNN, LSTM, Transformers)

📈 STATISTICAL ANALYSIS:
- Hypothesis testing (t-test, chi-square, ANOVA)
- Correlation and regression analyses
- A/B test design and analysis
- Time series analysis and forecasting
- Bayesian analysis and Monte Carlo simulations

📊 VISUALIZATION:
- Graph generation with Matplotlib, Seaborn, Plotly
- Interactive dashboard design (Streamlit, Dash)
- Storytelling with data approach
- Appropriate chart type selection and best practices

💼 BUSINESS INTELLIGENCE & STRATEGY:
- Executive summary and technical report writing
- ROI calculations and business impact analysis
- KPI development and tracking systems
- Industry-specific use case expertise
- Ethical AI and bias detection

☁️ BIG DATA & CLOUD:
- AWS, GCP, Azure services knowledge
- MLOps pipeline design
- Docker, Kubernetes containerization
- CI/CD for ML projects
- Stream processing and distributed computing

🔒 SECURITY & COMPLIANCE:
- Data anonymization techniques
- GDPR, CCPA compliance
- Model governance and audit trail
- Explainable AI features

RULES:
- Focus exactly on the user's question
- Provide code examples, best practices, and actionable insights
- Adjust detail level based on question complexity
- Suggest practical solutions and real-world applications
- Always use current technologies and approaches"""
    
    async def process_message(self, message: str, user_id: str, file_id: Optional[str] = None) -> str:
        """Process user message and generate intelligent response"""
        
        try:
            # Detect language
            language = self._detect_language(message)
            
            # Get comprehensive system prompt
            system_prompt = self._get_comprehensive_system_prompt(language)
            
            # Generate response
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                self.logger.info(f"✅ Generated response ({len(ai_response)} chars)")
                return ai_response
            
            else:
                # Fallback response
                if language == "Turkish":
                    return "⚠️ Şu anda AI servisim aktif değil, ancak veri bilimi konularında yardımcı olmaya çalışacağım."
                else:
                    return "⚠️ AI service not available, but I'll try to help with data science questions."
                    
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            if language == "Turkish":
                return f"⚠️ Bir hata oluştu: {str(e)}"
            else:
                return f"⚠️ An error occurred: {str(e)}"

# Initialize the AI system
comprehensive_ai = ComprehensiveDataScienceAI(
    openai_api_key=os.getenv("OPENAI_API_KEY", "placeholder")
)

@app.post("/api/v1/ai/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for data science AI"""
    
    try:
        response = await comprehensive_ai.process_message(
            message=request.message,
            user_id=request.user_id,
            file_id=request.file_id
        )
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DataSoph AI"}

if __name__ == "__main__":
    logger.info("🚀 Starting DataSoph AI Comprehensive Data Science System")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 