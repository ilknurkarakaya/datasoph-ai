"""
DATASOPH AI - RAG Pipeline
Main RAG system that combines document processing, vector storage, and retrieval
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

# LangChain imports
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Local imports
from document_processor import DocumentProcessor
from vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    RAG Pipeline for DATASOPH AI
    Combines document processing, vector storage, and retrieval
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize RAG Pipeline
        
        Args:
            api_key: OpenAI API key
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize components
        self.document_processor = DocumentProcessor(chunk_size, chunk_overlap)
        self.vector_store = VectorStore(api_key=self.api_key)
        
        # Initialize LLM
        self.llm = None
        if self.api_key:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-4",
                openai_api_key=self.api_key
            )
        
        # Initialize prompt template
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are DATASOPH AI, an expert assistant that helps users find information from their documents.
        
        Context from documents:
        {context}
        
        User question: {question}
        
        Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, say so. Be helpful and professional in your response.
        
        Answer:
        """)
        
        # Initialize LLM chain
        if self.llm:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        
        logger.info("RAG Pipeline initialized successfully")
    
    def upload_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Upload and process documents
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            Processing results
        """
        try:
            logger.info(f"Processing {len(file_paths)} documents")
            
            # Process documents
            documents = self.document_processor.process_multiple_documents(file_paths)
            
            if not documents:
                return {
                    "success": False,
                    "error": "No documents were successfully processed"
                }
            
            # Add to vector store
            success = self.vector_store.add_documents(documents)
            
            if not success:
                return {
                    "success": False,
                    "error": "Failed to add documents to vector store"
                }
            
            # Get summary
            summary = self.document_processor.get_document_summary(documents)
            
            return {
                "success": True,
                "documents_processed": len(file_paths),
                "chunks_created": len(documents),
                "summary": summary
            }
            
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def ask_question(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Ask a question and get answer based on uploaded documents
        
        Args:
            question: User's question
            k: Number of similar documents to retrieve
            
        Returns:
            Answer and context
        """
        try:
            if not self.llm:
                return self._mock_answer(question)
            
            # Search for relevant documents
            similar_docs = self.vector_store.similarity_search(question, k=k)
            
            if not similar_docs:
                return {
                    "success": False,
                    "error": "No relevant documents found",
                    "answer": "I couldn't find any relevant information in the uploaded documents to answer your question."
                }
            
            # Prepare context
            context = "\n\n".join([doc.page_content for doc, _ in similar_docs])
            
            # Generate answer
            response = self.llm_chain.run({
                "context": context,
                "question": question
            })
            
            # Prepare sources
            sources = []
            for doc, _ in similar_docs:
                if "source" in doc.metadata:
                    sources.append(doc.metadata["source"])
            
            return {
                "success": True,
                "answer": response,
                "sources": list(set(sources)),
                "context_documents": len(similar_docs),
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Error asking question: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mock_answer(self, question: str) -> Dict[str, Any]:
        """Generate mock answer when LLM is not available"""
        question_lower = question.lower()
        
        if "what" in question_lower and "document" in question_lower:
            answer = "Based on the uploaded documents, I can help you find information. Please ask specific questions about the content."
        elif "how" in question_lower and "work" in question_lower:
            answer = "The RAG system works by processing your documents, creating embeddings, and using similarity search to find relevant information when you ask questions."
        elif "upload" in question_lower or "add" in question_lower:
            answer = "You can upload PDF, DOCX, TXT, CSV, and JSON files. The system will process them and make the content searchable."
        else:
            answer = f"I understand you're asking about: '{question}'. This is a demonstration of the RAG system. In a real implementation with API access, I would search through your uploaded documents to provide specific answers."
        
        return {
            "success": True,
            "answer": answer,
            "sources": ["Mock response - no API key provided"],
            "context_documents": 0,
            "question": question
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            vector_stats = self.vector_store.get_collection_stats()
            
            stats = {
                "rag_system": "DATASOPH AI RAG Pipeline",
                "api_connected": self.api_key is not None,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "vector_store": vector_stats,
                "supported_file_types": list(self.document_processor.supported_extensions.keys())
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {"error": str(e)}
    
    def reset_system(self) -> bool:
        """Reset the entire RAG system"""
        try:
            success = self.vector_store.reset_collection()
            if success:
                logger.info("RAG system reset successfully")
            return success
        except Exception as e:
            logger.error(f"Error resetting RAG system: {e}")
            return False
    
    def export_system_info(self) -> Dict[str, Any]:
        """Export system information"""
        try:
            stats = self.get_system_stats()
            vector_info = self.vector_store.export_collection_info()
            
            export_data = {
                "system_stats": stats,
                "vector_store_info": vector_info,
                "export_timestamp": str(Path().absolute())
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting system info: {e}")
            return {"error": str(e)}


def main():
    """Demo function for RAG Pipeline"""
    print("🔍 DATASOPH AI - RAG Pipeline Demo")
    print("=" * 50)
    
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    # Show system stats
    stats = rag.get_system_stats()
    print(f"RAG System: {stats['rag_system']}")
    print(f"API Connected: {stats['api_connected']}")
    print(f"Supported file types: {stats['supported_file_types']}")
    print(f"Chunk size: {stats['chunk_size']}")
    print("-" * 50)
    
    # Example usage
    print("Example usage:")
    print("rag = RAGPipeline()")
    print("rag.upload_documents(['document.pdf'])")
    print("answer = rag.ask_question('What is this document about?')")


if __name__ == "__main__":
    main() 