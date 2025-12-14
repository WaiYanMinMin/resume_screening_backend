import numpy as np
from typing import List, Optional, Dict

class SimilarityCalculator:
    """Calculate similarity between resume and job description with skill gating and weighted scoring"""
    
    def __init__(self, min_skill_overlap: float = 0.2, skill_penalty: float = 0.5):
        """
        Initialize similarity calculator
        Args:
            min_skill_overlap: Minimum skill overlap ratio for full score (0.0 to 1.0)
            skill_penalty: Penalty multiplier when skill overlap is below threshold (0.0 to 1.0)
        """
        self.min_skill_overlap = min_skill_overlap
        self.skill_penalty = skill_penalty
    
    def skill_gate(self, resume_skills: List[str], jd_skills: List[str]) -> bool:
        """
        Check if resume has minimum skill overlap with job description
        This is the MOST IMPORTANT gate - prevents unrelated matches
        
        Args:
            resume_skills: List of skills from resume
            jd_skills: List of skills from job description
            
        Returns:
            True if skill overlap meets minimum threshold, False otherwise
        """
        if len(jd_skills) == 0:
            return True  # No skills in JD, allow through
        
        # Normalize skills to lowercase for comparison
        resume_skills_set = {skill.lower() for skill in resume_skills}
        jd_skills_set = {skill.lower() for skill in jd_skills}
        
        # Calculate overlap ratio
        overlap_ratio = len(resume_skills_set & jd_skills_set) / len(jd_skills_set)
        
        return overlap_ratio >= self.min_skill_overlap
    
    def skill_coverage(self, resume_skills: List[str], jd_skills: List[str]) -> float:
        """
        Calculate skill coverage ratio (how many JD skills are covered by resume)
        Returns value between 0 and 1
        """
        if len(jd_skills) == 0:
            return 1.0
        
        resume_skills_set = {skill.lower() for skill in resume_skills}
        jd_skills_set = {skill.lower() for skill in jd_skills}
        
        overlap = len(resume_skills_set & jd_skills_set)
        return overlap / len(jd_skills_set)
    
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
    
    def calculate_final_score(
        self,
        semantic_similarity: float,
        resume_skills: List[str],
        jd_skills: List[str],
        resume_category: Optional[str] = None,
        job_category: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate final similarity score with skill gating and weighted scoring
        This implements the production-ready formula
        
        Args:
            semantic_similarity: Cosine similarity from embeddings (0-1)
            resume_skills: List of skills from resume
            jd_skills: List of skills from job description
            resume_category: Category of resume (optional)
            job_category: Category of job description (optional)
            
        Returns:
            Dictionary with final_score, skill_coverage, and flags
        """
        # Extract skills from job description if not provided
        if not jd_skills:
            jd_skills = []
        
        # Calculate skill coverage
        skill_cov = self.skill_coverage(resume_skills, jd_skills)
        
        # Fix 1: Skill overlap penalty (instead of hard gate)
        skill_gate_passed = self.skill_gate(resume_skills, jd_skills)
        skill_penalty_multiplier = 1.0
        
        if not skill_gate_passed:
            # Apply penalty instead of returning 0
            skill_penalty_multiplier = self.skill_penalty  # e.g., 0.5 = 50% penalty
        
        # Fix 3: Domain mismatch penalty
        domain_penalty = 1.0
        if resume_category and job_category and resume_category != job_category:
            domain_penalty = 0.2  # 80% penalty for domain mismatch
        
        # Fix 2 & 5: Weighted final score with explainability
        # Production formula: 0.7 * semantic + 0.3 * skill_coverage
        weighted_score = (0.7 * semantic_similarity) + (0.3 * skill_cov)
        
        # Apply both skill and domain penalties
        final_score = weighted_score * skill_penalty_multiplier * domain_penalty
        
        # Explainability flags
        flags = []
        if not skill_gate_passed:
            flags.append(f"Low skill overlap ({skill_cov:.1%}) - {int((1 - skill_penalty_multiplier) * 100)}% penalty applied")
        if semantic_similarity > 0.5 and skill_cov < 0.1:
            flags.append("High semantic similarity but low skill relevance")
        if resume_category and job_category and resume_category != job_category:
            flags.append(f"Domain mismatch: {resume_category} vs {job_category}")
        
        return {
            "final_score": float(final_score),
            "semantic_similarity": semantic_similarity,
            "skill_coverage": skill_cov,
            "skill_gate_passed": skill_gate_passed,
            "skill_penalty_applied": skill_penalty_multiplier < 1.0,
            "domain_penalty": domain_penalty,
            "flag": "; ".join(flags) if flags else None
        }

