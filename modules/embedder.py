import numpy as np
from sentence_transformers import SentenceTransformer
import os

class Embedder:
    """Generate embeddings using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        Uses a lightweight model for faster processing
        """
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to a simpler approach...")
            self.model = None
    
    def embed(self, text: str) -> np.ndarray:
        """
        Generate embedding for given text
        """
        if not text:
            # Return zero vector if text is empty
            return np.zeros(384)  # Default dimension for all-MiniLM-L6-v2
        
        if self.model:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        else:
            # Fallback: simple TF-IDF like approach (very basic)
            # In production, always use proper model
            words = text.split()
            vocab_size = 384
            embedding = np.zeros(vocab_size)
            for i, word in enumerate(words[:vocab_size]):
                hash_val = hash(word) % vocab_size
                embedding[hash_val] += 1.0 / (i + 1)
            return embedding / (np.linalg.norm(embedding) + 1e-8)

