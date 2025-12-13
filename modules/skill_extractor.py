import re
from typing import List

class SkillExtractor:
    """Extract skills from resume text"""
    
    # Common technical skills keywords
    SKILL_KEYWORDS = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
        
        # Frameworks & Libraries
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
        'spring', 'express', 'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy',
        
        # Tools & Technologies
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins',
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
        'linux', 'unix', 'bash', 'powershell',
        
        # Data & Analytics
        'machine learning', 'deep learning', 'data science', 'data analysis',
        'big data', 'hadoop', 'spark', 'tableau', 'power bi',
        
        # Other Skills
        'agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'rest api',
        'graphql', 'html', 'css', 'sass', 'less', 'webpack', 'npm', 'yarn'
    ]
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text using keyword matching
        """
        if not resume_text:
            return []
        
        text_lower = resume_text.lower()
        found_skills = []
        
        # Check for each skill keyword
        for skill in self.SKILL_KEYWORDS:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and return
        return sorted(list(set(found_skills)))

