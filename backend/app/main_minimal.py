"""
DataSoph AI - MINIMAL Clean Implementation
90% code reduction while keeping ALL features
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from datetime import datetime
import pandas as pd

# Import our 3 core services
from app.services.core_ai import ai
from app.services.core_data import data  
from app.services.core_ml import ml

# Simple models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    file_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str

# FastAPI setup
app = FastAPI(title="DataSoph AI - Minimal")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Static files
os.makedirs("uploads", exist_ok=True)
os.makedirs("figures", exist_ok=True)
app.mount("/static/figures", StaticFiles(directory="figures"), name="figures")

# Global file storage (simple)
uploaded_files = {}

@app.post("/api/v1/ai/chat")
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    try:
        message = request.message
        file_id = request.file_id
        
        # Add file context if available
        if file_id and file_id in uploaded_files:
            file_info = uploaded_files[file_id]
            df = file_info.get('dataframe')
            if df is not None:
                analysis = file_info.get('analysis', {})
                context = f"""You have access to a dataset with {df.shape[0]} rows and {df.shape[1]} columns.
Columns: {', '.join(df.columns.tolist())}
Analysis: {analysis}

User question: {message}

Provide data science insights and answer their question."""
                message = context
        
        response = await ai.chat(message)
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """Simple file upload with analysis"""
    try:
        # Save file
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load and analyze data
        df = data.load_file(file_path)
        if df is None:
            return {"error": "Unsupported file type"}
        
        # Simple analysis
        analysis = data.analyze(df)
        
        # Store in memory
        uploaded_files[file_id] = {
            'filename': file.filename,
            'file_path': file_path,
            'dataframe': df,
            'analysis': analysis,
            'upload_time': datetime.now().isoformat()
        }
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "message": f"✅ File analyzed! {df.shape[0]} rows, {df.shape[1]} columns. Ask me anything about your data!",
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/auto-ml")
async def auto_ml_endpoint(file_id: str, target_column: str):
    """Simple AutoML endpoint"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_files[file_id]['dataframe']
        result = ml.auto_ml(df, target_column)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "DataSoph AI - Minimal & Clean! 🚀"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "minimal"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
