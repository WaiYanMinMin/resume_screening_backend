from typing import Dict, List, Optional
import uuid
from datetime import datetime
import numpy as np

class DataStore:
    """In-memory data store for resumes and processing results with session isolation"""
    
    def __init__(self):
        # Structure: {session_id: {resume_id: resume_data}}
        self.resumes: Dict[str, Dict[str, Dict]] = {}
    
    def _get_session_resumes(self, session_id: str) -> Dict[str, Dict]:
        """Get resumes for a specific session"""
        if session_id not in self.resumes:
            self.resumes[session_id] = {}
        return self.resumes[session_id]
    
    def add_resume(self, session_id: str, filename: str, text: str) -> str:
        """Add a new resume and return its ID (isolated by session)"""
        session_resumes = self._get_session_resumes(session_id)
        resume_id = str(uuid.uuid4())
        session_resumes[resume_id] = {
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
    
    def get_resume(self, session_id: str, resume_id: str) -> Optional[Dict]:
        """Get resume by ID (only if it belongs to the session)"""
        session_resumes = self._get_session_resumes(session_id)
        return session_resumes.get(resume_id)
    
    def update_resume_processing(
        self,
        session_id: str,
        resume_id: str,
        similarity_score: float,
        skills: List[str],
        cluster_label: int,
        embedding
    ):
        """Update resume with processing results (only if it belongs to the session)"""
        session_resumes = self._get_session_resumes(session_id)
        if resume_id in session_resumes:
            # Convert numpy array to list if needed
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            
            session_resumes[resume_id]["similarity_score"] = similarity_score
            session_resumes[resume_id]["skills"] = skills
            session_resumes[resume_id]["cluster_label"] = cluster_label
            session_resumes[resume_id]["embedding"] = embedding
            session_resumes[resume_id]["processed_at"] = datetime.now().isoformat()
    
    def get_all_candidates(self, session_id: str) -> List[Dict]:
        """Get all candidates for a specific session"""
        session_resumes = self._get_session_resumes(session_id)
        return list(session_resumes.values())
    
    def delete_resume(self, session_id: str, resume_id: str) -> bool:
        """Delete a resume by ID (only if it belongs to the session). Returns True if deleted, False if not found"""
        session_resumes = self._get_session_resumes(session_id)
        if resume_id in session_resumes:
            del session_resumes[resume_id]
            return True
        return False
    
    def clear_all(self, session_id: str):
        """Clear all stored data for a specific session"""
        if session_id in self.resumes:
            self.resumes[session_id].clear()

