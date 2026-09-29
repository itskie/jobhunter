import config
from typing import Dict, Any

class EmailGenerator:
    @classmethod
    def generate_email(cls, job: Dict[str, Any]) -> Dict[str, str]:
        title = job.get("title", "AI & Cloud Systems Engineer")
        recipient = job.get("primary_email", "recruiter@example.com")
        skills = job.get("skills", ["Python", "FastAPI", "AWS", "Docker", "Agentic AI"])

        skills_str = ", ".join(skills) if skills else "Python, FastAPI, AWS, Docker, Kubernetes, CI/CD, and AI/LLM Systems"

        subject = f"Application for {title} — {config.CANDIDATE_NAME} (AI & Cloud Systems Engineer | Immediate Joiner)"

        body = f"""Dear Hiring Team,

I hope this email finds you well.

I am writing to express my strong interest in the {title} position. As an AI & Cloud Systems Engineer with 1+ year of intensive production experience (Immediate Joiner, 0 days notice) building autonomous agentic architectures, scalable GenAI pipelines, and resilient cloud infrastructure, I would love to contribute to your engineering team.

Proven Builder & Production Track Record:
• Autonomous Agentic AI & Cognitive Memory (F.R.I.D.A.Y.): Creator of Friday (https://github.com/itskie/friday) — an open-source autonomous agent and long-term memory engine with 65+ GitHub Stars, 10 forks, and 280+ PyPI package downloads. Architected dual-layer semantic memory (ChromaDB vector embeddings + Neo4j knowledge graphs) with MCP (Model Context Protocol) tool execution over FastAPI.
• Production GenAI & SaaS Infrastructure (ReelDM): Architected and deployed a Meta Business Verified platform on AWS EC2, managing webhook pipelines, asynchronous Celery/Redis background task queues, and LLM-driven autonomous customer workflows.
• Cloud & AI Infrastructure: Deep hands-on experience provisioning and scaling containerized workloads with Docker, Kubernetes, and AWS (EC2, ECS Fargate, EKS, VPC, S3, IAM, CloudWatch).
• DevSecOps & Automation: Built automated CI/CD pipelines with GitHub Actions, automated vulnerability scanning with Aqua Trivy, and built InfraGenie (https://github.com/itskie/infragenie) for zero-touch cloud provisioning.
• Tech Alignment: Proficient in Python, FastAPI, Docker, Kubernetes, AWS, Vector DBs, LangChain/RAG, and Linux internals ({skills_str}).
• Experience & Background: 1+ year of hands-on production engineering experience | BCA in Cloud Computing (Amity University, 8.1 CGPA).

Availability & Preferences:
• Immediate Joiner (0 days notice period).
• Based in India; open to on-site (Bangalore / NCR / Pune / Hyderabad), hybrid, or remote engineering roles.

My latest resume is attached for your review. I would welcome the opportunity for a brief introductory conversation.

GitHub: {config.CANDIDATE_GITHUB}
LinkedIn: {config.CANDIDATE_LINKEDIN}

Thank you for your time and consideration!

Best regards,
{config.CANDIDATE_NAME}
AI & Cloud Systems Engineer
{config.CANDIDATE_EMAIL} | {config.CANDIDATE_PHONE}"""

        return {
            "to": recipient,
            "subject": subject,
            "body": body
        }
