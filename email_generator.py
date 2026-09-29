import config
from typing import Dict, Any

class EmailGenerator:
    @classmethod
    def generate_email(cls, job: Dict[str, Any]) -> Dict[str, str]:
        title = job.get("title", "Cloud & DevOps Engineer")
        recipient = job.get("primary_email", "recruiter@example.com")
        skills = job.get("skills", ["AWS", "Docker", "Linux"])

        skills_str = ", ".join(skills) if skills else "AWS, Docker, Kubernetes, CI/CD, and Linux"

        subject = f"Application for {title} — {config.CANDIDATE_NAME} (Immediate Joiner)"

        body = f"""Dear Hiring Team,

I hope this email finds you well.

I am writing to apply for the {title} position. As an Immediate Joiner (0 days notice) with end-to-end production experience across Cloud Infrastructure (AWS), Container Orchestration (Docker/Kubernetes), and Fullstack/Systems Engineering, I would love to contribute to your technical initiatives.

Proven Builder & Production Track Record:
• F.R.I.D.A.Y. (Open Source): Creator of Friday (https://github.com/itskie/friday) — an autonomous memory & cognitive AI infrastructure engine with 65+ GitHub Stars, 10 forks, and 280+ PyPI package downloads. Architecture built on FastAPI, ChromaDB, and Neo4j graph topologies.
• ReelDM (Production SaaS): Architected and deployed a Meta Business Verified SaaS platform on AWS EC2, managing webhook pipelines, async Celery/Redis queues, PostgreSQL, and resilient microservices.
• InfraGenie: Built open-source cloud tooling (https://github.com/itskie/infragenie) automating zero-touch AWS ECS Fargate cluster provisioning in under 2 minutes.
• Cloud & DevSecOps: Deep hands-on proficiency with AWS (EC2, ECS, EKS, VPC, S3, IAM, CloudWatch), Linux kernel administration, automated CI/CD via GitHub Actions, and vulnerability scanning with Aqua Trivy.
• Tech Alignment: Experienced with {skills_str}.

Availability & Preferences:
• Immediate Joiner (0 days notice period).
• Based in India; open to on-site (Bangalore / Pune / Hyderabad / NCR), hybrid, or remote engineering roles.

My latest resume is attached for your review. I would welcome the opportunity for a brief introductory discussion.

GitHub: {config.CANDIDATE_GITHUB}
LinkedIn: {config.CANDIDATE_LINKEDIN}

Thank you for your time and consideration!

Best regards,
{config.CANDIDATE_NAME}
Systems, Cloud & DevOps Engineer
{config.CANDIDATE_EMAIL} | {config.CANDIDATE_PHONE}"""

        return {
            "to": recipient,
            "subject": subject,
            "body": body
        }
