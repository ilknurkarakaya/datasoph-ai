"""
DataSoph AI - Enhanced Data Science Assistant
World-class AI with comprehensive data science knowledge and user-controlled file analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
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

# Import our working services only
from .services.conversation_manager import AdvancedConversationManager, IntentCategory
# from .services.secure_executor import SecureCodeExecutor  # Disabled for stability
from .services.data_science_engine import ComprehensiveDataScienceEngine
from .services.advanced_file_processor import AdvancedFileProcessor
from .services.business_intelligence import BusinessIntelligenceEngine, BusinessDomain
from .services.memory_system import ConversationMemory, MemoryType, ContextImportance

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="DataSoph AI", description="Enhanced Data Science Assistant")

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

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str
    size: Optional[int] = None
    type: Optional[str] = None

class FileAnalysisRequest(BaseModel):
    file_id: str
    user_id: Optional[str] = None

class FileContextManager:
    """Manages file context and user sessions"""
    
    def __init__(self):
        self.user_file_sessions: Dict[str, List[Dict]] = {}
        
    def register_file_for_user(self, user_id: str, file_id: str, filename: str) -> None:
        """Register that a user has uploaded a specific file"""
        if user_id not in self.user_file_sessions:
            self.user_file_sessions[user_id] = []
        
        self.user_file_sessions[user_id].append({
            "file_id": file_id,
            "filename": filename,
            "upload_time": datetime.now(),
            "analysis_done": False
        })
        logger.info(f"📁 File registered for user {user_id}: {filename} -> {file_id}")
    
    def get_user_files(self, user_id: str) -> List[Dict]:
        """Get all files for a specific user"""
        return self.user_file_sessions.get(user_id, [])
    
    def get_latest_file(self, user_id: str) -> Optional[Dict]:
        """Get the most recently uploaded file for user"""
        files = self.get_user_files(user_id)
        logger.info(f"🔍 Getting latest file for user {user_id}, found {len(files)} files")
        if files:
            logger.info(f"📄 Latest file: {files[-1]}")
        return files[-1] if files else None
    
    def mark_file_analyzed(self, user_id: str, file_id: str) -> None:
        """Mark a file as analyzed"""
        user_files = self.get_user_files(user_id)
        for file_info in user_files:
            if file_info["file_id"] == file_id:
                file_info["analysis_done"] = True
                break

class EnhancedConversationManager:
    """Enhanced conversation management with warmth and encouragement"""
    
    def __init__(self):
        self.conversation_starters = {
            "Turkish": [
                "Harika bir soru! 😊",
                "Çok güzel bir yaklaşım düşünmüşsün!",
                "Bu konuda sana yardımcı olmaktan memnuniyet duyarım!",
                "Veri biliminde bu gerçekten önemli bir konu!",
                "Birlikte bu problemi çözelim! 🚀",
                "Mükemmel! Bu tam benim uzmanlık alanım! ✨",
                "Bu soruya bayıldım! 💡"
            ],
            "English": [
                "That's a fantastic question! 😊",
                "I love this approach you're thinking about!",
                "I'm excited to help you with this!",
                "This is such an important aspect of data science!",
                "Let's dive into this together! 🚀",
                "Perfect! This is exactly my area of expertise! ✨",
                "I'm thrilled to work on this with you! 💡"
            ]
        }
        
        self.closings = {
            "Turkish": [
                "\n\n💡 Başka sorularını merakla bekliyorum!",
                "\n\nBu konuda daha derinlemesine gitmek istersen, her zaman buradayım! 😊",
                "\n\nUmarım bu açıklama faydalı olmuştur. Başka ne öğrenmek istersin?",
                "\n\n🚀 Veri bilimi yolculuğunda seni desteklemeye devam edeceğim!",
                "\n\n✨ Bu analizi geliştirmek için başka fikirlerim de var!"
            ],
            "English": [
                "\n\n💡 I'm here for any follow-up questions you might have!",
                "\n\nFeel free to ask if you'd like to dive deeper into any of this! 😊",
                "\n\nI hope this helps! What would you like to explore next?",
                "\n\n🚀 I'm excited to continue supporting your data science journey!",
                "\n\n✨ I have more ideas to enhance this analysis if you're interested!"
            ]
        }
    
    def add_warmth_to_response(self, response: str, language: str) -> str:
        """Add human warmth and encouragement to technical responses"""
        import random
        
        starters = self.conversation_starters[language]
        starter = random.choice(starters)
        
        closings = self.closings[language]
        closing = random.choice(closings)
        
        return f"{starter}\n\n{response}{closing}"

class ComprehensiveDataScienceAI:
    """Enhanced DataSoph AI with world-class data science knowledge"""
    
    def __init__(self, openai_api_key: str):
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.logger.info("🌐 Using OpenRouter for AI intelligence")
            self.openai_client = openai.OpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
        elif openai_api_key and openai_api_key != "placeholder":
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None
        
        # Initialize enhanced components
        self.conversation_manager = AdvancedConversationManager()
        self.enhanced_conversation = EnhancedConversationManager()
        self.file_manager = FileContextManager()
        self.data_science_engine = ComprehensiveDataScienceEngine()
        self.file_processor = AdvancedFileProcessor()
        self.business_intelligence = BusinessIntelligenceEngine()
        self.memory_system = ConversationMemory()
        
        # Enhanced model selection for different tasks
        self.model_config = {
            "casual": "anthropic/claude-3.5-haiku",
            "technical": "anthropic/claude-3.5-sonnet",
            "coding": "anthropic/claude-3.5-sonnet",
            "analysis": "openai/gpt-4o-mini"
        }
        
        self.logger.info("🚀 Enhanced DataSoph AI with world-class knowledge initialized!")

    async def process_message(self, message: str, user_id: str, file_id: Optional[str] = None) -> str:
        """Process message with enhanced AI capabilities and file context awareness"""
        
        try:
            # Detect intent and language
            intent, language, confidence = self.conversation_manager.detect_intent_and_language(message, user_id)
            context = self.conversation_manager.get_or_create_context(user_id)
            
            self.logger.info(f"🎯 Intent: {intent.value}, Language: {language}, Confidence: {confidence:.2f}")
            
            # Check if user has uploaded files recently (file context awareness)
            if not file_id:
                latest_file = self.file_manager.get_latest_file(user_id)
                if latest_file:
                    file_id = latest_file["file_id"]
                    self.logger.info(f"🔗 Using latest uploaded file: {latest_file['filename']}")
            
            # Enhanced response for casual chat
            if intent == IntentCategory.GREETING and len(message.split()) <= 3 and not file_id:
                return self._generate_enhanced_greeting(language)
            
            # File analysis if provided
            file_analysis = ""
            if file_id:
                file_analysis = await self._analyze_file_advanced(file_id, language)
            
            # Select optimal model
            model = self._select_optimal_model(intent, file_id is not None)
            
            # Generate comprehensive system prompt with world-class knowledge
            system_prompt = self._get_comprehensive_system_prompt(language, intent, file_analysis)
            
            # Create enhanced message
            enhanced_message = self._create_enhanced_message(message, file_analysis, language, intent)
            
            # Generate AI response
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": enhanced_message}
                    ],
                    max_tokens=2500,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                
                # Add warmth and encouragement to the response
                ai_response = self.enhanced_conversation.add_warmth_to_response(ai_response, language)
                
                # Store in memory
                self.memory_system.maintain_context(user_id, {
                    'message': message,
                    'response': ai_response,
                    'intent': intent.value,
                    'language': language,
                    'file_id': file_id,
                    'timestamp': datetime.now().isoformat()
                })
                
                return ai_response
            
            else:
                return self._generate_fallback_response(message, language)
                
        except Exception as e:
            self.logger.error(f"❌ Error: {e}")
            if language == "Turkish":
                return "⚠️ Bir hata oluştu, ancak size yardımcı olmaya devam edeceğim. Lütfen tekrar deneyin."
            else:
                return "⚠️ An error occurred, but I'll continue helping you. Please try again."

    async def analyze_file_completely(self, file_id: str, user_id: str = "default_user") -> str:
        """Comprehensive file analysis for immediate analysis requests"""
        try:
            # Mark file as being analyzed
            self.file_manager.mark_file_analyzed(user_id, file_id)
            
            file_data = self._get_file_data(file_id)
            if file_data is None:
                return "Sorry, I couldn't access the file for analysis. Please try uploading it again."
            
            # Detect language preference
            language = "English"  # Default, could be enhanced with user preference detection
            
            # Generate comprehensive analysis
            system_prompt = self._get_comprehensive_system_prompt(language, IntentCategory.DATA_ANALYSIS, "")
            
            analysis_request = f"""Please provide a comprehensive analysis of this dataset:

Dataset Overview:
- Shape: {file_data.shape[0]:,} rows × {file_data.shape[1]} columns
- Columns: {list(file_data.columns)}
- Data types: {dict(file_data.dtypes)}
- Missing values: {file_data.isnull().sum().to_dict()}

Sample data (first 5 rows):
{file_data.head().to_string()}

Statistical summary:
{file_data.describe().to_string()}

Please provide:
1. Data quality assessment
2. Key insights and patterns
3. Recommendations for analysis
4. Suggested next steps
5. Business value potential
6. Python code examples for further exploration"""
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model_config["technical"],
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": analysis_request}
                    ],
                    max_tokens=3000,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                return self.enhanced_conversation.add_warmth_to_response(ai_response, language)
            else:
                return self._generate_fallback_analysis_response(file_data, language)
                
        except Exception as e:
            self.logger.error(f"❌ File analysis error: {e}")
            return "I encountered an error while analyzing your file. Please try again or upload a different file."

    def _get_comprehensive_system_prompt(self, language: str, intent: IntentCategory, file_analysis: str) -> str:
        """Enhanced system prompt with world-class data science knowledge"""
        
        if language == "Turkish":
            base_prompt = """Sen DataSoph AI'sın - dünyanın en gelişmiş, en bilgili ve en kibar veri bilimi uzmanısın.

🧠 SENİN KAPSAMLI BİLGİN:

📊 VERİ BİLİMİ UZMANI:
- İstatistik: Bayesian inference, frequentist methods, hypothesis testing, A/B testing, causal inference, survival analysis
- Machine Learning: Supervised/unsupervised learning, deep learning, reinforcement learning, AutoML, few-shot learning
- Algoritmalar: Classical ML (SVM, Random Forest, XGBoost, LightGBM, CatBoost), neural networks (CNN, RNN, LSTM, Transformers, GANs, VAEs)
- Feature Engineering: Advanced selection techniques, automated feature creation, interaction terms, polynomial features
- Model Evaluation: Advanced cross-validation, Bayesian optimization, model interpretation (SHAP, LIME, permutation importance, anchor explanations)

🛠️ TEKNİK ARAÇLAR USTASI:
- Programming: Python (pandas, numpy, scikit-learn, tensorflow, pytorch, jax), R, SQL, Scala, Julia
- Visualization: Matplotlib, Seaborn, Plotly, D3.js, Bokeh, Altair, Tableau, PowerBI
- Big Data: Hadoop, Spark, Kafka, Flink, distributed computing, data lakes
- Cloud Platforms: AWS (SageMaker, S3, EMR), GCP (BigQuery, Vertex AI), Azure ML, Databricks
- MLOps: Docker, Kubernetes, Kubeflow, MLflow, DVC, CI/CD pipelines, model monitoring

💼 İŞ ANLAYIŞI:
- Industry Applications: Healthcare, finance, retail, manufacturing, tech, energy, telecommunications
- Business Metrics: ROI, customer lifetime value, churn prediction, price optimization, demand forecasting
- Strategic Planning: Data strategy, team building, technology roadmaps, budget planning
- Ethics & Governance: Bias detection, fairness metrics, privacy-preserving ML, GDPR compliance

🎯 MODERN TRENDS:
- Generative AI: Large language models, diffusion models, prompt engineering, fine-tuning
- MLOps: Model versioning, automated retraining, drift detection, A/B testing for ML
- Explainable AI: Interpretable models, counterfactual explanations, regulatory compliance
- Edge Computing: Mobile ML, federated learning, on-device inference
- Advanced Analytics: Graph neural networks, time series forecasting, causal ML, meta-learning

💡 KİŞİLİK VE YAKLAŞIM:
- Son derece kibar, sabırlı ve destekleyici
- Karmaşık konuları basit terimlerle açıklayabilen
- Practical örnekler veren, actionable insights sunan
- Hem technical hem business perspektifi birleştiren
- Sürekli öğrenmeyi teşvik eden, meraklı ve ilham verici
- Hatalardan öğrenmeyi normal karşılayan, yapıcı
- Her seviyedeki kullanıcıya uyum sağlayabilen (beginner to expert)

🗣️ KONUŞMA STİLİN:
- Sıcak ve samimi ama profesyonel
- Açık ve anlaşılır açıklamalar
- Örneklerle desteklenen teorik bilgi
- Adım adım rehberlik
- Cesaretlendirici ve motivasyonlu
- Soru sormaya teşvik edici
- "Birlikte keşfedelim" yaklaşımı

🔥 ÖNEMLİ: Her zaman executable Python kodu yaz ve sonuçları yorumla!

Her soruya şu yaklaşımla yanıt ver:
1. Sorunu anlayıp empati kurun
2. Açık ve dostane bir açıklama yap
3. Pratik kod örnekleri ver
4. Sonuçları business value ile bağla
5. Sonraki adımları öner
6. Öğrenmeye teşvik et

Sen sadece bir AI değil, güvenilir bir veri bilimi mentörüsün! ❤️"""
        
        else:  # English
            base_prompt = """You are DataSoph AI - the world's most advanced, knowledgeable, and genuinely caring data science expert.

🧠 YOUR COMPREHENSIVE EXPERTISE:

📊 DATA SCIENCE MASTERY:
- Statistics: Bayesian inference, frequentist methods, hypothesis testing, A/B testing, causal inference, survival analysis
- Machine Learning: Supervised/unsupervised learning, deep learning, reinforcement learning, AutoML, few-shot learning
- Algorithms: Classical ML (SVM, Random Forest, XGBoost, LightGBM, CatBoost), neural networks (CNN, RNN, LSTM, Transformers, GANs, VAEs)
- Feature Engineering: Advanced selection techniques, automated feature creation, interaction terms, polynomial features
- Model Evaluation: Advanced cross-validation, Bayesian optimization, model interpretation (SHAP, LIME, permutation importance, anchor explanations)

🛠️ TECHNICAL MASTERY:
- Programming: Python (pandas, numpy, scikit-learn, tensorflow, pytorch, jax), R, SQL, Scala, Julia
- Visualization: Matplotlib, Seaborn, Plotly, D3.js, Bokeh, Altair, Tableau, PowerBI
- Big Data: Hadoop, Spark, Kafka, Flink, distributed computing, data lakes
- Cloud Platforms: AWS (SageMaker, S3, EMR), GCP (BigQuery, Vertex AI), Azure ML, Databricks
- MLOps: Docker, Kubernetes, Kubeflow, MLflow, DVC, CI/CD pipelines, model monitoring

💼 BUSINESS INTELLIGENCE:
- Industry Applications: Healthcare, finance, retail, manufacturing, tech, energy, telecommunications
- Business Metrics: ROI, customer lifetime value, churn prediction, price optimization, demand forecasting
- Strategic Planning: Data strategy, team building, technology roadmaps, budget planning
- Ethics & Governance: Bias detection, fairness metrics, privacy-preserving ML, GDPR compliance

🎯 CUTTING-EDGE KNOWLEDGE:
- Generative AI: Large language models, diffusion models, prompt engineering, fine-tuning
- MLOps: Model versioning, automated retraining, drift detection, A/B testing for ML
- Explainable AI: Interpretable models, counterfactual explanations, regulatory compliance
- Edge Computing: Mobile ML, federated learning, on-device inference
- Advanced Analytics: Graph neural networks, time series forecasting, causal ML, meta-learning

💡 PERSONALITY & APPROACH:
- Exceptionally kind, patient, and supportive
- Able to explain complex concepts in simple, relatable terms
- Provides practical examples and actionable insights
- Combines technical depth with business perspective
- Encourages continuous learning and curiosity
- Treats mistakes as learning opportunities
- Adapts to all skill levels (beginner to expert)

🗣️ COMMUNICATION STYLE:
- Warm and friendly yet professional
- Clear and engaging explanations
- Theory supported by practical examples
- Step-by-step guidance when needed
- Encouraging and motivational
- Promotes asking questions
- "Let's explore this together" approach

🔥 CRITICAL: Always write executable Python code and interpret results!

Approach every question with:
1. Understanding and empathy for the user's situation
2. Clear, friendly explanations
3. Practical code examples that work
4. Connection to business value
5. Suggestions for next steps
6. Encouragement for continued learning

You're not just an AI - you're a trusted data science mentor who genuinely cares about helping people succeed! ❤️"""

        # Add file analysis if available
        if file_analysis:
            if language == "Turkish":
                base_prompt += f"\n\n📊 **MEVCUT VERİ SETİ ANALİZİ:**\n{file_analysis}\n\n🚨 ÖNEMLİ: Bu gerçek veri setini kullan! Mock data oluşturma, yukarıdaki veri analizi sonuçlarını kullan!"
            else:
                base_prompt += f"\n\n📊 **CURRENT DATASET ANALYSIS:**\n{file_analysis}\n\n🚨 IMPORTANT: Use this real dataset! Don't create mock data, use the analysis results above!"

        return base_prompt

    def _generate_enhanced_greeting(self, language: str) -> str:
        """Generate enhanced greeting response"""
        if language == "Turkish":
            return """🌟 **Merhaba! DataSoph AI'ya hoş geldiniz!**

Ben dünyanın en gelişmiş veri bilimi asistanıyım ve sizinle çalışmaktan çok heyecanlıyım! 🚀

🎯 **Yeteneklerim:**
• 📊 Kapsamlı veri analizi ve EDA
• 🤖 Makine öğrenmesi model geliştirme  
• 📈 İleri seviye görselleştirmeler
• 💼 İş zekası ve ROI analizi
• 🔍 İstatistiksel analiz ve hipotez testleri
• 💻 Otomatik kod üretimi ve çalıştırma
• 🎨 Gelişmiş model interpretability
• 🌐 Modern MLOps ve deployment stratejileri

💡 **Nasıl yardımcı olabilirim?**
- Veri dosyanızı yükleyin (CSV, Excel, JSON destekleniyor)
- Veri bilimi sorunuzu sorun
- İstatistiksel analiz konularında rehberlik isteyin
- ML model önerileri için danışın

Birlikte harika şeyler başaracağız! ✨"""
        else:
            return """🌟 **Hello! Welcome to DataSoph AI!**

I'm the world's most advanced data science assistant, and I'm absolutely thrilled to work with you! 🚀

🎯 **My Capabilities:**
• 📊 Comprehensive data analysis and EDA
• 🤖 Machine learning model development
• 📈 Advanced visualizations
• 💼 Business intelligence and ROI analysis  
• 🔍 Statistical analysis and hypothesis testing
• 💻 Automatic code generation and execution
• 🎨 Advanced model interpretability
• 🌐 Modern MLOps and deployment strategies

💡 **How can I help you today?**
- Upload your data file (CSV, Excel, JSON supported)
- Ask your data science questions
- Get guidance on statistical analysis
- Consult on ML model recommendations

Let's create something amazing together! ✨"""

    def _select_optimal_model(self, intent: IntentCategory, has_file: bool) -> str:
        """Select optimal model based on context"""
        if has_file or intent == IntentCategory.DATA_ANALYSIS:
            return self.model_config["technical"]
        elif intent in [IntentCategory.GREETING, IntentCategory.CASUAL_CHAT]:
            return self.model_config["casual"]
        else:
            return self.model_config["analysis"]

    def _create_enhanced_message(self, message: str, file_analysis: str, language: str, intent: IntentCategory) -> str:
        """Create enhanced message with context"""
        
        enhanced_parts = [f"KULLANICI MESAJI: {message}" if language == "Turkish" else f"USER MESSAGE: {message}"]
        
        if file_analysis:
            enhanced_parts.append(file_analysis)
        
        if language == "Turkish":
            enhanced_parts.append("BEKLENEN YAKLAŞIM: Uzman seviyesinde analiz, pratik öneriler, kod örnekleri ve iş değeri perspektifi")
        else:
            enhanced_parts.append("EXPECTED APPROACH: Expert-level analysis, practical recommendations, code examples and business value perspective")
        
        return "\n\n".join(enhanced_parts)

    async def _analyze_file_advanced(self, file_id: str, language: str) -> str:
        """Enhanced file analysis with actual content"""
        try:
            self.logger.info(f"🔬 Starting enhanced file analysis for: {file_id}")
            file_data = self._get_file_data(file_id)
            if file_data is None:
                self.logger.warning(f"❌ No file data found for: {file_id}")
                return ""
            
            self.logger.info(f"📊 File data loaded successfully: {file_data.shape}")
            
            if language == "Turkish":
                analysis = f"""📊 VERİ SETİ DETAYLI ANALİZİ:

🔍 GENEL BİLGİLER:
• Boyut: {file_data.shape[0]:,} satır × {file_data.shape[1]} sütun
• Eksik değer: {file_data.isnull().sum().sum()} adet
• Sayısal sütun: {len(file_data.select_dtypes(include=[np.number]).columns)}
• Kategorik sütun: {len(file_data.select_dtypes(include=['object']).columns)}

📋 SÜTUN İSİMLERİ:
{', '.join(file_data.columns.tolist())}

📈 İLK 5 SATIR:
{file_data.head().to_string()}

📊 SAYISAL İSTATİSTİKLER:
{file_data.describe().to_string()}

🏷️ VERİ TİPLERİ:
{file_data.dtypes.to_string()}"""

                # Eksik değerler varsa detayını ekle
                if file_data.isnull().sum().sum() > 0:
                    analysis += f"\n\n❌ EKSİK DEĞER DETAYI:\n{file_data.isnull().sum().to_string()}"
                
                # Kategorik sütunlar varsa dağılımlarını ekle
                categorical_cols = file_data.select_dtypes(include=['object']).columns
                if len(categorical_cols) > 0:
                    analysis += "\n\n🏷️ KATEGORİK SÜTUN DAĞILIMLARI:"
                    for col in categorical_cols:
                        analysis += f"\n\n{col}:\n{file_data[col].value_counts().to_string()}"
                        
            else:  # English
                analysis = f"""📊 COMPREHENSIVE DATASET ANALYSIS:

🔍 OVERVIEW:
• Shape: {file_data.shape[0]:,} rows × {file_data.shape[1]} columns  
• Missing values: {file_data.isnull().sum().sum()} total
• Numerical columns: {len(file_data.select_dtypes(include=[np.number]).columns)}
• Categorical columns: {len(file_data.select_dtypes(include=['object']).columns)}

📋 COLUMN NAMES:
{', '.join(file_data.columns.tolist())}

📈 FIRST 5 ROWS:
{file_data.head().to_string()}

📊 NUMERICAL STATISTICS:
{file_data.describe().to_string()}

🏷️ DATA TYPES:
{file_data.dtypes.to_string()}"""

                # Add missing values detail if any
                if file_data.isnull().sum().sum() > 0:
                    analysis += f"\n\n❌ MISSING VALUES DETAIL:\n{file_data.isnull().sum().to_string()}"
                
                # Add categorical distributions if any
                categorical_cols = file_data.select_dtypes(include=['object']).columns
                if len(categorical_cols) > 0:
                    analysis += "\n\n🏷️ CATEGORICAL DISTRIBUTIONS:"
                    for col in categorical_cols:
                        analysis += f"\n\n{col}:\n{file_data[col].value_counts().to_string()}"
            
            self.logger.info(f"✅ Enhanced file analysis completed: {len(analysis)} characters")
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ File analysis error: {e}")
            return ""

    async def _execute_and_enhance_response(self, response: str, file_id: str, language: str) -> str:
        """Execute code and enhance response"""
        
        import re
        code_blocks = re.findall(r'```python\n(.*?)```', response, re.DOTALL)
        
        if not code_blocks:
            return response
        
        # Prepare execution context
        data_context = {}
        if file_id:
            file_data = self._get_file_data(file_id)
            if file_data is not None:
                data_context = {'df': file_data, 'data': file_data}
        
        # Execute code blocks
        execution_results = []
        for code in code_blocks:
            result = self.secure_executor.execute_code_safely(code.strip(), data_context)
            execution_results.append(result)
        
        # Add results to response
        if execution_results:
            if language == "Turkish":
                response += "\n\n🔥 **KOD ÇALIŞTIRMA SONUÇLARI:**\n"
            else:
                response += "\n\n🔥 **CODE EXECUTION RESULTS:**\n"
            
            for i, result in enumerate(execution_results, 1):
                if result['success']:
                    if language == "Turkish":
                        response += f"\n**✅ Kod Bloğu {i} - Başarıyla Çalıştırıldı**\n"
                    else:
                        response += f"\n**✅ Code Block {i} - Successfully Executed**\n"
                    
                    if result['output']:
                        response += f"```\n{result['output']}\n```\n"
                else:
                    if language == "Turkish":
                        response += f"\n**❌ Kod Bloğu {i} - Hata:** {result['error']}\n"
                    else:
                        response += f"\n**❌ Code Block {i} - Error:** {result['error']}\n"
        
        return response

    def _generate_fallback_response(self, message: str, language: str) -> str:
        """Generate fallback response when AI is not available"""
        if language == "Turkish":
            return """⚠️ AI servisim şu anda aktif değil, ancak DataSoph AI yetenekleri:

📊 **Veri Analizi:**
• Otomatik EDA ve veri kalitesi değerlendirmesi
• İstatistiksel analiz ve hipotez testleri
• Gelişmiş görselleştirmeler

🤖 **Makine Öğrenmesi:**
• Otomatik model seçimi ve hyperparameter tuning
• Cross-validation ve performance evaluation
• Feature engineering önerileri

💼 **İş Zekası:**
• ROI hesaplamaları ve iş etkisi analizi
• Executive summary ve actionable insights

Lütfen sorunuzu tekrar sorun veya bir veri dosyası yükleyin."""
        else:
            return """⚠️ AI service not currently active, but DataSoph AI capabilities include:

📊 **Data Analysis:**
• Automated EDA and data quality assessment
• Statistical analysis and hypothesis testing
• Advanced visualizations

🤖 **Machine Learning:**
• Automatic model selection and hyperparameter tuning
• Cross-validation and performance evaluation
• Feature engineering recommendations

💼 **Business Intelligence:**
• ROI calculations and business impact analysis
• Executive summaries and actionable insights

Please restate your question or upload a data file."""

    def _detect_language(self, text: str) -> str:
        """Detect language"""
        turkish_words = ['merhaba', 'nasılsın', 'naber', 'selam', 'veri', 'analiz', 'nedir', 'nasıl']
        english_words = ['hello', 'hi', 'how', 'data', 'analysis', 'what', 'can', 'help']
        
        text_lower = text.lower()
        turkish_count = sum(1 for word in turkish_words if word in text_lower)
        english_count = sum(1 for word in english_words if word in text_lower)
        
        return "Turkish" if turkish_count >= english_count else "English"

    def _get_file_data(self, file_id: str) -> Optional[pd.DataFrame]:
        """Get file data"""
        try:
            self.logger.info(f"🔍 Looking for file with ID: {file_id}")
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            self.logger.info(f"📁 Found matching files: {matching_files}")
            
            if not matching_files:
                self.logger.warning(f"❌ No files found for ID: {file_id}")
                return None
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            filename = matching_files[0]
            self.logger.info(f"📄 Reading file: {filename} from {file_path}")
            
            if filename.lower().endswith('.csv'):
                data = pd.read_csv(file_path)
                self.logger.info(f"📊 CSV data shape: {data.shape}")
                self.logger.info(f"📋 CSV columns: {list(data.columns)}")
                return data
            elif filename.lower().endswith(('.xlsx', '.xls')):
                data = pd.read_excel(file_path)
                self.logger.info(f"📊 Excel data shape: {data.shape}")
                return data
            elif filename.lower().endswith('.json'):
                data = pd.read_json(file_path)
                self.logger.info(f"📊 JSON data shape: {data.shape}")
                return data
            
            self.logger.warning(f"❌ Unsupported file type: {filename}")
            return None
        except Exception as e:
            self.logger.error(f"❌ File reading error: {e}")
            return None

    def _generate_fallback_response(self, message: str, language: str) -> str:
        """Generate fallback response when AI is not available"""
        if language == "Turkish":
            return """⚠️ AI servisim şu anda aktif değil, ancak DataSoph AI yetenekleri:

📊 **Veri Analizi:**
• Otomatik EDA ve veri kalitesi değerlendirmesi
• İstatistiksel analiz ve hipotez testleri
• Gelişmiş görselleştirmeler

🤖 **Makine Öğrenmesi:**
• Otomatik model seçimi ve hyperparameter tuning
• Cross-validation ve performance evaluation
• Feature engineering önerileri

💼 **İş Zekası:**
• ROI hesaplamaları ve iş etkisi analizi
• Executive summary ve actionable insights

Lütfen sorunuzu tekrar sorun veya bir veri dosyası yükleyin."""
        else:
            return """⚠️ AI service not currently active, but DataSoph AI capabilities include:

📊 **Data Analysis:**
• Automated EDA and data quality assessment
• Statistical analysis and hypothesis testing
• Advanced visualizations

🤖 **Machine Learning:**
• Automatic model selection and hyperparameter tuning
• Cross-validation and performance evaluation
• Feature engineering recommendations

💼 **Business Intelligence:**
• ROI calculations and business impact analysis
• Executive summaries and actionable insights

Please restate your question or upload a data file."""

    def _generate_fallback_analysis_response(self, file_data: pd.DataFrame, language: str) -> str:
        """Generate fallback analysis when AI is not available"""
        if language == "Turkish":
            return f"""📊 **Veri Seti Analizi (Fallback Modu)**

**Temel İstatistikler:**
- Satır sayısı: {file_data.shape[0]:,}
- Sütun sayısı: {file_data.shape[1]}
- Eksik değer: {file_data.isnull().sum().sum()}
- Sayısal sütunlar: {len(file_data.select_dtypes(include=[np.number]).columns)}
- Kategorik sütunlar: {len(file_data.select_dtypes(include=['object']).columns)}

**Sütunlar:** {', '.join(file_data.columns.tolist())}

Bu dosya başarıyla yüklendi! AI servisi aktif olduğunda daha detaylı analiz yapabilirim."""
        else:
            return f"""📊 **Dataset Analysis (Fallback Mode)**

**Basic Statistics:**
- Rows: {file_data.shape[0]:,}
- Columns: {file_data.shape[1]}
- Missing values: {file_data.isnull().sum().sum()}
- Numerical columns: {len(file_data.select_dtypes(include=[np.number]).columns)}
- Categorical columns: {len(file_data.select_dtypes(include=['object']).columns)}

**Columns:** {', '.join(file_data.columns.tolist())}

Your file has been successfully uploaded! I can provide more detailed analysis when AI service is active."""

# Initialize the AI system
enhanced_ai = ComprehensiveDataScienceAI(
    openai_api_key=os.getenv("OPENAI_API_KEY", "placeholder")
)

@app.post("/api/v1/ai/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Enhanced chat endpoint"""
    try:
        response = await enhanced_ai.process_message(
            message=request.message,
            user_id=request.user_id,
            file_id=request.file_id
        )
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "service": "DataSoph AI - Enhanced System"}

@app.post("/api/v1/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and store file - NO automatic analysis"""
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
        
        # Register file for user session (using default user for now)
        user_id = "web_user"  # Could be passed as parameter in future
        enhanced_ai.file_manager.register_file_for_user(user_id, file_id, file.filename)
        
        logger.info(f"📁 File uploaded: {file.filename} -> {file_id}")
        
        # ONLY return upload confirmation - NO AI analysis yet
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            message=f"✅ File '{file.filename}' uploaded successfully. You can now ask questions about this data or click 'Analyze File' to get automatic insights.",
            size=file.size,
            type=file.content_type
        )
        
    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/v1/analyze-file")
async def analyze_file_immediately(request: FileAnalysisRequest):
    """Trigger immediate analysis of uploaded file"""
    try:
        user_id = request.user_id or "web_user"
        analysis_result = await enhanced_ai.analyze_file_completely(request.file_id, user_id)
        return ChatResponse(
            response=analysis_result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"❌ File analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced DataSoph AI")
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=False,
        log_level="info"
    ) 