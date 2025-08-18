"""
OCR Service for extracting text from PDFs and images
Supports: PDF, PNG, JPG, JPEG, TIFF, BMP
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# OCR and document processing
try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    import PyPDF2
    import pdfplumber
    OCR_AVAILABLE = True
except ImportError as e:
    logging.warning(f"OCR libraries not available: {e}")
    OCR_AVAILABLE = False

logger = logging.getLogger(__name__)

class OCRService:
    """Service for extracting text from documents and images"""
    
    def __init__(self):
        self.supported_image_formats = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
        self.supported_pdf_formats = {'.pdf'}
        self.supported_formats = self.supported_image_formats | self.supported_pdf_formats
        
        if not OCR_AVAILABLE:
            logger.warning("OCR libraries not installed. Install with: pip install pytesseract Pillow opencv-python PyPDF2 pdfplumber")
    
    def is_supported(self, file_path: str) -> bool:
        """Check if file format is supported for OCR"""
        return Path(file_path).suffix.lower() in self.supported_formats
    
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from document or image
        Returns: {
            'text': extracted_text,
            'method': extraction_method,
            'confidence': confidence_score,
            'error': error_message if any
        }
        """
        if not OCR_AVAILABLE:
            return {
                'text': '',
                'method': 'none',
                'confidence': 0,
                'error': 'OCR libraries not installed'
            }
        
        if not os.path.exists(file_path):
            return {
                'text': '',
                'method': 'none', 
                'confidence': 0,
                'error': f'File not found: {file_path}'
            }
        
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext in self.supported_pdf_formats:
                return self._extract_from_pdf(file_path)
            elif file_ext in self.supported_image_formats:
                return self._extract_from_image(file_path)
            else:
                return {
                    'text': '',
                    'method': 'unsupported',
                    'confidence': 0,
                    'error': f'Unsupported file format: {file_ext}'
                }
        
        except Exception as e:
            logger.error(f"OCR extraction failed for {file_path}: {e}")
            return {
                'text': '',
                'method': 'error',
                'confidence': 0,
                'error': str(e)
            }
    
    def _extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF using multiple methods"""
        text_content = ""
        method = "unknown"
        
        # Method 1: Try pdfplumber (better for complex layouts)
        try:
            with pdfplumber.open(file_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                
                if pages_text:
                    text_content = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
                    method = "pdfplumber"
                    
        except Exception as e:
            logger.warning(f"pdfplumber failed for {file_path}: {e}")
        
        # Method 2: Fallback to PyPDF2 if pdfplumber fails
        if not text_content:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    pages_text = []
                    
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text.strip():
                            pages_text.append(f"Page {page_num + 1}:\n{page_text}")
                    
                    if pages_text:
                        text_content = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
                        method = "PyPDF2"
                        
            except Exception as e:
                logger.warning(f"PyPDF2 failed for {file_path}: {e}")
        
        # Calculate confidence based on text length and content
        confidence = min(100, max(0, len(text_content.strip()) / 10))
        
        return {
            'text': text_content.strip(),
            'method': method,
            'confidence': confidence,
            'error': None if text_content.strip() else 'No text extracted from PDF'
        }
    
    def _extract_from_image(self, file_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR"""
        try:
            # Load and preprocess image
            image = cv2.imread(file_path)
            if image is None:
                # Fallback to PIL
                pil_image = Image.open(file_path)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Preprocess image for better OCR
            processed_image = self._preprocess_image(image)
            
            # Extract text using Tesseract
            custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6
            text_data = pytesseract.image_to_data(processed_image, config=custom_config, output_type=pytesseract.Output.DICT)
            
            # Extract text and calculate confidence
            extracted_text = []
            confidences = []
            
            for i, word in enumerate(text_data['text']):
                if word.strip():
                    confidence = int(text_data['conf'][i])
                    if confidence > 30:  # Only include words with reasonable confidence
                        extracted_text.append(word)
                        confidences.append(confidence)
            
            final_text = ' '.join(extracted_text)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': final_text,
                'method': 'tesseract_ocr',
                'confidence': avg_confidence,
                'error': None if final_text.strip() else 'No text detected in image'
            }
            
        except Exception as e:
            logger.error(f"Image OCR failed for {file_path}: {e}")
            return {
                'text': '',
                'method': 'tesseract_error',
                'confidence': 0,
                'error': str(e)
            }
    
    def _preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.medianBlur(gray, 3)
        
        # Increase contrast
        contrast = cv2.convertScaleAbs(denoised, alpha=1.5, beta=0)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def analyze_content(self, extracted_text: str) -> Dict[str, Any]:
        """Analyze extracted text content"""
        if not extracted_text.strip():
            return {
                'word_count': 0,
                'char_count': 0,
                'language': 'unknown',
                'content_type': 'empty',
                'summary': 'No text content found'
            }
        
        words = extracted_text.split()
        chars = len(extracted_text)
        
        # Simple content type detection
        content_type = 'document'
        if any(word.lower() in ['invoice', 'receipt', 'total', 'amount', '$', '€', '₺'] for word in words):
            content_type = 'financial'
        elif any(word.lower() in ['chart', 'graph', 'data', 'analysis', 'report'] for word in words):
            content_type = 'analytical'
        elif len(words) < 20:
            content_type = 'short_text'
        
        # Create summary
        summary = f"Document contains {len(words)} words, {chars} characters. "
        summary += f"Content appears to be {content_type.replace('_', ' ')}. "
        
        if len(words) > 50:
            # Get first 100 characters as preview
            preview = extracted_text[:100].strip()
            if len(extracted_text) > 100:
                preview += "..."
            summary += f"Preview: '{preview}'"
        else:
            summary += f"Full text: '{extracted_text[:200]}'"
        
        return {
            'word_count': len(words),
            'char_count': chars,
            'language': 'auto-detected',  # Could add language detection
            'content_type': content_type,
            'summary': summary
        }

# Global OCR service instance
ocr_service = OCRService()

def extract_text_from_file(file_path: str) -> Dict[str, Any]:
    """Convenience function for text extraction"""
    return ocr_service.extract_text(file_path)

def is_ocr_supported(file_path: str) -> bool:
    """Check if file supports OCR"""
    return ocr_service.is_supported(file_path)
