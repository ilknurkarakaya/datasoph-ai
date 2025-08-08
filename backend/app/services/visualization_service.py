"""
DataSoph AI - Advanced Data Visualization Service
World-class data visualization with Plotly, Seaborn, and more
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Optional, Any, Tuple
import base64
import io
from pathlib import Path
import logging

# Visualization libraries
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import plotly.utils
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class VisualizationService:
    """Advanced data visualization service"""
    
    def __init__(self):
        self.default_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def create_comprehensive_dashboard(self, file_path: str) -> Dict[str, Any]:
        """Create comprehensive data dashboard"""
        try:
            # Load data
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            dashboard = {
                "summary": self._create_data_summary(df),
                "visualizations": []
            }
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # 1. Data Overview Chart
            overview_chart = self._create_data_overview_chart(df)
            if overview_chart:
                dashboard["visualizations"].append(overview_chart)
            
            # 2. Missing Data Heatmap
            missing_chart = self._create_missing_data_chart(df)
            if missing_chart:
                dashboard["visualizations"].append(missing_chart)
            
            # 3. Numeric Variables Distribution
            if numeric_cols:
                dist_charts = self._create_distribution_charts(df, numeric_cols[:6])
                dashboard["visualizations"].extend(dist_charts)
            
            # 4. Correlation Heatmap
            if len(numeric_cols) >= 2:
                corr_chart = self._create_correlation_heatmap(df, numeric_cols)
                if corr_chart:
                    dashboard["visualizations"].append(corr_chart)
            
            # 5. Categorical Analysis
            if categorical_cols:
                cat_charts = self._create_categorical_charts(df, categorical_cols[:4])
                dashboard["visualizations"].extend(cat_charts)
            
            # 6. Outlier Detection
            if numeric_cols:
                outlier_chart = self._create_outlier_chart(df, numeric_cols[:4])
                if outlier_chart:
                    dashboard["visualizations"].append(outlier_chart)
            
            # 7. Pairwise Relationships
            if len(numeric_cols) >= 2:
                pair_chart = self._create_pairplot_chart(df, numeric_cols[:4])
                if pair_chart:
                    dashboard["visualizations"].append(pair_chart)
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Dashboard creation error: {e}")
            return {"error": f"Dashboard creation failed: {str(e)}"}
    
    def create_custom_visualization(self, file_path: str, chart_type: str, 
                                  x_column: Optional[str] = None, 
                                  y_column: Optional[str] = None,
                                  color_column: Optional[str] = None,
                                  **kwargs) -> Dict[str, Any]:
        """Create custom visualization based on user specification"""
        try:
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            chart_config = {
                "type": chart_type,
                "x_column": x_column,
                "y_column": y_column,
                "color_column": color_column,
                "title": kwargs.get("title", f"{chart_type.title()} Chart"),
                "height": kwargs.get("height", 500),
                "width": kwargs.get("width", 700)
            }
            
            if chart_type == "scatter":
                return self._create_scatter_plot(df, x_column, y_column, color_column, chart_config)
            elif chart_type == "line":
                return self._create_line_plot(df, x_column, y_column, color_column, chart_config)
            elif chart_type == "bar":
                return self._create_bar_plot(df, x_column, y_column, color_column, chart_config)
            elif chart_type == "histogram":
                return self._create_histogram(df, x_column, chart_config)
            elif chart_type == "box":
                return self._create_box_plot(df, x_column, y_column, chart_config)
            elif chart_type == "heatmap":
                return self._create_heatmap(df, chart_config)
            else:
                return {"error": f"Chart type '{chart_type}' not supported"}
                
        except Exception as e:
            logger.error(f"Custom visualization error: {e}")
            return {"error": f"Visualization creation failed: {str(e)}"}
    
    def _load_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load data from file"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                return pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif file_ext == '.json':
                return pd.read_json(file_path)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Data loading error: {e}")
            return None
    
    def _create_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Create data summary"""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": len(df.select_dtypes(include=['object', 'category']).columns),
            "missing_values": df.isnull().sum().sum(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024**2),
            "column_names": df.columns.tolist()
        }
    
    def _create_data_overview_chart(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Create data overview chart"""
        if not HAS_PLOTLY:
            return None
            
        try:
            numeric_count = len(df.select_dtypes(include=[np.number]).columns)
            categorical_count = len(df.select_dtypes(include=['object', 'category']).columns)
            datetime_count = len(df.select_dtypes(include=['datetime64']).columns)
            
            fig = go.Figure(data=[
                go.Bar(name='Column Types', 
                      x=['Numeric', 'Categorical', 'DateTime'],
                      y=[numeric_count, categorical_count, datetime_count],
                      marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'])
            ])
            
            fig.update_layout(
                title="Data Overview - Column Types",
                xaxis_title="Column Type",
                yaxis_title="Count",
                height=400
            )
            
            return {
                "id": "data_overview",
                "title": "Data Overview",
                "type": "bar",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            logger.error(f"Data overview chart error: {e}")
            return None
    
    def _create_missing_data_chart(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Create missing data visualization"""
        if not HAS_PLOTLY:
            return None
            
        try:
            missing_data = df.isnull().sum()
            missing_pct = (missing_data / len(df)) * 100
            
            if missing_data.sum() == 0:
                return None
                
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing_Count': missing_data.values,
                'Missing_Percentage': missing_pct.values
            }).sort_values('Missing_Count', ascending=True)
            
            missing_df = missing_df[missing_df['Missing_Count'] > 0]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=missing_df['Column'],
                x=missing_df['Missing_Percentage'],
                orientation='h',
                name='Missing %',
                marker_color='#ff7f0e'
            ))
            
            fig.update_layout(
                title="Missing Data Analysis",
                xaxis_title="Missing Percentage (%)",
                yaxis_title="Columns",
                height=max(400, len(missing_df) * 30)
            )
            
            return {
                "id": "missing_data",
                "title": "Missing Data Analysis",
                "type": "bar",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            logger.error(f"Missing data chart error: {e}")
            return None
    
    def _create_distribution_charts(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """Create distribution charts for numeric columns"""
        charts = []
        
        if not HAS_PLOTLY:
            return charts
            
        for col in numeric_cols:
            try:
                fig = go.Figure()
                
                fig.add_trace(go.Histogram(
                    x=df[col].dropna(),
                    name=col,
                    nbinsx=30,
                    marker_color='#1f77b4',
                    opacity=0.7
                ))
                
                fig.update_layout(
                    title=f"Distribution of {col}",
                    xaxis_title=col,
                    yaxis_title="Frequency",
                    height=400
                )
                
                charts.append({
                    "id": f"dist_{col.lower().replace(' ', '_')}",
                    "title": f"Distribution of {col}",
                    "type": "histogram",
                    "plotly_json": json.loads(fig.to_json())
                })
                
            except Exception as e:
                logger.error(f"Distribution chart error for {col}: {e}")
                continue
                
        return charts
    
    def _create_correlation_heatmap(self, df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """Create correlation heatmap"""
        if not HAS_PLOTLY or len(numeric_cols) < 2:
            return None
            
        try:
            corr_matrix = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title="Correlation Matrix",
                height=max(400, len(numeric_cols) * 40),
                width=max(500, len(numeric_cols) * 40)
            )
            
            return {
                "id": "correlation_heatmap",
                "title": "Correlation Matrix",
                "type": "heatmap",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            logger.error(f"Correlation heatmap error: {e}")
            return None
    
    def _create_categorical_charts(self, df: pd.DataFrame, categorical_cols: List[str]) -> List[Dict[str, Any]]:
        """Create charts for categorical columns"""
        charts = []
        
        if not HAS_PLOTLY:
            return charts
            
        for col in categorical_cols:
            try:
                value_counts = df[col].value_counts().head(10)  # Top 10 categories
                
                fig = go.Figure(data=[
                    go.Bar(x=value_counts.index, y=value_counts.values,
                          marker_color='#2ca02c')
                ])
                
                fig.update_layout(
                    title=f"Distribution of {col}",
                    xaxis_title=col,
                    yaxis_title="Count",
                    height=400,
                    xaxis_tickangle=-45
                )
                
                charts.append({
                    "id": f"cat_{col.lower().replace(' ', '_')}",
                    "title": f"Distribution of {col}",
                    "type": "bar",
                    "plotly_json": json.loads(fig.to_json())
                })
                
            except Exception as e:
                logger.error(f"Categorical chart error for {col}: {e}")
                continue
                
        return charts
    
    def _create_outlier_chart(self, df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """Create outlier detection chart"""
        if not HAS_PLOTLY:
            return None
            
        try:
            fig = make_subplots(
                rows=1, cols=len(numeric_cols),
                subplot_titles=numeric_cols,
                shared_yaxis=False
            )
            
            for i, col in enumerate(numeric_cols, 1):
                fig.add_trace(
                    go.Box(y=df[col].dropna(), name=col, boxpoints='outliers'),
                    row=1, col=i
                )
            
            fig.update_layout(
                title="Outlier Detection (Box Plots)",
                height=400,
                showlegend=False
            )
            
            return {
                "id": "outlier_detection",
                "title": "Outlier Detection",
                "type": "box",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            logger.error(f"Outlier chart error: {e}")
            return None
    
    def _create_pairplot_chart(self, df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """Create pairwise relationship chart"""
        if not HAS_PLOTLY or len(numeric_cols) < 2:
            return None
            
        try:
            # Sample data if too large
            sample_df = df.sample(min(1000, len(df))) if len(df) > 1000 else df
            
            fig = px.scatter_matrix(
                sample_df[numeric_cols],
                title="Pairwise Relationships"
            )
            
            fig.update_layout(height=600, width=800)
            
            return {
                "id": "pairplot",
                "title": "Pairwise Relationships",
                "type": "scatter_matrix",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            logger.error(f"Pairplot error: {e}")
            return None
    
    def _create_scatter_plot(self, df: pd.DataFrame, x_col: str, y_col: str, 
                           color_col: Optional[str], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create scatter plot"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            if color_col:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=config["title"])
            else:
                fig = px.scatter(df, x=x_col, y=y_col, title=config["title"])
            
            fig.update_layout(height=config["height"], width=config["width"])
            
            return {
                "id": "custom_scatter",
                "title": config["title"],
                "type": "scatter",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Scatter plot error: {str(e)}"}
    
    def _create_line_plot(self, df: pd.DataFrame, x_col: str, y_col: str, 
                         color_col: Optional[str], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create line plot"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            if color_col:
                fig = px.line(df, x=x_col, y=y_col, color=color_col, title=config["title"])
            else:
                fig = px.line(df, x=x_col, y=y_col, title=config["title"])
            
            fig.update_layout(height=config["height"], width=config["width"])
            
            return {
                "id": "custom_line",
                "title": config["title"],
                "type": "line",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Line plot error: {str(e)}"}
    
    def _create_bar_plot(self, df: pd.DataFrame, x_col: str, y_col: Optional[str], 
                        color_col: Optional[str], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create bar plot"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            if y_col:
                if color_col:
                    fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=config["title"])
                else:
                    fig = px.bar(df, x=x_col, y=y_col, title=config["title"])
            else:
                # Count plot
                value_counts = df[x_col].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values, title=config["title"])
                fig.update_xaxes(title=x_col)
                fig.update_yaxes(title="Count")
            
            fig.update_layout(height=config["height"], width=config["width"])
            
            return {
                "id": "custom_bar",
                "title": config["title"],
                "type": "bar",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Bar plot error: {str(e)}"}
    
    def _create_histogram(self, df: pd.DataFrame, x_col: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create histogram"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            fig = px.histogram(df, x=x_col, title=config["title"])
            fig.update_layout(height=config["height"], width=config["width"])
            
            return {
                "id": "custom_histogram",
                "title": config["title"],
                "type": "histogram",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Histogram error: {str(e)}"}
    
    def _create_box_plot(self, df: pd.DataFrame, x_col: Optional[str], y_col: str, 
                        config: Dict[str, Any]) -> Dict[str, Any]:
        """Create box plot"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            if x_col:
                fig = px.box(df, x=x_col, y=y_col, title=config["title"])
            else:
                fig = px.box(df, y=y_col, title=config["title"])
            
            fig.update_layout(height=config["height"], width=config["width"])
            
            return {
                "id": "custom_box",
                "title": config["title"],
                "type": "box",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Box plot error: {str(e)}"}
    
    def _create_heatmap(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create heatmap"""
        if not HAS_PLOTLY:
            return {"error": "Plotly not available"}
            
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) < 2:
                return {"error": "Need at least 2 numeric columns for heatmap"}
            
            corr_matrix = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0
            ))
            
            fig.update_layout(
                title=config["title"],
                height=config["height"], 
                width=config["width"]
            )
            
            return {
                "id": "custom_heatmap",
                "title": config["title"],
                "type": "heatmap",
                "plotly_json": json.loads(fig.to_json())
            }
            
        except Exception as e:
            return {"error": f"Heatmap error: {str(e)}"}

# Global visualization service instance
visualization_service = VisualizationService() 