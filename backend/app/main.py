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
app.mount("/figures", StaticFiles(directory="figures"), name="figures_direct")  # Direct access

# Global file storage (simple)
uploaded_files = {}

# Conversation memory (simple)
conversation_history = {}

@app.post("/api/v1/ai/chat")
async def chat(request: ChatRequest):
    """Enhanced chat endpoint with improved file context"""
    try:
        message = request.message
        file_id = request.file_id
        user_id = request.user_id or "default_user"
        
        print(f"🔍 DEBUG - Chat request: message='{message[:50]}...', file_id={file_id}, uploaded_files_count={len(uploaded_files)}")
        
        # Initialize conversation history for user
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add current message to history
        conversation_history[user_id].append({"role": "user", "content": message})
        
        # Keep only last 10 messages to prevent context overflow
        if len(conversation_history[user_id]) > 10:
            conversation_history[user_id] = conversation_history[user_id][-10:]
        
        # Enhanced file context injection
        context_message = message
        file_context_added = False
        
        # Method 1: Direct file_id from request
        if file_id and file_id in uploaded_files:
            file_info = uploaded_files[file_id]
            filename = file_info.get('filename', 'unknown')
            file_type = file_info.get('file_type', 'unknown')
            
            print(f"✅ DEBUG - Found file context: {filename}, type={file_type}")
            
            # Get recent conversation context
            recent_context = ""
            if len(conversation_history[user_id]) > 1:
                recent_msgs = conversation_history[user_id][-4:-1]  # Last 3 messages (excluding current)
                recent_context = "RECENT CONVERSATION:\n" + "\n".join([f"- {msg['content']}" for msg in recent_msgs]) + "\n\n"
            
            if file_type == 'data':
                # Data file context
                df = file_info.get('dataframe')
                if df is not None:
                analysis = file_info.get('analysis', {})
                    
                    context_message = f"""DATASET: "{filename}" ({df.shape[0]:,} rows, {df.shape[1]} columns: {', '.join(df.columns.tolist())})

{recent_context}CURRENT REQUEST: {message}

RESPONSE GUIDELINES:
- Answer the specific question about this dataset
- For "görselleştir/visualize": Provide Python code using matplotlib/seaborn
- For "makine öğrenmesi/ML model": Suggest specific models for this data type
- For "kod yaz/write code": Write actual executable Python code
- For "analiz et/analyze": Give specific insights about patterns in the data
- For "ne anlatıyor/what does this show": Explain what the data reveals
- Use actual column names and data patterns from this dataset
- Be specific and actionable, avoid generic responses
- If charts exist at /figures/correlation.png, mention: "Chart available at http://localhost:8000/figures/correlation.png"

DATA STATS: {analysis.get('summary', {})}"""
                    
                    file_context_added = True
            
            elif file_type == 'ocr':
                # OCR file context
                ocr_content = file_info.get('ocr_content', {})
                extracted_text = ocr_content.get('text', '')
                word_count = ocr_content.get('word_count', 0)
                content_type = ocr_content.get('content_type', 'document')
                confidence = ocr_content.get('confidence', 0)
                
                if extracted_text.strip():
                    # Include document content in context
                    context_message = f"""DOCUMENT: "{filename}" ({content_type}, {word_count} words, {confidence:.1f}% OCR confidence)

DOCUMENT CONTENT:
{extracted_text}

{recent_context}CURRENT REQUEST: {message}

RESPONSE GUIDELINES:
- Answer questions about the document content above
- For "özetle/summarize": Provide a clear summary of the document
- For "analiz et/analyze": Analyze the document content and key points
- For "çevir/translate": Translate the document content
- For "önemli noktalar/key points": Extract main points from the document
- For "kod yaz/write code": Write code to process this text data
- Reference specific content from the document in your response
- Be specific about what the document contains
- Quote relevant sections when answering questions

DOCUMENT TYPE: {content_type}"""
                else:
                    # No text extracted
                    context_message = f"""DOCUMENT: "{filename}" (OCR processed but no text extracted)

{recent_context}CURRENT REQUEST: {message}

NOTE: This document was processed with OCR but no readable text was found. This could be:
- An image without text
- A complex document layout
- Poor image quality
- Unsupported language or format

RESPONSE GUIDELINES:
- Inform user that no text content was extracted
- Suggest ways to improve OCR results (better image quality, different format)
- Offer to help with other types of analysis if possible"""
                
                file_context_added = True
        
        # Method 2: Auto-detect latest uploaded file if no file_id provided
        elif not file_id and len(uploaded_files) > 0:
            # Get the most recent file
            latest_file_id = max(uploaded_files.keys(), key=lambda k: uploaded_files[k].get('upload_time', ''))
            latest_file = uploaded_files[latest_file_id]
            filename = latest_file.get('filename', 'unknown')
            file_type = latest_file.get('file_type', 'unknown')
            
            print(f"🔗 DEBUG - Auto-detected latest file: {filename}, type={file_type}")
            
            # Get recent conversation context
            recent_context = ""
            if len(conversation_history[user_id]) > 1:
                recent_msgs = conversation_history[user_id][-4:-1]  # Last 3 messages (excluding current)
                recent_context = "RECENT CONVERSATION:\n" + "\n".join([f"- {msg['content']}" for msg in recent_msgs]) + "\n\n"
            
            if file_type == 'data':
                # Auto-detected data file
                df = latest_file.get('dataframe')
                if df is not None:
                    analysis = latest_file.get('analysis', {})
                    
                    context_message = f"""DATASET: "{filename}" ({df.shape[0]:,} rows, {df.shape[1]} columns: {', '.join(df.columns.tolist())})

{recent_context}CURRENT REQUEST: {message}

RESPONSE GUIDELINES:
- Answer the specific question about this dataset
- For "görselleştir/visualize": Provide Python code using matplotlib/seaborn
- For "makine öğrenmesi/ML model": Suggest specific models for this data type
- For "kod yaz/write code": Write actual executable Python code
- For "analiz et/analyze": Give specific insights about patterns in the data
- For "ne anlatıyor/what does this show": Explain what the data reveals
- Use actual column names and data patterns from this dataset
- Be specific and actionable, avoid generic responses
- If charts exist at /figures/correlation.png, mention: "Chart available at http://localhost:8000/figures/correlation.png"

DATA STATS: {analysis.get('summary', {})}"""
                    
                    file_context_added = True
            
            elif file_type == 'ocr':
                # Auto-detected OCR file
                ocr_content = latest_file.get('ocr_content', {})
                extracted_text = ocr_content.get('text', '')
                word_count = ocr_content.get('word_count', 0)
                content_type = ocr_content.get('content_type', 'document')
                confidence = ocr_content.get('confidence', 0)
                
                if extracted_text.strip():
                    context_message = f"""DOCUMENT: "{filename}" ({content_type}, {word_count} words, {confidence:.1f}% OCR confidence)

DOCUMENT CONTENT:
{extracted_text}

{recent_context}CURRENT REQUEST: {message}

RESPONSE GUIDELINES:
- Answer questions about the document content above
- For "özetle/summarize": Provide a clear summary of the document
- For "analiz et/analyze": Analyze the document content and key points
- For "çevir/translate": Translate the document content
- For "önemli noktalar/key points": Extract main points from the document
- For "kod yaz/write code": Write code to process this text data
- Reference specific content from the document in your response
- Be specific about what the document contains
- Quote relevant sections when answering questions

DOCUMENT TYPE: {content_type}"""
                else:
                    context_message = f"""DOCUMENT: "{filename}" (OCR processed but no text extracted)

{recent_context}CURRENT REQUEST: {message}

NOTE: This document was processed with OCR but no readable text was found.

RESPONSE GUIDELINES:
- Inform user that no text content was extracted
- Suggest ways to improve OCR results
- Offer alternative analysis approaches"""
                
                file_context_added = True
        
        if not file_context_added:
            print("⚠️ DEBUG - No file context found")
            if len(uploaded_files) == 0:
                print("📁 DEBUG - No files uploaded yet")
            else:
                print(f"📁 DEBUG - Available files: {list(uploaded_files.keys())}")
        
        response = await ai.chat(context_message)
        
        # Add AI response to conversation history
        conversation_history[user_id].append({"role": "assistant", "content": response})
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        print(f"❌ DEBUG - Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """Enhanced file upload with OCR and data analysis support"""
    try:
        # Clear old uploaded files to prevent memory issues
        global uploaded_files
        old_count = len(uploaded_files)
        uploaded_files.clear()  # Clear old files for fresh context
        
        if old_count > 0:
            print(f"🔄 DEBUG - Cleared {old_count} old file(s) for fresh context")
        
        # Save file
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"📁 DEBUG - Saved file: {file.filename} -> {file_id}")
        
        # Import the enhanced file handler
        from app.services.universal_file_handler import handler
        
        # Process file to detect type and extract content
        processing_result = handler.detect_and_process(file_path)
        
        if not processing_result.get('success'):
            return {"error": processing_result.get('error', 'File processing failed')}
        
        file_type = processing_result['processing_result'].get('type')
        
        if file_type == 'data':
            # Handle data files (CSV, Excel, JSON)
        df = data.load_file(file_path)
        if df is None:
                return {"error": "Failed to load data file"}
            
            print(f"📊 DEBUG - Loaded data: shape={df.shape}, columns={df.columns.tolist()}")
        
        # Simple analysis
        analysis = data.analyze(df)
        
            # Store in memory with enhanced metadata
        uploaded_files[file_id] = {
            'filename': file.filename,
            'file_path': file_path,
                'file_type': 'data',
            'dataframe': df,
            'analysis': analysis,
                'upload_time': datetime.now().isoformat(),
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': dict(df.dtypes.astype(str)),
                'ocr_content': None
            }
            
            print(f"💾 DEBUG - Stored data file in memory: file_id={file_id}, total_files={len(uploaded_files)}")
            
            return {
                "file_id": file_id,
                "filename": file.filename,
                "file_type": "data",
                "message": f"✅ Data file analyzed! {df.shape[0]} rows, {df.shape[1]} columns. Ask me anything about your data!",
                "analysis": analysis,
                "shape": df.shape,
                "columns": df.columns.tolist()
            }
            
        elif file_type == 'ocr':
            # Handle OCR files (PDF, images)
            ocr_content = processing_result['processing_result'].get('ocr_content', {})
            extracted_text = ocr_content.get('text', '')
            confidence = ocr_content.get('confidence', 0)
            method = ocr_content.get('method', 'unknown')
            analysis = ocr_content.get('analysis', {})
            
            print(f"📄 DEBUG - OCR extracted {len(extracted_text)} characters using {method} (confidence: {confidence:.1f}%)")
            
            if not extracted_text.strip():
                print(f"⚠️ DEBUG - No text extracted from {file.filename}")
                message = f"⚠️ File uploaded but no text could be extracted. This might be an image without text or a complex PDF."
            else:
                word_count = analysis.get('word_count', 0)
                content_type = analysis.get('content_type', 'document')
                message = f"✅ Document processed! Extracted {len(extracted_text)} characters, {word_count} words. Content type: {content_type}. Ask me about the document content!"
            
            # Store in memory with OCR metadata
            uploaded_files[file_id] = {
                'filename': file.filename,
                'file_path': file_path,
                'file_type': 'ocr',
                'dataframe': None,
                'analysis': None,
                'upload_time': datetime.now().isoformat(),
                'shape': None,
                'columns': None,
                'dtypes': None,
                'ocr_content': {
                    'text': extracted_text,
                    'method': method,
                    'confidence': confidence,
                    'word_count': analysis.get('word_count', 0),
                    'char_count': analysis.get('char_count', 0),
                    'content_type': analysis.get('content_type', 'document'),
                    'summary': analysis.get('summary', 'No content summary available')
                }
            }
            
            print(f"💾 DEBUG - Stored OCR file in memory: file_id={file_id}, total_files={len(uploaded_files)}")
        
        return {
            "file_id": file_id,
            "filename": file.filename,
                "file_type": "ocr",
                "message": message,
                "ocr_content": {
                    'text_length': len(extracted_text),
                    'word_count': analysis.get('word_count', 0),
                    'confidence': confidence,
                    'method': method,
                    'content_type': analysis.get('content_type', 'document'),
                    'preview': extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                }
            }
        
        else:
            return {"error": f"Unknown file type: {file_type}"}
        
    except Exception as e:
        print(f"❌ DEBUG - Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Existing route için alias ekle
@app.post("/upload")
async def upload_file_alias(file: UploadFile = File(...)):
    return await upload_file(file)  # Existing endpoint'i çağır

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
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
@app.post("/api/v1/clear-data-context")
async def clear_data_context():
    """Clear all uploaded files and context"""
    global uploaded_files
    old_count = len(uploaded_files)
    uploaded_files.clear()
    print(f"🗑️ DEBUG - Cleared {old_count} files from context")
    return {"message": f"Data context cleared. Removed {old_count} file(s).", "files_cleared": old_count}

@app.get("/api/v1/debug/files")
async def debug_files():
    """Debug endpoint to check uploaded files status"""
    files_info = {}
    for file_id, file_data in uploaded_files.items():
        file_info = {
            "filename": file_data.get("filename"),
            "upload_time": file_data.get("upload_time"),
            "file_type": file_data.get("file_type", "unknown")
        }
        
        if file_data.get("file_type") == "data":
            file_info.update({
                "shape": file_data.get("shape"),
                "columns": file_data.get("columns"),
                "has_dataframe": file_data.get("dataframe") is not None
            })
        elif file_data.get("file_type") == "ocr":
            ocr_content = file_data.get("ocr_content", {})
            file_info.update({
                "text_length": len(ocr_content.get("text", "")),
                "word_count": ocr_content.get("word_count", 0),
                "confidence": ocr_content.get("confidence", 0),
                "content_type": ocr_content.get("content_type", "unknown"),
                "has_text": bool(ocr_content.get("text", "").strip())
            })
        
        files_info[file_id] = file_info
    
    return {
        "total_files": len(uploaded_files),
        "files": files_info,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/charts")
async def list_charts():
    """List available charts"""
    import os
    charts = []
    if os.path.exists("figures"):
        for file in os.listdir("figures"):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                charts.append({
                    "filename": file,
                    "url": f"http://localhost:8000/figures/{file}",
                    "path": f"/figures/{file}"
                })
    
    return {
        "charts": charts,
        "total": len(charts),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    return await upload_file(file)
