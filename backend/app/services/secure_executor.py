"""
DataSoph AI - Secure Code Executor
Enterprise-grade secure Python code execution with comprehensive sandboxing
"""

import ast
import sys
import io
import types
import time
import signal
import multiprocessing
import resource
from typing import Dict, Any, Optional, List, Union
from contextlib import redirect_stdout, redirect_stderr
import logging
import traceback
import inspect
import builtins

logger = logging.getLogger(__name__)

class CodeExecutionError(Exception):
    """Custom exception for code execution errors"""
    pass

class SecurityViolationError(Exception):
    """Exception for security policy violations"""
    pass

class ExecutionTimeoutError(Exception):
    """Exception for execution timeout"""
    pass

class SecureCodeExecutor:
    """
    Enterprise-grade secure Python code executor with comprehensive safety
    """
    
    def __init__(self):
        self.max_execution_time = 30  # seconds
        self.max_memory_mb = 512      # MB
        self.max_output_length = 50000  # characters
        
        # Allowed imports - comprehensive data science stack
        self.allowed_imports = {
            # Core data science
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'scipy',
            'sklearn', 'statsmodels', 'xgboost', 'lightgbm', 'catboost',
            
            # Deep learning
            'tensorflow', 'torch', 'keras',
            
            # Data processing
            'json', 'csv', 'datetime', 'collections', 'itertools',
            'math', 'statistics', 'random', 're',
            
            # Visualization
            'altair', 'bokeh',
            
            # Time series
            'prophet',
            
            # Business intelligence
            'yfinance',
            
            # Utils
            'warnings', 'os.path', 'pathlib.Path'
        }
        
        # Completely blocked functions and modules
        self.blocked_functions = {
            'exec', 'eval', 'compile', 'open', '__import__',
            'globals', 'locals', 'vars', 'dir', 'getattr', 'setattr',
            'delattr', 'hasattr', 'callable', 'isinstance', 'issubclass',
            'input', 'raw_input', 'file', 'execfile', 'reload',
            'exit', 'quit'
        }
        
        self.blocked_modules = {
            'os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib',
            'requests', 'ftplib', 'smtplib', 'poplib', 'imaplib',
            'telnetlib', 'xmlrpc', 'pickle', 'cPickle', 'marshal',
            'shelve', 'dbm', 'gdbm', 'dumbdbm', 'anydbm', 'whichdb',
            'threading', 'multiprocessing', 'signal', 'resource',
            'ctypes', 'imp', 'importlib'
        }
        
        # Safe built-ins for restricted environment
        self.safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
            'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter',
            'float', 'frozenset', 'hex', 'int', 'len', 'list', 'map',
            'max', 'min', 'oct', 'ord', 'pow', 'range', 'reversed',
            'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple',
            'type', 'zip', 'True', 'False', 'None'
        }

    def validate_code_ast(self, code: str) -> bool:
        """
        Validate code using AST parsing to detect dangerous operations
        """
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.blocked_functions:
                            raise SecurityViolationError(f"Blocked function: {node.func.id}")
                    elif isinstance(node.func, ast.Attribute):
                        if node.func.attr in self.blocked_functions:
                            raise SecurityViolationError(f"Blocked method: {node.func.attr}")
                
                # Check for dangerous imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if module_name in self.blocked_modules:
                            raise SecurityViolationError(f"Blocked import: {module_name}")
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module.split('.')[0]
                        if module_name in self.blocked_modules:
                            raise SecurityViolationError(f"Blocked import from: {module_name}")
                
                # Check for file operations
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'open':
                        raise SecurityViolationError("File operations not allowed")
                
                # Check for attribute access that might be dangerous
                elif isinstance(node, ast.Attribute):
                    dangerous_attrs = ['__globals__', '__locals__', '__dict__', 
                                     '__class__', '__bases__', '__mro__']
                    if node.attr in dangerous_attrs:
                        raise SecurityViolationError(f"Blocked attribute access: {node.attr}")
            
            return True
            
        except SyntaxError as e:
            raise CodeExecutionError(f"Syntax error: {str(e)}")

    def create_safe_environment(self, additional_globals: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a secure execution environment with limited built-ins
        """
        # Import allowed libraries safely
        safe_globals = {}
        
        try:
            # Core data science imports
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Add to safe environment
            safe_globals.update({
                'pd': pd,
                'numpy': np,
                'np': np,
                'plt': plt,
                'sns': sns,
                'seaborn': sns
            })
            
            # Try to import additional libraries if available
            try:
                import plotly.express as px
                import plotly.graph_objects as go
                safe_globals.update({'px': px, 'go': go})
            except ImportError:
                pass
            
            try:
                from sklearn.model_selection import train_test_split
                from sklearn.metrics import accuracy_score, classification_report
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.linear_model import LinearRegression, LogisticRegression
                safe_globals.update({
                    'train_test_split': train_test_split,
                    'accuracy_score': accuracy_score,
                    'classification_report': classification_report,
                    'RandomForestClassifier': RandomForestClassifier,
                    'LinearRegression': LinearRegression,
                    'LogisticRegression': LogisticRegression
                })
            except ImportError:
                pass
            
            try:
                import scipy.stats as stats
                safe_globals['stats'] = stats
            except ImportError:
                pass
                
        except ImportError as e:
            logger.warning(f"Could not import some libraries: {e}")
        
        # Add safe built-ins
        safe_builtins = {}
        for name in self.safe_builtins:
            if hasattr(builtins, name):
                safe_builtins[name] = getattr(builtins, name)
        
        safe_globals['__builtins__'] = safe_builtins
        
        # Add additional globals if provided
        if additional_globals:
            safe_globals.update(additional_globals)
        
        return safe_globals

    def execute_with_timeout(self, code: str, globals_dict: Dict[str, Any], 
                           timeout: int = None) -> Dict[str, Any]:
        """
        Execute code with timeout protection using signal
        """
        if timeout is None:
            timeout = self.max_execution_time
        
        result = {'success': False, 'output': '', 'error': '', 'variables': {}}
        
        def timeout_handler(signum, frame):
            raise ExecutionTimeoutError(f"Code execution exceeded {timeout} seconds")
        
        # Set up timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        try:
            # Capture output
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Execute the code
                exec(code, globals_dict)
            
            # Get captured output
            result['output'] = stdout_capture.getvalue()
            error_output = stderr_capture.getvalue()
            if error_output:
                result['error'] = error_output
            
            # Capture created variables
            result['variables'] = self._extract_variables(globals_dict)
            result['success'] = True
            
        except ExecutionTimeoutError:
            result['error'] = f"Execution timed out after {timeout} seconds"
        except Exception as e:
            result['error'] = f"Execution error: {str(e)}\\n{traceback.format_exc()}"
        finally:
            # Reset alarm
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
        
        return result

    def _extract_variables(self, globals_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user-created variables from globals dictionary
        """
        variables = {}
        excluded_names = {
            'pd', 'np', 'plt', 'sns', 'px', 'go', 'stats',
            'train_test_split', 'accuracy_score', 'classification_report',
            'RandomForestClassifier', 'LinearRegression', 'LogisticRegression',
            '__builtins__', '__name__', '__doc__', '__package__'
        }
        
        for name, value in globals_dict.items():
            if not name.startswith('_') and name not in excluded_names:
                try:
                    # Handle different types appropriately
                    if isinstance(value, (int, float, str, bool, type(None))):
                        variables[name] = value
                    elif isinstance(value, (list, tuple)) and len(value) <= 20:
                        variables[name] = list(value)[:20]  # Limit size
                    elif isinstance(value, dict) and len(value) <= 10:
                        variables[name] = dict(list(value.items())[:10])  # Limit size
                    elif hasattr(value, 'shape') and hasattr(value, 'dtype'):
                        # Pandas DataFrame/Series or NumPy array
                        if hasattr(value, 'columns'):  # DataFrame
                            variables[name] = {
                                'type': 'DataFrame',
                                'shape': value.shape,
                                'columns': list(value.columns),
                                'dtypes': value.dtypes.to_dict()
                            }
                        elif hasattr(value, 'name'):  # Series
                            variables[name] = {
                                'type': 'Series',
                                'length': len(value),
                                'dtype': str(value.dtype),
                                'name': value.name
                            }
                        else:  # NumPy array
                            variables[name] = {
                                'type': 'ndarray',
                                'shape': value.shape,
                                'dtype': str(value.dtype)
                            }
                    else:
                        variables[name] = {
                            'type': type(value).__name__,
                            'value': str(value)[:200]  # Limit string representation
                        }
                except Exception:
                    # If we can't serialize the variable, just note its type
                    variables[name] = f"<{type(value).__name__} object>"
        
        return variables

    def execute_code_safely(self, code: str, data_context: Dict[str, Any] = None,
                          max_execution_time: int = None) -> Dict[str, Any]:
        """
        Main method to execute Python code with comprehensive safety measures
        """
        try:
            # Validate input
            if not code or not code.strip():
                return {
                    'success': False,
                    'error': 'No code provided',
                    'output': '',
                    'variables': {}
                }
            
            # Check code length
            if len(code) > 10000:  # 10KB limit
                return {
                    'success': False,
                    'error': 'Code too long (max 10KB)',
                    'output': '',
                    'variables': {}
                }
            
            # Validate code using AST
            self.validate_code_ast(code)
            
            # Create safe execution environment
            safe_globals = self.create_safe_environment(data_context)
            
            # Execute with timeout
            result = self.execute_with_timeout(
                code, 
                safe_globals, 
                max_execution_time or self.max_execution_time
            )
            
            # Limit output length
            if len(result['output']) > self.max_output_length:
                result['output'] = result['output'][:self.max_output_length] + "\\n... (output truncated)"
            
            return result
            
        except SecurityViolationError as e:
            return {
                'success': False,
                'error': f"Security violation: {str(e)}",
                'output': '',
                'variables': {}
            }
        except CodeExecutionError as e:
            return {
                'success': False,
                'error': str(e),
                'output': '',
                'variables': {}
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'output': '',
                'variables': {}
            }

    def test_security(self) -> Dict[str, bool]:
        """
        Test security measures with known dangerous code patterns
        """
        test_cases = [
            "import os; os.system('ls')",  # OS commands
            "exec('print(1)')",            # Exec function
            "eval('1+1')",                # Eval function
            "open('/etc/passwd')",         # File access
            "__import__('os')",           # Import bypass
            "globals()",                  # Global access
            "().__class__.__bases__[0].__subclasses__()",  # Class inspection
        ]
        
        results = {}
        for i, test_code in enumerate(test_cases):
            try:
                result = self.execute_code_safely(test_code)
                results[f"test_{i+1}"] = not result['success']  # Should fail
            except Exception:
                results[f"test_{i+1}"] = True  # Properly blocked
        
        return results 