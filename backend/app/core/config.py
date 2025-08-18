"""
DataSoph AI - Configuration Management
Network detection and service configuration
"""

import os
import socket
import httpx
import asyncio
import logging
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    app_name: str = "DataSoph AI"
    debug: bool = Field(default=True, env="DEBUG")  # Enable debug for development
    
    # Primary AI - OpenRouter Configuration (REQUIRED)
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_default_model: str = Field(default="anthropic/claude-3.5-sonnet", env="OPENROUTER_DEFAULT_MODEL")
    
    # Optional - Anthropic Claude Configuration (for fallback or specific use cases)
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-sonnet-20240229", env="ANTHROPIC_MODEL")
    
    network_timeout: int = Field(default=5, env="NETWORK_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    enable_advanced_services: bool = Field(default=True, env="ENABLE_ADVANCED_SERVICES")
    offline_mode: bool = Field(default=False, env="OFFLINE_MODE")
    
    max_file_size: int = Field(default=100 * 1024 * 1024, env="MAX_FILE_SIZE")
    upload_path: str = Field(default="uploads", env="UPLOAD_PATH")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

class NetworkManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._is_online: Optional[bool] = None
        self._last_check_time = 0
        self._check_interval = 30
    
    async def check_internet_connectivity(self) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.settings.network_timeout)
            result = sock.connect_ex(('8.8.8.8', 53))
            sock.close()
            return result == 0
        except Exception as e:
            logger.warning(f"Internet connectivity check failed: {e}")
            return False
    
    async def check_api_availability(self) -> bool:
        if not self.settings.openrouter_api_key:
            logger.warning("OpenRouter API key not configured")
            return False
        
        try:
            async with httpx.AsyncClient(timeout=self.settings.network_timeout) as client:
                response = await client.get(
                    f"{self.settings.openrouter_base_url}/models",
                    headers={"Authorization": f"Bearer {self.settings.openrouter_api_key}"}
                )
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"API availability check failed: {e}")
            return False
    
    async def get_network_status(self) -> Dict[str, Any]:
        import time
        current_time = time.time()
        
        if (self._is_online is not None and 
            current_time - self._last_check_time < self._check_interval):
            return {
                "online": self._is_online,
                "cached": True,
                "last_check": self._last_check_time
            }
        
        if self.settings.offline_mode:
            self._is_online = False
            self._last_check_time = current_time
            return {
                "online": False,
                "forced_offline": True,
                "last_check": current_time
            }
        
        internet_available = await self.check_internet_connectivity()
        api_available = False
        
        if internet_available:
            api_available = await self.check_api_availability()
        
        self._is_online = internet_available and api_available
        self._last_check_time = current_time
        
        return {
            "online": self._is_online,
            "internet_available": internet_available,
            "api_available": api_available,
            "cached": False,
            "last_check": current_time
        }
    
    async def is_online(self) -> bool:
        status = await self.get_network_status()
        return status["online"]

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_network_manager() -> NetworkManager:
    return NetworkManager(get_settings())

settings = get_settings()
network_manager = get_network_manager()
