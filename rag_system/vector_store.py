"""
DATASOPH AI - Vector Store Manager
ChromaDB and FAISS integration for vector storage and retrieval
"""

from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import OpenAIEmbeddings
from typing import List, Dict, Any, Optional, Tuple
import chromadb
import logging
import os
import pickle
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Advanced vector store management with Chroma and FAISS support"""
    
    def __init__(self, store_type: str = "chroma", embedding_model: str = "openai"):
        self.store_type = store_type
        self.embedding_model = embedding_model
        self.vector_store = None
        
        # Initialize embeddings
        self._initialize_embeddings()
        
        # Initialize vector store
        self._initialize_vector_store()
    
    def _initialize_embeddings(self):
        """Initialize embedding model"""
        try:
            if self.embedding_model == "openai":
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=settings.OPENAI_API_KEY,
                    model="text-embedding-ada-002"
                )
            else:
                # Could add support for other embedding models like HuggingFace
                raise ValueError(f"Unsupported embedding model: {self.embedding_model}")
            
            logger.info(f"Initialized embeddings with model: {self.embedding_model}")
            
        except Exception as e:
            logger.error(f"Error initializing embeddings: {e}")
            raise
    
    def _initialize_vector_store(self):
        """Initialize vector store client"""
        try:
            if self.store_type == "chroma":
                # Ensure directory exists
                Path(settings.VECTORSTORE_DIRECTORY).mkdir(parents=True, exist_ok=True)
                
                self.client = chromadb.PersistentClient(
                    path=settings.VECTORSTORE_DIRECTORY
                )
                logger.info("Initialized ChromaDB client")
                
            elif self.store_type == "faiss":
                # FAISS initialization will be done when creating/loading
                self.faiss_index_path = os.path.join(
                    settings.VECTORSTORE_DIRECTORY, 
                    "faiss_index"
                )
                logger.info("Initialized FAISS configuration")
                
            else:
                raise ValueError(f"Unsupported vector store type: {self.store_type}")
                
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    async def create_collection(
        self,
        collection_name: str,
        documents: List[Dict[str, Any]],
        metadata_filter: Optional[Dict] = None
    ) -> str:
        """
        Create a new vector collection from documents
        """
        try:
            texts = [doc["content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            if self.store_type == "chroma":
                # Create Chroma collection
                self.vector_store = Chroma.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas,
                    collection_name=collection_name,
                    client=self.client,
                    persist_directory=settings.VECTORSTORE_DIRECTORY
                )
                
                # Persist the collection
                self.vector_store.persist()
                
            elif self.store_type == "faiss":
                # Create FAISS index
                self.vector_store = FAISS.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas
                )
                
                # Save FAISS index
                index_path = f"{self.faiss_index_path}_{collection_name}"
                self.vector_store.save_local(index_path)
            
            logger.info(f"Created collection '{collection_name}' with {len(documents)} documents")
            return collection_name
            
        except Exception as e:
            logger.error(f"Error creating collection {collection_name}: {e}")
            raise
    
    async def load_collection(self, collection_name: str) -> bool:
        """
        Load an existing vector collection
        """
        try:
            if self.store_type == "chroma":
                # Load Chroma collection
                self.vector_store = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                    client=self.client,
                    persist_directory=settings.VECTORSTORE_DIRECTORY
                )
                
            elif self.store_type == "faiss":
                # Load FAISS index
                index_path = f"{self.faiss_index_path}_{collection_name}"
                if os.path.exists(index_path):
                    self.vector_store = FAISS.load_local(
                        index_path,
                        self.embeddings
                    )
                else:
                    logger.warning(f"FAISS index not found: {index_path}")
                    return False
            
            logger.info(f"Loaded collection: {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading collection {collection_name}: {e}")
            return False
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        collection_name: Optional[str] = None
    ) -> List[str]:
        """
        Add documents to existing collection
        """
        try:
            if not self.vector_store:
                if collection_name:
                    await self.load_collection(collection_name)
                else:
                    raise ValueError("No vector store loaded and no collection name provided")
            
            texts = [doc["content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            # Add texts to vector store
            ids = self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            # Persist changes for Chroma
            if self.store_type == "chroma":
                self.vector_store.persist()
            
            logger.info(f"Added {len(documents)} documents to collection")
            return ids
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    async def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter_dict: Optional[Dict] = None,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search with optional filtering
        """
        try:
            if not self.vector_store:
                raise ValueError("No vector store loaded")
            
            # Perform similarity search with scores
            if score_threshold is not None:
                docs_and_scores = self.vector_store.similarity_search_with_score(
                    query, k=k * 2  # Get more results to filter by score
                )
                
                # Filter by score threshold
                filtered_docs = [
                    (doc, score) for doc, score in docs_and_scores 
                    if score >= score_threshold
                ][:k]
            else:
                docs_and_scores = self.vector_store.similarity_search_with_score(
                    query, k=k
                )
                filtered_docs = docs_and_scores
            
            # Apply metadata filtering if provided
            if filter_dict:
                filtered_docs = [
                    (doc, score) for doc, score in filtered_docs
                    if self._matches_filter(doc.metadata, filter_dict)
                ]
            
            # Format results
            results = []
            for doc, score in filtered_docs:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score),
                    "relevance_score": self._calculate_relevance_score(score)
                }
                results.append(result)
            
            logger.info(f"Similarity search returned {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise
    
    async def semantic_search(
        self,
        query: str,
        k: int = 4,
        search_type: str = "similarity"
    ) -> List[Dict[str, Any]]:
        """
        Advanced semantic search with different search strategies
        """
        try:
            if not self.vector_store:
                raise ValueError("No vector store loaded")
            
            if search_type == "similarity":
                return await self.similarity_search(query, k)
                
            elif search_type == "mmr":
                # Maximum Marginal Relevance search
                docs = self.vector_store.max_marginal_relevance_search(
                    query, k=k, fetch_k=k*2
                )
                
                results = []
                for doc in docs:
                    result = {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": 0.0,  # MMR doesn't provide scores
                        "relevance_score": 0.8,  # Default relevance for MMR
                        "search_type": "mmr"
                    }
                    results.append(result)
                
                return results
                
            else:
                raise ValueError(f"Unsupported search type: {search_type}")
                
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise
    
    async def hybrid_search(
        self,
        query: str,
        k: int = 4,
        alpha: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining semantic and keyword search
        """
        try:
            # For now, this is a simplified hybrid search
            # In production, you might combine with BM25 or other keyword search
            
            # Get semantic results
            semantic_results = await self.similarity_search(query, k=k*2)
            
            # Simple keyword matching boost
            boosted_results = []
            query_words = set(query.lower().split())
            
            for result in semantic_results:
                content_words = set(result["content"].lower().split())
                keyword_overlap = len(query_words.intersection(content_words))
                keyword_score = keyword_overlap / len(query_words) if query_words else 0
                
                # Combine semantic and keyword scores
                combined_score = (
                    alpha * result["similarity_score"] + 
                    (1 - alpha) * keyword_score
                )
                
                result["combined_score"] = combined_score
                result["keyword_score"] = keyword_score
                boosted_results.append(result)
            
            # Sort by combined score and return top k
            boosted_results.sort(key=lambda x: x["combined_score"], reverse=True)
            return boosted_results[:k]
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            raise
    
    def _matches_filter(self, metadata: Dict, filter_dict: Dict) -> bool:
        """Check if metadata matches filter criteria"""
        try:
            for key, value in filter_dict.items():
                if key not in metadata:
                    return False
                
                if isinstance(value, list):
                    if metadata[key] not in value:
                        return False
                elif metadata[key] != value:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error matching filter: {e}")
            return False
    
    def _calculate_relevance_score(self, similarity_score: float) -> float:
        """Calculate relevance score from similarity score"""
        try:
            # Convert similarity score to relevance score (0-1 range)
            # This is a simplified calculation
            if similarity_score <= 0:
                return 0.0
            elif similarity_score >= 1:
                return 1.0
            else:
                return min(1.0, max(0.0, 1.0 - similarity_score))
                
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.0
    
    async def delete_collection(self, collection_name: str) -> bool:
        """Delete a vector collection"""
        try:
            if self.store_type == "chroma":
                try:
                    self.client.delete_collection(collection_name)
                except Exception:
                    # Collection might not exist
                    pass
                    
            elif self.store_type == "faiss":
                index_path = f"{self.faiss_index_path}_{collection_name}"
                if os.path.exists(index_path):
                    import shutil
                    shutil.rmtree(index_path)
            
            logger.info(f"Deleted collection: {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {e}")
            return False
    
    async def list_collections(self) -> List[str]:
        """List all available collections"""
        try:
            if self.store_type == "chroma":
                collections = self.client.list_collections()
                return [col.name for col in collections]
                
            elif self.store_type == "faiss":
                # List FAISS indices
                if os.path.exists(self.faiss_index_path):
                    indices = [
                        f.replace(f"{self.faiss_index_path}_", "")
                        for f in os.listdir(os.path.dirname(self.faiss_index_path))
                        if f.startswith(os.path.basename(self.faiss_index_path))
                    ]
                    return indices
                return []
                
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            return []
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics about a collection"""
        try:
            if not await self.load_collection(collection_name):
                return {}
            
            if self.store_type == "chroma":
                collection = self.client.get_collection(collection_name)
                count = collection.count()
                
                return {
                    "collection_name": collection_name,
                    "document_count": count,
                    "store_type": self.store_type,
                    "embedding_model": self.embedding_model
                }
                
            elif self.store_type == "faiss":
                # FAISS stats would need to be stored separately
                return {
                    "collection_name": collection_name,
                    "store_type": self.store_type,
                    "embedding_model": self.embedding_model
                }
                
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {} 