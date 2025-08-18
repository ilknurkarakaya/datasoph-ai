"""
OpenRouter Client - Pure OpenRouter implementation without OpenAI dependencies
Replaces all OpenAI functionality with direct OpenRouter API calls using requests
"""

import os
import requests
import json
import time
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OpenRouterMessage:
    role: str
    content: str

@dataclass
class OpenRouterChoice:
    index: int
    message: OpenRouterMessage
    finish_reason: str

@dataclass
class OpenRouterUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class OpenRouterResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[OpenRouterChoice]
    usage: OpenRouterUsage

class OpenRouterClient:
    """Pure OpenRouter client implementation using requests library"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url
        
        if not self.api_key:
            logger.warning("OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable.")
            
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """Setup requests session with default headers"""
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://datasoph.ai",  # Optional: Your site URL
                "X-Title": "DataSoph AI"  # Optional: Your app name
            })
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to OpenRouter API"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.post(url, json=data, timeout=60)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request failed: {e}")
            raise Exception(f"OpenRouter API error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenRouter response: {e}")
            raise Exception(f"Invalid response from OpenRouter: {str(e)}")
    
    def chat_completions_create(
        self,
        model: str = "anthropic/claude-3.5-sonnet",
        messages: List[Dict[str, str]] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stream: bool = False,
        **kwargs
    ) -> OpenRouterResponse:
        """
        Create chat completion using OpenRouter API
        
        Args:
            model: OpenRouter model identifier (e.g., "anthropic/claude-3.5-sonnet")
            messages: List of message objects with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
            stream: Whether to stream the response
            **kwargs: Additional parameters
            
        Returns:
            OpenRouterResponse object with choices and usage information
        """
        if not self.api_key:
            raise Exception("OpenRouter API key not configured")
            
        if messages is None:
            messages = []
            
        # Prepare request data
        request_data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stream": stream,
            **kwargs
        }
        
        # Remove None values
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        logger.info(f"Making OpenRouter request to model: {model}")
        
        try:
            response_data = self._make_request("chat/completions", request_data)
            
            # Parse response into structured format
            choices = []
            for choice_data in response_data.get("choices", []):
                message_data = choice_data.get("message", {})
                message = OpenRouterMessage(
                    role=message_data.get("role", "assistant"),
                    content=message_data.get("content", "")
                )
                
                choice = OpenRouterChoice(
                    index=choice_data.get("index", 0),
                    message=message,
                    finish_reason=choice_data.get("finish_reason", "stop")
                )
                choices.append(choice)
            
            # Parse usage information
            usage_data = response_data.get("usage", {})
            usage = OpenRouterUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            )
            
            # Create response object
            openrouter_response = OpenRouterResponse(
                id=response_data.get("id", ""),
                object=response_data.get("object", "chat.completion"),
                created=response_data.get("created", int(time.time())),
                model=response_data.get("model", model),
                choices=choices,
                usage=usage
            )
            
            logger.info(f"OpenRouter request completed. Tokens used: {usage.total_tokens}")
            return openrouter_response
            
        except Exception as e:
            logger.error(f"OpenRouter chat completion failed: {e}")
            raise

class OpenRouterChatCompletions:
    """Chat completions interface compatible with OpenAI SDK style"""
    
    def __init__(self, client: OpenRouterClient):
        self.client = client
    
    def create(self, **kwargs) -> OpenRouterResponse:
        """Create chat completion - OpenAI SDK compatible interface"""
        return self.client.chat_completions_create(**kwargs)

class OpenRouterChat:
    """Chat interface compatible with OpenAI SDK style"""
    
    def __init__(self, client: OpenRouterClient):
        self.completions = OpenRouterChatCompletions(client)

# Main OpenRouter client class that mimics OpenAI SDK structure
class OpenRouter:
    """
    Main OpenRouter client class
    Drop-in replacement for OpenAI client with OpenRouter functionality
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.client = OpenRouterClient(api_key, base_url)
        self.chat = OpenRouterChat(self.client)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from OpenRouter"""
        try:
            url = f"{self.client.base_url}/models"
            response = self.client.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            return []
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        models = self.get_available_models()
        for model in models:
            if model.get("id") == model_id:
                return model
        return {}

# Utility functions for easy migration from OpenAI
def create_openrouter_client(api_key: Optional[str] = None) -> OpenRouter:
    """Create OpenRouter client instance"""
    return OpenRouter(api_key)

def openrouter_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "anthropic/claude-3.5-sonnet",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Simple function to get chat completion from OpenRouter
    
    Args:
        messages: List of message objects
        model: OpenRouter model identifier
        api_key: OpenRouter API key (optional, uses env var if not provided)
        **kwargs: Additional parameters for the API call
        
    Returns:
        The content of the first choice message
    """
    client = create_openrouter_client(api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "No response generated"
            
    except Exception as e:
        logger.error(f"OpenRouter chat completion failed: {e}")
        return f"Error: {str(e)}"

# Default model configurations
DEFAULT_MODELS = {
    "fast": "anthropic/claude-3-haiku",
    "balanced": "anthropic/claude-3.5-sonnet", 
    "powerful": "anthropic/claude-3-opus",
    "coding": "anthropic/claude-3.5-sonnet",
    "analysis": "anthropic/claude-3.5-sonnet"
}

def get_recommended_model(task_type: str = "balanced") -> str:
    """Get recommended model for specific task type"""
    return DEFAULT_MODELS.get(task_type, DEFAULT_MODELS["balanced"])

# Test function
def test_openrouter_connection(api_key: Optional[str] = None) -> Dict[str, Any]:
    """Test OpenRouter connection and return status"""
    try:
        client = create_openrouter_client(api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="anthropic/claude-3-haiku",  # Use fastest model for testing
            messages=[{"role": "user", "content": "Hello! Just testing the connection."}],
            max_tokens=50
        )
        
        return {
            "success": True,
            "message": "OpenRouter connection successful",
            "model": response.model,
            "tokens_used": response.usage.total_tokens,
            "response_preview": response.choices[0].message.content[:100] if response.choices else "No response"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"OpenRouter connection failed: {str(e)}",
            "error": str(e)
        }

if __name__ == "__main__":
    # Test the client
    test_result = test_openrouter_connection()
    print(f"OpenRouter Test Result: {test_result}")
