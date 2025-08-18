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
from pathlib import Path
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
        
        # Add file context if available (data files or documents)
        if file_id and file_id in uploaded_files:
            file_info = uploaded_files[file_id]
            file_type = file_info.get('file_type', 'unknown')
            
            if file_type == 'data':
                # Data file context
                df = file_info.get('dataframe')
                if df is not None:
                    analysis = file_info.get('analysis', {})
                    context = f"""DATASET CONTEXT:
You have access to a dataset with {df.shape[0]} rows and {df.shape[1]} columns.
Columns: {', '.join(df.columns.tolist())}
Analysis: {analysis}

USER QUESTION: {message}

INSTRUCTIONS:
- Respond in the SAME LANGUAGE as the user's question
- Provide expert data science insights about this specific dataset
- Be intelligent, helpful, and specific
- Use actual data from the columns and analysis above
- Give actionable recommendations
- If user asks in Turkish, respond in Turkish
- If user asks in English, respond in English"""
                    message = context
            
            elif file_type == 'document':
                # Document content context
                text_content = file_info.get('text_content', {})
                if text_content and text_content.get('text'):
                    extracted_text = text_content['text']
                    content_type = text_content.get('content_type', 'document')
                    word_count = text_content.get('word_count', 0)
                    
                    context = f"""DOCUMENT CONTEXT:
You have access to this document content:

DOCUMENT TYPE: {content_type}
WORD COUNT: {word_count}

DOCUMENT CONTENT:
{extracted_text}

USER QUESTION: {message}

INSTRUCTIONS:
- Respond in the SAME LANGUAGE as the user's question
- Answer questions about the document content above
- For "summarize" or "özetle": Provide a clear summary
- For "translate" or "çevir": Translate the content 
- For "key points" or "önemli noktalar": Extract main points
- For "analyze" or "analiz et": Analyze the content
- Reference specific parts of the document in your response
- Be intelligent, helpful, and provide expert insights
- If user asks in Turkish, respond in Turkish
- If user asks in English, respond in English"""
                    message = context
        
        # Auto-detect latest file if no file_id provided
        elif len(uploaded_files) > 0:
            # Get most recent file
            latest_file_id = max(uploaded_files.keys(), key=lambda k: uploaded_files[k].get('upload_time', ''))
            file_info = uploaded_files[latest_file_id]
            file_type = file_info.get('file_type', 'unknown')
            
            if file_type == 'data':
                df = file_info.get('dataframe')
                if df is not None:
                    analysis = file_info.get('analysis', {})
                    context = f"""RECENT DATASET CONTEXT:
You have access to a recently uploaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.
Columns: {', '.join(df.columns.tolist())}

USER QUESTION: {message}

INSTRUCTIONS:
- Respond in the SAME LANGUAGE as the user's question
- Provide expert insights about this specific dataset
- Be intelligent, helpful, and actionable
- Use the actual column names and data structure
- If user asks in Turkish, respond in Turkish
- If user asks in English, respond in English"""
                    message = context
            
            elif file_type == 'document':
                text_content = file_info.get('text_content', {})
                if text_content and text_content.get('text'):
                    extracted_text = text_content['text']
                    content_type = text_content.get('content_type', 'document')
                    
                    context = f"""RECENT DOCUMENT CONTEXT:
You have access to this recently uploaded document:

DOCUMENT TYPE: {content_type}

DOCUMENT CONTENT:
{extracted_text}

USER QUESTION: {message}

INSTRUCTIONS:
- Respond in the SAME LANGUAGE as the user's question
- Answer questions about this document content
- Be intelligent, helpful, and provide expert insights
- Reference specific parts of the document
- If user asks in Turkish, respond in Turkish
- If user asks in English, respond in English"""
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
        
        # Universal file processing with OCR
        from app.universal_ocr import universal_ocr
        
        # Try data file first (CSV, Excel)
        df = data.load_file(file_path)
        
        if df is not None:
            # Data file processing
            print(f"📊 DEBUG - Loaded data: shape={df.shape}, columns={df.columns.tolist()}")
            
            analysis = data.analyze(df)
            
            uploaded_files[file_id] = {
                'filename': file.filename,
                'file_path': file_path,
                'file_type': 'data',
                'dataframe': df,
                'analysis': analysis,
                'upload_time': datetime.now().isoformat(),
                'text_content': None
            }
            
            print(f"💾 DEBUG - Stored data file: file_id={file_id}")
            
            return {
                "file_id": file_id,
                "filename": file.filename,
                "file_type": "data",
                "message": f"✅ Data file analyzed! {df.shape[0]} rows, {df.shape[1]} columns. Ask me anything about your data!",
                "analysis": analysis
            }
        
        else:
            # Try universal OCR for documents/images
            if universal_ocr.is_supported(file_path):
                print(f"📄 DEBUG - Processing with universal OCR: {file.filename}")
                ocr_result = universal_ocr.extract_text(file_path)
                
                if ocr_result['success']:
                    extracted_text = ocr_result['text']
                    method = ocr_result['method']
                    content_type = universal_ocr.get_content_type(file_path, extracted_text)
                    
                    print(f"📝 DEBUG - OCR extracted {len(extracted_text)} characters using {method}")
                    
                    uploaded_files[file_id] = {
                        'filename': file.filename,
                        'file_path': file_path,
                        'file_type': 'document',
                        'dataframe': None,
                        'analysis': None,
                        'upload_time': datetime.now().isoformat(),
                        'text_content': {
                            'text': extracted_text,
                            'method': method,
                            'content_type': content_type,
                            'word_count': len(extracted_text.split()),
                            'char_count': len(extracted_text)
                        }
                    }
                    
                    print(f"💾 DEBUG - Stored document: file_id={file_id}")
                    
                    word_count = len(extracted_text.split())
                    preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                    
                    return {
                        "file_id": file_id,
                        "filename": file.filename,
                        "file_type": "document",
                        "message": f"✅ Document processed! Extracted {len(extracted_text)} characters, {word_count} words from {content_type}. Ask me about the content!",
                        "content": {
                            "method": method,
                            "content_type": content_type,
                            "word_count": word_count,
                            "char_count": len(extracted_text),
                            "preview": preview
                        }
                    }
                else:
                    return {"error": f"Could not extract text: {ocr_result.get('error', 'Unknown error')}"}
            
            else:
                return {"error": f"Unsupported file type: {Path(file_path).suffix}"}
        
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

# Existing route için alias ekle
@app.post("/upload")
async def upload_file_alias(file: UploadFile = File(...)):
    return await upload_file(file)  # Existing endpoint'i çağır

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "minimal"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
