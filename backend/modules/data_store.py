from typing import Dict, List, Optional
import uuid
from datetime import datetime
import numpy as np
class DataStore:
    """In-memory data store for resumes and processing results"""
    
    def __init__(self):
        self.resumes: Dict[str, Dict] = {}
    
    def add_resume(self, filename: str, text: str) -> str:
        """Add a new resume and return its ID"""
        resume_id = str(uuid.uuid4())
        self.resumes[resume_id] = {
            "resume_id": resume_id,
            "filename": filename,
            "text": text,
            "similarity_score": 0.0,
            "skills": [],
            "cluster_label": 0,
            "embedding": None,
            "uploaded_at": datetime.now().isoformat()
        }
        return resume_id
    
    def get_resume(self, resume_id: str) -> Optional[Dict]:
        """Get resume by ID"""
        return self.resumes.get(resume_id)
    
    def update_resume_processing(
        self,
        resume_id: str,
        similarity_score: float,
        skills: List[str],
        cluster_label: int,
        embedding
    ):
        """Update resume with processing results"""
        if resume_id in self.resumes:
          
            # Convert numpy array to list if needed
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            
            self.resumes[resume_id]["similarity_score"] = similarity_score
            self.resumes[resume_id]["skills"] = skills
            self.resumes[resume_id]["cluster_label"] = cluster_label
            self.resumes[resume_id]["embedding"] = embedding
            self.resumes[resume_id]["processed_at"] = datetime.now().isoformat()
    
    def get_all_candidates(self) -> List[Dict]:
        """Get all candidates"""
        return list(self.resumes.values())
    
    def delete_resume(self, resume_id: str) -> bool:
        """Delete a resume by ID. Returns True if deleted, False if not found"""
        if resume_id in self.resumes:
            del self.resumes[resume_id]
            return True
        return False
    
    def clear_all(self):
        """Clear all stored data"""
        self.resumes.clear()

