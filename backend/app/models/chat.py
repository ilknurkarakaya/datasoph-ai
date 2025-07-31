"""
DATASOPH AI - Chat Models
Database models for chat sessions and message management
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ChatSession(Base):
    """Chat session model for organizing conversations"""
    
    __tablename__ = "chat_sessions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Session details
    title = Column(String(255), nullable=False, default="New Chat")
    description = Column(Text, nullable=True)
    
    # Session configuration
    model_name = Column(String(100), default="anthropic/claude-3-sonnet")
    system_prompt = Column(Text, nullable=True)
    temperature = Column(String(10), default="0.7")
    max_tokens = Column(Integer, default=4000)
    
    # RAG configuration
    rag_enabled = Column(Boolean, default=False)
    document_ids = Column(JSON, default=list)  # List of document IDs for RAG
    
    # Session status
    is_active = Column(Boolean, default=True)
    is_pinned = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert chat session to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "model_name": self.model_name,
            "system_prompt": self.system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "rag_enabled": self.rag_enabled,
            "document_ids": self.document_ids,
            "is_active": self.is_active,
            "is_pinned": self.is_pinned,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
            "message_count": len(self.messages) if self.messages else 0
        }

class ChatMessage(Base):
    """Chat message model for storing conversation history"""
    
    __tablename__ = "chat_messages"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    
    # Message details
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    
    # Message metadata
    token_count = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    processing_time = Column(String(20), nullable=True)  # in seconds
    
    # RAG information
    rag_sources = Column(JSON, default=list)  # Source documents used
    rag_chunks = Column(JSON, default=list)  # Text chunks retrieved
    
    # Message status
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role='{self.role}', session_id={self.session_id})>"
    
    def to_dict(self):
        """Convert chat message to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "token_count": self.token_count,
            "model_used": self.model_used,
            "processing_time": self.processing_time,
            "rag_sources": self.rag_sources,
            "rag_chunks": self.rag_chunks,
            "is_edited": self.is_edited,
            "is_deleted": self.is_deleted,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 