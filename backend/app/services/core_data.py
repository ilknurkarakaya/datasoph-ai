"""
Core Data Service - Minimal file processing and analysis
Replaces: enhanced_file_processor.py + universal_file_handler.py + auto_eda_generator.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Fix macOS GUI thread issue
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CoreData:
    def __init__(self):
        self.figures_dir = "figures"
        os.makedirs(self.figures_dir, exist_ok=True)
        plt.style.use('default')
    
    def load_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load any common file type"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                return pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            else:
                return None
        except Exception as e:
            logger.error(f"File load error: {e}")
            return None
    
    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Basic analysis - no complexity"""
        try:
            # Simple stats - JSON serializable
            analysis = {
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()},
                'missing': {col: int(count) for col, count in df.isnull().sum().to_dict().items()},
                'summary': {col: {k: float(v) if pd.notna(v) else None for k, v in stats.items()} 
                           for col, stats in df.describe().to_dict().items()} if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
            }
            
            # Create simple visualization
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                plt.figure(figsize=(10, 6))
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='RdBu_r')
                plt.title('Correlation Matrix')
                plt.tight_layout()
                chart_path = f"{self.figures_dir}/correlation.png"
                plt.savefig(chart_path)
                plt.close()
                analysis['chart'] = chart_path
            
            return analysis
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {'error': str(e)}

# Global instance
data = CoreData()
