"""
Simple File Handler - Basic file processing
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleFileHandler:
    def __init__(self):
        self.supported_formats = {'.csv', '.xlsx', '.xls', '.json', '.txt'}
    
    def detect_and_process(self, file_path: str) -> Dict[str, Any]:
        """Simple file processing"""
        try:
            path = Path(file_path)
            ext = path.suffix.lower()
            
            if ext not in self.supported_formats:
                return {'success': False, 'error': f'Unsupported format: {ext}'}
            
            # Basic file info
            file_info = {
                'filename': path.name,
                'size_mb': path.stat().st_size / (1024 * 1024),
                'format': ext[1:]  # Remove dot
            }
            
            return {
                'success': True,
                'file_info': file_info,
                'processing_result': {
                    'success': True,
                    'format': ext[1:]
                }
            }
            
        except Exception as e:
            logger.error(f"File processing error: {e}")
            return {'success': False, 'error': str(e)}

# Global instance
handler = SimpleFileHandler()
