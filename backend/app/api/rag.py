"""
DATASOPH AI - RAG API
Retrieval-Augmented Generation endpoints for document chat
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["rag"])

# Pydantic models
class RAGQuery(BaseModel):
    question: str
    collection_name: Optional[str] = "default"
    k: Optional[int] = 4
    use_conversation_history: Optional[bool] = True

class RAGResponse(BaseModel):
    answer: str
    question: str
    sources: List[Dict[str, Any]]
    confidence_score: float
    processing_time: float
    collection_used: str

class DocumentUpload(BaseModel):
    filename: str
    file_type: str
    size: int
    status: str
    collection_name: str
    chunks_created: int
    uploaded_at: str

class DocumentInfo(BaseModel):
    id: str
    filename: str
    file_type: str
    size: int
    chunks: int
    collection: str
    uploaded_at: str
    status: str

@router.post("/upload-document", response_model=DocumentUpload)
async def upload_document(
    file: UploadFile = File(...),
    collection_name: Optional[str] = "default",
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload document for RAG processing
    """
    try:
        # Validate file type
        allowed_types = ['pdf', 'docx', 'txt', 'md']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {allowed_types}"
            )
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Mock document processing
        mock_chunks = 25 if file_extension == 'pdf' else 15
        
        return DocumentUpload(
            filename=file.filename,
            file_type=file_extension,
            size=file_size,
            status="processed",
            collection_name=collection_name,
            chunks_created=mock_chunks,
            uploaded_at=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )

@router.post("/query", response_model=RAGResponse)
async def query_documents(
    query: RAGQuery,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Query documents using RAG
    """
    try:
        start_time = datetime.now()
        
        # Mock RAG response
        mock_answer = f"Based on the documents in the '{query.collection_name}' collection, I can provide the following information about your question: '{query.question}'. This is a demo response from the RAG system. In the full implementation, this would use ChromaDB vector search and LangChain to provide accurate answers with source citations."
        
        mock_sources = [
            {
                "document": "research_paper.pdf",
                "chunk_id": 1,
                "content": "Relevant excerpt from the document...",
                "similarity_score": 0.89,
                "page": 3
            },
            {
                "document": "technical_report.docx",
                "chunk_id": 7,
                "content": "Another relevant section...",
                "similarity_score": 0.84,
                "page": 12
            }
        ]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return RAGResponse(
            answer=mock_answer,
            question=query.question,
            sources=mock_sources,
            confidence_score=0.87,
            processing_time=processing_time,
            collection_used=query.collection_name
        )
        
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG query failed: {str(e)}"
        )

@router.get("/documents", response_model=List[DocumentInfo])
async def get_documents(
    collection_name: Optional[str] = None,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's uploaded documents
    """
    try:
        # Mock document list
        documents = [
            DocumentInfo(
                id="doc_1",
                filename="research_paper.pdf",
                file_type="pdf",
                size=2048000,
                chunks=25,
                collection="research",
                uploaded_at=datetime.now().isoformat(),
                status="ready"
            ),
            DocumentInfo(
                id="doc_2",
                filename="technical_report.docx",
                file_type="docx", 
                size=1024000,
                chunks=18,
                collection="reports",
                uploaded_at=datetime.now().isoformat(),
                status="ready"
            )
        ]
        
        # Filter by collection if specified
        if collection_name:
            documents = [doc for doc in documents if doc.collection == collection_name]
        
        return documents
        
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )

@router.get("/collections")
async def get_collections(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's document collections
    """
    try:
        # Mock collections
        collections = [
            {
                "name": "research",
                "document_count": 5,
                "total_chunks": 125,
                "created_at": datetime.now().isoformat()
            },
            {
                "name": "reports",
                "document_count": 3,
                "total_chunks": 78,
                "created_at": datetime.now().isoformat()
            },
            {
                "name": "default",
                "document_count": 2,
                "total_chunks": 45,
                "created_at": datetime.now().isoformat()
            }
        ]
        
        return {
            "collections": collections,
            "total": len(collections)
        }
        
    except Exception as e:
        logger.error(f"Error getting collections: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve collections"
        )

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document from RAG system
    """
    try:
        return {
            "message": f"Document {document_id} deleted successfully from RAG system"
        }
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )

@router.delete("/collections/{collection_name}")
async def delete_collection(
    collection_name: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document collection
    """
    try:
        if collection_name == "default":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete default collection"
            )
        
        return {
            "message": f"Collection '{collection_name}' deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting collection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete collection"
        )

@router.get("/health")
async def rag_health():
    """RAG service health check"""
    return {
        "status": "healthy",
        "service": "rag",
        "timestamp": datetime.now().isoformat()
    } 