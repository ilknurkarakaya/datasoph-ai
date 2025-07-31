"""
DATASOPH AI - RAG Pipeline
Complete RAG workflow with LangChain integration and conversation memory
"""

from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from .vector_store import VectorStoreManager
from .document_processor import DocumentProcessor
from app.services.openrouter_service import openrouter_service

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Advanced RAG pipeline with conversation memory and context awareness"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager
        self.document_processor = DocumentProcessor()
        self.llm_service = openrouter_service
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Custom prompt templates
        self._initialize_prompts()
        
        # RAG chain
        self.rag_chain = None
    
    def _initialize_prompts(self):
        """Initialize custom prompt templates for RAG"""
        
        # System prompt for RAG responses
        self.system_prompt = """You are Datasoph AI, an expert data scientist and AI assistant. You have access to relevant documents and should use them to provide accurate, helpful responses.

When answering questions:
1. Use the provided context from documents to support your answers
2. If the context doesn't contain relevant information, say so clearly
3. Cite specific sources when referencing document content
4. Be concise but thorough in your explanations
5. If asked about data analysis, provide practical insights and recommendations

Always maintain a friendly, professional, and helpful tone."""

        # RAG prompt template
        self.rag_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Helpful Answer:"""

        self.rag_prompt = PromptTemplate(
            template=self.rag_template,
            input_variables=["context", "question"]
        )
        
        # Conversational RAG template
        self.conversational_template = """Use the following pieces of context and chat history to answer the question at the end. If you don't know the answer based on the context, just say that you don't know.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Helpful Answer:"""

        self.conversational_prompt = PromptTemplate(
            template=self.conversational_template,
            input_variables=["context", "chat_history", "question"]
        )
    
    async def setup_rag_chain(
        self,
        collection_name: str,
        chain_type: str = "conversational",
        search_kwargs: Optional[Dict] = None
    ):
        """
        Setup RAG chain with specified configuration
        """
        try:
            # Load vector store collection
            success = await self.vector_store_manager.load_collection(collection_name)
            if not success:
                raise Exception(f"Failed to load collection: {collection_name}")
            
            # Configure retriever
            search_kwargs = search_kwargs or {"k": 4}
            retriever = self.vector_store_manager.vector_store.as_retriever(
                search_kwargs=search_kwargs
            )
            
            if chain_type == "conversational":
                # Setup conversational retrieval chain
                self.rag_chain = ConversationalRetrievalChain.from_llm(
                    llm=self._create_llm_wrapper(),
                    retriever=retriever,
                    memory=self.memory,
                    return_source_documents=True,
                    verbose=True,
                    chain_type="stuff",
                    combine_docs_chain_kwargs={"prompt": self.conversational_prompt}
                )
            else:
                # Setup basic retrieval QA chain
                self.rag_chain = RetrievalQA.from_chain_type(
                    llm=self._create_llm_wrapper(),
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True,
                    chain_type_kwargs={"prompt": self.rag_prompt}
                )
            
            logger.info(f"RAG chain setup completed for collection: {collection_name}")
            
        except Exception as e:
            logger.error(f"Error setting up RAG chain: {e}")
            raise
    
    async def query_documents(
        self,
        question: str,
        collection_name: Optional[str] = None,
        user_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Query documents using RAG pipeline
        """
        try:
            start_time = datetime.now()
            
            # Setup RAG chain if not already done
            if not self.rag_chain and collection_name:
                await self.setup_rag_chain(collection_name)
            
            if not self.rag_chain:
                raise Exception("RAG chain not initialized")
            
            # Add user context to the question if provided
            if context:
                contextualized_question = self._add_context_to_question(question, context)
            else:
                contextualized_question = question
            
            # Execute RAG query
            if hasattr(self.rag_chain, 'acall'):
                # Async call if available
                response = await self.rag_chain.acall({
                    "question": contextualized_question,
                    "chat_history": self.memory.chat_memory.messages if hasattr(self.memory, 'chat_memory') else []
                })
            else:
                # Sync call fallback
                response = self.rag_chain({
                    "question": contextualized_question
                })
            
            # Process response
            result = await self._process_rag_response(
                response, question, user_id, start_time
            )
            
            logger.info(f"RAG query completed for question: {question[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "error": str(e),
                "source_documents": [],
                "processing_time": 0,
                "question": question
            }
    
    async def _process_rag_response(
        self,
        response: Dict,
        original_question: str,
        user_id: Optional[str],
        start_time: datetime
    ) -> Dict[str, Any]:
        """
        Process and format RAG response
        """
        try:
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Extract answer
            answer = response.get("answer", "No answer provided")
            
            # Process source documents
            source_docs = response.get("source_documents", [])
            processed_sources = []
            
            for i, doc in enumerate(source_docs):
                source_info = {
                    "index": i,
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "unknown"),
                    "page": doc.metadata.get("page", None),
                    "relevance_score": doc.metadata.get("relevance_score", 0.0)
                }
                processed_sources.append(source_info)
            
            # Get relevant chunks for additional context
            try:
                additional_chunks = await self.vector_store_manager.similarity_search(
                    original_question, k=2
                )
            except Exception as e:
                logger.warning(f"Could not get additional chunks: {e}")
                additional_chunks = []
            
            return {
                "answer": answer,
                "source_documents": processed_sources,
                "relevant_chunks": additional_chunks,
                "question": original_question,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "has_sources": len(processed_sources) > 0,
                "confidence_score": self._calculate_confidence_score(
                    answer, processed_sources
                )
            }
            
        except Exception as e:
            logger.error(f"Error processing RAG response: {e}")
            return {
                "answer": "Error processing response",
                "error": str(e),
                "source_documents": [],
                "processing_time": 0,
                "question": original_question
            }
    
    def _add_context_to_question(self, question: str, context: Dict) -> str:
        """
        Add user context to the question for better RAG results
        """
        try:
            context_parts = []
            
            if context.get("user_name"):
                context_parts.append(f"User: {context['user_name']}")
            
            if context.get("previous_topic"):
                context_parts.append(f"Previous topic: {context['previous_topic']}")
            
            if context.get("specific_focus"):
                context_parts.append(f"Focus on: {context['specific_focus']}")
            
            if context_parts:
                context_string = " | ".join(context_parts)
                return f"[Context: {context_string}] {question}"
            
            return question
            
        except Exception as e:
            logger.error(f"Error adding context to question: {e}")
            return question
    
    def _calculate_confidence_score(
        self,
        answer: str,
        source_docs: List[Dict]
    ) -> float:
        """
        Calculate confidence score based on answer and sources
        """
        try:
            if not source_docs:
                return 0.2  # Low confidence without sources
            
            # Base confidence from number of sources
            source_confidence = min(0.8, len(source_docs) * 0.2)
            
            # Boost confidence if answer references specific facts/numbers
            import re
            has_numbers = bool(re.search(r'\d+', answer))
            has_specifics = any(word in answer.lower() for word in [
                'according to', 'the document states', 'as mentioned',
                'specifically', 'precisely', 'data shows'
            ])
            
            specificity_boost = 0.1 if has_numbers else 0.0
            specificity_boost += 0.1 if has_specifics else 0.0
            
            # Final confidence score
            confidence = min(1.0, source_confidence + specificity_boost)
            
            return round(confidence, 2)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _create_llm_wrapper(self):
        """
        Create LLM wrapper for LangChain integration
        """
        from langchain.llms.base import LLM
        from langchain.callbacks.manager import CallbackManagerForLLMRun
        from typing import Optional, List, Any
        
        class OpenRouterLLM(LLM):
            """Custom LLM wrapper for OpenRouter"""
            
            def __init__(self, openrouter_service, model: str = None):
                super().__init__()
                self.openrouter_service = openrouter_service
                self.model = model or "anthropic/claude-3-sonnet"
            
            @property
            def _llm_type(self) -> str:
                return "openrouter"
            
            def _call(
                self,
                prompt: str,
                stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = None,
                **kwargs: Any,
            ) -> str:
                # Convert prompt to messages format
                messages = [{"role": "user", "content": prompt}]
                
                # Make synchronous call (LangChain requires sync)
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    response = loop.run_until_complete(
                        self.openrouter_service.create_chat_completion(
                            messages=messages,
                            model=self.model,
                            **kwargs
                        )
                    )
                    
                    return response["choices"][0]["message"]["content"]
                finally:
                    loop.close()
        
        return OpenRouterLLM(self.llm_service)
    
    async def process_and_index_document(
        self,
        file_path: str,
        file_type: str,
        collection_name: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process document and add to vector store
        """
        try:
            # Process document
            chunks = await self.document_processor.process_document(
                file_path, file_type
            )
            
            # Add custom metadata if provided
            if metadata:
                for chunk in chunks:
                    chunk["metadata"].update(metadata)
            
            # Create or load collection
            try:
                await self.vector_store_manager.load_collection(collection_name)
                # Add to existing collection
                ids = await self.vector_store_manager.add_documents(chunks)
            except:
                # Create new collection
                collection_id = await self.vector_store_manager.create_collection(
                    collection_name, chunks
                )
            
            return {
                "success": True,
                "collection_name": collection_name,
                "chunks_processed": len(chunks),
                "file_path": file_path,
                "file_type": file_type
            }
            
        except Exception as e:
            logger.error(f"Error processing and indexing document: {e}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    def clear_memory(self):
        """Clear conversation memory"""
        try:
            self.memory.clear()
            logger.info("Conversation memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
    
    def get_memory_summary(self) -> str:
        """Get summary of conversation memory"""
        try:
            if hasattr(self.memory, 'chat_memory') and self.memory.chat_memory.messages:
                messages = self.memory.chat_memory.messages
                return f"Conversation history: {len(messages)} messages"
            return "No conversation history"
        except Exception as e:
            logger.error(f"Error getting memory summary: {e}")
            return "Memory unavailable" 