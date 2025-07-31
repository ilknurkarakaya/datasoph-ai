"""
DATASOPH AI - OpenRouter Service
Integration with OpenRouter API for AI model access
"""

import httpx
from typing import Dict, List, Optional, AsyncIterator
import logging
import json
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.default_model = settings.OPENROUTER_MODEL
        
        # HTTP client configuration
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://datasoph.ai",
            "X-Title": "Datasoph AI"
        }
    
    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """
        Create a chat completion using OpenRouter API
        """
        try:
            model = model or self.default_model
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream,
                **kwargs
            }
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"Chat completion created with model: {model}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"OpenRouter API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"OpenRouter service error: {e}")
            raise
    
    async def create_streaming_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Create a streaming chat completion
        """
        try:
            model = model or self.default_model
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
                **kwargs
            }
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            
                            if data == "[DONE]":
                                break
                            
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter streaming API error: {e.response.status_code}")
            raise Exception(f"OpenRouter streaming API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"OpenRouter streaming service error: {e}")
            raise
    
    async def get_available_models(self) -> List[Dict]:
        """
        Get list of available models from OpenRouter
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                
                response.raise_for_status()
                result = response.json()
                
                logger.info("Retrieved available models from OpenRouter")
                return result.get("data", [])
                
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter models API error: {e.response.status_code}")
            raise Exception(f"OpenRouter models API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"OpenRouter models service error: {e}")
            raise
    
    async def get_model_info(self, model_id: str) -> Dict:
        """
        Get information about a specific model
        """
        try:
            models = await self.get_available_models()
            for model in models:
                if model.get("id") == model_id:
                    return model
            
            logger.warning(f"Model {model_id} not found")
            return {}
            
        except Exception as e:
            logger.error(f"Error getting model info for {model_id}: {e}")
            return {}
    
    async def estimate_cost(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None
    ) -> Dict:
        """
        Estimate the cost of a chat completion request
        """
        try:
            model = model or self.default_model
            model_info = await self.get_model_info(model)
            
            if not model_info:
                return {"error": "Model not found"}
            
            # Rough token estimation (1 token ≈ 4 characters)
            total_chars = sum(len(msg.get("content", "")) for msg in messages)
            estimated_input_tokens = total_chars // 4
            
            pricing = model_info.get("pricing", {})
            prompt_cost = float(pricing.get("prompt", "0")) * estimated_input_tokens / 1000000
            completion_cost = float(pricing.get("completion", "0")) * 1000 / 1000000  # Estimate 1000 output tokens
            
            total_estimated_cost = prompt_cost + completion_cost
            
            return {
                "model": model,
                "estimated_input_tokens": estimated_input_tokens,
                "estimated_output_tokens": 1000,
                "estimated_cost_usd": round(total_estimated_cost, 6),
                "prompt_cost_usd": round(prompt_cost, 6),
                "completion_cost_usd": round(completion_cost, 6)
            }
            
        except Exception as e:
            logger.error(f"Error estimating cost: {e}")
            return {"error": str(e)}
    
    async def get_generation_stats(self, response: Dict) -> Dict:
        """
        Extract generation statistics from OpenRouter response
        """
        try:
            usage = response.get("usage", {})
            model = response.get("model", "unknown")
            
            return {
                "model_used": model,
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
                "generation_time": response.get("generation_time"),
                "created": response.get("created", int(datetime.now().timestamp()))
            }
            
        except Exception as e:
            logger.error(f"Error extracting generation stats: {e}")
            return {}
    
    def validate_model(self, model: str) -> bool:
        """
        Validate if a model ID is in the correct format
        """
        # Basic validation for OpenRouter model format
        return "/" in model and len(model.split("/")) >= 2
    
    def get_supported_models(self) -> List[str]:
        """
        Get list of commonly supported models
        """
        return [
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-haiku",
            "anthropic/claude-3-opus",
            "openai/gpt-4-turbo",
            "openai/gpt-4",
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-2-70b-chat",
            "google/palm-2-chat-bison",
            "mistralai/mistral-7b-instruct"
        ]

# Create global instance
openrouter_service = OpenRouterService() 