"""
DATASOPH AI - Document Processor
Intelligent document processing with support for PDF, DOCX, TXT, and CSV files
"""

from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from typing import List, Dict, Any, Optional
import os
import hashlib
import logging
from pathlib import Path
import pandas as pd
import docx2txt

from app.core.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Advanced document processing with intelligent chunking"""
    
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        
        # Initialize text splitters
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )
        
        self.token_splitter = TokenTextSplitter(
            chunk_size=self.chunk_size // 4,  # Approximate token count
            chunk_overlap=self.chunk_overlap // 4
        )
    
    async def process_document(
        self,
        file_path: str,
        file_type: str,
        chunk_strategy: str = "recursive"
    ) -> List[Dict[str, Any]]:
        """
        Process document and return chunks with metadata
        """
        try:
            logger.info(f"Processing document: {file_path} (type: {file_type})")
            
            # Load document based on type
            documents = await self._load_document(file_path, file_type)
            
            # Extract text content
            full_text = ""
            for doc in documents:
                full_text += doc.page_content + "\n\n"
            
            # Generate document statistics
            stats = self._calculate_document_stats(full_text, documents)
            
            # Split into chunks
            chunks = await self._split_into_chunks(documents, chunk_strategy)
            
            # Process chunks with metadata
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    "chunk_index": i,
                    "content": chunk.page_content,
                    "content_hash": self._generate_content_hash(chunk.page_content),
                    "metadata": {
                        **chunk.metadata,
                        "file_path": file_path,
                        "file_type": file_type,
                        "chunk_strategy": chunk_strategy,
                        "chunk_size": len(chunk.page_content),
                        "word_count": len(chunk.page_content.split()),
                        "character_count": len(chunk.page_content)
                    },
                    "document_stats": stats
                }
                processed_chunks.append(chunk_data)
            
            logger.info(f"Successfully processed document into {len(processed_chunks)} chunks")
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            raise
    
    async def _load_document(self, file_path: str, file_type: str):
        """Load document based on file type"""
        try:
            if file_type.lower() == "pdf":
                loader = PyPDFLoader(file_path)
            elif file_type.lower() in ["docx", "doc"]:
                loader = Docx2txtLoader(file_path)
            elif file_type.lower() == "txt":
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_type.lower() == "csv":
                loader = CSVLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            documents = loader.load()
            return documents
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            raise
    
    async def _split_into_chunks(self, documents, strategy: str):
        """Split documents into chunks using specified strategy"""
        try:
            if strategy == "recursive":
                chunks = self.recursive_splitter.split_documents(documents)
            elif strategy == "token":
                chunks = self.token_splitter.split_documents(documents)
            elif strategy == "semantic":
                chunks = await self._semantic_chunking(documents)
            elif strategy == "fixed":
                chunks = await self._fixed_chunking(documents)
            else:
                # Default to recursive
                chunks = self.recursive_splitter.split_documents(documents)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise
    
    async def _semantic_chunking(self, documents):
        """Semantic chunking based on content structure"""
        try:
            # This is a simplified semantic chunking
            # In a production system, you might use more advanced NLP techniques
            chunks = []
            
            for doc in documents:
                content = doc.page_content
                
                # Split by paragraphs first
                paragraphs = content.split('\n\n')
                
                current_chunk = ""
                for paragraph in paragraphs:
                    # If adding this paragraph would exceed chunk size, create a new chunk
                    if len(current_chunk) + len(paragraph) > self.chunk_size:
                        if current_chunk:
                            chunk_doc = doc.__class__(
                                page_content=current_chunk.strip(),
                                metadata=doc.metadata
                            )
                            chunks.append(chunk_doc)
                        current_chunk = paragraph
                    else:
                        current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                
                # Add the last chunk
                if current_chunk:
                    chunk_doc = doc.__class__(
                        page_content=current_chunk.strip(),
                        metadata=doc.metadata
                    )
                    chunks.append(chunk_doc)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error in semantic chunking: {e}")
            # Fallback to recursive chunking
            return self.recursive_splitter.split_documents(documents)
    
    async def _fixed_chunking(self, documents):
        """Fixed size chunking with overlap"""
        try:
            chunks = []
            
            for doc in documents:
                content = doc.page_content
                
                # Split into fixed size chunks
                start = 0
                while start < len(content):
                    end = min(start + self.chunk_size, len(content))
                    chunk_content = content[start:end]
                    
                    chunk_doc = doc.__class__(
                        page_content=chunk_content,
                        metadata={**doc.metadata, "chunk_start": start, "chunk_end": end}
                    )
                    chunks.append(chunk_doc)
                    
                    # Move start position with overlap
                    start += self.chunk_size - self.chunk_overlap
                    if start >= len(content):
                        break
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error in fixed chunking: {e}")
            return self.recursive_splitter.split_documents(documents)
    
    def _calculate_document_stats(self, full_text: str, documents) -> Dict[str, Any]:
        """Calculate document statistics"""
        try:
            stats = {
                "total_characters": len(full_text),
                "total_words": len(full_text.split()),
                "total_pages": len(documents),
                "estimated_tokens": len(full_text) // 4,  # Rough estimate
                "language": "en"  # Could be detected using langdetect library
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating document stats: {e}")
            return {}
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA256 hash of content"""
        try:
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        except Exception as e:
            logger.error(f"Error generating content hash: {e}")
            return ""
    
    async def extract_metadata(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extract metadata from document"""
        try:
            metadata = {
                "filename": Path(file_path).name,
                "file_size": os.path.getsize(file_path),
                "file_type": file_type,
                "created_at": os.path.getctime(file_path),
                "modified_at": os.path.getmtime(file_path)
            }
            
            # Type-specific metadata extraction
            if file_type.lower() == "pdf":
                metadata.update(await self._extract_pdf_metadata(file_path))
            elif file_type.lower() in ["docx", "doc"]:
                metadata.update(await self._extract_docx_metadata(file_path))
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}
    
    async def _extract_pdf_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract PDF-specific metadata"""
        try:
            # This would require PyPDF2 or similar library for more detailed metadata
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            return {
                "page_count": len(documents),
                "pdf_metadata": {}  # Could extract title, author, creation date, etc.
            }
            
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {e}")
            return {}
    
    async def _extract_docx_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract DOCX-specific metadata"""
        try:
            # Extract basic DOCX information
            text = docx2txt.process(file_path)
            
            return {
                "word_count": len(text.split()),
                "character_count": len(text),
                "docx_metadata": {}  # Could extract more detailed metadata
            }
            
        except Exception as e:
            logger.error(f"Error extracting DOCX metadata: {e}")
            return {}
    
    def get_supported_file_types(self) -> List[str]:
        """Get list of supported file types"""
        return ["pdf", "docx", "doc", "txt", "csv"]
    
    def validate_file_type(self, file_type: str) -> bool:
        """Validate if file type is supported"""
        return file_type.lower() in self.get_supported_file_types() 