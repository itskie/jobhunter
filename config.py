import os
import glob
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "applied_history.json"
SENT_LOG_FILE = BASE_DIR / "sent_applications.csv"
ENV_FILE = BASE_DIR / ".env"

# Helper to load .env variables if python-dotenv is not installed
def load_env_vars():
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

load_env_vars()

def find_latest_resume() -> str:
    search_patterns = [
        str(BASE_DIR / "*.pdf"),
        str(Path.home() / "Developer" / "*.pdf"),
        str(Path.home() / "Desktop" / "*.pdf")
    ]
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            matches.sort(key=os.path.getmtime, reverse=True)
            return matches[0]
    return "resume.pdf"

RESUME_PATH = os.getenv("RESUME_PATH", find_latest_resume())

# Candidate Details (Loaded from .env / Environment)
CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "Your Name")
CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL", "your_email@gmail.com")
CANDIDATE_PHONE = os.getenv("CANDIDATE_PHONE", "+91 9876543210")
CANDIDATE_GITHUB = os.getenv("CANDIDATE_GITHUB", "https://github.com/yourusername")
CANDIDATE_LINKEDIN = os.getenv("CANDIDATE_LINKEDIN", "https://linkedin.com/in/yourprofile")

# SMTP Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")

# Target Keywords & Domains
TARGET_KEYWORDS = [
    "devops", "cloud", "aws", "infrastructure", "ai infra", "platform engineer",
    "site reliability", "sre", "kubernetes", "k8s", "docker", "terraform", "iac",
    "python", "linux", "sysadmin", "system administrator", "ci/cd", "github actions",
    "devsecops", "cloud security", "trivy", "sonarqube", "prometheus", "grafana",
    "elk", "fastapi", "server specialist", "cloud operations", "cloud trainee",
    "build and release", "cloud migration", "backend", "langchain", "rag"
]

MAX_EXPERIENCE_YEARS = int(os.getenv("MAX_EXPERIENCE_YEARS", 2))
MAX_DAILY_APPLICATIONS = None  # Unlimited
