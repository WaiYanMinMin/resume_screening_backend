import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from typing import List

class Clusterer:
    """Cluster candidates using KMeans and generate visualization coordinates"""
    
    def __init__(self, n_clusters: int = 3):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.all_embeddings = []
        self.fitted = False
    
    def fit(self, embeddings: List[np.ndarray]):
        """Fit KMeans on embeddings"""
        if len(embeddings) < 2:
            return
        
        embeddings_array = np.array(embeddings)
        n_clusters = min(self.n_clusters, len(embeddings))
        
        if n_clusters < 2:
            n_clusters = 2
        
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans.fit(embeddings_array)
        self.all_embeddings = embeddings
        self.fitted = True
    
    def assign_cluster(self, embedding) -> int:
        """Assign a cluster label to an embedding"""
        # Convert to numpy array if needed
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        
        # If not fitted yet, try to fit
        if not self.fitted or self.kmeans is None:
            # Try to fit with existing embeddings if we have enough
            if len(self.all_embeddings) >= 2:
                self.fit(self.all_embeddings)
            else:
                # Not enough embeddings yet, return default cluster
                return 0
        
        # Double-check: if still not fitted (e.g., fit returned early), return default
        if self.kmeans is None:
            return 0
        
        # Predict cluster - kmeans should be initialized now
        try:
            cluster_label = self.kmeans.predict(embedding.reshape(1, -1))[0]
            return int(cluster_label)
        except Exception as e:
            # Fallback if prediction fails
            print(f"Error predicting cluster: {e}")
            return 0
    
    def add_embedding(self, embedding):
        """Add embedding to the collection"""
        # Convert to numpy array if needed
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        
        self.all_embeddings.append(embedding)
        # Refit if we have enough embeddings
        if len(self.all_embeddings) >= 2:
            self.fit(self.all_embeddings)
    
    def get_visualization_coordinates(self, embeddings) -> np.ndarray:
        """
        Get 2D coordinates for visualization using PCA (fallback to t-SNE for small sets)
        """
        if len(embeddings) < 2:
            # Return dummy coordinates
            return np.array([[0, 0] for _ in embeddings])
        
        # Convert to numpy array, handling list of lists or list of arrays
        if isinstance(embeddings[0], list):
            embeddings_array = np.array(embeddings)
        else:
            embeddings_array = np.array(embeddings)
        
        # Use PCA for dimensionality reduction (faster than t-SNE)
        # For small datasets, we can still use PCA effectively
        try:
            if len(embeddings) > 2:
                pca = PCA(n_components=2, random_state=42)
                coordinates = pca.fit_transform(embeddings_array)
            else:
                # For very small datasets, just use first two dimensions
                coordinates = embeddings_array[:, :2] if embeddings_array.shape[1] >= 2 else embeddings_array
            
            return coordinates
        except Exception as e:
            print(f"Error in visualization: {e}")
            # Fallback: use first two dimensions
            if embeddings_array.shape[1] >= 2:
                return embeddings_array[:, :2]
            else:
                return np.array([[0, 0] for _ in embeddings])

