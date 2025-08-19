"""
Core AI Service - Pure OpenRouter integration
Replaces: smart_response_generator.py + conversation complexity
NO OPENAI DEPENDENCIES - Uses only OpenRouter
"""
import os
from typing import Dict, Any
import logging
from .openrouter_client import create_openrouter_client, openrouter_chat_completion

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

logger = logging.getLogger(__name__)

class CoreAI:
    def __init__(self):
        # Pure OpenRouter setup - NO OpenAI
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not found in environment variables")
            
        self.client = create_openrouter_client(self.api_key) if self.api_key else None
        self.model = "openai/gpt-3.5-turbo"
    
    async def chat(self, message: str, user_id: str = "user") -> str:
        """Expert AI chat with multilingual support and intelligent responses"""
        if not self.client or not self.api_key:
            return "AI service not available - OpenRouter API key not configured"
        
        # Enhanced Expert AI System Prompt with Perfect Turkish Support
        system_prompt = """Sen DataSoph AI'sın - 20+ yıllık deneyime sahip dünya çapında uzman bir veri bilimcisin. İstatistik, makine öğrenmesi, veri analizi, iş zekası ve en son AI tekniklerinde derin bilgiye sahipsin.

KRİTİK DİL KURALI:
- Kullanıcının yazdığı dille AYNI DİLDE yanıt ver
- Türkçe soru gelirse Türkçe yanıtla
- İngilizce soru gelirse İngilizce yanıtla
- Her iki dilde de uzmanlık seviyeni koru

UZMANLIK ALANLARIN:
- İleri düzey istatistiksel analiz ve makine öğrenmesi
- Veri görselleştirme ve iş zekası
- Programlama (Python, R, SQL) ve veri mühendisliği
- İş stratejisi ve veri odaklı karar verme
- Araştırma metodolojisi ve bilimsel titizlik
- Eğitim ve öğretim (özellikle Python, veri analizi)

İLETİŞİM TARZI:
- Akıllı, anlayışlı ve gerçekten yardımcı ol
- Spesifik, uygulanabilir tavsiyeler ver
- Uygun teknik terminoloji kullan
- Veri bilimi kavramlarına derin anlayış göster
- Pratik, gerçek dünya çözümleri sun
- Samimi ama profesyonel ol

YANIT REHBERLERİ:
- Soruları uzman seviyesinde derinlikte yanıtla
- Uygun olduğunda kod örnekleri ver
- En iyi uygulamaları ve metodolojileri öner
- Karmaşık kavramları açık şekilde açıkla
- Uygun olduğunda birden fazla yaklaşım sun
- İş bağlamını ve pratik kısıtlamaları dikkate al
- Öğretmen gibi davran - sabırla öğret ve açıkla

ÖZELLİKLE:
- Python öğretimi için adım adım rehberlik ver
- Kod örnekleri ile açıkla
- Basit terimlerle başla, karmaşığa ilerle
- Pratik uygulamalarla destekle
- Öğrenci seviyesine göre uyarla

ASLA:
- Genel veya robotik cevaplar verme
- "Yardım edemem" deme, alternatifler sun
- Kullanıcının dil tercihini görmezden gelme
- Yüzeysel veya faydasız cevaplar verme
- Temel veri bilimi konularında şaşkın davranma
- Hata mesajları verme, her zaman yardım et

Sen kullanıcının uzman veri bilimi danışmanı ve öğretmenisin."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=3000,  # Increased for detailed teaching responses
                temperature=0.7,
                timeout=20  # Increased timeout for complex responses
            )
            
            ai_response = response.choices[0].message.content
            
            # Ensure response is helpful - never return generic errors
            if not ai_response or len(ai_response.strip()) < 10:
                # Fallback response in appropriate language
                if any(turkish_char in message.lower() for turkish_char in ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç']):
                    return "Merhaba! Ben DataSoph AI, veri bilimi uzmanıyım. Size nasıl yardımcı olabilirim? Python öğrenmek, veri analizi yapmak veya herhangi bir teknik konuda sorularınız varsa çekinmeden sorun!"
                else:
                    return "Hello! I'm DataSoph AI, your data science expert. How can I help you today? Whether you want to learn Python, analyze data, or have any technical questions, feel free to ask!"
            
            return ai_response
            
        except Exception as e:
            logger.error(f"OpenRouter AI error: {e}")
            # Always provide helpful response, never just error messages
            if any(turkish_char in message.lower() for turkish_char in ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç']):
                return """Merhaba! Ben DataSoph AI, veri bilimi uzmanıyım. 

Şu anda bağlantıda küçük bir sorun var ama size yine de yardımcı olmaya çalışayım:

🐍 **Python öğrenmek istiyorsanız:**
- Python'a giriş yapmak için temel veri tiplerinden başlayalım
- Değişkenler, listeler, döngüler gibi temel kavramları öğrenelim
- Pratik örneklerle adım adım ilerleyelim

📊 **Veri analizi konusunda:**
- Pandas ve NumPy kütüphanelerini kullanabiliriz
- Veri görselleştirme için Matplotlib/Seaborn öğrenebiliriz
- Gerçek veri setleriyle çalışabiliriz

Sorularınızı tekrar sormayı deneyin, size kesinlikle yardımcı olacağım!"""
            else:
                return """Hello! I'm DataSoph AI, your expert data scientist assistant.

I'm experiencing a minor connection issue, but let me still help you:

🐍 **If you want to learn Python:**
- We can start with basic data types and variables
- Learn fundamental concepts like lists, loops, and functions
- Practice with hands-on examples step by step

📊 **For data analysis:**
- We can explore Pandas and NumPy libraries
- Learn data visualization with Matplotlib/Seaborn
- Work with real datasets

Please try asking your question again - I'm here to help you succeed!"""

# Global instance
ai = CoreAI()
