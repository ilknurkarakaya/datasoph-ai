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
import sys
import io
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from dotenv import load_dotenv
from contextlib import redirect_stdout, redirect_stderr

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

🔥 ÖNEMLİ: OTOMATIK KOD ÇALIŞTIRMA YETENEĞİN VAR!

📝 CEVAP FORMATIN:
1. Soruyu anla ve açıkla
2. Python kodu yaz (```python ve ``` arasında)
3. Kod otomatik çalışacak ve sonuçları göreceksin
4. Sonuçları analiz et ve kullanıcıya açıkla
5. İç görüler ve öneriler ver

🎯 ÖRNEKLERİN:
- Veri analizi iste → Kodu yaz, çalıştır, sonuçları açıkla
- Grafik iste → Visualization kodu yaz, oluştur, yorumla  
- Model iste → ML kodu yaz, train et, performance göster
- İstatistik iste → Hesaplama kodu yaz, çalıştır, sonucu açıkla

💡 HER ZAMAN:
- Kullanıcıya önce ne yapacağını açıkla
- Kodu yaz ve çalıştır  
- Sonuçları detaylı yorumla
- Pratik öneriler ver
- Sade ve anlaşılır dil kullan

Kısa, öz ve pratik cevaplar ver. Kullanıcı veri bilimi bilmese bile anlayacak şekilde açıkla."""
        
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

🔥 IMPORTANT: YOU HAVE AUTOMATIC CODE EXECUTION CAPABILITY!

📝 YOUR RESPONSE FORMAT:
1. Understand and explain the question clearly
2. Write comprehensive Python code (between ```python and ```)
3. Execute code automatically and capture all outputs
4. Analyze results deeply with statistical insights
5. Provide actionable recommendations and next steps

🎯 DATA SCIENTIST CAPABILITIES:
- Automatic EDA with statistical summaries
- Model selection and hyperparameter optimization
- Feature engineering and selection
- Data visualization with interpretation
- Statistical hypothesis testing
- Time series analysis and forecasting
- Deep learning model architecture design
- Business insights and ROI analysis

💡 INTELLIGENT EXECUTION:
- Run code automatically and capture outputs
- Show plots, tables, and statistical results
- Interpret findings like a senior data scientist
- Suggest improvements and next steps
- Handle errors intelligently
- Generate publication-ready insights

🔬 ANALYSIS DEPTH:
- Always perform statistical significance tests
- Provide confidence intervals and p-values
- Explain practical significance vs statistical significance
- Suggest business actions based on findings
- Identify potential biases and limitations

Give comprehensive, actionable insights that a human data scientist would provide.

RULES:
- Write code that produces tangible results
- Always interpret outputs statistically
- Provide business recommendations
- Show your work step by step
- Handle data quality issues automatically"""
    
    async def process_message(self, message: str, user_id: str, file_id: Optional[str] = None) -> str:
        """Process user message and generate intelligent response"""
        
        try:
            # Detect language
            language = self._detect_language(message)
            
            # Get comprehensive system prompt
            system_prompt = self._get_comprehensive_system_prompt(language)
            
            # Add file analysis if file_id provided
            file_analysis = ""
            if file_id:
                file_analysis = self._analyze_uploaded_file(file_id)
            
            # Prepare enhanced message with file context
            enhanced_message = message
            if file_analysis:
                if language == "Turkish":
                    enhanced_message = f"""KULLANICI MESAJI: {message}

YÜKLENEN DOSYA ANALİZİ:
{file_analysis}

Bu dosya analizi bilgilerini kullanarak kullanıcının sorusuna detaylı ve akıllı bir cevap ver."""
                else:
                    enhanced_message = f"""USER MESSAGE: {message}

UPLOADED FILE ANALYSIS:
{file_analysis}

Use this file analysis information to provide a detailed and intelligent answer to the user's question."""
            
            # Generate response
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": enhanced_message}
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                self.logger.info(f"✅ Generated response ({len(ai_response)} chars)")
                
                # Execute any Python code in the response
                if "```python" in ai_response:
                    code_blocks = self._extract_python_code(ai_response)
                    file_data = None
                    
                    # Get file data if available
                    if file_id:
                        file_data = self._get_file_data(file_id)
                    
                    executed_results = []
                    for code in code_blocks:
                        result = self._execute_python_code(code, file_data)
                        executed_results.append(result)
                    
                    # Add execution results to response
                    if executed_results:
                        ai_response = self._add_execution_results(ai_response, executed_results, language)
                
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

    def _analyze_uploaded_file(self, file_id: str) -> str:
        """Analyze uploaded file and return insights"""
        try:
            # Find the file
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            if not matching_files:
                return "❌ File not found"
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            filename = matching_files[0]
            
            # Basic file info
            file_size = os.path.getsize(file_path)
            
            analysis_results = []
            analysis_results.append(f"📁 File: {filename}")
            analysis_results.append(f"📏 Size: {file_size:,} bytes")
            
            # Try to analyze based on file type
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
                analysis_results.append(f"📊 Rows: {len(df):,}")
                analysis_results.append(f"📊 Columns: {len(df.columns)}")
                analysis_results.append(f"📊 Column Names: {', '.join(df.columns[:10])}" + ("..." if len(df.columns) > 10 else ""))
                
                # Data types
                analysis_results.append(f"📊 Data Types: {df.dtypes.value_counts().to_dict()}")
                
                # Missing values
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    analysis_results.append(f"⚠️ Missing Values: {missing[missing > 0].to_dict()}")
                
                # Basic statistics for numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    analysis_results.append(f"📈 Numeric Columns: {', '.join(numeric_cols[:5])}" + ("..." if len(numeric_cols) > 5 else ""))
            
            elif filename.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
                analysis_results.append(f"📊 Rows: {len(df):,}")
                analysis_results.append(f"📊 Columns: {len(df.columns)}")
                analysis_results.append(f"📊 Column Names: {', '.join(df.columns[:10])}" + ("..." if len(df.columns) > 10 else ""))
            
            elif filename.lower().endswith('.json'):
                with open(file_path, 'r') as f:
                    data = pd.read_json(f)
                    analysis_results.append(f"📊 JSON records: {len(data)}")
                    if hasattr(data, 'columns'):
                        analysis_results.append(f"📊 Fields: {', '.join(data.columns[:10])}" + ("..." if len(data.columns) > 10 else ""))
            
            return "\\n".join(analysis_results)
            
        except Exception as e:
            return f"❌ File analysis error: {str(e)}"

    def _execute_python_code(self, code: str, file_data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Execute Python code safely and return results"""
        try:
            # Create a safe execution environment
            safe_globals = {
                'pd': pd,
                'np': np,
                'plt': plt,
                'sns': sns,
                'print': print,
                '__builtins__': {
                    '__import__': __import__,
                    'len': len,
                    'range': range,
                    'list': list,
                    'dict': dict,
                    'str': str,
                    'int': int,
                    'float': float,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'round': round
                },
                'len': len,
                'range': range,
                'list': list,
                'dict': dict,
                'str': str,
                'int': int,
                'float': float,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round
            }
            
            # Add file data to globals if provided
            if file_data is not None:
                safe_globals['df'] = file_data
                safe_globals['data'] = file_data
            
            # Capture output
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            # Execute code and capture output
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                # If this is a single expression, evaluate and capture result
                lines = code.strip().split('\n')
                if len(lines) == 1 and not any(keyword in lines[0] for keyword in ['import', 'def', 'class', 'for', 'while', 'if', 'try']):
                    # Single expression - evaluate and capture result
                    try:
                        result = eval(lines[0], safe_globals)
                        if result is not None:
                            print(result)
                    except:
                        # If eval fails, execute as statement
                        exec(code, safe_globals)
                else:
                    # Multi-line or statement - execute normally
                    exec(code, safe_globals)
            
            # Get results
            stdout_output = output_buffer.getvalue()
            stderr_output = error_buffer.getvalue()
            
            # Extract any created variables
            results = {}
            for key, value in safe_globals.items():
                if not key.startswith('_') and key not in ['pd', 'np', 'plt', 'sns', 'print', 'len', 'range', 'list', 'dict', 'str', 'int', 'float', 'sum', 'max', 'min', 'abs', 'round']:
                    if isinstance(value, (str, int, float, bool)):
                        results[key] = value
                    elif isinstance(value, list) and len(value) <= 10:  # Only small lists
                        results[key] = value
                    elif isinstance(value, dict) and len(value) <= 5:  # Only small dicts
                        results[key] = value
                    elif hasattr(value, 'shape') and hasattr(value, 'dtypes'):  # pandas DataFrame
                        results[key] = f"DataFrame({value.shape[0]} rows, {value.shape[1]} columns)"
                    elif hasattr(value, 'shape') and not hasattr(value, 'dtypes'):  # numpy array
                        results[key] = f"Array{value.shape}"
                    elif hasattr(value, 'dtype'):  # pandas Series
                        results[key] = f"Series(length={len(value)})"
                    else:
                        # For other objects, just show type and basic info
                        results[key] = f"{type(value).__name__} object"
        
            return {
                'success': True,
                'output': stdout_output,
                'error': stderr_output,
                'results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'results': {}
            }
    
    def _extract_python_code(self, text: str) -> list:
        """Extract Python code blocks from text"""
        import re
        pattern = r'```python\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches]
    
    def _get_file_data(self, file_id: str) -> Optional[pd.DataFrame]:
        """Get file data as DataFrame for code execution"""
        try:
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            if not matching_files:
                return None
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            filename = matching_files[0]
            
            if filename.lower().endswith('.csv'):
                return pd.read_csv(file_path)
            elif filename.lower().endswith(('.xlsx', '.xls')):
                return pd.read_excel(file_path)
            elif filename.lower().endswith('.json'):
                return pd.read_json(file_path)
            
            return None
        except Exception as e:
            self.logger.error(f"Error loading file data: {e}")
            return None
    
    def _add_execution_results(self, response: str, results: list, language: str) -> str:
        """Add code execution results to the AI response"""
        if language == "Turkish":
            execution_header = "\n\n🔥 **KOD ÇALIŞTIRMA SONUÇLARI:**\n"
        else:
            execution_header = "\n\n🔥 **CODE EXECUTION RESULTS:**\n"
        
        execution_text = execution_header
        
        for i, result in enumerate(results, 1):
            if result['success']:
                if language == "Turkish":
                    execution_text += f"\n**Kod Bloğu {i} - Başarılı ✅**\n"
                else:
                    execution_text += f"\n**Code Block {i} - Success ✅**\n"
                
                if result['output']:
                    execution_text += f"```\n{result['output']}\n```\n"
                
                if result['results']:
                    if language == "Turkish":
                        execution_text += "**Oluşturulan Değişkenler:**\n"
                    else:
                        execution_text += "**Created Variables:**\n"
                    
                    for key, value in result['results'].items():
                        execution_text += f"- `{key}`: {value}\n"
            else:
                if language == "Turkish":
                    execution_text += f"\n**Kod Bloğu {i} - Hata ❌**\n"
                    execution_text += f"```\n{result['error']}\n```\n"
                else:
                    execution_text += f"\n**Code Block {i} - Error ❌**\n"
                    execution_text += f"```\n{result['error']}\n```\n"
        
        return response + execution_text

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

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str

@app.post("/api/v1/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process data files"""
    
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'txt'
        stored_filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, stored_filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"📁 File uploaded: {file.filename} -> {file_id}")
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            message=f"File {file.filename} uploaded successfully. You can now ask questions about this data."
        )
        
    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 Starting DataSoph AI Comprehensive Data Science System")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # DISABLED: Sürekli restart'ı durdur
        log_level="info"
    ) 