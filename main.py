# Render deployment - Import from actual app
from backend.app.main import app

# Re-export the app for uvicorn
__all__ = ['app']