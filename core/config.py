"""
DATASOPH AI - Configuration Settings
Configuration for world-class AI Data Scientist
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import ConfigDict

class Settings(BaseSettings):
    """Application settings for AI Data Scientist"""
    
    model_config = ConfigDict(
        extra='ignore',
        env_file=".env"
    )
    
    # Application
    APP_NAME: str = "DataSoph AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # AI Configuration - OpenRouter
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIRECTORY: str = "./uploads"
    
    # CORS for frontend
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size to bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    def create_directories(self):
        """Create upload directory if it doesn't exist"""
        Path(self.UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()
settings.create_directories() 