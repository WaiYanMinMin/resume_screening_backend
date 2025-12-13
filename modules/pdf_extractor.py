import PyPDF2
import pdfplumber
from typing import Optional

class PDFExtractor:
    """Extract text from PDF files"""
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF using multiple methods for better accuracy
        """
        text = ""
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Fallback to PyPDF2 if pdfplumber didn't work
        if not text.strip():
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
        
        if not text.strip():
            raise ValueError(f"Could not extract text from PDF: {file_path}")
        
        return text.strip()

