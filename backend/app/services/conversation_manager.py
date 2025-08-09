"""
DataSoph AI - Advanced Conversation Manager
Handles natural conversation, context awareness, and intelligent responses
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class IntentCategory(Enum):
    """Categories of user intents"""
    GREETING = "greeting"
    DATA_ANALYSIS = "data_analysis"
    VISUALIZATION = "visualization"
    MACHINE_LEARNING = "machine_learning"
    STATISTICS = "statistics"
    BUSINESS_QUESTION = "business_question"
    TECHNICAL_HELP = "technical_help"
    CASUAL_CHAT = "casual_chat"
    FILE_PROCESSING = "file_processing"
    CODE_ASSISTANCE = "code_assistance"
    EXPORT_RESULTS = "export_results"
    SYSTEM_QUERY = "system_query"

class ExpertiseLevel(Enum):
    """User expertise levels for response adaptation"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class ConversationContext:
    """Context information for conversation continuity"""
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, Any]]
    uploaded_files: List[str]
    user_preferences: Dict[str, Any]
    expertise_level: ExpertiseLevel
    primary_language: str
    last_activity: datetime
    analysis_results_cache: Dict[str, Any]
    conversation_mood: str  # professional, casual, exploratory, urgent

@dataclass
class UserProfile:
    """Extended user profile for personalization"""
    user_id: str
    name: Optional[str]
    expertise_level: ExpertiseLevel
    preferred_language: str
    industry_context: Optional[str]
    frequently_used_tools: List[str]
    conversation_style: str  # direct, detailed, visual, code-focused
    business_role: Optional[str]  # analyst, manager, researcher, student
    learning_goals: List[str]
    created_at: datetime
    last_updated: datetime

class AdvancedConversationManager:
    """
    Advanced conversation manager with Claude/ChatGPT-level intelligence
    """
    
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        self.session_timeout = timedelta(hours=2)
        self.logger = logging.getLogger(__name__)
        
        # Language detection patterns
        self.turkish_patterns = {
            'greetings': ['merhaba', 'selam', 'naber', 'nasılsın', 'iyi günler', 'günaydın', 'iyi akşamlar'],
            'questions': ['nedir', 'nasıl', 'nerede', 'ne zaman', 'hangi', 'kaç', 'kim', 'neden', 'niçin'],
            'data_terms': ['veri', 'analiz', 'grafik', 'model', 'makine öğrenmesi', 'istatistik', 'tahmin'],
            'common_words': ['ben', 'sen', 'bu', 'şu', 'var', 'yok', 'için', 'ile', 'bir', 'çok', 'az'],
            'turkish_chars': 'çğıöşüÇĞIÖŞÜ'
        }
        
        self.english_patterns = {
            'greetings': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'questions': ['what', 'how', 'where', 'when', 'which', 'who', 'why', 'can', 'will', 'would'],
            'data_terms': ['data', 'analysis', 'chart', 'graph', 'model', 'machine learning', 'statistics', 'predict'],
            'common_words': ['the', 'is', 'are', 'and', 'or', 'but', 'with', 'for', 'in', 'on', 'at']
        }
        
        # Intent detection patterns
        self.intent_patterns = {
            IntentCategory.GREETING: [
                r'\b(hi|hello|hey|merhaba|selam|naber|nasılsın)\b',
                r'(good morning|good afternoon|good evening|günaydın|iyi günler|iyi akşamlar)',
                r'\b(how are you|nasılsın|nasıl gidiyor)\b'
            ],
            IntentCategory.DATA_ANALYSIS: [
                r'\b(analyze|analysis|analiz|examine|explore|investigate|keşfet|incele)\b',
                r'\b(data|dataset|veri|information|bilgi)\b.*\b(analyze|analysis|analiz)\b',
                r'\b(summary|özet|describe|tanımla|profile|profil)\b',
                r'\b(correlation|korelasyon|relationship|ilişki|trend|eğilim)\b'
            ],
            IntentCategory.VISUALIZATION: [
                r'\b(plot|chart|graph|grafik|visualize|görselleştir|show|göster)\b',
                r'\b(histogram|scatter|line|bar|pie|pasta|çizgi|dağılım)\b',
                r'\b(dashboard|panel|interactive|interaktif)\b'
            ],
            IntentCategory.MACHINE_LEARNING: [
                r'\b(model|predict|tahmin|classification|sınıflandırma|regression|regresyon)\b',
                r'\b(machine learning|makine öğrenmesi|ML|AI|yapay zeka)\b',
                r'\b(train|eğit|accuracy|doğruluk|performance|performans)\b',
                r'\b(random forest|xgboost|neural network|sinir ağı)\b'
            ],
            IntentCategory.STATISTICS: [
                r'\b(statistics|istatistik|statistical|istatistiksel|test|hypothesis|hipotez)\b',
                r'\b(mean|ortalama|median|medyan|std|standard deviation|standart sapma)\b',
                r'\b(p-value|significance|anlamlılık|confidence|güven)\b'
            ],
            IntentCategory.BUSINESS_QUESTION: [
                r'\b(business|iş|company|şirket|revenue|gelir|profit|kar|ROI|customer|müşteri)\b',
                r'\b(strategy|strateji|decision|karar|recommendation|öneri|impact|etki)\b',
                r'\b(KPI|metric|metrik|performance|performans|goal|hedef)\b'
            ],
            IntentCategory.CODE_ASSISTANCE: [
                r'\b(code|kod|python|pandas|numpy|matplotlib|seaborn|sklearn)\b',
                r'\b(function|fonksiyon|script|betik|programming|programlama)\b',
                r'\b(error|hata|debug|exception|istisna)\b'
            ]
        }
        
        # Personality responses for different contexts
        self.personality_responses = {
            'turkish': {
                'casual_greeting': [
                    "Merhaba! 👋 DataSoph AI burada - veri bilimi konularında size nasıl yardımcı olabilirim?",
                    "Selam! 🚀 Bugün hangi verilerle çalışacağız?", 
                    "İyi günler! 📊 Veri analizi, makine öğrenmesi veya başka bir konuda yardımcı olabilirim."
                ],
                'professional_greeting': [
                    "Merhaba! DataSoph AI olarak kapsamlı veri bilimi desteği sunuyorum. Size nasıl yardımcı olabilirim?",
                    "İyi günler! Veri analizi, makine öğrenmesi, görselleştirme ve iş zekası konularında uzmanlığım bulunuyor.",
                    "Hoş geldiniz! Profesyonel veri bilimi projelerinizde size destek olmak için buradayım."
                ],
                'encouragement': [
                    "Harika soru! 🎯 Bu konuda size detaylı yardım edebilirim.",
                    "Mükemmel! 💡 Bu analizi birlikte yapalım.",
                    "Çok güzel bir yaklaşım! 🔥 Hemen başlayalım."
                ],
                'complex_explanation': [
                    "Bu biraz karmaşık bir konu, ama endişelenmeyin - adım adım açıklayacağım.",
                    "İyi soru! Bu konuyu hem teknik hem de pratik açıdan ele alalım.",
                    "Bu önemli bir analiz - hem sonuçları hem de yorumları detaylı göstereceğim."
                ]
            },
            'english': {
                'casual_greeting': [
                    "Hello! 👋 I'm DataSoph AI - how can I help you with data science today?",
                    "Hey there! 🚀 What data challenges are we tackling today?",
                    "Hi! 📊 I'm here to help with data analysis, machine learning, or any data science questions."
                ],
                'professional_greeting': [
                    "Hello! I'm DataSoph AI, providing comprehensive data science expertise. How may I assist you?",
                    "Good day! I specialize in data analysis, machine learning, visualization, and business intelligence.",
                    "Welcome! I'm here to support your professional data science initiatives."
                ],
                'encouragement': [
                    "Excellent question! 🎯 I can provide detailed assistance with this.",
                    "Perfect! 💡 Let's dive into this analysis together.",
                    "Great approach! 🔥 Let's get started immediately."
                ],
                'complex_explanation': [
                    "This is quite sophisticated - don't worry, I'll break it down step by step.",
                    "Excellent question! Let me address both the technical and practical aspects.",
                    "This is an important analysis - I'll show both results and interpretations in detail."
                ]
            }
        }

    def detect_intent_and_language(self, message: str, user_id: str) -> Tuple[IntentCategory, str, float]:
        """
        Advanced intent detection with context awareness
        Returns: (intent, language, confidence)
        """
        # Language detection
        language = self._detect_language_advanced(message)
        
        # Get user context
        context = self.get_or_create_context(user_id)
        
        # Intent detection with scoring
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message.lower()))
                score += matches
            
            # Context-based boosting
            if intent == IntentCategory.DATA_ANALYSIS and context.uploaded_files:
                score += 2
            if intent == IntentCategory.VISUALIZATION and 'chart' in context.conversation_history[-3:]:
                score += 1
                
            intent_scores[intent] = score
        
        # Find highest scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 5.0, 1.0)  # Normalize to 0-1
            
            # Fallback to casual chat if confidence is low
            if confidence < 0.3:
                best_intent = IntentCategory.CASUAL_CHAT
                confidence = 0.8
        else:
            best_intent = IntentCategory.CASUAL_CHAT
            confidence = 0.5
            
        return best_intent, language, confidence

    def _detect_language_advanced(self, text: str) -> str:
        """Advanced language detection with pattern matching"""
        text_lower = text.lower()
        
        # Check for Turkish characters
        if any(char in text for char in self.turkish_patterns['turkish_chars']):
            return "Turkish"
        
        # Count pattern matches
        turkish_score = 0
        english_score = 0
        
        for category, words in self.turkish_patterns.items():
            if category != 'turkish_chars':
                for word in words:
                    turkish_score += text_lower.count(word)
        
        for category, words in self.english_patterns.items():
            for word in words:
                english_score += text_lower.count(word)
        
        # Determine language
        if turkish_score > english_score:
            return "Turkish"
        elif english_score > turkish_score:
            return "English"
        else:
            # Default based on user history or fallback to Turkish
            return "Turkish"

    def get_or_create_context(self, user_id: str, session_id: str = None) -> ConversationContext:
        """Get or create conversation context for user"""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        context_key = f"{user_id}_{session_id}"
        
        if context_key not in self.contexts:
            self.contexts[context_key] = ConversationContext(
                user_id=user_id,
                session_id=session_id,
                conversation_history=[],
                uploaded_files=[],
                user_preferences={},
                expertise_level=ExpertiseLevel.INTERMEDIATE,
                primary_language="Turkish",
                last_activity=datetime.now(),
                analysis_results_cache={},
                conversation_mood="professional"
            )
        
        return self.contexts[context_key]

    def generate_contextual_response(self, intent: IntentCategory, message: str, 
                                   language: str, context: ConversationContext,
                                   user_profile: Optional[UserProfile] = None) -> str:
        """Generate intelligent, contextual responses"""
        
        # Update context
        context.last_activity = datetime.now()
        context.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'intent': intent.value,
            'language': language
        })
        
        # Generate response based on intent and context
        if intent == IntentCategory.GREETING:
            return self._generate_greeting_response(language, context, user_profile)
        elif intent == IntentCategory.CASUAL_CHAT:
            return self._generate_casual_response(message, language, context)
        elif intent in [IntentCategory.DATA_ANALYSIS, IntentCategory.VISUALIZATION, 
                       IntentCategory.MACHINE_LEARNING, IntentCategory.STATISTICS]:
            return self._generate_technical_response(intent, message, language, context)
        elif intent == IntentCategory.BUSINESS_QUESTION:
            return self._generate_business_response(message, language, context)
        else:
            return self._generate_default_response(message, language, context)

    def _generate_greeting_response(self, language: str, context: ConversationContext, 
                                  user_profile: Optional[UserProfile]) -> str:
        """Generate personalized greeting responses"""
        
        lang_key = 'turkish' if language == 'Turkish' else 'english'
        
        # Determine greeting style based on context
        if len(context.conversation_history) <= 1:  # First interaction
            if user_profile and user_profile.conversation_style == 'casual':
                responses = self.personality_responses[lang_key]['casual_greeting']
            else:
                responses = self.personality_responses[lang_key]['professional_greeting']
        else:
            # Returning user
            if language == 'Turkish':
                responses = [
                    "Tekrar hoş geldiniz! 🌟 Bugün hangi analiz için bir araya geldik?",
                    "Merhaba yine! 📈 Önceki çalışmalarımızdan devam edelim mi?",
                    "Selam! 🚀 Yeni veriler mi var, yoksa önceki analizleri mi derinleştiriyoruz?"
                ]
            else:
                responses = [
                    "Welcome back! 🌟 What analysis are we diving into today?",
                    "Hello again! 📈 Shall we continue from where we left off?",
                    "Hi there! 🚀 New data to explore or deepening previous analysis?"
                ]
        
        import random
        base_response = random.choice(responses)
        
        # Add context-aware additions
        if context.uploaded_files:
            if language == 'Turkish':
                base_response += f"\n\n📁 Aktif dosyalarınız: {len(context.uploaded_files)} adet. Hangi analizi yapmak istiyorsunuz?"
            else:
                base_response += f"\n\n📁 Active files: {len(context.uploaded_files)}. What analysis would you like to perform?"
        
        return base_response

    def _generate_casual_response(self, message: str, language: str, context: ConversationContext) -> str:
        """Generate engaging casual conversation responses"""
        
        message_lower = message.lower()
        
        # How are you responses
        if any(phrase in message_lower for phrase in ['how are you', 'nasılsın', 'nasıl gidiyor']):
            if language == 'Turkish':
                return """İyiyim, teşekkür ederim! 😊 

Bugün verilerinizle nasıl büyülü şeyler yapabileceğimizi düşünüyorum. Elimde güçlü araçlar var:
📊 Veri analizi ve görselleştirme
🤖 Makine öğrenmesi modelleri  
📈 İstatistiksel analizler
💼 İş zekası öngörüleri

Peki siz nasılsınız? Hangi veri merakınızı çözelim? 🚀"""
            else:
                return """I'm doing great, thank you! 😊 

I'm excited about the data magic we can create today. I have powerful tools at my disposal:
📊 Data analysis and visualization
🤖 Machine learning models
📈 Statistical analyses  
💼 Business intelligence insights

How are you doing? What data curiosity shall we solve? 🚀"""
        
        # General casual responses
        if language == 'Turkish':
            casual_responses = [
                "Mükemmel! 🎯 Veri bilimi konularında size nasıl yardımcı olabilirim?",
                "Harika! 💡 Bugün hangi analitik macerayı yaşayalım?",
                "Süper! 🚀 Verilerinizi anlamlı içgörülere dönüştürmek için buradayım."
            ]
        else:
            casual_responses = [
                "Excellent! 🎯 How can I assist you with data science today?",
                "Awesome! 💡 What analytical adventure shall we embark on?",
                "Great! 🚀 I'm here to transform your data into meaningful insights."
            ]
        
        import random
        return random.choice(casual_responses)

    def _generate_technical_response(self, intent: IntentCategory, message: str, 
                                   language: str, context: ConversationContext) -> str:
        """Generate technical response with appropriate complexity"""
        
        # This will be enhanced with actual analysis capabilities
        if language == 'Turkish':
            return f"""Anlıyorum! {intent.value.replace('_', ' ').title()} konusunda yardım istiyorsunuz. 

🔥 **Yapabileceğim analizler:**
- Otomatik veri profilleme ve kalite değerlendirmesi
- İstatistiksel analiz ve hipotez testleri
- Makine öğrenmesi model geliştirme
- İnteraktif görselleştirmeler
- İş zekası öngörüleri

Lütfen verilerinizi yükleyin veya spesifik bir soru sorun, hemen başlayalım! 📊"""
        else:
            return f"""I understand! You need help with {intent.value.replace('_', ' ')}. 

🔥 **Analyses I can perform:**
- Automatic data profiling and quality assessment
- Statistical analysis and hypothesis testing
- Machine learning model development
- Interactive visualizations
- Business intelligence insights

Please upload your data or ask a specific question, and let's get started! 📊"""

    def _generate_business_response(self, message: str, language: str, context: ConversationContext) -> str:
        """Generate business-focused responses"""
        
        if language == 'Turkish':
            return """Mükemmel! İş stratejisi ve veri analitiği konusunda uzmanım. 💼

**İş odaklı analizlerim:**
🎯 ROI hesaplamaları ve iş etkisi analizi
📈 KPI geliştirme ve performans takibi
💡 Stratejik öneriler ve eylem planları
🔍 Pazar analizi ve müşteri segmentasyonu
⚡ Operasyonel verimlilik optimizasyonu

Hangi iş problemini çözmek istiyorsunuz? Verilerinizi iş değerine dönüştürelim! 🚀"""
        else:
            return """Excellent! I specialize in business strategy and data analytics. 💼

**My business-focused analyses:**
🎯 ROI calculations and business impact analysis
📈 KPI development and performance tracking
💡 Strategic recommendations and action plans
🔍 Market analysis and customer segmentation
⚡ Operational efficiency optimization

What business problem would you like to solve? Let's transform your data into business value! 🚀"""

    def _generate_default_response(self, message: str, language: str, context: ConversationContext) -> str:
        """Generate default helpful response"""
        
        if language == 'Turkish':
            return """Size nasıl yardımcı olabilirim? 🤔

DataSoph AI olarak şunları yapabilirim:
📊 **Veri Analizi**: CSV, Excel, JSON dosyalarını analiz etme
🤖 **Makine Öğrenmesi**: Tahmin modelleri geliştirme  
📈 **Görselleştirme**: İnteraktif grafikler ve dashboardlar
📋 **Raporlama**: Executive özet ve teknik raporlar
💬 **Kodlama**: Python, pandas, sklearn kodu yazma

Bir dosya yükleyin veya spesifik bir soru sorun! 🚀"""
        else:
            return """How can I help you? 🤔

As DataSoph AI, I can:
📊 **Data Analysis**: Analyze CSV, Excel, JSON files
🤖 **Machine Learning**: Develop prediction models
📈 **Visualization**: Create interactive charts and dashboards  
📋 **Reporting**: Executive summaries and technical reports
💬 **Coding**: Write Python, pandas, sklearn code

Upload a file or ask a specific question! 🚀"""

    def update_user_expertise(self, user_id: str, message: str, response_quality: float):
        """Update user expertise level based on interactions"""
        # This would analyze technical language usage and adjust expertise
        pass

    def get_conversation_summary(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Generate conversation summary for memory"""
        context_key = f"{user_id}_{session_id}"
        if context_key in self.contexts:
            context = self.contexts[context_key]
            return {
                'total_messages': len(context.conversation_history),
                'files_uploaded': len(context.uploaded_files),
                'primary_topics': self._extract_main_topics(context),
                'expertise_level': context.expertise_level.value,
                'language_preference': context.primary_language
            }
        return {}

    def _extract_main_topics(self, context: ConversationContext) -> List[str]:
        """Extract main conversation topics for memory"""
        topics = []
        for msg in context.conversation_history[-10:]:  # Last 10 messages
            if 'intent' in msg:
                topics.append(msg['intent'])
        return list(set(topics))

    def cleanup_old_sessions(self):
        """Clean up expired conversation sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for context_key, context in self.contexts.items():
            if current_time - context.last_activity > self.session_timeout:
                expired_sessions.append(context_key)
        
        for key in expired_sessions:
            del self.contexts[key]
            
        if expired_sessions:
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions") 