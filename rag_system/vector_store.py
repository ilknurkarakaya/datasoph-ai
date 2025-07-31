"""
DATASOPH AI - Vector Store
ChromaDB-based vector store for document embeddings and similarity search
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json

# Vector store imports
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# LangChain imports
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """
    Vector Store for RAG System
    Uses ChromaDB for document embeddings and similarity search
    """
    
    def __init__(self, 
                 persist_directory: str = "./rag_system/vectorstore",
                 embedding_model: str = "openai",
                 api_key: Optional[str] = None):
        """
        Initialize Vector Store
        
        Args:
            persist_directory: Directory to persist vector store
            embedding_model: Embedding model to use
            api_key: API key for OpenAI embeddings
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.embedding_model = embedding_model
        
        # Initialize embeddings
        self.embeddings = self._initialize_embeddings()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize collection
        self.collection_name = "datasoph_documents"
        self.collection = self._get_or_create_collection()
        
        logger.info(f"Vector store initialized at {self.persist_directory}")
    
    def _initialize_embeddings(self):
        """Initialize embedding model"""
        if self.embedding_model == "openai" and self.api_key:
            logger.info("Using OpenAI embeddings")
            return OpenAIEmbeddings(
                openai_api_key=self.api_key,
                model="text-embedding-ada-002"
            )
        else:
            logger.info("Using HuggingFace embeddings (sentence-transformers)")
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
    
    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        try:
            collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self._get_embedding_function()
            )
            logger.info(f"Using existing collection: {self.collection_name}")
        except:
            collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self._get_embedding_function(),
                metadata={"description": "DATASOPH AI Document Collection"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        
        return collection
    
    def _get_embedding_function(self):
        """Get embedding function for ChromaDB"""
        if self.embedding_model == "openai" and self.api_key:
            return embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                model_name="text-embedding-ada-002"
            )
        else:
            return embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to vector store
        
        Args:
            documents: List of LangChain documents
            
        Returns:
            Success status
        """
        try:
            if not documents:
                logger.warning("No documents provided")
                return False
            
            # Prepare documents for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for i, doc in enumerate(documents):
                doc_id = f"doc_{i}_{hash(doc.page_content) % 10000}"
                ids.append(doc_id)
                texts.append(doc.page_content)
                metadatas.append(doc.metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return False
    
    def similarity_search(self, 
                        query: str, 
                        k: int = 5,
                        filter_metadata: Optional[Dict] = None) -> List[Tuple[Document, float]]:
        """
        Perform similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        try:
            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=filter_metadata
            )
            
            # Convert to LangChain format
            documents = []
            for i in range(len(results['documents'][0])):
                doc = Document(
                    page_content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i]
                )
                # Note: ChromaDB doesn't return scores in this format
                # You might need to use different method for scores
                documents.append((doc, 0.0))  # Placeholder score
            
            logger.info(f"Found {len(documents)} similar documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            count = self.collection.count()
            
            stats = {
                "collection_name": self.collection_name,
                "total_documents": count,
                "embedding_model": self.embedding_model,
                "persist_directory": str(self.persist_directory),
                "api_connected": self.api_key is not None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def delete_collection(self) -> bool:
        """Delete the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False
    
    def reset_collection(self) -> bool:
        """Reset the collection (delete and recreate)"""
        try:
            self.delete_collection()
            self.collection = self._get_or_create_collection()
            logger.info("Collection reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return False
    
    def export_collection_info(self) -> Dict[str, Any]:
        """Export collection information"""
        try:
            stats = self.get_collection_stats()
            
            # Get sample documents
            sample_results = self.collection.query(
                query_texts=["sample"],
                n_results=min(5, stats.get("total_documents", 0))
            )
            
            export_data = {
                "stats": stats,
                "sample_documents": sample_results.get('documents', []),
                "sample_metadatas": sample_results.get('metadatas', []),
                "export_timestamp": str(Path().absolute())
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting collection info: {e}")
            return {"error": str(e)}


def main():
    """Demo function for Vector Store"""
    print("🗄️ DATASOPH AI - Vector Store Demo")
    print("=" * 50)
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Show stats
    stats = vector_store.get_collection_stats()
    print(f"Collection: {stats['collection_name']}")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Embedding model: {stats['embedding_model']}")
    print(f"API connected: {stats['api_connected']}")
    print("-" * 50)
    
    # Example usage
    print("Example usage:")
    print("vector_store = VectorStore()")
    print("vector_store.add_documents(documents)")
    print("results = vector_store.similarity_search('query')")


if __name__ == "__main__":
    main() 