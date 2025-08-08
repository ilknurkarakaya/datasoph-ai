"""
Business Intelligence Service for DataSoph AI
Provides business-focused analysis and actionable recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class BusinessInsight:
    """Structured business insight"""
    insight_type: str
    title: str
    description: str
    business_impact: str
    confidence_level: float
    action_items: List[str]
    metrics: Dict[str, Any]
    priority: str  # 'high', 'medium', 'low'

@dataclass
class BusinessRecommendation:
    """Actionable business recommendation"""
    recommendation_id: str
    category: str
    title: str
    description: str
    expected_impact: str
    implementation_effort: str
    timeline: str
    success_metrics: List[str]
    risk_level: str

class BusinessIntelligenceEngine:
    """Advanced business intelligence and recommendations"""
    
    def __init__(self):
        self.business_domains = {
            "customer_analytics": CustomerAnalytics(),
            "sales_analytics": SalesAnalytics(),
            "marketing_analytics": MarketingAnalytics(),
            "financial_analytics": FinancialAnalytics(),
            "operational_analytics": OperationalAnalytics()
        }
        
        self.kpi_library = self._initialize_kpi_library()
        self.industry_benchmarks = self._load_industry_benchmarks()
    
    def analyze_business_context(self, df: pd.DataFrame, business_domain: str = "auto") -> Dict[str, Any]:
        """Analyze business context and generate insights"""
        try:
            # Auto-detect business domain if not specified
            if business_domain == "auto":
                business_domain = self._detect_business_domain(df)
            
            # Get appropriate analytics engine
            analytics_engine = self.business_domains.get(business_domain)
            if not analytics_engine:
                analytics_engine = self.business_domains["customer_analytics"]  # Default
            
            # Generate comprehensive business analysis
            analysis_result = {
                "business_domain": business_domain,
                "key_insights": analytics_engine.generate_insights(df),
                "kpi_analysis": self._analyze_kpis(df, business_domain),
                "recommendations": analytics_engine.generate_recommendations(df),
                "risk_assessment": self._assess_business_risks(df),
                "opportunity_analysis": self._identify_opportunities(df),
                "competitive_benchmarks": self._compare_to_benchmarks(df, business_domain),
                "action_plan": self._create_action_plan(df, business_domain)
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Business analysis error: {e}")
            return {"error": str(e)}
    
    def _detect_business_domain(self, df: pd.DataFrame) -> str:
        """Auto-detect business domain from data patterns"""
        column_names = ' '.join(df.columns).lower()
        
        # Customer analytics indicators
        if any(term in column_names for term in ['customer', 'user', 'client', 'churn', 'retention']):
            return "customer_analytics"
        
        # Sales analytics indicators
        elif any(term in column_names for term in ['sales', 'revenue', 'order', 'transaction', 'purchase']):
            return "sales_analytics"
        
        # Marketing analytics indicators
        elif any(term in column_names for term in ['campaign', 'conversion', 'click', 'impression', 'cpm', 'ctr']):
            return "marketing_analytics"
        
        # Financial analytics indicators
        elif any(term in column_names for term in ['profit', 'cost', 'expense', 'budget', 'financial']):
            return "financial_analytics"
        
        # Operations analytics indicators
        elif any(term in column_names for term in ['inventory', 'supply', 'production', 'logistics']):
            return "operational_analytics"
        
        return "customer_analytics"  # Default
    
    def _analyze_kpis(self, df: pd.DataFrame, domain: str) -> Dict[str, Any]:
        """Analyze key performance indicators"""
        kpi_results = {}
        domain_kpis = self.kpi_library.get(domain, {})
        
        for kpi_name, kpi_config in domain_kpis.items():
            try:
                kpi_value = self._calculate_kpi(df, kpi_config)
                benchmark = self.industry_benchmarks.get(domain, {}).get(kpi_name)
                
                kpi_results[kpi_name] = {
                    "value": kpi_value,
                    "benchmark": benchmark,
                    "performance": self._assess_kpi_performance(kpi_value, benchmark),
                    "trend": self._calculate_kpi_trend(df, kpi_config),
                    "business_impact": kpi_config.get("business_impact", "")
                }
            except Exception as e:
                logger.warning(f"Could not calculate KPI {kpi_name}: {e}")
        
        return kpi_results
    
    def _calculate_kpi(self, df: pd.DataFrame, kpi_config: Dict) -> float:
        """Calculate KPI value based on configuration"""
        calculation_type = kpi_config.get("calculation", "mean")
        column = kpi_config.get("column")
        
        if not column or column not in df.columns:
            return 0.0
        
        if calculation_type == "mean":
            return df[column].mean()
        elif calculation_type == "sum":
            return df[column].sum()
        elif calculation_type == "count":
            return len(df)
        elif calculation_type == "ratio":
            numerator = kpi_config.get("numerator")
            denominator = kpi_config.get("denominator")
            if numerator in df.columns and denominator in df.columns:
                return (df[numerator].sum() / df[denominator].sum()) * 100
        
        return 0.0
    
    def _assess_kpi_performance(self, value: float, benchmark: Optional[float]) -> str:
        """Assess KPI performance against benchmark"""
        if not benchmark:
            return "no_benchmark"
        
        if value >= benchmark * 1.1:
            return "excellent"
        elif value >= benchmark * 1.05:
            return "good"
        elif value >= benchmark * 0.95:
            return "average"
        elif value >= benchmark * 0.9:
            return "below_average"
        else:
            return "poor"
    
    def _calculate_kpi_trend(self, df: pd.DataFrame, kpi_config: Dict) -> str:
        """Calculate KPI trend if temporal data available"""
        # Simplified trend calculation
        # In production, would use time series analysis
        return "stable"
    
    def _assess_business_risks(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Assess business risks from data patterns"""
        risks = []
        
        # Data quality risks
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio > 0.2:
            risks.append({
                "type": "data_quality",
                "severity": "medium",
                "description": f"High missing data ratio ({missing_ratio:.1%}) may impact analysis reliability",
                "mitigation": "Implement data quality monitoring and improve data collection processes"
            })
        
        # Sample size risks
        if len(df) < 100:
            risks.append({
                "type": "statistical_power",
                "severity": "high",
                "description": "Small sample size may lead to unreliable insights",
                "mitigation": "Collect more data before making strategic decisions"
            })
        
        return risks
    
    def _identify_opportunities(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify business opportunities from data"""
        opportunities = []
        
        # High-value segments
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:3]:
                top_10_percent = df[col].quantile(0.9)
                high_value_count = len(df[df[col] >= top_10_percent])
                
                if high_value_count > 0:
                    opportunities.append({
                        "type": "high_value_segment",
                        "description": f"High-value segment in {col} represents {high_value_count} records",
                        "potential_impact": "Focus on replicating characteristics of top performers",
                        "action": f"Analyze what makes top 10% in {col} successful"
                    })
        
        return opportunities
    
    def _compare_to_benchmarks(self, df: pd.DataFrame, domain: str) -> Dict[str, Any]:
        """Compare metrics to industry benchmarks"""
        return {
            "industry": domain,
            "benchmark_comparison": "Analysis shows performance relative to industry standards",
            "competitive_position": "average",  # Would be calculated from actual benchmarks
            "improvement_areas": ["data quality", "sample size"]
        }
    
    def _create_action_plan(self, df: pd.DataFrame, domain: str) -> List[Dict[str, Any]]:
        """Create actionable business plan"""
        action_items = []
        
        # Data-driven action items
        action_items.append({
            "priority": "high",
            "category": "data_quality",
            "action": "Improve data collection and quality processes",
            "timeline": "2-4 weeks",
            "expected_outcome": "More reliable insights and decision-making"
        })
        
        action_items.append({
            "priority": "medium",
            "category": "analytics",
            "action": "Implement advanced analytics and monitoring",
            "timeline": "4-8 weeks",
            "expected_outcome": "Proactive business insights and trend identification"
        })
        
        return action_items
    
    def _initialize_kpi_library(self) -> Dict[str, Dict[str, Any]]:
        """Initialize KPI calculation library"""
        return {
            "customer_analytics": {
                "customer_lifetime_value": {
                    "calculation": "mean",
                    "column": "lifetime_value",
                    "business_impact": "Identifies most valuable customer segments"
                },
                "churn_rate": {
                    "calculation": "ratio",
                    "numerator": "churned_customers",
                    "denominator": "total_customers",
                    "business_impact": "Measures customer retention effectiveness"
                }
            },
            "sales_analytics": {
                "average_order_value": {
                    "calculation": "mean",
                    "column": "order_value",
                    "business_impact": "Measures sales effectiveness per transaction"
                },
                "conversion_rate": {
                    "calculation": "ratio",
                    "numerator": "conversions",
                    "denominator": "visitors",
                    "business_impact": "Measures sales funnel efficiency"
                }
            }
        }
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Load industry benchmark data"""
        return {
            "customer_analytics": {
                "churn_rate": 5.0,  # 5% monthly churn
                "customer_lifetime_value": 1000.0
            },
            "sales_analytics": {
                "conversion_rate": 2.5,  # 2.5% conversion rate
                "average_order_value": 150.0
            }
        }

class CustomerAnalytics:
    """Customer-focused business analytics"""
    
    def generate_insights(self, df: pd.DataFrame) -> List[BusinessInsight]:
        """Generate customer-focused insights"""
        insights = []
        
        # Customer segmentation insight
        if len(df) > 100:
            insights.append(BusinessInsight(
                insight_type="segmentation",
                title="Customer Segmentation Opportunity",
                description="Dataset size supports advanced customer segmentation analysis",
                business_impact="Can identify high-value customer segments for targeted marketing",
                confidence_level=0.8,
                action_items=[
                    "Perform RFM analysis",
                    "Create customer personas",
                    "Develop targeted campaigns"
                ],
                metrics={"customer_count": len(df)},
                priority="high"
            ))
        
        return insights
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[BusinessRecommendation]:
        """Generate customer analytics recommendations"""
        recommendations = []
        
        recommendations.append(BusinessRecommendation(
            recommendation_id="cust_001",
            category="customer_retention",
            title="Implement Customer Retention Program",
            description="Develop predictive churn model to identify at-risk customers",
            expected_impact="15-25% reduction in customer churn",
            implementation_effort="medium",
            timeline="8-12 weeks",
            success_metrics=["churn_rate", "customer_lifetime_value"],
            risk_level="low"
        ))
        
        return recommendations

class SalesAnalytics:
    """Sales-focused business analytics"""
    
    def generate_insights(self, df: pd.DataFrame) -> List[BusinessInsight]:
        """Generate sales-focused insights"""
        insights = []
        
        # Revenue opportunity insight
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if any('revenue' in col.lower() or 'sales' in col.lower() for col in numeric_cols):
            insights.append(BusinessInsight(
                insight_type="revenue_optimization",
                title="Revenue Optimization Opportunity",
                description="Sales data shows potential for revenue optimization analysis",
                business_impact="Identify top-performing products and sales strategies",
                confidence_level=0.9,
                action_items=[
                    "Analyze sales performance by product/region",
                    "Identify seasonal patterns",
                    "Optimize pricing strategy"
                ],
                metrics={"data_completeness": 0.85},
                priority="high"
            ))
        
        return insights
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[BusinessRecommendation]:
        """Generate sales analytics recommendations"""
        recommendations = []
        
        recommendations.append(BusinessRecommendation(
            recommendation_id="sales_001",
            category="sales_forecasting",
            title="Implement Sales Forecasting Model",
            description="Build predictive model for sales forecasting and planning",
            expected_impact="10-20% improvement in forecast accuracy",
            implementation_effort="high",
            timeline="12-16 weeks",
            success_metrics=["forecast_accuracy", "sales_variance"],
            risk_level="medium"
        ))
        
        return recommendations

class MarketingAnalytics:
    """Marketing-focused business analytics"""
    
    def generate_insights(self, df: pd.DataFrame) -> List[BusinessInsight]:
        """Generate marketing-focused insights"""
        return []
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[BusinessRecommendation]:
        """Generate marketing analytics recommendations"""
        return []

class FinancialAnalytics:
    """Financial-focused business analytics"""
    
    def generate_insights(self, df: pd.DataFrame) -> List[BusinessInsight]:
        """Generate financial-focused insights"""
        return []
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[BusinessRecommendation]:
        """Generate financial analytics recommendations"""
        return []

class OperationalAnalytics:
    """Operations-focused business analytics"""
    
    def generate_insights(self, df: pd.DataFrame) -> List[BusinessInsight]:
        """Generate operations-focused insights"""
        return []
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[BusinessRecommendation]:
        """Generate operational analytics recommendations"""
        return []

# Global business intelligence service instance
business_intelligence = BusinessIntelligenceEngine() 