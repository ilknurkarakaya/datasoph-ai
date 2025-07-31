"""
DATASOPH AI - Document Models
Database models for document management and RAG system
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    """Document model for file management and RAG system"""
    
    __tablename__ = "documents"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, txt, csv
    file_size = Column(Integer, nullable=False)  # in bytes
    file_path = Column(String(500), nullable=False)
    
    # Document metadata
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processing_error = Column(Text, nullable=True)
    
    # Vector store information
    vector_store_id = Column(String(100), nullable=True)
    collection_name = Column(String(100), nullable=True)
    chunk_count = Column(Integer, default=0)
    
    # Document statistics
    word_count = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)
    character_count = Column(Integer, nullable=True)
    
    # Access control
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Tags and categories
    tags = Column(JSON, default=list)
    category = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert document to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "file_path": self.file_path,
            "title": self.title,
            "description": self.description,
            "language": self.language,
            "is_processed": self.is_processed,
            "processing_status": self.processing_status,
            "processing_error": self.processing_error,
            "vector_store_id": self.vector_store_id,
            "collection_name": self.collection_name,
            "chunk_count": self.chunk_count,
            "word_count": self.word_count,
            "page_count": self.page_count,
            "character_count": self.character_count,
            "is_public": self.is_public,
            "is_active": self.is_active,
            "tags": self.tags,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }

class DocumentChunk(Base):
    """Document chunk model for RAG text chunks"""
    
    __tablename__ = "document_chunks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Chunk information
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=True)  # SHA256 hash of content
    
    # Chunk metadata
    chunk_type = Column(String(50), default="text")  # text, table, image_description
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(255), nullable=True)
    
    # Vector information
    embedding_model = Column(String(100), nullable=True)
    vector_id = Column(String(100), nullable=True)  # ID in vector store
    
    # Chunk statistics
    word_count = Column(Integer, nullable=True)
    character_count = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    
    # Quality metrics
    similarity_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, chunk_index={self.chunk_index}, document_id={self.document_id})>"
    
    def to_dict(self):
        """Convert document chunk to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "chunk_index": self.chunk_index,
            "content": self.content,
            "content_hash": self.content_hash,
            "chunk_type": self.chunk_type,
            "page_number": self.page_number,
            "section_title": self.section_title,
            "embedding_model": self.embedding_model,
            "vector_id": self.vector_id,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "token_count": self.token_count,
            "similarity_score": self.similarity_score,
            "relevance_score": self.relevance_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 