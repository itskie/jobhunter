import re
from typing import List, Dict, Any, Optional

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

DEV_KEYWORDS = [
    "devops", "cloud", "aws", "infrastructure", "ai infra", "platform engineer",
    "site reliability", "sre", "kubernetes", "k8s", "docker", "terraform", "iac",
    "python", "linux", "sysadmin", "system administrator", "ci/cd", "github actions",
    "devsecops", "cloud security", "trivy", "sonarqube", "prometheus", "grafana",
    "elk", "fastapi", "server specialist", "cloud operations", "cloud trainee",
    "build and release", "cloud migration", "backend", "langchain", "rag",
    "fresher", "intern", "junior", "fullstack", "software engineer", "sde", "ai engineer"
]

class JobPostExtractor:
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
        cleaned = [e.strip().lower() for e in emails if not e.lower().endswith((".png", ".jpg", ".svg", ".gif", ".webp", ".jpeg", ".ai"))]
        return list(dict.fromkeys(cleaned))

    @staticmethod
    def extract_experience_years(text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        if any(w in text_lower for w in ["fresher", "fresh graduate", "intern", "internship", "0-1 year", "0-1 yr", "0 to 1", "entry level", "immediate joiner"]):
            return {"min_exp": 0, "max_exp": 1, "is_fresher_friendly": True}
        
        match = re.search(r'(\d+)\s*[-–to]\s*(\d+)\s*(?:years?|yrs?)', text_lower)
        if match:
            min_e, max_e = int(match.group(1)), int(match.group(2))
            return {"min_exp": min_e, "max_exp": max_e, "is_fresher_friendly": min_e <= 2}
        
        match_single = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', text_lower)
        if match_single:
            val = int(match_single.group(1))
            return {"min_exp": val, "max_exp": val, "is_fresher_friendly": val <= 2}
        
        return {"min_exp": 0, "max_exp": 2, "is_fresher_friendly": True}

    @staticmethod
    def is_target_role(text: str) -> bool:
        text_lower = text.lower()
        return any(k in text_lower for k in DEV_KEYWORDS)

    @classmethod
    def parse_post(cls, post_text: str) -> Optional[Dict[str, Any]]:
        emails = cls.extract_emails(post_text)
        if not emails:
            return None
        
        if not cls.is_target_role(post_text):
            return None
        
        exp_info = cls.extract_experience_years(post_text)
        if exp_info["min_exp"] > 2:  # Strict filter: max 2 years
            return None

        lines = [l.strip() for l in post_text.strip().split("\n") if l.strip()]
        title = "Cloud & DevOps Engineer"
        for line in lines[:6]:
            line_clean = re.sub(r'^(we are hiring|hiring for|urgently hiring|looking for|opening for|position)\s*[:\-–]?\s*', '', line, flags=re.IGNORECASE).strip()
            if any(k in line.lower() for k in ["engineer", "developer", "specialist", "intern", "trainee", "architect", "lead", "devops", "cloud", "sre"]):
                title = line_clean[:65].strip()
                break

        # Comprehensive skill detection
        skills_found = []
        for s in ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "GitHub Actions", "Python", "Linux", "FastAPI", "Prometheus", "Grafana", "Trivy", "SonarQube", "ELK", "SRE", "LangChain", "RAG", "Bash", "PostgreSQL", "Nginx", "Redis"]:
            if re.search(rf'\b{re.escape(s)}\b', post_text, re.IGNORECASE):
                skills_found.append(s)

        return {
            "title": title,
            "emails": emails,
            "primary_email": emails[0],
            "exp_info": exp_info,
            "skills": skills_found,
            "raw_text": post_text.strip()
        }

    @classmethod
    def parse_multiple_posts(cls, raw_content: str) -> List[Dict[str, Any]]:
        chunks = re.split(r'\n\s*---\s*\n|\n\s*===\s*\n|\n{3,}', raw_content)
        results = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            parsed = cls.parse_post(chunk)
            if parsed:
                results.append(parsed)
        return results
