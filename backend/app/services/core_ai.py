"""
Core AI Service - Minimal OpenAI/OpenRouter integration
Replaces: smart_response_generator.py + conversation complexity
"""
import openai
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CoreAI:
    def __init__(self):
        # Simple OpenRouter setup
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.client = openai.OpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = "anthropic/claude-3.5-sonnet"
        else:
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4"
    
    async def chat(self, message: str, user_id: str = "user") -> str:
        """Simple chat - no complexity"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

# Global instance
ai = CoreAI()
