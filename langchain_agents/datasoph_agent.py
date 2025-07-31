"""
DATASOPH AI - Main Datasoph Agent
The primary AI agent with comprehensive data science and analysis capabilities
"""

from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from typing import Optional, List, Any, Dict
import logging
import asyncio

from langchain_agents.tools.data_analysis_tools import DataAnalysisTools
from langchain_agents.tools.visualization_tools import VisualizationTools
from langchain_agents.tools.statistical_tools import StatisticalTools
from rag_system.rag_pipeline import RAGPipeline
from app.services.openrouter_service import openrouter_service

logger = logging.getLogger(__name__)

class OpenRouterLLM(LLM):
    """Custom LLM wrapper for OpenRouter integration with LangChain"""
    
    def __init__(self, openrouter_service, model: str = "anthropic/claude-3-sonnet"):
        super().__init__()
        self.openrouter_service = openrouter_service
        self.model = model
    
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
        """Call OpenRouter API synchronously for LangChain compatibility"""
        try:
            # Convert prompt to messages format
            messages = [
                {
                    "role": "system", 
                    "content": "You are Datasoph AI, an expert data scientist and AI assistant. Provide helpful, accurate, and insightful responses."
                },
                {"role": "user", "content": prompt}
            ]
            
            # Create new event loop for async call
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(
                    self.openrouter_service.create_chat_completion(
                        messages=messages,
                        model=self.model,
                        temperature=0.7,
                        max_tokens=4000,
                        **kwargs
                    )
                )
                
                return response["choices"][0]["message"]["content"]
                
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Error in OpenRouter LLM call: {e}")
            return f"I encountered an error: {str(e)}"

class DatasophAgent:
    """Main Datasoph AI agent with comprehensive capabilities"""
    
    def __init__(self, rag_pipeline: Optional[RAGPipeline] = None):
        self.rag_pipeline = rag_pipeline
        
        # Initialize LLM
        self.llm = OpenRouterLLM(openrouter_service)
        
        # Initialize tools
        self.data_tools = DataAnalysisTools()
        self.viz_tools = VisualizationTools()
        self.stat_tools = StatisticalTools()
        
        # Initialize memory
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=10,
            return_messages=True,
            output_key="output"
        )
        
        # Initialize tools list
        self.tools = self._create_tools()
        
        # Initialize agent
        self.agent = self._initialize_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools available to the agent"""
        tools = [
            Tool(
                name="Data Analysis",
                func=self._data_analysis_wrapper,
                description="Perform comprehensive statistical analysis on datasets. Input should be a description of the analysis needed and file path if applicable."
            ),
            Tool(
                name="Create Visualization",
                func=self._visualization_wrapper,
                description="Create professional visualizations and charts. Input should describe the type of chart and data requirements."
            ),
            Tool(
                name="Statistical Tests",
                func=self._statistical_tests_wrapper,
                description="Perform hypothesis testing and statistical significance tests. Input should describe the test type and parameters."
            ),
            Tool(
                name="Data Summary",
                func=self._data_summary_wrapper,
                description="Generate comprehensive data summaries and insights. Input should be the dataset path or description."
            ),
            Tool(
                name="Correlation Analysis",
                func=self._correlation_analysis_wrapper,
                description="Analyze correlations between variables. Input should specify the variables and dataset."
            ),
            Tool(
                name="Time Series Analysis",
                func=self._time_series_wrapper,
                description="Perform time series analysis and forecasting. Input should describe the time series data and analysis type."
            )
        ]
        
        # Add RAG tool if pipeline is available
        if self.rag_pipeline:
            tools.append(
                Tool(
                    name="Query Documents",
                    func=self._rag_query_wrapper,
                    description="Search and query uploaded documents using RAG. Input should be the question about the documents."
                )
            )
        
        return tools
    
    def _initialize_agent(self):
        """Initialize the LangChain agent"""
        try:
            agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                early_stopping_method="generate"
            )
            
            logger.info("Datasoph agent initialized successfully")
            return agent
            
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise
    
    async def chat(
        self,
        message: str,
        user_context: Optional[Dict] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main chat interface for the Datasoph agent
        """
        try:
            logger.info(f"Processing chat message: {message[:100]}...")
            
            # Add user context to the message if provided
            if user_context:
                contextual_message = self._add_context_to_message(message, user_context)
            else:
                contextual_message = message
            
            # Run the agent
            response = await self._run_agent_async(contextual_message)
            
            # Process and format response
            result = {
                "response": response,
                "message": message,
                "session_id": session_id,
                "agent_type": "datasoph",
                "tools_used": self._extract_tools_used(response),
                "has_analysis": self._has_data_analysis(response),
                "has_visualization": self._has_visualization(response),
                "confidence_score": self._calculate_response_confidence(response)
            }
            
            logger.info(f"Chat response generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in agent chat: {e}")
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "error": str(e),
                "message": message,
                "session_id": session_id
            }
    
    async def _run_agent_async(self, message: str) -> str:
        """Run agent asynchronously"""
        try:
            # Run in thread to avoid blocking
            import asyncio
            loop = asyncio.get_event_loop()
            
            # Run agent in executor
            response = await loop.run_in_executor(
                None,
                lambda: self.agent.run(message)
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            return f"I encountered an error: {str(e)}"
    
    def _add_context_to_message(self, message: str, context: Dict) -> str:
        """Add user context to enhance the message"""
        try:
            context_parts = []
            
            if context.get("user_name"):
                context_parts.append(f"User: {context['user_name']}")
            
            if context.get("expertise_level"):
                context_parts.append(f"Expertise: {context['expertise_level']}")
            
            if context.get("current_task"):
                context_parts.append(f"Task: {context['current_task']}")
            
            if context.get("data_context"):
                context_parts.append(f"Data: {context['data_context']}")
            
            if context_parts:
                context_string = " | ".join(context_parts)
                return f"[Context: {context_string}]\n\n{message}"
            
            return message
            
        except Exception as e:
            logger.error(f"Error adding context: {e}")
            return message
    
    # Tool wrapper methods
    def _data_analysis_wrapper(self, input_str: str) -> str:
        """Wrapper for data analysis tool"""
        try:
            return self.data_tools.analyze_dataset(input_str)
        except Exception as e:
            return f"Data analysis error: {str(e)}"
    
    def _visualization_wrapper(self, input_str: str) -> str:
        """Wrapper for visualization tool"""
        try:
            return self.viz_tools.create_chart(input_str)
        except Exception as e:
            return f"Visualization error: {str(e)}"
    
    def _statistical_tests_wrapper(self, input_str: str) -> str:
        """Wrapper for statistical tests tool"""
        try:
            return self.stat_tools.perform_statistical_tests(input_str)
        except Exception as e:
            return f"Statistical test error: {str(e)}"
    
    def _data_summary_wrapper(self, input_str: str) -> str:
        """Wrapper for data summary tool"""
        try:
            return self.data_tools.generate_data_summary(input_str)
        except Exception as e:
            return f"Data summary error: {str(e)}"
    
    def _correlation_analysis_wrapper(self, input_str: str) -> str:
        """Wrapper for correlation analysis tool"""
        try:
            return self.stat_tools.correlation_analysis(input_str)
        except Exception as e:
            return f"Correlation analysis error: {str(e)}"
    
    def _time_series_wrapper(self, input_str: str) -> str:
        """Wrapper for time series analysis tool"""
        try:
            return self.data_tools.time_series_analysis(input_str)
        except Exception as e:
            return f"Time series analysis error: {str(e)}"
    
    def _rag_query_wrapper(self, input_str: str) -> str:
        """Wrapper for RAG query tool"""
        try:
            if not self.rag_pipeline:
                return "Document querying is not available. Please upload documents first."
            
            # Run RAG query synchronously for LangChain compatibility
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.rag_pipeline.query_documents(input_str)
                )
                
                answer = result.get("answer", "No answer found")
                sources = result.get("source_documents", [])
                
                if sources:
                    source_info = f"\n\nSources: {len(sources)} documents referenced"
                    return f"{answer}{source_info}"
                else:
                    return answer
                    
            finally:
                loop.close()
                
        except Exception as e:
            return f"Document query error: {str(e)}"
    
    # Response analysis methods
    def _extract_tools_used(self, response: str) -> List[str]:
        """Extract which tools were used in the response"""
        tools_used = []
        tool_indicators = {
            "Data Analysis": ["analysis", "dataset", "statistics"],
            "Visualization": ["chart", "graph", "plot", "visualization"],
            "Statistical Tests": ["test", "hypothesis", "significance"],
            "Query Documents": ["document", "source", "reference"]
        }
        
        response_lower = response.lower()
        for tool, indicators in tool_indicators.items():
            if any(indicator in response_lower for indicator in indicators):
                tools_used.append(tool)
        
        return tools_used
    
    def _has_data_analysis(self, response: str) -> bool:
        """Check if response contains data analysis"""
        analysis_indicators = [
            "mean", "median", "standard deviation", "correlation",
            "regression", "distribution", "outliers", "trends"
        ]
        return any(indicator in response.lower() for indicator in analysis_indicators)
    
    def _has_visualization(self, response: str) -> bool:
        """Check if response mentions visualizations"""
        viz_indicators = [
            "chart", "graph", "plot", "visualization", "figure",
            "scatter", "histogram", "bar chart", "line chart"
        ]
        return any(indicator in response.lower() for indicator in viz_indicators)
    
    def _calculate_response_confidence(self, response: str) -> float:
        """Calculate confidence score for the response"""
        try:
            # Base confidence
            confidence = 0.7
            
            # Boost for specific data mentions
            if any(word in response.lower() for word in ["data shows", "analysis reveals", "statistics indicate"]):
                confidence += 0.1
            
            # Boost for tool usage
            tools_used = len(self._extract_tools_used(response))
            confidence += min(0.2, tools_used * 0.05)
            
            # Reduce for error mentions
            if "error" in response.lower():
                confidence -= 0.3
            
            return max(0.1, min(1.0, confidence))
            
        except Exception:
            return 0.5
    
    def clear_memory(self):
        """Clear agent conversation memory"""
        try:
            self.memory.clear()
            logger.info("Agent memory cleared")
        except Exception as e:
            logger.error(f"Error clearing agent memory: {e}")
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        try:
            if hasattr(self.memory, 'chat_memory') and self.memory.chat_memory.messages:
                return f"Conversation with {len(self.memory.chat_memory.messages)} messages"
            return "No conversation history"
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return "Conversation summary unavailable"
    
    def update_rag_pipeline(self, rag_pipeline: RAGPipeline):
        """Update the RAG pipeline and refresh tools"""
        self.rag_pipeline = rag_pipeline
        self.tools = self._create_tools()
        self.agent = self._initialize_agent()
        logger.info("RAG pipeline updated and agent refreshed") 