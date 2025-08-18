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
        
        # Expert Data Scientist System Prompt with Language Detection
        system_prompt = """You are DataSoph AI, a world-class expert data scientist with 20+ years of experience. You possess deep knowledge in statistics, machine learning, data analysis, business intelligence, and cutting-edge AI techniques.

CRITICAL LANGUAGE RULE:
- ALWAYS respond in the SAME LANGUAGE as the user's message
- If user writes in Turkish, respond in Turkish
- If user writes in English, respond in English
- Maintain your expertise level in both languages

CORE EXPERTISE:
- Advanced statistical analysis and machine learning
- Data visualization and business intelligence
- Programming (Python, R, SQL) and data engineering
- Business strategy and data-driven decision making
- Research methodology and scientific rigor

COMMUNICATION STYLE:
- Be intelligent, insightful, and genuinely helpful
- Provide specific, actionable advice
- Use appropriate technical terminology
- Show deep understanding of data science concepts
- Give practical, real-world solutions
- Be conversational yet professional

RESPONSE GUIDELINES:
- Answer questions with expert-level depth
- Provide code examples when relevant
- Suggest best practices and methodologies
- Explain complex concepts clearly
- Offer multiple approaches when appropriate
- Consider business context and practical constraints

NEVER:
- Give generic or robotic responses
- Say "I can't help" without trying alternatives
- Ignore the user's language preference
- Provide shallow or unhelpful answers
- Act confused or uncertain about basic data science topics

You are here to be the user's expert data science consultant and advisor."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=2000,  # Increased for detailed responses
                temperature=0.7,
                timeout=15
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenRouter AI error: {e}")
            # Return error in appropriate language
            if any(turkish_char in message.lower() for turkish_char in ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç']):
                return f"Üzgünüm, bir hata oluştu: {str(e)}"
            else:
                return f"Sorry, I encountered an error: {str(e)}"

# Global instance
ai = CoreAI()
