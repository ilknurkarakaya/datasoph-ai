"""
DATASOPH AI - AI Chat Feature
Simple AI chat functionality that takes user input and generates responses
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIChatFeature:
    """
    AI Chat Feature - Core functionality for AI conversations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Chat Feature
        
        Args:
            api_key: OpenRouter API key (optional, can be set via environment)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.conversation_history: List[Dict] = []
        self.model = "anthropic/claude-3-sonnet"
        
        if not self.api_key:
            logger.warning("No API key provided. Using mock responses for demo.")
    
    def add_message_to_history(self, role: str, content: str) -> None:
        """
        Add message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_conversation_context(self) -> List[Dict]:
        """
        Get conversation context for API calls
        
        Returns:
            List of messages in OpenAI format
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history[-10:]  # Keep last 10 messages
        ]
    
    def call_openrouter_api(self, messages: List[Dict]) -> Optional[str]:
        """
        Call OpenRouter API to get AI response
        
        Args:
            messages: List of conversation messages
            
        Returns:
            AI response text or None if error
        """
        if not self.api_key:
            return self._get_mock_response(messages[-1]["content"])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://datasoph.ai",
            "X-Title": "DATASOPH AI"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return self._get_mock_response(messages[-1]["content"])
                
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return self._get_mock_response(messages[-1]["content"])
    
    def _get_mock_response(self, user_message: str) -> str:
        """
        Generate mock response when API is not available
        
        Args:
            user_message: User's input message
            
        Returns:
            Mock AI response
        """
        message_lower = user_message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm DATASOPH AI, your intelligent data science assistant. How can I help you today?"
        
        elif "data" in message_lower or "analysis" in message_lower:
            return "I can help you with data analysis! You can upload CSV files, Excel spreadsheets, or ask me questions about your data. What would you like to analyze?"
        
        elif "statistics" in message_lower or "stats" in message_lower:
            return "I'm well-versed in statistics! I can help with t-tests, ANOVA, correlation analysis, regression, and more. What statistical analysis do you need?"
        
        elif "help" in message_lower:
            return "I can help you with data analysis, statistical tests, data visualization, machine learning recommendations, and business intelligence insights. What would you like to work on?"
        
        elif "?" in user_message:
            return f"I understand you're asking about: '{user_message}'. I can help you with this topic. Would you like me to provide more detailed information or help you analyze related data?"
        
        else:
            return f"I see you're discussing: '{user_message}'. This is an interesting topic! I can help you analyze data related to this, create visualizations, or provide statistical insights. How would you like to proceed?"
    
    def chat(self, user_message: str) -> Dict:
        """
        Main chat function - process user input and generate AI response
        
        Args:
            user_message: User's input message
            
        Returns:
            Dictionary with AI response and metadata
        """
        try:
            # Add user message to history
            self.add_message_to_history("user", user_message)
            
            # Get conversation context
            messages = self.get_conversation_context()
            
            # Get AI response
            ai_response = self.call_openrouter_api(messages)
            
            if ai_response:
                # Add AI response to history
                self.add_message_to_history("assistant", ai_response)
                
                return {
                    "success": True,
                    "response": ai_response,
                    "model_used": self.model,
                    "timestamp": datetime.now().isoformat(),
                    "conversation_length": len(self.conversation_history)
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate response",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                "success": False,
                "error": f"Chat processing error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_conversation_summary(self) -> Dict:
        """
        Get summary of current conversation
        
        Returns:
            Dictionary with conversation summary
        """
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len([m for m in self.conversation_history if m["role"] == "user"]),
            "ai_messages": len([m for m in self.conversation_history if m["role"] == "assistant"]),
            "start_time": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "last_message": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def export_conversation(self, filename: str = None) -> str:
        """
        Export conversation to JSON file
        
        Args:
            filename: Optional filename, defaults to timestamp
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        export_data = {
            "conversation": self.conversation_history,
            "summary": self.get_conversation_summary(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Conversation exported to {filename}")
        return filename


def main():
    """
    Demo function to test AI Chat Feature
    """
    print("🤖 DATASOPH AI - Chat Feature Demo")
    print("=" * 50)
    
    # Initialize AI Chat Feature
    ai_chat = AIChatFeature()
    
    print("AI Chat initialized! Type 'quit' to exit.")
    print("You can ask me about data analysis, statistics, or any other topics.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 AI: Goodbye! Thanks for using DATASOPH AI!")
                break
            
            if not user_input:
                continue
            
            # Get AI response
            result = ai_chat.chat(user_input)
            
            if result["success"]:
                print(f"\n🤖 AI: {result['response']}")
                print(f"📊 Model: {result['model_used']}")
            else:
                print(f"\n❌ Error: {result['error']}")
        
        except KeyboardInterrupt:
            print("\n\n🤖 AI: Goodbye! Thanks for using DATASOPH AI!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    # Show conversation summary
    summary = ai_chat.get_conversation_summary()
    print(f"\n📈 Conversation Summary:")
    print(f"   Total messages: {summary['total_messages']}")
    print(f"   User messages: {summary['user_messages']}")
    print(f"   AI messages: {summary['ai_messages']}")


if __name__ == "__main__":
    main() 