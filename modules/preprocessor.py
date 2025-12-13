import re
import string

class TextPreprocessor:
    """Preprocess and clean text for embedding generation"""
    
    def preprocess(self, text: str) -> str:
        """
        Clean and preprocess text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces and punctuation for readability
        text = re.sub(r'[^\w\s\.\,\;\!\?\-\:]', ' ', text)
        
        # Replace multiple whitespaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra spaces
        text = text.strip()
        
        return text

