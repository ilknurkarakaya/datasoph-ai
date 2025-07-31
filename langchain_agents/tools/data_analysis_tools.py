"""
DATASOPH AI - Data Analysis Tools
Comprehensive data analysis capabilities for LangChain agents
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DataAnalysisTools:
    """Advanced data analysis tools for Datasoph AI"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.json', '.parquet']
        self.current_dataset = None
        self.analysis_cache = {}
    
    def analyze_dataset(self, input_description: str) -> str:
        """
        Perform comprehensive dataset analysis
        """
        try:
            # Parse input to extract file path and analysis type
            analysis_params = self._parse_analysis_input(input_description)
            
            if analysis_params.get('file_path'):
                # Load dataset
                df = self._load_dataset(analysis_params['file_path'])
                if df is None:
                    return "Error: Could not load the specified dataset."
                
                self.current_dataset = df
            elif self.current_dataset is not None:
                df = self.current_dataset
            else:
                return "Error: No dataset specified or loaded. Please provide a file path."
            
            # Perform analysis
            analysis_type = analysis_params.get('type', 'comprehensive')
            
            if analysis_type == 'comprehensive':
                return self._comprehensive_analysis(df)
            elif analysis_type == 'summary':
                return self._basic_summary(df)
            elif analysis_type == 'quality':
                return self._data_quality_analysis(df)
            elif analysis_type == 'distribution':
                return self._distribution_analysis(df)
            else:
                return self._comprehensive_analysis(df)
                
        except Exception as e:
            logger.error(f"Error in dataset analysis: {e}")
            return f"Analysis error: {str(e)}"
    
    def generate_data_summary(self, input_description: str) -> str:
        """
        Generate a comprehensive data summary
        """
        try:
            # Parse input
            params = self._parse_analysis_input(input_description)
            
            if params.get('file_path'):
                df = self._load_dataset(params['file_path'])
                if df is None:
                    return "Error: Could not load the specified dataset."
            elif self.current_dataset is not None:
                df = self.current_dataset
            else:
                return "Error: No dataset available for summary."
            
            # Generate summary
            summary = {
                "Dataset Overview": {
                    "Shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
                    "Memory Usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
                    "Data Types": df.dtypes.value_counts().to_dict()
                },
                "Numerical Summary": self._get_numerical_summary(df),
                "Categorical Summary": self._get_categorical_summary(df),
                "Missing Data": self._get_missing_data_summary(df),
                "Key Insights": self._generate_insights(df)
            }
            
            return self._format_summary_output(summary)
            
        except Exception as e:
            logger.error(f"Error generating data summary: {e}")
            return f"Summary generation error: {str(e)}"
    
    def time_series_analysis(self, input_description: str) -> str:
        """
        Perform time series analysis
        """
        try:
            # Parse input for time series parameters
            params = self._parse_analysis_input(input_description)
            
            if params.get('file_path'):
                df = self._load_dataset(params['file_path'])
            elif self.current_dataset is not None:
                df = self.current_dataset
            else:
                return "Error: No dataset available for time series analysis."
            
            # Identify date columns
            date_columns = self._identify_date_columns(df)
            if not date_columns:
                return "Error: No date/time columns found in the dataset."
            
            # Perform time series analysis
            date_col = date_columns[0]  # Use first date column
            
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
                df[date_col] = pd.to_datetime(df[date_col])
            
            # Sort by date
            df = df.sort_values(date_col)
            
            # Analyze time series patterns
            results = {
                "Time Range": f"{df[date_col].min()} to {df[date_col].max()}",
                "Data Points": len(df),
                "Frequency": self._detect_frequency(df[date_col]),
                "Trends": self._analyze_trends(df, date_col),
                "Seasonality": self._detect_seasonality(df, date_col),
                "Missing Periods": self._find_missing_periods(df, date_col)
            }
            
            return self._format_time_series_output(results)
            
        except Exception as e:
            logger.error(f"Error in time series analysis: {e}")
            return f"Time series analysis error: {str(e)}"
    
    def _load_dataset(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load dataset from file path"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None
            
            if file_path.suffix.lower() == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif file_path.suffix.lower() == '.json':
                return pd.read_json(file_path)
            elif file_path.suffix.lower() == '.parquet':
                return pd.read_parquet(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path.suffix}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None
    
    def _parse_analysis_input(self, input_str: str) -> Dict[str, Any]:
        """Parse analysis input to extract parameters"""
        try:
            params = {}
            
            # Look for file path
            words = input_str.split()
            for word in words:
                if any(ext in word.lower() for ext in self.supported_formats):
                    params['file_path'] = word.strip('\'"')
                    break
            
            # Determine analysis type
            input_lower = input_str.lower()
            if 'summary' in input_lower:
                params['type'] = 'summary'
            elif 'quality' in input_lower:
                params['type'] = 'quality'
            elif 'distribution' in input_lower:
                params['type'] = 'distribution'
            elif 'time series' in input_lower or 'temporal' in input_lower:
                params['type'] = 'time_series'
            else:
                params['type'] = 'comprehensive'
            
            return params
            
        except Exception as e:
            logger.error(f"Error parsing analysis input: {e}")
            return {'type': 'comprehensive'}
    
    def _comprehensive_analysis(self, df: pd.DataFrame) -> str:
        """Perform comprehensive dataset analysis"""
        try:
            analysis = {
                "Basic Info": {
                    "Shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
                    "Columns": list(df.columns),
                    "Data Types": df.dtypes.astype(str).to_dict(),
                    "Memory Usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
                },
                "Numerical Analysis": self._get_numerical_summary(df),
                "Categorical Analysis": self._get_categorical_summary(df),
                "Data Quality": {
                    "Missing Values": df.isnull().sum().to_dict(),
                    "Duplicate Rows": df.duplicated().sum(),
                    "Completeness": f"{(1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%"
                },
                "Insights": self._generate_insights(df)
            }
            
            return self._format_analysis_output(analysis)
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return f"Analysis error: {str(e)}"
    
    def _get_numerical_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary for numerical columns"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return {"message": "No numerical columns found"}
            
            summary = {}
            for col in numeric_cols:
                summary[col] = {
                    "count": int(df[col].count()),
                    "mean": round(df[col].mean(), 3),
                    "std": round(df[col].std(), 3),
                    "min": round(df[col].min(), 3),
                    "25%": round(df[col].quantile(0.25), 3),
                    "50%": round(df[col].median(), 3),
                    "75%": round(df[col].quantile(0.75), 3),
                    "max": round(df[col].max(), 3),
                    "outliers": self._count_outliers(df[col])
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error in numerical summary: {e}")
            return {"error": str(e)}
    
    def _get_categorical_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary for categorical columns"""
        try:
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            
            if len(cat_cols) == 0:
                return {"message": "No categorical columns found"}
            
            summary = {}
            for col in cat_cols:
                summary[col] = {
                    "unique_count": df[col].nunique(),
                    "most_frequent": df[col].mode().iloc[0] if not df[col].mode().empty else "N/A",
                    "frequency": int(df[col].value_counts().iloc[0]) if len(df[col].value_counts()) > 0 else 0,
                    "top_5_values": df[col].value_counts().head().to_dict()
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error in categorical summary: {e}")
            return {"error": str(e)}
    
    def _get_missing_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get missing data summary"""
        try:
            missing = df.isnull().sum()
            missing_percent = (missing / len(df)) * 100
            
            missing_summary = {}
            for col in df.columns:
                if missing[col] > 0:
                    missing_summary[col] = {
                        "count": int(missing[col]),
                        "percentage": round(missing_percent[col], 2)
                    }
            
            return {
                "total_missing": int(missing.sum()),
                "columns_with_missing": len(missing_summary),
                "by_column": missing_summary
            }
            
        except Exception as e:
            logger.error(f"Error in missing data summary: {e}")
            return {"error": str(e)}
    
    def _generate_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate key insights about the dataset"""
        try:
            insights = []
            
            # Shape insights
            if df.shape[0] > 100000:
                insights.append("Large dataset with over 100,000 rows - consider sampling for exploration")
            elif df.shape[0] < 100:
                insights.append("Small dataset - statistical analysis may have limited power")
            
            # Missing data insights
            missing_percent = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            if missing_percent > 20:
                insights.append(f"High missing data rate ({missing_percent:.1f}%) - data cleaning recommended")
            elif missing_percent > 5:
                insights.append(f"Moderate missing data ({missing_percent:.1f}%) - investigate patterns")
            
            # Data type insights
            numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
            cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
            
            if numeric_cols > cat_cols:
                insights.append("Primarily numerical data - suitable for statistical analysis and ML")
            elif cat_cols > numeric_cols:
                insights.append("Primarily categorical data - consider encoding for ML models")
            
            # Duplicate insights
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                insights.append(f"Found {duplicates} duplicate rows - consider deduplication")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return ["Error generating insights"]
    
    def _count_outliers(self, series: pd.Series) -> int:
        """Count outliers using IQR method"""
        try:
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = series[(series < lower_bound) | (series > upper_bound)]
            return len(outliers)
            
        except Exception:
            return 0
    
    def _identify_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify date/time columns in the dataset"""
        try:
            date_columns = []
            
            for col in df.columns:
                # Check if already datetime
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    date_columns.append(col)
                    continue
                
                # Try to parse as datetime
                if df[col].dtype == 'object':
                    sample = df[col].dropna().head(100)
                    try:
                        pd.to_datetime(sample)
                        date_columns.append(col)
                    except:
                        continue
            
            return date_columns
            
        except Exception as e:
            logger.error(f"Error identifying date columns: {e}")
            return []
    
    def _detect_frequency(self, date_series: pd.Series) -> str:
        """Detect the frequency of time series data"""
        try:
            # Calculate differences between consecutive dates
            diffs = date_series.diff().dropna()
            mode_diff = diffs.mode().iloc[0] if not diffs.mode().empty else pd.Timedelta(days=1)
            
            days = mode_diff.days
            if days == 1:
                return "Daily"
            elif days == 7:
                return "Weekly"
            elif 28 <= days <= 31:
                return "Monthly"
            elif 90 <= days <= 92:
                return "Quarterly"
            elif 365 <= days <= 366:
                return "Yearly"
            else:
                return f"Irregular ({days} days)"
                
        except Exception as e:
            logger.error(f"Error detecting frequency: {e}")
            return "Unknown"
    
    def _analyze_trends(self, df: pd.DataFrame, date_col: str) -> Dict[str, Any]:
        """Analyze trends in time series data"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return {"message": "No numerical columns for trend analysis"}
            
            trends = {}
            for col in numeric_cols[:3]:  # Analyze first 3 numeric columns
                # Simple linear trend
                x = np.arange(len(df))
                y = df[col].fillna(df[col].mean())
                
                correlation = np.corrcoef(x, y)[0, 1]
                
                if correlation > 0.5:
                    trend = "Strong Upward"
                elif correlation > 0.2:
                    trend = "Moderate Upward"
                elif correlation > -0.2:
                    trend = "Stable"
                elif correlation > -0.5:
                    trend = "Moderate Downward"
                else:
                    trend = "Strong Downward"
                
                trends[col] = {
                    "trend": trend,
                    "correlation": round(correlation, 3)
                }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}
    
    def _detect_seasonality(self, df: pd.DataFrame, date_col: str) -> str:
        """Simple seasonality detection"""
        try:
            # Basic seasonality detection based on data frequency
            date_range = df[date_col].max() - df[date_col].min()
            
            if date_range.days >= 365:
                return "Potential yearly seasonality detected"
            elif date_range.days >= 90:
                return "Potential quarterly patterns possible"
            elif date_range.days >= 30:
                return "Potential monthly patterns possible"
            else:
                return "Insufficient data for seasonality analysis"
                
        except Exception as e:
            logger.error(f"Error detecting seasonality: {e}")
            return "Seasonality analysis unavailable"
    
    def _find_missing_periods(self, df: pd.DataFrame, date_col: str) -> Dict[str, Any]:
        """Find missing time periods in the data"""
        try:
            # Create expected date range
            date_range = pd.date_range(
                start=df[date_col].min(),
                end=df[date_col].max(),
                freq='D'  # Assume daily frequency
            )
            
            missing_dates = date_range.difference(df[date_col])
            
            return {
                "missing_periods": len(missing_dates),
                "first_missing": str(missing_dates[0]) if len(missing_dates) > 0 else "None",
                "completeness": f"{((len(date_range) - len(missing_dates)) / len(date_range)) * 100:.1f}%"
            }
            
        except Exception as e:
            logger.error(f"Error finding missing periods: {e}")
            return {"error": str(e)}
    
    def _format_analysis_output(self, analysis: Dict[str, Any]) -> str:
        """Format analysis output for display"""
        try:
            output = "📊 **COMPREHENSIVE DATA ANALYSIS**\n\n"
            
            # Basic Info
            if "Basic Info" in analysis:
                output += "🔍 **Dataset Overview:**\n"
                info = analysis["Basic Info"]
                output += f"• Shape: {info['Shape']}\n"
                output += f"• Memory Usage: {info['Memory Usage']}\n"
                output += f"• Data Types: {len(info['Data Types'])} different types\n\n"
            
            # Numerical Analysis
            if "Numerical Analysis" in analysis and "error" not in analysis["Numerical Analysis"]:
                output += "📈 **Numerical Columns Analysis:**\n"
                num_analysis = analysis["Numerical Analysis"]
                if "message" not in num_analysis:
                    for col, stats in list(num_analysis.items())[:3]:  # Show first 3
                        output += f"• {col}: Mean={stats['mean']}, Std={stats['std']}, Outliers={stats['outliers']}\n"
                    if len(num_analysis) > 3:
                        output += f"• ... and {len(num_analysis) - 3} more numerical columns\n"
                else:
                    output += f"• {num_analysis['message']}\n"
                output += "\n"
            
            # Data Quality
            if "Data Quality" in analysis:
                output += "🔍 **Data Quality Assessment:**\n"
                quality = analysis["Data Quality"]
                output += f"• Completeness: {quality['Completeness']}\n"
                output += f"• Duplicate Rows: {quality['Duplicate Rows']}\n"
                missing_cols = sum(1 for v in quality['Missing Values'].values() if v > 0)
                output += f"• Columns with Missing Data: {missing_cols}\n\n"
            
            # Insights
            if "Insights" in analysis:
                output += "💡 **Key Insights:**\n"
                for insight in analysis["Insights"]:
                    output += f"• {insight}\n"
            
            return output
            
        except Exception as e:
            logger.error(f"Error formatting analysis output: {e}")
            return f"Analysis completed but formatting error: {str(e)}"
    
    def _format_summary_output(self, summary: Dict[str, Any]) -> str:
        """Format summary output for display"""
        try:
            output = "📋 **DATA SUMMARY REPORT**\n\n"
            
            for section, content in summary.items():
                output += f"**{section}:**\n"
                
                if isinstance(content, dict):
                    for key, value in content.items():
                        if isinstance(value, (int, float, str)):
                            output += f"• {key}: {value}\n"
                        elif isinstance(value, dict) and len(value) <= 3:
                            output += f"• {key}: {value}\n"
                elif isinstance(content, list):
                    for item in content:
                        output += f"• {item}\n"
                else:
                    output += f"• {content}\n"
                
                output += "\n"
            
            return output
            
        except Exception as e:
            logger.error(f"Error formatting summary output: {e}")
            return f"Summary generated but formatting error: {str(e)}"
    
    def _format_time_series_output(self, results: Dict[str, Any]) -> str:
        """Format time series analysis output"""
        try:
            output = "📅 **TIME SERIES ANALYSIS**\n\n"
            
            for key, value in results.items():
                if isinstance(value, dict):
                    output += f"**{key}:**\n"
                    for subkey, subvalue in value.items():
                        output += f"• {subkey}: {subvalue}\n"
                    output += "\n"
                else:
                    output += f"**{key}:** {value}\n"
            
            return output
            
        except Exception as e:
            logger.error(f"Error formatting time series output: {e}")
            return f"Time series analysis completed but formatting error: {str(e)}" 