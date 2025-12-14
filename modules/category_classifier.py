import re
from typing import Optional

class CategoryClassifier:
    """Classify resumes and job descriptions into categories"""
    
    # Category keywords and patterns
    CATEGORIES = {
        "data_science": {
            "keywords": [
                "data science", "data scientist", "data analyst", "data analysis",
                "machine learning", "deep learning", "ml engineer", "ai engineer",
                "statistics", "statistical", "predictive modeling", "data mining",
                "python", "r", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
                "jupyter", "sql", "data visualization", "tableau", "power bi",
                "big data", "hadoop", "spark", "data pipeline", "etl"
            ],
            "weight": 1.0
        },
        "software_development": {
            "keywords": [
                "software engineer", "software developer", "developer", "programmer",
                "full stack", "backend", "frontend", "web developer", "mobile developer",
                "java", "javascript", "typescript", "react", "angular", "vue", "node.js",
                "django", "flask", "spring", "api", "rest", "microservices",
                "git", "agile", "scrum", "code review", "testing", "debugging"
            ],
            "weight": 1.0
        },
        "marketing": {
            "keywords": [
                "marketing", "marketer", "digital marketing", "content marketing",
                "social media", "seo", "sem", "ppc", "google ads", "facebook ads",
                "brand management", "campaign", "analytics", "roi", "conversion",
                "email marketing", "marketing strategy", "advertising", "pr",
                "public relations", "market research", "customer acquisition"
            ],
            "weight": 1.0
        },
        "design": {
            "keywords": [
                "designer", "ui/ux", "user interface", "user experience", "graphic design",
                "figma", "adobe", "photoshop", "illustrator", "sketch", "prototyping",
                "wireframe", "visual design", "interaction design", "design system"
            ],
            "weight": 1.0
        },
        "business": {
            "keywords": [
                "business analyst", "product manager", "project manager", "consultant",
                "strategy", "operations", "finance", "accounting", "sales",
                "business development", "management", "leadership"
            ],
            "weight": 1.0
        }
    }
    
    def classify(self, text: str) -> Optional[str]:
        """
        Classify text into a category
        Returns the category name or None if no strong match
        """
        if not text:
            return None
        
        text_lower = text.lower()
        category_scores = {}
        
        # Score each category based on keyword matches
        for category, config in self.CATEGORIES.items():
            score = 0
            for keyword in config["keywords"]:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text_lower))
                score += matches * config["weight"]
            
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or None if no matches
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return None
    
    def get_category_match(self, category1: Optional[str], category2: Optional[str]) -> bool:
        """Check if two categories match"""
        if not category1 or not category2:
            return True  # If we can't determine, don't penalize
        return category1 == category2

