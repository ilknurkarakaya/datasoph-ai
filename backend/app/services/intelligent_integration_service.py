"""
Intelligent Integration Service - Unified Interface for DataSoph AI
Integrates all intelligent AI components into a cohesive system
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

# Import all intelligent services
from .intelligent_ai_service import IntelligentDataSophAI, ContextManager, ExpertiseEngine
from .code_generation_service import ProfessionalCodeGenerator  
from .business_intelligence_service import BusinessIntelligenceEngine

logger = logging.getLogger(__name__)

class IntelligentSystemOrchestrator:
    """
    Master orchestrator for the intelligent DataSoph AI system
    Coordinates all AI components for optimal user experience
    """
    
    def __init__(self):
        # Initialize all AI components
        self.intelligent_ai = IntelligentDataSophAI()
        self.code_generator = ProfessionalCodeGenerator()
        self.business_intelligence = BusinessIntelligenceEngine()
        
        # System state tracking
        self.system_health = {
            "intelligent_ai": True,
            "code_generation": True,
            "business_intelligence": True,
            "overall_status": "operational"
        }
        
        # Performance metrics
        self.metrics = {
            "total_requests": 0,
            "successful_responses": 0,
            "error_count": 0,
            "average_response_time": 0.0,
            "user_satisfaction": 0.0
        }
        
        logger.info("Intelligent DataSoph AI System initialized successfully")
    
    async def process_user_request(self, user_message: str, file_path: Optional[str] = None, 
                                  user_id: str = "default") -> Dict[str, Any]:
        """
        Process user request through the complete intelligent system
        """
        import time
        start_time = time.time()
        
        try:
            self.metrics["total_requests"] += 1
            
            # Step 1: Analyze request intent and complexity
            intent_analysis = await self.intelligent_ai.analyze_intent(user_message)
            
            # Step 2: Assess data context if file provided
            data_context = {}
            if file_path:
                data_context = await self.intelligent_ai.assess_data_context(file_path)
            
            # Step 3: Generate intelligent response
            ai_response = await self.intelligent_ai.generate_expert_response(
                intent_analysis, data_context, user_message
            )
            
            # Step 4: Generate code if requested
            code_response = None
            if self._should_generate_code(user_message, intent_analysis):
                code_response = await self._generate_contextual_code(
                    intent_analysis, data_context, user_message
                )
            
            # Step 5: Business intelligence analysis
            business_insights = None
            if data_context.get("has_data") and self._should_analyze_business(user_message):
                business_insights = await self._generate_business_insights(
                    file_path, data_context
                )
            
            # Step 6: Integrate all responses
            integrated_response = self._integrate_responses(
                ai_response, code_response, business_insights, intent_analysis
            )
            
            # Step 7: Track performance
            end_time = time.time()
            response_time = end_time - start_time
            self._update_metrics(response_time, True)
            
            return {
                "status": "success",
                "response": integrated_response,
                "metadata": {
                    "response_time": response_time,
                    "intent": intent_analysis,
                    "has_code": code_response is not None,
                    "has_business_insights": business_insights is not None,
                    "data_context": data_context.get("has_data", False)
                }
            }
            
        except Exception as e:
            logger.error(f"Intelligent system error: {e}")
            self._update_metrics(time.time() - start_time, False)
            
            # Graceful degradation
            return await self._handle_system_error(user_message, str(e))
    
    def _should_generate_code(self, user_message: str, intent: Dict) -> bool:
        """Determine if code generation is needed"""
        code_keywords = [
            "code", "python", "implementation", "script", "algorithm",
            "show me how", "generate", "create", "build", "develop"
        ]
        
        return (
            any(keyword in user_message.lower() for keyword in code_keywords) or
            intent.get("primary_intent") in ["ml_modeling", "statistical_analysis", "data_analysis"] or
            intent.get("complexity_level") == "high"
        )
    
    def _should_analyze_business(self, user_message: str) -> bool:
        """Determine if business analysis is needed"""
        business_keywords = [
            "business", "revenue", "profit", "roi", "kpi", "metric",
            "performance", "insight", "recommendation", "strategy",
            "customer", "sales", "marketing", "operations"
        ]
        
        return any(keyword in user_message.lower() for keyword in business_keywords)
    
    async def _generate_contextual_code(self, intent: Dict, data_context: Dict, 
                                       user_message: str) -> str:
        """Generate contextual code based on intent and data"""
        try:
            analysis_type = intent.get("primary_intent", "eda")
            
            # Map intent to code type
            code_type_mapping = {
                "data_analysis": "eda",
                "statistical_analysis": "statistical_analysis", 
                "ml_modeling": "machine_learning",
                "visualization": "visualization"
            }
            
            code_type = code_type_mapping.get(analysis_type, "eda")
            
            # Prepare parameters
            parameters = {
                "filename": "uploaded_data.csv",
                "user_query": user_message,
                "columns": data_context.get("column_names", []),
                "numeric_columns": data_context.get("numeric_columns", []),
                "categorical_columns": data_context.get("categorical_columns", [])
            }
            
            # Generate code
            code = self.code_generator.generate_analysis_code(
                code_type, data_context, parameters
            )
            
            return code
            
        except Exception as e:
            logger.error(f"Code generation error: {e}")
            return f"# Code generation error: {e}\n# Please try again with more specific requirements"
    
    async def _generate_business_insights(self, file_path: str, 
                                        data_context: Dict) -> Dict[str, Any]:
        """Generate business intelligence insights"""
        try:
            import pandas as pd
            
            # Load data for business analysis
            df = pd.read_csv(file_path)
            
            # Generate business insights
            insights = self.business_intelligence.analyze_business_context(df)
            
            return insights
            
        except Exception as e:
            logger.error(f"Business intelligence error: {e}")
            return {"error": str(e)}
    
    def _integrate_responses(self, ai_response: str, code_response: Optional[str],
                           business_insights: Optional[Dict], intent: Dict) -> str:
        """Integrate all response components into a cohesive response"""
        integrated_response = ai_response
        
        # Add code section if available
        if code_response:
            integrated_response += f"\n\n## 🛠️ Implementation Code\n\n```python\n{code_response}\n```"
        
        # Add business insights if available
        if business_insights and not business_insights.get("error"):
            integrated_response += self._format_business_insights(business_insights)
        
        # Add next steps based on intent
        next_steps = self._generate_next_steps(intent)
        if next_steps:
            integrated_response += f"\n\n## 🎯 Recommended Next Steps\n\n{next_steps}"
        
        return integrated_response
    
    def _format_business_insights(self, insights: Dict) -> str:
        """Format business insights for display"""
        if not insights or insights.get("error"):
            return ""
        
        formatted = "\n\n## 💼 Business Intelligence Insights\n\n"
        
        # Add domain information
        domain = insights.get("business_domain", "Unknown")
        formatted += f"**Business Domain**: {domain.replace('_', ' ').title()}\n\n"
        
        # Add key insights
        key_insights = insights.get("key_insights", [])
        if key_insights:
            formatted += "**Key Insights**:\n"
            for insight in key_insights[:3]:  # Top 3 insights
                if hasattr(insight, 'title') and hasattr(insight, 'description'):
                    formatted += f"• {insight.title}: {insight.description}\n"
        
        # Add recommendations
        recommendations = insights.get("recommendations", [])
        if recommendations:
            formatted += "\n**Strategic Recommendations**:\n"
            for rec in recommendations[:2]:  # Top 2 recommendations
                if hasattr(rec, 'title') and hasattr(rec, 'description'):
                    formatted += f"• {rec.title}: {rec.description}\n"
        
        return formatted
    
    def _generate_next_steps(self, intent: Dict) -> str:
        """Generate contextual next steps"""
        steps = []
        
        primary_intent = intent.get("primary_intent", "general_query")
        complexity = intent.get("complexity_level", "medium")
        
        if primary_intent == "data_analysis":
            steps.extend([
                "1. Review the data quality assessment",
                "2. Execute the provided analysis code",
                "3. Examine statistical patterns and outliers",
                "4. Consider additional feature engineering"
            ])
        elif primary_intent == "ml_modeling":
            steps.extend([
                "1. Run the model training pipeline",
                "2. Evaluate model performance metrics",
                "3. Analyze feature importance",
                "4. Plan model deployment and monitoring"
            ])
        elif primary_intent == "business_analysis":
            steps.extend([
                "1. Review business insights and KPIs",
                "2. Validate findings with stakeholders",
                "3. Implement recommended actions",
                "4. Set up monitoring for key metrics"
            ])
        
        if complexity == "high":
            steps.append("5. Consider advanced techniques and ensemble methods")
        
        return "\n".join(steps) if steps else ""
    
    async def _handle_system_error(self, user_message: str, error: str) -> Dict[str, Any]:
        """Handle system errors gracefully"""
        fallback_response = f"""I apologize, but I encountered a technical issue while processing your request. 

**Error Details**: {error}

**What I can still help with**:
• General data science questions and advice
• Statistical concepts and methodology explanations  
• Machine learning algorithm recommendations
• Data analysis best practices

Please try rephrasing your question or breaking it into smaller parts. If you're working with data, ensure the file is accessible and in a supported format (CSV, Excel, JSON).

Would you like me to help you with a specific data science concept or methodology instead?"""
        
        return {
            "status": "error",
            "response": fallback_response,
            "metadata": {
                "error": error,
                "fallback_used": True
            }
        }
    
    def _update_metrics(self, response_time: float, success: bool):
        """Update system performance metrics"""
        if success:
            self.metrics["successful_responses"] += 1
        else:
            self.metrics["error_count"] += 1
        
        # Update average response time
        total_responses = self.metrics["successful_responses"] + self.metrics["error_count"]
        self.metrics["average_response_time"] = (
            (self.metrics["average_response_time"] * (total_responses - 1) + response_time) 
            / total_responses
        )
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        error_rate = (
            self.metrics["error_count"] / max(self.metrics["total_requests"], 1)
        )
        
        health_status = "healthy"
        if error_rate > 0.1:  # More than 10% error rate
            health_status = "degraded"
        elif error_rate > 0.05:  # More than 5% error rate
            health_status = "warning"
        
        return {
            "status": health_status,
            "components": self.system_health,
            "metrics": self.metrics,
            "uptime": "operational",
            "last_updated": "2024-12-19T10:30:00Z"
        }
    
    async def optimize_performance(self):
        """Optimize system performance based on usage patterns"""
        try:
            # Clear old context data
            if hasattr(self.intelligent_ai.context_manager, 'session_context'):
                context = self.intelligent_ai.context_manager.session_context
                
                # Keep only recent data (last 24 hours)
                from datetime import datetime, timedelta
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                # Clean old analyses
                context["analyses"] = [
                    analysis for analysis in context["analyses"]
                    if analysis.get("timestamp", datetime.min) > cutoff_time
                ]
                
                # Clean old conversations
                context["conversation_history"] = [
                    conv for conv in context["conversation_history"]
                    if conv.get("timestamp", datetime.min) > cutoff_time
                ]
            
            logger.info("System performance optimized")
            
        except Exception as e:
            logger.error(f"Performance optimization error: {e}")

# Global intelligent system orchestrator
intelligent_system = IntelligentSystemOrchestrator() 