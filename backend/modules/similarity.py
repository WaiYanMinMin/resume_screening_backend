import numpy as np

class SimilarityCalculator:
    """Calculate similarity between resume and job description embeddings"""
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        Returns value between 0 and 1
        """
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        
        # Ensure value is between 0 and 1 (normalize from -1 to 1 range)
        similarity = (similarity + 1) / 2
        
        return float(similarity)

