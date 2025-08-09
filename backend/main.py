"""
DataSoph AI Backend - Entry Point
Professional AI-powered data science platform
"""

import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"""
🚀 DataSoph AI - Intelligent Data Science Platform
==================================================
Server starting on: http://localhost:8000
API Documentation: http://localhost:8000/docs
==================================================
    """)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 