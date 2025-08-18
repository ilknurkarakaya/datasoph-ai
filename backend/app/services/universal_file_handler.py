"""
Enhanced File Handler - With OCR support for documents and images
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from .ocr_service import ocr_service

logger = logging.getLogger(__name__)

class EnhancedFileHandler:
    def __init__(self):
        # Data formats
        self.data_formats = {'.csv', '.xlsx', '.xls', '.json', '.txt'}
        
        # OCR formats  
        self.ocr_formats = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
        
        # All supported formats
        self.supported_formats = self.data_formats | self.ocr_formats
    
    def detect_and_process(self, file_path: str) -> Dict[str, Any]:
        """Enhanced file processing with OCR support"""
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
            
            # Determine processing type
            processing_result = {}
            
            if ext in self.data_formats:
                # Standard data file processing
                processing_result = {
                    'success': True,
                    'format': ext[1:],
                    'type': 'data',
                    'ocr_content': None
                }
            
            elif ext in self.ocr_formats:
                # OCR processing for documents and images
                logger.info(f"Processing OCR file: {path.name}")
                ocr_result = ocr_service.extract_text(file_path)
                
                processing_result = {
                    'success': True,
                    'format': ext[1:],
                    'type': 'ocr',
                    'ocr_content': {
                        'text': ocr_result.get('text', ''),
                        'method': ocr_result.get('method', 'unknown'),
                        'confidence': ocr_result.get('confidence', 0),
                        'error': ocr_result.get('error'),
                        'analysis': ocr_service.analyze_content(ocr_result.get('text', ''))
                    }
                }
                
                # Log OCR results
                text_length = len(ocr_result.get('text', ''))
                logger.info(f"OCR extracted {text_length} characters from {path.name} using {ocr_result.get('method')}")
                
                if ocr_result.get('error'):
                    logger.warning(f"OCR warning for {path.name}: {ocr_result.get('error')}")
            
            return {
                'success': True,
                'file_info': file_info,
                'processing_result': processing_result
            }
            
        except Exception as e:
            logger.error(f"File processing error: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_ocr_file(self, file_path: str) -> bool:
        """Check if file is an OCR-supported format"""
        ext = Path(file_path).suffix.lower()
        return ext in self.ocr_formats
    
    def is_data_file(self, file_path: str) -> bool:
        """Check if file is a data format"""
        ext = Path(file_path).suffix.lower()
        return ext in self.data_formats

# Global instance
handler = EnhancedFileHandler()
