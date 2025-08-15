"""
Simple Code Executor - Execute basic Python for data analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import logging
import sys
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleCodeExecutor:
    def __init__(self):
        self.safe_globals = {
            'pd': pd, 'np': np, 'plt': plt, 'sns': sns,
            '__builtins__': {'len': len, 'sum': sum, 'max': max, 'min': min, 'round': round}
        }
    
    def execute(self, code: str, df: pd.DataFrame = None) -> Dict[str, Any]:
        """Execute simple pandas/numpy code"""
        try:
            # Add dataframe to context
            if df is not None:
                self.safe_globals['df'] = df
                self.safe_globals['data'] = df
            
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Execute code
            exec(code, self.safe_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return {'success': True, 'output': output}
            
        except Exception as e:
            logger.error(f"Code execution error: {e}")
            return {'success': False, 'error': str(e)}

# Global instance
executor = SimpleCodeExecutor()