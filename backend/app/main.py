"""
DataSoph AI Backend
World-class AI Data Scientist with comprehensive analysis capabilities
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import uuid
import shutil
from datetime import datetime
import logging
import os

from app.core.config import settings
from app.services.ai_service import datasoph_ai
from app.services.visualization_service import visualization_service
from app.services.data_quality_service import data_quality_service
from app.services.ml_service import ml_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="World-class AI Data Scientist Assistant",
    version=settings.APP_VERSION
)

# Global storage for uploaded files (in production, use a proper database)
uploaded_files = {}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIRECTORY), name="uploads")

# Models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    file_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    type: str
    message: str

class VisualizationRequest(BaseModel):
    file_id: str
    chart_type: Optional[str] = "dashboard"  # dashboard, scatter, line, bar, histogram, box, heatmap
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    color_column: Optional[str] = None
    title: Optional[str] = None

class VisualizationResponse(BaseModel):
    status: str
    visualizations: List[Dict[str, Any]]
    message: str

class DataQualityRequest(BaseModel):
    file_id: str
    generate_code: Optional[bool] = False

class DataQualityResponse(BaseModel):
    status: str
    overall_score: float
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    cleaning_code: Optional[str] = None
    message: str

class MLAnalysisRequest(BaseModel):
    file_id: str

class MLTrainingRequest(BaseModel):
    file_id: str
    target_column: str
    model_type: Optional[str] = "auto"
    task_type: Optional[str] = "auto"
    test_size: Optional[float] = 0.2
    cross_validation: Optional[bool] = True

class MLPredictionRequest(BaseModel):
    model_id: str
    file_id: str

class MLResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"🚀 {settings.APP_NAME} - World's Smartest AI Data Scientist!",
        "status": "success",
        "version": settings.APP_VERSION,
        "features": [
            "🔬 Advanced Data Analysis & ML Models",
            "📊 Statistical Tests & Insights", 
            "📈 Interactive Data Visualizations",
            "🤖 AI-Powered Smart Analysis",
            "📁 Multi-format File Support",
            "⏰ Time Series Analysis",
            "🧠 NLP & Text Analysis",
            "👁️ Computer Vision Support",
            "🗺️ Geospatial Analysis",
            "🚀 Performance Optimization"
        ]
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_configured": bool(settings.OPENROUTER_API_KEY),
        "endpoints": [
            "/", "/health", 
            "/api/v1/chat", 
            "/api/v1/upload",
            "/api/v1/visualize",
            "/api/v1/data-quality",
            "/api/v1/data/{file_id}/info",
            "/api/v1/data/{file_id}/columns",
            "/api/v1/data/{file_id}/clean-code",
            "/api/v1/ml/analyze",
            "/api/v1/ml/train",
            "/api/v1/ml/predict",
            "/api/v1/ml/models",
            "/api/v1/ml/models/{model_id}"
        ],
        "ml_libraries": [
            "scikit-learn", "xgboost", "lightgbm", "tensorflow", "pytorch",
            "statsmodels", "scipy", "plotly", "seaborn"
        ]
    }

# Add debug endpoint for troubleshooting
@app.get("/api/v1/debug/files")
async def debug_files():
    """Debug endpoint to check uploaded files"""
    return {
        "uploaded_files_count": len(uploaded_files),
        "uploaded_files": {
            file_id: {
                "filename": info["filename"],
                "size": info["size"],
                "type": info["type"],
                "uploaded_at": info["uploaded_at"],
                "file_exists": os.path.exists(info["path"])
            }
            for file_id, info in uploaded_files.items()
        },
        "upload_directory": settings.UPLOAD_DIRECTORY,
        "directory_exists": os.path.exists(settings.UPLOAD_DIRECTORY)
    }

@app.get("/api/v1/debug/system")
async def debug_system():
    """Debug endpoint to check system status"""
    try:
        from app.services.intelligent_integration_service import intelligent_system
        ai_status = "intelligent_system_available"
        health = intelligent_system.get_system_health()
    except ImportError:
        ai_status = "intelligent_system_not_available"
        health = {"error": "Import failed"}
    except Exception as e:
        ai_status = f"intelligent_system_error: {e}"
        health = {"error": str(e)}
    
    return {
        "ai_system_status": ai_status,
        "health": health,
        "upload_directory": settings.UPLOAD_DIRECTORY,
        "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
        "api_key_configured": bool(settings.OPENROUTER_API_KEY)
    }

# Chat endpoint - updated to use intelligent system orchestrator
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Enhanced chat endpoint with complete intelligent data science AI system
    """
    try:
        logger.info(f"Chat request from user {request.user_id}: {request.message[:100]}...")
        
        # Get file data if file_id provided
        file_path = None
        if request.file_id:
            # Check if file_id exists in uploaded files
            if request.file_id in uploaded_files:
                file_info = uploaded_files[request.file_id]
                file_path = file_info['path']
                logger.info(f"Using uploaded file: {file_info['filename']}")
            else:
                # Try direct path construction as fallback
                potential_path = os.path.join(settings.UPLOAD_DIRECTORY, f"{request.file_id}")
                if os.path.exists(potential_path):
                    file_path = potential_path
                else:
                    logger.warning(f"File not found for file_id: {request.file_id}")
                    file_path = None
        
        # Use the integrated intelligent system
        try:
            from app.services.intelligent_integration_service import intelligent_system
            
            # Process request through complete intelligent system
            result = await intelligent_system.process_user_request(
                user_message=request.message,
                file_path=file_path,
                user_id=request.user_id
            )
            
            logger.info(f"Intelligent system response - Status: {result['status']}, "
                       f"Response time: {result.get('metadata', {}).get('response_time', 0):.2f}s")
            
            return ChatResponse(
                response=result["response"],
                status=result["status"]
            )
            
        except ImportError as ie:
            logger.warning(f"Intelligent system not available: {ie}, falling back to original AI")
            raise Exception("Intelligent system import failed")
        except Exception as ai_error:
            logger.error(f"Intelligent system error: {ai_error}")
            raise ai_error
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        
        # Graceful fallback to original AI service
        try:
            from app.services.ai_service import datasoph_ai
            
            file_data = None
            if file_path:
                # Try to get basic file analysis
                try:
                    response = await datasoph_ai.analyze_data_comprehensive(file_path, request.message)
                except:
                    response = await datasoph_ai.chat(request.message)
            else:
                response = await datasoph_ai.chat(request.message)
                
            return ChatResponse(response=response, status="success")
            
        except Exception as fallback_error:
            logger.error(f"Fallback error: {fallback_error}")
            
            error_message = """I apologize, but I'm experiencing technical difficulties. 

**What I can still help with**:
• Data science methodology questions
• Statistical analysis guidance  
• Machine learning algorithm recommendations
• Best practices and industry insights

Please try again in a moment, or rephrase your question to be more specific about what you'd like to learn."""
            
            return ChatResponse(
                response=error_message,
                status="error"
            )

@app.post("/api/v1/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for comprehensive data analysis"""
    try:
        logger.info(f"File upload attempt: {file.filename}, content_type: {file.content_type}")
        
        # File validation
        allowed_types = [
            'text/csv', 'application/json', 'text/plain',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/csv',  # Some browsers send CSV as this
            'text/x-csv'        # Alternative CSV content type
        ]
        
        if file.content_type not in allowed_types:
            logger.warning(f"Unsupported file type: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported: {file.content_type}. Supported: CSV, Excel, JSON, TXT"
            )
        
        # Size validation
        content = await file.read()
        if len(content) > settings.max_file_size_bytes:
            logger.warning(f"File too large: {len(content)} bytes")
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
        
        # Save file
        file_id = str(uuid.uuid4())
        # Clean filename to avoid path issues
        clean_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ").strip()
        file_path = f"{settings.UPLOAD_DIRECTORY}/{file_id}_{clean_filename}"
        
        # Reset file pointer and save
        await file.seek(0)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Store file info
        uploaded_files[file_id] = {
            "filename": file.filename,
            "type": file.content_type,
            "size": len(content),
            "path": file_path,
            "uploaded_at": datetime.now().isoformat()
        }
        
        logger.info(f"File uploaded successfully: {file.filename} ({len(content)} bytes) -> {file_path}")
        
        return FileUploadResponse(
            file_id=file_id,
            filename=file.filename,
            size=len(content),
            type=file.content_type,
            message=f"✅ File uploaded successfully! Ready for AI analysis. ({len(content)/1024:.1f} KB)"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}. Please try again."
        )

@app.post("/api/v1/visualize", response_model=VisualizationResponse)
async def create_visualization(viz_request: VisualizationRequest):
    """Create advanced data visualizations"""
    try:
        file_id = viz_request.file_id
        
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found. Please upload a file first."
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Creating visualization for: {file_info['filename']}")
        
        if viz_request.chart_type == "dashboard":
            # Create comprehensive dashboard
            result = visualization_service.create_comprehensive_dashboard(file_path)
        else:
            # Create custom visualization
            result = visualization_service.create_custom_visualization(
                file_path=file_path,
                chart_type=viz_request.chart_type,
                x_column=viz_request.x_column,
                y_column=viz_request.y_column,
                color_column=viz_request.color_column,
                title=viz_request.title
            )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        if viz_request.chart_type == "dashboard":
            visualizations = result.get("visualizations", [])
            message = f"📊 Dashboard created with {len(visualizations)} visualizations!"
        else:
            visualizations = [result] if result else []
            message = f"📈 {viz_request.chart_type.title()} chart created successfully!"
        
        return VisualizationResponse(
            status="success",
            visualizations=visualizations,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Visualization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Visualization creation failed. Please try again."
        )

@app.get("/api/v1/data/{file_id}/info")
async def get_data_info(file_id: str):
    """Get detailed information about uploaded data"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        # Get comprehensive data analysis
        result = await datasoph_ai._perform_advanced_analysis(file_path)
        
        return {
            "status": "success",
            "file_info": file_info,
            "analysis": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get data information"
        )

@app.get("/api/v1/data/{file_id}/columns")
async def get_data_columns(file_id: str):
    """Get column information for visualization setup"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        # Load data to get column info
        try:
            import pandas as pd
            from pathlib import Path
            
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            else:
                raise HTTPException(400, "Unsupported file format")
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            return {
                "status": "success",
                "columns": {
                    "all": df.columns.tolist(),
                    "numeric": numeric_cols,
                    "categorical": categorical_cols,
                    "datetime": datetime_cols
                },
                "shape": {"rows": len(df), "columns": len(df.columns)},
                "data_types": df.dtypes.astype(str).to_dict()
            }
            
        except Exception as e:
            raise HTTPException(400, f"Failed to analyze file: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Column info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail="Failed to get column information"
         )

@app.post("/api/v1/data-quality", response_model=DataQualityResponse)
async def assess_data_quality(quality_request: DataQualityRequest):
    """Comprehensive data quality assessment with cleaning recommendations"""
    try:
        file_id = quality_request.file_id
        
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found. Please upload a file first."
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Assessing data quality for: {file_info['filename']}")
        
        # Perform comprehensive data quality assessment
        assessment = data_quality_service.assess_data_quality(file_path)
        
        if "error" in assessment:
            raise HTTPException(
                status_code=400,
                detail=assessment["error"]
            )
        
        cleaning_code = None
        if quality_request.generate_code:
            code_result = data_quality_service.generate_cleaning_code(file_path)
            if "error" not in code_result:
                cleaning_code = code_result.get("cleaning_code")
        
        overall_score = assessment.get("overall_score", 0)
        issues = assessment.get("issues", [])
        recommendations = assessment.get("recommendations", [])
        
        # Generate status message
        if overall_score >= 90:
            status_msg = f"🌟 Excellent data quality! Score: {overall_score:.1f}/100"
        elif overall_score >= 70:
            status_msg = f"👍 Good data quality with minor issues. Score: {overall_score:.1f}/100"
        elif overall_score >= 50:
            status_msg = f"⚠️ Moderate data quality issues detected. Score: {overall_score:.1f}/100"
        else:
            status_msg = f"❌ Significant data quality issues found. Score: {overall_score:.1f}/100"
        
        return DataQualityResponse(
            status="success",
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations,
            cleaning_code=cleaning_code,
            message=status_msg
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data quality assessment error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data quality assessment failed. Please try again."
        )

@app.get("/api/v1/data/{file_id}/clean-code")
async def get_cleaning_code(file_id: str):
    """Generate automated data cleaning code"""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Generating cleaning code for: {file_info['filename']}")
        
        # Generate cleaning code
        result = data_quality_service.generate_cleaning_code(file_path)
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "cleaning_code": result.get("cleaning_code"),
            "summary": result.get("summary"),
            "issues_addressed": result.get("issues_addressed"),
            "message": "🛠️ Automated cleaning code generated successfully!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cleaning code generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail="Failed to generate cleaning code"
         )

@app.post("/api/v1/ml/analyze", response_model=MLResponse)
async def analyze_ml_potential(ml_request: MLAnalysisRequest):
    """Analyze data and recommend ML approaches"""
    try:
        file_id = ml_request.file_id
        
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found. Please upload a file first."
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Analyzing ML potential for: {file_info['filename']}")
        
        # Perform ML analysis
        analysis = ml_service.auto_analyze_and_recommend(file_path)
        
        if "error" in analysis:
            raise HTTPException(
                status_code=400,
                detail=analysis["error"]
            )
        
        return MLResponse(
            status="success",
            message="🤖 ML analysis completed! Check recommendations for optimal models.",
            data=analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ML analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ML analysis failed. Please try again."
        )

@app.post("/api/v1/ml/train", response_model=MLResponse)
async def train_ml_model(training_request: MLTrainingRequest):
    """Train machine learning model"""
    try:
        file_id = training_request.file_id
        
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found. Please upload a file first."
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Training model for: {file_info['filename']}")
        
        # Train model
        result = ml_service.train_model(
            file_path=file_path,
            target_column=training_request.target_column,
            model_type=training_request.model_type,
            task_type=training_request.task_type,
            test_size=training_request.test_size,
            cross_validation=training_request.cross_validation
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return MLResponse(
            status="success",
            message=result.get("message", "Model trained successfully!"),
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model training error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model training failed. Please try again."
        )

@app.post("/api/v1/ml/predict", response_model=MLResponse)
async def make_predictions(prediction_request: MLPredictionRequest):
    """Make predictions using trained model"""
    try:
        model_id = prediction_request.model_id
        file_id = prediction_request.file_id
        
        if file_id not in uploaded_files:
            raise HTTPException(
                status_code=404,
                detail="File not found. Please upload a file first."
            )
        
        file_info = uploaded_files[file_id]
        file_path = file_info['path']
        
        logger.info(f"Making predictions with model {model_id}")
        
        # Make predictions
        result = ml_service.make_predictions(model_id, file_path)
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return MLResponse(
            status="success",
            message=result.get("message", "Predictions generated successfully!"),
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed. Please try again."
        )

@app.get("/api/v1/ml/models")
async def list_trained_models():
    """List all trained models"""
    try:
        result = ml_service.list_models()
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "models": result.get("models", []),
            "count": result.get("count", 0),
            "message": f"📋 Found {result.get('count', 0)} trained models"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"List models error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list models"
        )

@app.get("/api/v1/ml/models/{model_id}")
async def get_model_details(model_id: str):
    """Get detailed information about a specific model"""
    try:
        result = ml_service.get_model_info(model_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=404,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "model_info": result.get("model_info", {}),
            "message": "📊 Model information retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get model information"
        )

@app.get("/api/v1/ai/health")
async def ai_health_check():
    """
    Health check for the intelligent AI system
    """
    try:
        from app.services.intelligent_integration_service import intelligent_system
        
        health_status = intelligent_system.get_system_health()
        return {
            "status": "healthy",
            "ai_system": health_status,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0-intelligent"
        }
        
    except Exception as e:
        logger.error(f"AI health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0-intelligent"
        }

@app.get("/api/v1/ai/capabilities")
async def ai_capabilities():
    """
    Get AI system capabilities and features
    """
    return {
        "intelligent_ai": {
            "senior_data_scientist_persona": True,
            "15_years_experience": True,
            "contextual_awareness": True,
            "business_focus": True
        },
        "analytics_capabilities": [
            "Exploratory Data Analysis",
            "Statistical Hypothesis Testing", 
            "Machine Learning Modeling",
            "Time Series Forecasting",
            "Customer Analytics",
            "Business Intelligence",
            "A/B Testing",
            "Causal Inference"
        ],
        "code_generation": [
            "Production-ready Python code",
            "Statistical analysis scripts",
            "ML model pipelines", 
            "Data visualization code",
            "Best practices implementation"
        ],
        "business_intelligence": [
            "KPI analysis and monitoring",
            "Customer segmentation insights",
            "Revenue optimization recommendations",
            "Risk assessment",
            "Opportunity identification",
            "ROI analysis"
        ],
        "communication_style": {
            "professional": True,
            "business_focused": True,
            "actionable_insights": True,
            "technical_precision": True,
            "multilingual": ["English", "Turkish"]
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 