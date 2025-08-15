"""
DataSoph AI - Enhanced Data Science Assistant
World-class AI with comprehensive data science knowledge and user-controlled file analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import uvicorn
import logging
import os
import openai
import pandas as pd
import numpy as np
import uuid
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our working services only
from app.services.conversation_manager import AdvancedConversationManager, IntentCategory
# from app.services.secure_executor import SecureCodeExecutor  # Disabled for stability
from app.services.data_science_engine import ComprehensiveDataScienceEngine
from app.services.advanced_file_processor import AdvancedFileProcessor
from app.services.universal_file_handler import UniversalFileHandler
from app.services.ocr_processor import OCRProcessor
from app.services.business_intelligence import BusinessIntelligenceEngine, BusinessDomain
from app.services.memory_system import ConversationMemory, MemoryType, ContextImportance
from app.services.expert_data_scientist import ExpertDataAnalyzer, DataScienceConversationAI, get_expert_analyzer, get_conversation_ai

# Import new comprehensive DataSoph AI system
from app.services.datasoph_ai_main import DataSophAI
from app.services.safety_guardrails import PIIDetector, StatisticalGuardrails, ErrorResilienceManager

# Import Smart Response Generator for brilliant multilingual conversations
from app.services.smart_response_generator import smart_response_generator

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

# Serve generated charts and reports
from fastapi.staticfiles import StaticFiles
import os

# 🔧 FIXED: Proper static file serving
import os
from pathlib import Path

# Get absolute paths to static directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
figures_dir = BASE_DIR / "figures"
reports_dir = BASE_DIR / "reports" 
exports_dir = BASE_DIR / "exports"

# Create directories if they don't exist
figures_dir.mkdir(exist_ok=True)
reports_dir.mkdir(exist_ok=True)
exports_dir.mkdir(exist_ok=True)

# Mount static file directories with absolute paths
app.mount("/static/figures", StaticFiles(directory=str(figures_dir)), name="figures")
app.mount("/static/reports", StaticFiles(directory=str(reports_dir)), name="reports")
app.mount("/static/exports", StaticFiles(directory=str(exports_dir)), name="exports")

logger.info(f"📁 Static directories mounted:")
logger.info(f"  - Figures: {figures_dir}")
logger.info(f"  - Reports: {reports_dir}")
logger.info(f"  - Exports: {exports_dir}")

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
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
        """Register that a user has uploaded a specific file and clear old context"""
        # CLEAR OLD DATA: Reset user's file sessions to prevent confusion with old data
        if user_id in self.user_file_sessions and len(self.user_file_sessions[user_id]) > 0:
            old_count = len(self.user_file_sessions[user_id])
            logger.info(f"🔄 Clearing {old_count} old file(s) for user {user_id} to prevent data confusion")
        
        # Initialize fresh session for this user
        self.user_file_sessions[user_id] = []
        
        self.user_file_sessions[user_id].append({
            "file_id": file_id,
            "filename": filename,
            "upload_time": datetime.now(),
            "analysis_done": False
        })
        logger.info(f"📁 File registered for user {user_id}: {filename} -> {file_id} (fresh context)")
    
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
        self.universal_file_handler = UniversalFileHandler()
        
        # Initialize Expert Data Scientist AI
        self.expert_analyzer = get_expert_analyzer()
        self.expert_conversation_ai = get_conversation_ai()
        
        # Check OCR availability for enhanced prompts
        self.ocr_available = hasattr(self.universal_file_handler, 'ocr_available') and self.universal_file_handler.ocr_available
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
                
                # If file analysis is empty, try to read from generated EDA report
                if not file_analysis:
                    try:
                        report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "REPORT.md")
                        summary_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "summary.json")
                        
                        if os.path.exists(report_path):
                            with open(report_path, 'r', encoding='utf-8') as f:
                                report_content = f.read()
                            
                            if os.path.exists(summary_path):
                                with open(summary_path, 'r', encoding='utf-8') as f:
                                    summary_data = json.load(f)
                                
                                if language == "Turkish":
                                    file_analysis = f"""📊 **OTOMATIK EDA ANALİZ SONUÇLARI**

🔍 **VERİ SETİ ÖZETİ:**
• Boyut: {summary_data.get('dataset_shape', {}).get('rows', 'N/A')} satır × {summary_data.get('dataset_shape', {}).get('columns', 'N/A')} sütun
• Eksik değerli sütunlar: {len(summary_data.get('top_missing_columns', []))}
• Oluşturulan grafik sayısı: {summary_data.get('figures_generated', 0)}

📈 **ÖNE ÇIKAN KORELASYONLAR:**
{chr(10).join([f"• {corr['column1']} vs {corr['column2']}: {corr['correlation']:.3f}" for corr in summary_data.get('top_correlations', [])[:3]])}

📄 **DETAYLI RAPOR MEVCUT:** `reports/REPORT.md` dosyasında tam analiz bulunuyor.

💡 **KULLANICININ SORULARINI CEVAPLAYABILIRSIN:** Bu analiz sonuçlarını kullanarak kullanıcının veri hakkındaki sorularını cevaplayabilirsin."""
                                else:
                                    file_analysis = f"""📊 **AUTOMATED EDA ANALYSIS RESULTS**

🔍 **DATASET SUMMARY:**
• Size: {summary_data.get('dataset_shape', {}).get('rows', 'N/A')} rows × {summary_data.get('dataset_shape', {}).get('columns', 'N/A')} columns  
• Columns with missing values: {len(summary_data.get('top_missing_columns', []))}
• Generated visualizations: {summary_data.get('figures_generated', 0)}

📈 **TOP CORRELATIONS:**
{chr(10).join([f"• {corr['column1']} vs {corr['column2']}: {corr['correlation']:.3f}" for corr in summary_data.get('top_correlations', [])[:3]])}

📄 **DETAILED REPORT AVAILABLE:** Full analysis is available in `reports/REPORT.md`.

💡 **YOU CAN ANSWER USER QUESTIONS:** Use these analysis results to answer the user's questions about their data."""
                            
                        self.logger.info(f"📊 Used EDA report as file analysis for file_id: {file_id}")
                    except Exception as e:
                        self.logger.warning(f"⚠️ Could not read EDA report: {e}")
            
            # Select optimal model
            model = self._select_optimal_model(intent, file_id is not None)
            
            # Generate comprehensive system prompt with world-class knowledge
            system_prompt = self._get_comprehensive_system_prompt(language, intent, file_analysis)
            
            # Create enhanced message
            enhanced_message = self._create_enhanced_message(message, file_analysis, language, intent)
            
            # Generate AI response
            if self.openai_client:
                # 🔬 EXPERT DATA SCIENTIST AI MODE
                # Check if we should use Expert AI instead of regular AI
                should_use_expert_ai = (
                    file_analysis or 
                    any(keyword in message.lower() for keyword in [
                        'analiz', 'analyze', 'analysis', 'model', 'veri', 'data', 
                        'grafik', 'chart', 'görselleştir', 'visualize', 'insight',
                        'öneri', 'recommend', 'ml', 'machine learning', 'makine öğrenmesi',
                        'istatistik', 'statistic', 'korelasyon', 'correlation'
                    ])
                )
                
                if should_use_expert_ai:
                    self.logger.info("🔬 Using Expert Data Scientist AI for response")
                    
                    # Try to get existing analysis results if file is available
                    expert_analysis_results = None
                    if file_id:
                        try:
                            expert_results = await self.analyze_file_with_expert_ai(file_id, user_id)
                            if expert_results.get("success", False):
                                expert_analysis_results = expert_results["expert_analysis"]
                        except Exception as e:
                            self.logger.warning(f"Could not get expert analysis: {e}")
                    
                    # Generate expert conversation response
                    expert_response = self.expert_conversation_ai.generate_expert_response(
                        message, expert_analysis_results
                    )
                    
                    # Add expert analysis details if available
                    if expert_analysis_results:
                        if language == "Turkish":
                            enhanced_expert_response = f"""🔬 **EXPERT DATA SCIENTIST ANALYSIS**

{expert_response}

---

📊 **ANALIZ SONUÇLARI:**
• Veri Kalitesi: {expert_analysis_results.get('data_quality', {}).get('quality_score', 'N/A')}/100
• Dataset Boyutu: {expert_analysis_results.get('basic_info', {}).get('shape', ['N/A', 'N/A'])[0]} satır × {expert_analysis_results.get('basic_info', {}).get('shape', ['N/A', 'N/A'])[1]} sütun
• Güçlü Korelasyonlar: {len(expert_analysis_results.get('statistical_analysis', {}).get('correlations', {}).get('high_correlations', []))} adet
• Görselleştirmeler: {len(expert_analysis_results.get('visualizations', {}))} adet oluşturuldu
• İş Önerileri: {len(expert_analysis_results.get('business_insights', []))} actionable insight

💡 **Daha detaylı analiz için '/api/v1/expert-analysis' endpoint'ini kullanabilirsiniz.**"""
                        else:
                            enhanced_expert_response = f"""🔬 **EXPERT DATA SCIENTIST ANALYSIS**

{expert_response}

---

📊 **ANALYSIS RESULTS:**
• Data Quality: {expert_analysis_results.get('data_quality', {}).get('quality_score', 'N/A')}/100
• Dataset Size: {expert_analysis_results.get('basic_info', {}).get('shape', ['N/A', 'N/A'])[0]} rows × {expert_analysis_results.get('basic_info', {}).get('shape', ['N/A', 'N/A'])[1]} columns
• Strong Correlations: {len(expert_analysis_results.get('statistical_analysis', {}).get('correlations', {}).get('high_correlations', []))} found
• Visualizations: {len(expert_analysis_results.get('visualizations', {}))} created
• Business Insights: {len(expert_analysis_results.get('business_insights', []))} actionable recommendations

💡 **For detailed analysis, use '/api/v1/expert-analysis' endpoint.**"""
                        
                        ai_response = enhanced_expert_response
                    else:
                        ai_response = f"🔬 **EXPERT DATA SCIENTIST AI**\n\n{expert_response}"
                
                else:
                    # Regular AI response
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
                
                # FORCE MODE: If AI ignores file context, override with direct analysis
                # 🚨 ULTIMATE FORCE MODE - Check for ANY file-not-found phrases
                force_triggers = [
                    "don't see", "no file", "not uploaded", "attached", "shared", 
                    "i apologize", "csv file", "can't access", "notice i can", 
                    "actually access", "file directly", "please upload", "could you please"
                ]
                should_force = file_analysis and any(trigger in ai_response.lower() for trigger in force_triggers)
                
                if should_force:
                    self.logger.warning("🚨 AI ignored file context - forcing direct analysis")
                    if language == "Turkish":
                        ai_response = f"""🎯 Verilerinizi analiz ettim! İşte bulgularım:

{file_analysis}

Bu analiz gerçek verilerinize dayanmaktadır. Daha detaylı analiz istiyorsanız, spesifik sorular sorabilirsiniz!"""
                    else:
                        ai_response = f"""🎯 I've analyzed your data! Here are my findings:

{file_analysis}

This analysis is based on your actual data. Feel free to ask specific questions for deeper insights!"""
                
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
        """Comprehensive file analysis for immediate analysis requests - supports OCR"""
        try:
            # Mark file as being analyzed
            self.file_manager.mark_file_analyzed(user_id, file_id)
            
            # Find the file path
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            if not matching_files:
                return "Sorry, I couldn't access the file for analysis. Please try uploading it again."
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            
            # Use UniversalFileHandler for comprehensive analysis
            processing_result = self.universal_file_handler.detect_and_process(file_path)
            
            if not processing_result.get('processing_result', {}).get('success', False):
                return "Sorry, there was an error processing your file. Please try uploading it again."
            
            # Detect language preference (could be enhanced with user detection)
            language = "Turkish"  # Set to Turkish as user is Turkish
            
            # Get processing results
            proc_result = processing_result['processing_result']
            file_info = processing_result['file_info']
            
            # Check if this is OCR data (image with text extraction)
            is_ocr_data = 'ocr_analysis' in proc_result
            
            if is_ocr_data:
                # Get OCR analysis results
                ocr_analysis = proc_result['ocr_analysis']
                extracted_text = ocr_analysis.get('extracted_text', '')
                confidence = ocr_analysis.get('confidence_score', 0)
                
                # Check if we have structured data (table)
                structured_data = ocr_analysis.get('structured_data')
                
                if structured_data is not None:
                    # This is structured OCR data (table)
                    analysis_request = f"""Bu OCR ile çıkarılan tablo verisini analiz et:

Tablo Bilgileri:
- Boyut: {structured_data.shape[0]} satır × {structured_data.shape[1]} sütun
- Sütunlar: {list(structured_data.columns)}
- OCR Güven Skoru: {confidence:.1f}%

Veri Örneği:
{structured_data.head().to_string()}

Lütfen şunları analiz et:
1. Tablonun içeriği ve amacı
2. Veri kalitesi ve eksik değerler
3. Önemli trendler ve patterns
4. İş değeri potansiyeli
5. Önerilen analizler
6. Python kod örnekleri"""
                else:
                    # Text-only OCR data
                    analysis_request = f"""Bu OCR ile çıkarılan metni analiz et:

OCR Sonuçları:
- Güven skoru: {confidence:.1f}%
- Metin uzunluğu: {len(extracted_text)} karakter
- Kelime sayısı: {len(extracted_text.split())} kelime

Çıkarılan Metin:
{extracted_text}

Lütfen şunları analiz et:
1. Metnin içeriği ve türü (fatura, tablo, form, vb.)
2. Önemli bilgiler ve sayısal veriler
3. Veri kalitesi değerlendirmesi
4. Potansiyel kullanım alanları
5. Öneriler ve sonraki adımlar
6. Python ile nasıl işlenebileceği"""
            else:
                # Regular file analysis based on format
                file_format = proc_result.get('format', 'unknown')
                
                if file_format in ['csv', 'excel', 'json', 'parquet']:
                    # Structured data analysis
                    if 'sample_data' in proc_result and proc_result['sample_data']:
                        sample_data = proc_result['sample_data'][:5]  # First 5 rows
                        columns = proc_result.get('columns', [])
                        data_shape = proc_result.get('data_shape', [0, 0])
                        
                        analysis_request = f"""Bu veri setini kapsamlı olarak analiz et:

Veri Seti Genel Bilgileri:
- Format: {file_format.upper()}
- Boyut: {data_shape[0]:,} satır × {data_shape[1]} sütun
- Sütunlar: {columns}

Örnek Veriler (ilk 5 satır):
{sample_data}

Lütfen şunları analiz et:
1. Veri kalitesi değerlendirmesi
2. Ana bulgular ve trendler
3. Analiz önerileri
4. Sonraki adımlar
5. İş değeri potansiyeli
6. Python kod örnekleri"""
                
                elif file_format == 'pdf':
                    # PDF document analysis
                    text_content = proc_result.get('text_content', '')
                    page_count = proc_result.get('page_count', 0)
                    tables_found = proc_result.get('tables_found', 0)
                    
                    analysis_request = f"""Bu PDF belgesini analiz et:

PDF Bilgileri:
- Sayfa sayısı: {page_count}
- Bulunan tablo sayısı: {tables_found}
- Metin çıkarma durumu: {'✅ Başarılı' if proc_result.get('text_extracted') else '❌ Başarısız'}

İçerik Örneği:
{text_content[:500]}...

Lütfen şunları analiz et:
1. Belgenin türü ve amacı
2. Önemli bilgi ve veriler
3. Yapısal analiz
4. Potansiyel kullanım alanları
5. Öneriler ve sonraki adımlar"""
                
                elif file_format == 'docx':
                    # Word document analysis
                    sample_text = proc_result.get('sample_text', '')
                    word_count = proc_result.get('word_count', 0)
                    table_count = proc_result.get('table_count', 0)
                    
                    analysis_request = f"""Bu Word belgesini analiz et:

Belge Bilgileri:
- Kelime sayısı: {word_count}
- Tablo sayısı: {table_count}
- Paragraf sayısı: {proc_result.get('paragraph_count', 0)}

İçerik Örneği:
{sample_text}

Lütfen şunları analiz et:
1. Belgenin türü ve amacı
2. Ana içerik ve yapı
3. Önemli bilgiler
4. Potansiyel kullanım alanları
5. Öneriler ve sonraki adımlar"""
                
                else:
                    # Generic file analysis
                    analysis_request = f"""Bu dosyayı analiz et:

Dosya Bilgileri:
- Format: {file_format.upper()}
- Boyut: {file_info.get('size_mb', 0):.2f} MB
- İşleme durumu: {'✅ Başarılı' if proc_result.get('success') else '❌ Başarısız'}

İşleme Sonuçları:
{str(proc_result)[:1000]}

Lütfen bu dosya hakkında genel bir analiz ve değerlendirme yap."""
            
            # Generate comprehensive system prompt
            system_prompt = self._get_comprehensive_system_prompt(language, IntentCategory.DATA_ANALYSIS, "")
            
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
                
                # Combine with OCR technical analysis if available
                if is_ocr_data and ocr_analysis:
                    combined_response = f"""{ai_response}

---

📊 **TEKNİK OCR ANALİZ DETAYLARI:**

{ocr_analysis}"""
                    return self.enhanced_conversation.add_warmth_to_response(combined_response, language)
                else:
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

📷 OCR & GÖRSEL ANALİZ USTASI:
- Taranmış belgeler, fotoğraflar ve ekran görüntülerinden metin çıkarma
- Resimlerdeki tabloları pandas DataFrame'e çevirme  
- El yazısı metinleri dijitalleştirme
- Fatura, makbuz, finansal belge işleme
- Kağıt anket formlarını dataset'e çevirme
- Dashboard screenshot'larından KPI çıkarma
- Çoklu dil desteği (Türkçe, İngilizce, 90+ dil)
- Metin yapısını koruyarak akıllı formatlama

🔬 EXPERT DATA SCIENTIST YETENEKLER:
- Comprehensive EDA: Otomatik veri keşfi, kalite değerlendirmesi, istatistiksel analiz
- Advanced Visualizations: Publication-quality charts, correlation heatmaps, distribution analysis
- Predictive Modeling: Automated model selection, hyperparameter tuning, performance evaluation
- Business Intelligence: ROI analysis, actionable insights, strategic recommendations
- Statistical Testing: Hypothesis testing, significance analysis, confidence intervals
- Feature Engineering: Automated feature creation, selection, and transformation

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

🔍 OCR & IMAGE ANALYSIS EXPERT:
- Optical Character Recognition for scanned documents, photos, screenshots
- Table extraction from images → Convert to pandas DataFrame
- Handwritten text recognition and digitization
- Financial document processing (invoices, receipts, statements)
- Survey form digitization → Dataset creation
- Dashboard screenshot analysis → Extract KPIs and metrics
- Multi-language text extraction (English, Turkish, 90+ languages)
- Text structure preservation and intelligent formatting

🔬 EXPERT DATA SCIENTIST CAPABILITIES:
- Comprehensive EDA: Automated data discovery, quality assessment, statistical analysis
- Advanced Visualizations: Publication-quality charts, correlation heatmaps, distribution analysis
- Predictive Modeling: Automated model selection, hyperparameter tuning, performance evaluation
- Business Intelligence: ROI analysis, actionable insights, strategic recommendations
- Statistical Testing: Hypothesis testing, significance analysis, confidence intervals
- Feature Engineering: Automated feature creation, selection, and transformation

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
                base_prompt += f"\n\n📊 **MEVCUT VERİ SETİ ANALİZİ:**\n{file_analysis}\n\n🚨 KRİTİK UYARI: KULLANICI ZATEN DOSYA YÜKLEDİ! Yukarıdaki analiz gerçek veridir. 'Dosya yok' deme, yukarıdaki veri analizini kullan!"
            else:
                base_prompt += f"\n\n📊 **CURRENT DATASET ANALYSIS:**\n{file_analysis}\n\n🚨 CRITICAL: THE USER HAS ALREADY UPLOADED A FILE! The analysis above is real data. DO NOT say 'no file uploaded', use the data analysis above!"

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
• 📷 OCR ile görsel analiz (fotoğraf, taranmış belge, tablo çıkarma)

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
• 📷 OCR & Visual Analysis (photos, scanned docs, table extraction)

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
            if language == "Turkish":
                enhanced_parts.append("🚨 DOSYA MEVCUT: Kullanıcı dosya yükledi ve aşağıda analizi var:")
            else:
                enhanced_parts.append("🚨 FILE AVAILABLE: User has uploaded a file and analysis is below:")
            enhanced_parts.append(file_analysis)
            if language == "Turkish":
                enhanced_parts.append("⚠️ ASLA 'dosya yok' deme! Yukarıdaki veri analizini kullan!")
            else:
                enhanced_parts.append("⚠️ NEVER say 'no file uploaded'! Use the data analysis above!")
        
        if language == "Turkish":
            enhanced_parts.append("BEKLENEN YAKLAŞIM: Uzman seviyesinde analiz, pratik öneriler, kod örnekleri ve iş değeri perspektifi")
        else:
            enhanced_parts.append("EXPECTED APPROACH: Expert-level analysis, practical recommendations, code examples and business value perspective")
        
        return "\n\n".join(enhanced_parts)

    async def _analyze_file_advanced(self, file_id: str, language: str) -> str:
        """Enhanced file analysis with actual content - supports OCR results"""
        try:
            self.logger.info(f"🔬 Starting enhanced file analysis for: {file_id}")
            file_data = self._get_file_data(file_id)
            if file_data is None:
                self.logger.warning(f"❌ No file data found for: {file_id}")
                return ""
            
            self.logger.info(f"📊 File data loaded successfully: {file_data.shape}")
            
            # Check if this is OCR extracted data
            is_ocr_data = 'extracted_text' in file_data.columns or 'source_file' in file_data.columns
            
            if is_ocr_data:
                # Special handling for OCR results
                if language == "Turkish":
                    if 'extracted_text' in file_data.columns:
                        extracted_text = file_data.iloc[0]['extracted_text']
                        confidence = file_data.iloc[0].get('confidence_score', 0)
                        source_file = file_data.iloc[0].get('source_file', 'Unknown')
                        
                        analysis = f"""📷 OCR GÖRSEL ANALİZ SONUÇLARI:

🔍 DOSYA BİLGİLERİ:
• Kaynak dosya: {source_file}
• OCR güven skoru: {confidence:.2f} ({self._get_confidence_level(confidence)})
• Çıkarılan metin uzunluğu: {len(extracted_text)} karakter
• İşleme yöntemi: OCR (Optical Character Recognition)

📝 ÇIKARILAN METİN:
{extracted_text}

🔍 METİN ANALİZİ:
• Kelime sayısı: {len(extracted_text.split())} kelime
• Satır sayısı: {len(extracted_text.split('\n'))} satır
• Sayı içeriyor mu: {'Evet' if any(char.isdigit() for char in extracted_text) else 'Hayır'}
• Finansal veri: {'Evet' if any(symbol in extracted_text for symbol in ['₺', '$', '€', '£']) else 'Hayır'}

💡 ANLAM VE ÖNERİLER:
Bu görselden başarıyla metin çıkardım! Şimdi bu veriyi analiz edebilir, temizleyebilir veya başka formatlara dönüştürebilirim."""
                    else:
                        # This is structured OCR data (table)
                        analysis = f"""📊 OCR TABLO ANALİZ SONUÇLARI:

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

💡 OCR TABLO BAŞARIYLA ÇIKARILDI:
Bu görseldeeki tablo başarıyla pandas DataFrame'e dönüştürüldü! Artık bu veriyi analiz edebilir, görselleştirebilir ve manipüle edebilirim."""
                        
                else:  # English
                    if 'extracted_text' in file_data.columns:
                        extracted_text = file_data.iloc[0]['extracted_text']
                        confidence = file_data.iloc[0].get('confidence_score', 0)
                        source_file = file_data.iloc[0].get('source_file', 'Unknown')
                        
                        analysis = f"""📷 OCR IMAGE ANALYSIS RESULTS:

🔍 FILE INFORMATION:
• Source file: {source_file}
• OCR confidence score: {confidence:.2f} ({self._get_confidence_level(confidence)})
• Extracted text length: {len(extracted_text)} characters
• Processing method: OCR (Optical Character Recognition)

📝 EXTRACTED TEXT:
{extracted_text}

🔍 TEXT ANALYSIS:
• Word count: {len(extracted_text.split())} words
• Line count: {len(extracted_text.split('\n'))} lines
• Contains numbers: {'Yes' if any(char.isdigit() for char in extracted_text) else 'No'}
• Financial data: {'Yes' if any(symbol in extracted_text for symbol in ['₺', '$', '€', '£']) else 'No'}

💡 INSIGHTS AND RECOMMENDATIONS:
Successfully extracted text from your image! I can now analyze, clean, or transform this data into different formats."""
                    else:
                        # This is structured OCR data (table)
                        analysis = f"""📊 OCR TABLE ANALYSIS RESULTS:

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

💡 OCR TABLE SUCCESSFULLY EXTRACTED:
Successfully converted the table from your image into a pandas DataFrame! I can now analyze, visualize, and manipulate this data."""
            
            else:
                # Regular structured data analysis
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

    def _get_confidence_level(self, confidence: float) -> str:
        """Get confidence level description"""
        if confidence >= 0.8:
            return "Yüksek / High"
        elif confidence >= 0.6:
            return "Orta / Medium"
        elif confidence >= 0.4:
            return "Düşük / Low"
        else:
            return "Çok Düşük / Very Low"

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
        """Get file data - now supports OCR results from images"""
        try:
            self.logger.info(f"🔍 Looking for file with ID: {file_id}")
            print(f"DEBUG: Looking for file with ID: {file_id}")
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            self.logger.info(f"📁 Found matching files: {matching_files}")
            print(f"DEBUG: Found matching files: {matching_files}")
            
            if not matching_files:
                self.logger.warning(f"❌ No files found for ID: {file_id}")
                print(f"DEBUG: No files found for ID: {file_id}")
                return None
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            filename = matching_files[0]
            self.logger.info(f"📄 Reading file: {filename} from {file_path}")
            
            # Handle structured data files
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
            
            # Handle image files with OCR
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.heic')):
                self.logger.info(f"🔍 Processing image file with OCR: {filename}")
                
                try:
                    # Use UniversalFileHandler to get OCR results
                    processing_result = self.universal_file_handler.detect_and_process(file_path)
                    ocr_analysis = processing_result.get('processing_result', {}).get('ocr_analysis', {})
                    
                    if ocr_analysis:
                        # Check if we have structured data (table) from OCR
                        structured_data = ocr_analysis.get('structured_data')
                        if structured_data is not None and isinstance(structured_data, pd.DataFrame):
                            self.logger.info(f"📊 OCR extracted table with shape: {structured_data.shape}")
                            return structured_data
                        
                        # If no table, create a simple DataFrame with extracted text
                        extracted_text = ocr_analysis.get('extracted_text', '')
                        if extracted_text:
                            self.logger.info(f"📝 OCR extracted {len(extracted_text)} characters of text")
                            # Create a simple DataFrame with the extracted text
                            text_df = pd.DataFrame({
                                'extracted_text': [extracted_text],
                                'source_file': [filename],
                                'confidence_score': [ocr_analysis.get('confidence_score', 0)],
                                'processing_method': [ocr_analysis.get('processing_method', 'ocr')]
                            })
                            return text_df
                    
                    self.logger.warning(f"⚠️ No OCR results found for image: {filename}")
                    return None
                    
                except Exception as ocr_error:
                    self.logger.error(f"❌ OCR processing error for {filename}: {ocr_error}")
                    return None
            
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

    async def analyze_file_with_expert_ai(self, file_id: str, user_id: str = "default_user") -> Dict[str, Any]:
        """Run comprehensive expert data scientist analysis on uploaded file"""
        try:
            # Find the file path
            matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)]
            if not matching_files:
                return {"error": "File not found", "success": False}
            
            file_path = os.path.join(UPLOAD_DIR, matching_files[0])
            
            self.logger.info(f"🔬 Starting Expert Data Scientist Analysis for: {file_path}")
            
            # Run comprehensive analysis with expert analyzer
            analysis_results = self.expert_analyzer.comprehensive_analysis(file_path)
            
            if "error" in analysis_results:
                return {"error": analysis_results["error"], "success": False}
            
            # Generate expert conversation response
            expert_response = self.expert_conversation_ai.generate_expert_response(
                "Provide comprehensive analysis insights", 
                analysis_results
            )
            
            # Mark file as analyzed
            self.file_manager.mark_file_analyzed(user_id, file_id)
            
            return {
                "success": True,
                "expert_analysis": analysis_results,
                "expert_insights": expert_response,
                "analysis_timestamp": datetime.now().isoformat(),
                "file_id": file_id
            }
            
        except Exception as e:
            self.logger.error(f"❌ Expert analysis error: {e}")
            return {"error": str(e), "success": False}

# Initialize the AI systems
enhanced_ai = ComprehensiveDataScienceAI(
    openai_api_key=os.getenv("OPENAI_API_KEY", "placeholder")
)

# Initialize the new comprehensive DataSoph AI system
datasoph_ai = DataSophAI()

# Initialize safety components
pii_detector = PIIDetector()
statistical_guardrails = StatisticalGuardrails()
error_resilience = ErrorResilienceManager()

# Initialize Smart Response Generator
# Use global instance from smart_response_generator module
smart_responder = smart_response_generator

@app.post("/api/v1/ai/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Enhanced chat that ACTUALLY uses the smart multilingual system"""
    
    # 🔥 DEBUG: Fonksiyonun çağrıldığını kontrol et
    logger.info(f"🎯 SMART AI ENDPOINT CALLED! Message: {request.message[:50]}...")
    
    try:
        # 🚀 FIXED: PROPERLY AWAIT THE ASYNC FUNCTION!
        logger.info(f"🧠 Using SmartResponseGenerator for: {request.message}")
        response = await smart_responder.generate_response(
            message=request.message,
            user_id=request.user_id or "default"
        )
        logger.info(f"✅ Smart AI response generated: {response[:100]}...")
        
        # Enhanced response data
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Smart AI error: {e}")
        
        # Multilingual error handling based on message content
        is_turkish = any(char in 'çğıöşüÇĞIÖŞÜ' for char in request.message)
        
        error_msg = (
            f"Üzgünüm, bir sorun yaşadım: {str(e)}. Tekrar dener misin? 🔧" if is_turkish
            else f"Sorry, I encountered an issue: {str(e)}. Could you try again? 🔧"
        )
        
        return ChatResponse(
            response=error_msg,
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/v1/ai/reset-conversation")
async def reset_conversation(request: ChatRequest):
    """Reset conversation for fresh start"""
    try:
        result = smart_responder.reset_conversation(request.user_id or "default")
        
        return {
            'success': result['success'],
            'message': result['message'],
            'user_id': result['user_id'],
            'cleared_exchanges': result.get('cleared_exchanges', 0),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Reset conversation error: {e}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.post("/api/v1/ai/test-language")
async def test_language(request: ChatRequest):
    """Test language detection"""
    try:
        result = smart_responder.test_language_detection(request.message)
        
        return {
            'success': True,
            'detection_result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Language test error: {e}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.get("/api/v1/ai/conversation-stats/{user_id}")
async def get_conversation_stats(user_id: str):
    """Get conversation statistics for user"""
    try:
        stats = smart_responder.get_conversation_stats(user_id)
        
        return {
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Conversation stats error: {e}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.get("/api/v1/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "service": "DataSoph AI - Enhanced Multilingual System"}

@app.get("/api/v1/supported-formats")
async def get_supported_formats():
    """Get comprehensive list of supported file formats"""
    try:
        supported_formats = enhanced_ai.universal_file_handler.get_supported_formats()
        return {
            "status": "success",
            "formats": supported_formats,
            "total_formats": sum(len(category['formats']) if 'formats' in category else 0 
                               for category in supported_formats.values()),
            "message": "DataSoph AI supports comprehensive file format analysis"
        }
    except Exception as e:
        logger.error(f"❌ Error getting supported formats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and store file with enhanced format support"""
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
        
        # Quick format validation using UniversalFileHandler
        try:
            # Just check if format is supported without full processing
            file_ext = ('.' + file_extension).lower()
            is_supported = file_ext in enhanced_ai.universal_file_handler.supported_formats
            
            if is_supported:
                priority = enhanced_ai.universal_file_handler._get_format_priority(file_ext)
                success_message = enhanced_ai.universal_file_handler.upload_messages['supported'].format(
                    file_type=file_extension.upper()
                )
            else:
                success_message = enhanced_ai.universal_file_handler.upload_messages['partially_supported'].format(
                    file_type=file_extension.upper()
                )
                
        except Exception as validation_error:
            logger.warning(f"⚠️ Format validation error: {validation_error}")
            success_message = f"✅ File '{file.filename}' uploaded successfully. I'll do my best to analyze this format."
        
        # Register file for user session (using default user for now)
        user_id = "web_user"  # Could be passed as parameter in future
        enhanced_ai.file_manager.register_file_for_user(user_id, file_id, file.filename)
        
        # CLEAR OLD CONVERSATION CONTEXT: Reset AI conversation history to prevent confusion
        try:
            # Clear smart response generator conversation history for fresh context
            if hasattr(smart_responder, 'reset_conversation'):
                smart_responder.reset_conversation(user_id)
            
            # Clear any old data context from DataSoph AI
            if hasattr(enhanced_ai, 'start_new_session'):
                enhanced_ai.start_new_session(user_id)
            
            logger.info(f"🔄 Cleared conversation history for user {user_id} - Fresh data context established")
        except Exception as clear_error:
            logger.warning(f"⚠️ Could not clear old context: {clear_error} - continuing with upload")
        
        # NO AUTOMATIC CHARTS - Let AI create them on demand based on user questions
        logger.info(f"📁 File ready for intelligent AI analysis: {file.filename}")
        success_message += f"\n\n🧠 **Intelligent AI Analysis Ready!**\n\n📊 Your data is now loaded and ready for smart analysis. I'll analyze your data in real-time based on your specific questions.\n\n💡 **Ask me anything about your data:**\n• \"Verimdeki ana trendler neler?\" \n• \"En güçlü korelasyonları göster\"\n• \"Anomali tespiti yap\"\n• \"Makine öğrenmesi modeli öner\"\n• \"İş için hangi önerileriniz var?\"\n• \"Python kodu ile analiz yap\"\n\nHer sorunuz için özel analiz ve görselleştirme yapacağım! 🎯"
        
        # NO AUTOMATIC EXPERT ANALYSIS - AI will handle everything on-demand
        logger.info(f"📊 File ready for intelligent AI conversation: {file.filename}")
        # All analysis will be done by AI when user asks specific questions
        
        logger.info(f"📁 File uploaded: {file.filename} -> {file_id} (format: {file_extension})")
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            message=success_message,
            size=file.size,
            type=file.content_type
        )
        
    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/v1/analyze-file")
async def analyze_file_immediately(request: FileAnalysisRequest):
    """Trigger immediate comprehensive analysis of uploaded file using UniversalFileHandler"""
    try:
        user_id = request.user_id or "web_user"
        
        # Find the file path
        matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(request.file_id)]
        if not matching_files:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = os.path.join(UPLOAD_DIR, matching_files[0])
        
        # Use UniversalFileHandler for comprehensive analysis
        logger.info(f"🔬 Starting universal file analysis for: {file_path}")
        processing_result = enhanced_ai.universal_file_handler.detect_and_process(file_path)
        
        # Generate AI-powered analysis response
        if processing_result.get('success', True):
            # Create analysis summary for AI
            analysis_summary = f"""📊 **COMPREHENSIVE FILE ANALYSIS RESULTS:**

**File Information:**
- Filename: {processing_result['file_info'].get('filename', 'Unknown')}
- Size: {processing_result['file_info'].get('size_mb', 0):.2f} MB
- Format: {processing_result['processing_result'].get('format', 'Unknown')}
- Processing Status: {'✅ Success' if processing_result['processing_result'].get('success', False) else '❌ Failed'}

**Processing Details:**
{str(processing_result['processing_result'])[:2000]}

Please provide a comprehensive analysis and actionable insights based on this file processing result."""
            
            # Get AI-powered insights
            analysis_result = await enhanced_ai.analyze_file_completely(request.file_id, user_id)
            
            # Combine technical analysis with AI insights
            combined_response = f"""{analysis_result}

---

**🔧 Technical Processing Details:**
- **Format Priority:** {processing_result.get('format_priority', 'Unknown')}
- **Processor Version:** {processing_result.get('processor_version', '3.0')}
- **Analysis Timestamp:** {processing_result.get('analysis_timestamp', datetime.now().isoformat())}

{processing_result['processing_result'].get('user_message', '')}"""
            
        else:
            # Handle processing errors
            error_message = processing_result.get('error', 'Unknown processing error')
            combined_response = f"""❌ **File Processing Error:**

{error_message}

**What you can try:**
• Check if your file format is supported
• Ensure the file isn't corrupted
• Try converting to a standard format (CSV, Excel, JSON)
• Contact support if the issue persists

**Supported formats include:** CSV, Excel, JSON, PDF, images, statistical software files, and many more."""

        # Mark file as analyzed
        enhanced_ai.file_manager.mark_file_analyzed(user_id, request.file_id)
        
        return ChatResponse(
            response=combined_response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Universal file analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v1/expert-analysis")
async def expert_data_scientist_analysis(request: FileAnalysisRequest):
    """Run comprehensive expert data scientist analysis with advanced insights"""
    try:
        user_id = request.user_id or "web_user"
        
        # Run expert analysis
        logger.info(f"🔬 Starting Expert Data Scientist Analysis for file: {request.file_id}")
        expert_results = await enhanced_ai.analyze_file_with_expert_ai(request.file_id, user_id)
        
        if not expert_results.get("success", False):
            raise HTTPException(status_code=400, detail=expert_results.get("error", "Analysis failed"))
        
        # Format comprehensive response
        analysis = expert_results["expert_analysis"]
        insights = expert_results["expert_insights"]
        
        # Build detailed response
        response_parts = ["🔬 **EXPERT DATA SCIENTIST ANALYSIS COMPLETE**\n"]
        
        # Basic info
        if "basic_info" in analysis:
            basic = analysis["basic_info"]
            response_parts.append(f"📊 **Dataset Overview:**")
            response_parts.append(f"• Shape: {basic['shape'][0]:,} rows × {basic['shape'][1]} columns")
            response_parts.append(f"• Memory: {basic['memory_mb']:.2f} MB")
            response_parts.append("")
        
        # Data quality
        if "data_quality" in analysis:
            quality = analysis["data_quality"]
            score = quality.get("quality_score", 0)
            emoji = "🟢" if score > 80 else "🟡" if score > 60 else "🔴"
            response_parts.append(f"🔍 **Data Quality Assessment:**")
            response_parts.append(f"• Overall Score: {emoji} {score:.1f}/100")
            response_parts.append(f"• Missing value columns: {quality.get('missing_columns', 0)}")
            response_parts.append(f"• Duplicate rows: {quality.get('duplicates', 0):,}")
            response_parts.append("")
        
        # Statistical insights
        if "statistical_analysis" in analysis:
            stats = analysis["statistical_analysis"]
            if "correlations" in stats and "high_correlations" in stats["correlations"]:
                high_corrs = stats["correlations"]["high_correlations"]
                if high_corrs:
                    response_parts.append(f"📈 **Key Correlations Found:**")
                    for corr in high_corrs[:3]:
                        direction = "📈" if corr["correlation"] > 0 else "📉"
                        response_parts.append(f"• {direction} {corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f}")
                    response_parts.append("")
        
        # Predictive modeling
        if "predictive_modeling" in analysis:
            modeling = analysis["predictive_modeling"]
            model_type = modeling.get("model_type", "unknown")
            response_parts.append(f"🤖 **Predictive Model Results:**")
            response_parts.append(f"• Model Type: {model_type.title()}")
            response_parts.append(f"• Target Variable: {modeling.get('target_variable', 'N/A')}")
            
            if model_type == "classification":
                acc = modeling.get("accuracy", 0)
                response_parts.append(f"• Accuracy: {acc:.1%}")
            elif model_type == "regression":
                r2 = modeling.get("r2_score", 0)
                response_parts.append(f"• R² Score: {r2:.3f}")
            
            if "feature_importance" in modeling:
                top_feature = max(modeling["feature_importance"], key=modeling["feature_importance"].get)
                response_parts.append(f"• Most Important Feature: {top_feature}")
            response_parts.append("")
        
        # Business insights
        if "business_insights" in analysis:
            insights_list = analysis["business_insights"]
            response_parts.append("💡 **Business Insights & Recommendations:**")
            for i, insight in enumerate(insights_list[:5], 1):
                response_parts.append(f"{i}. {insight}")
            response_parts.append("")
        
        # Expert conversation insights
        response_parts.append("🎯 **Expert AI Insights:**")
        response_parts.append(insights)
        
        # Visualizations note
        if "visualizations" in analysis:
            viz_count = len(analysis["visualizations"])
            response_parts.append(f"\n📊 **Generated {viz_count} Professional Visualizations:**")
            viz_types = list(analysis["visualizations"].keys())
            for viz_type in viz_types:
                response_parts.append(f"• {viz_type.replace('_', ' ').title()}")
        
        combined_response = "\n".join(response_parts)
        
        return ChatResponse(
            response=combined_response,
            timestamp=expert_results["analysis_timestamp"]
        )
        
    except Exception as e:
        logger.error(f"❌ Expert analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Expert analysis failed: {str(e)}")

# NEW COMPREHENSIVE DATASOPH AI ENDPOINTS

@app.post("/api/v2/datasoph/chat")
async def datasoph_chat_endpoint(request: ChatRequest):
    """Enhanced DataSoph AI chat endpoint with full feature set"""
    try:
        response = datasoph_ai.process_user_input(
            user_input=request.message,
            file_path=None,
            user_id=request.user_id
        )
        
        return ChatResponse(
            response=response['response'],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ DataSoph chat error: {e}")
        return ChatResponse(
            response=error_resilience.safe_execute_analysis_step(
                lambda: "I encountered an issue. Please try rephrasing your question.",
                str(e)
            )['result'],
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/v2/datasoph/analyze-file")
async def datasoph_file_analysis(file: UploadFile = File(...)):
    """Comprehensive file analysis with DataSoph AI"""
    try:
        # Save uploaded file temporarily
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'txt'
        stored_filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, stored_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Run comprehensive analysis with DataSoph AI
        result = datasoph_ai.process_user_input(
            user_input="Analyze this file comprehensively",
            file_path=file_path,
            user_id="web_user"
        )
        
        return {
            "analysis_result": result,
            "file_id": file_id,
            "filename": file.filename,
            "status": "completed" if result['success'] else "failed"
        }
        
    except Exception as e:
        logger.error(f"❌ DataSoph file analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/datasoph/status")
async def get_datasoph_status():
    """Get comprehensive DataSoph AI system status"""
    try:
        status = datasoph_ai.get_system_status()
        
        # Add safety system status
        status['safety_systems'] = {
            'pii_detector': 'ready',
            'statistical_guardrails': 'ready',
            'error_resilience': 'ready',
            'error_summary': error_resilience.get_error_summary()
        }
        
        return status
        
    except Exception as e:
        logger.error(f"❌ Status check error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/v2/datasoph/pii-scan")
async def scan_for_pii(request: FileAnalysisRequest):
    """Scan uploaded file for PII and privacy concerns"""
    try:
        # Find the file
        matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(request.file_id)]
        if not matching_files:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = os.path.join(UPLOAD_DIR, matching_files[0])
        
        # Load data and scan for PII
        df = pd.read_csv(file_path)  # Basic loading for PII scan
        pii_results = pii_detector.scan_dataset_for_pii(df)
        
        return {
            "pii_scan_results": pii_results,
            "file_id": request.file_id,
            "scan_timestamp": datetime.now().isoformat(),
            "recommendations": pii_results.get('masking_suggestions', {})
        }
        
    except Exception as e:
        logger.error(f"❌ PII scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/datasoph/export-session")
async def export_session_analysis():
    """Export current session analysis"""
    try:
        export_result = datasoph_ai.export_session_analysis(format='notebook')
        
        return {
            "export_result": export_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/datasoph/start-session")
async def start_datasoph_session(user_id: str = "web_user"):
    """Start new DataSoph AI session"""
    try:
        session_result = datasoph_ai.start_new_session(user_id)
        
        return {
            "session": session_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Session start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/ai/clear-data-context")
async def clear_data_context(request: ChatRequest):
    """Clear all data context and conversation history for fresh analysis"""
    try:
        user_id = request.user_id or "web_user"
        
        # Clear conversation history from smart responder
        conversation_result = smart_responder.reset_conversation(user_id)
        
        # Clear file context from file manager
        if user_id in enhanced_ai.file_manager.user_file_sessions:
            old_files = len(enhanced_ai.file_manager.user_file_sessions[user_id])
            enhanced_ai.file_manager.user_file_sessions[user_id] = []
            logger.info(f"🗑️ Cleared {old_files} file(s) from context for user {user_id}")
        else:
            old_files = 0
        
        # Start fresh DataSoph AI session
        try:
            if hasattr(enhanced_ai, 'start_new_session'):
                enhanced_ai.start_new_session(user_id)
        except Exception as session_error:
            logger.warning(f"⚠️ Could not reset DataSoph session: {session_error}")
        
        # Detect language for response
        is_turkish = any(char in 'çğıöşüÇĞIÖŞÜ' for char in request.message) if request.message else False
        
        clear_message = (
            f"✨ Tüm veri bağlamı temizlendi! ({conversation_result.get('cleared_exchanges', 0)} konuşma + {old_files} dosya) "
            "Şimdi yeni verileriniz için tamamen temiz bir başlangıç yapabilirsiniz. 🔄" 
            if is_turkish else 
            f"✨ All data context cleared! ({conversation_result.get('cleared_exchanges', 0)} conversations + {old_files} files) "
            "You now have a completely fresh start for your new data. 🔄"
        )
        
        return {
            'success': True,
            'message': clear_message,
            'user_id': user_id,
            'cleared_conversations': conversation_result.get('cleared_exchanges', 0),
            'cleared_files': old_files,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Clear data context error: {e}")
        
        error_message = (
            f"Veri bağlamı temizlenirken hata oluştu: {str(e)}" if 'çğıöşü' in str(e).lower() 
            else f"Error clearing data context: {str(e)}"
        )
        
        return {
            'success': False,
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced DataSoph AI")
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=False,
        log_level="info"
    ) 