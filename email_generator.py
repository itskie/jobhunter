import config
from typing import Dict, Any

class EmailGenerator:
    @classmethod
    def generate_email(cls, job: Dict[str, Any]) -> Dict[str, str]:
        title = job.get("title", "Cloud & DevOps Engineer")
        recipient = job.get("primary_email", "recruiter@example.com")
        skills = job.get("skills", ["AWS", "Docker", "Linux"])

        skills_str = ", ".join(skills) if skills else "AWS, Docker, CI/CD, and Linux"

        subject = f"Application for {title} — {config.CANDIDATE_NAME} (Immediate Joiner)"

        body = f"""Dear Hiring Team,

I hope this email finds you well.

I am writing to express my strong interest in the {title} role. As an Immediate Joiner with hands-on experience in Cloud Infrastructure (AWS), containerization (Docker/Kubernetes), and Infrastructure as Code (Terraform), I would love to contribute to your engineering operations.

Key Highlights of My Experience:
• Cloud & Infrastructure: Hands-on experience with AWS core services (EC2, ECS Fargate, EKS, VPC, S3, IAM, CloudWatch) and Linux system administration.
• Containers & DevSecOps: Containerized microservices with Docker, built automated CI/CD pipelines via GitHub Actions, and implemented automated security vulnerability scanning with Aqua Trivy.
• Project & Builder Proof: Built InfraGenie ({config.CANDIDATE_GITHUB}/infragenie), an open-source tool that provisions zero-touch AWS ECS clusters in <2 minutes.
• Skills Alignment: Hands-on proficiency in {skills_str}.
• Education & Background: Strong foundation in Cloud Computing.

I am based in India, an Immediate Joiner (0 days notice), and open to on-site, hybrid, or remote work arrangements.

I have attached my latest resume for your review. Would greatly appreciate the opportunity to connect for a brief introductory conversation.

GitHub: {config.CANDIDATE_GITHUB}
LinkedIn: {config.CANDIDATE_LINKEDIN}
Phone: {config.CANDIDATE_PHONE}

Thank you for your time and consideration!

Best regards,
{config.CANDIDATE_NAME}
Cloud & DevOps Engineer
{config.CANDIDATE_EMAIL} | {config.CANDIDATE_PHONE}"""

        return {
            "to": recipient,
            "subject": subject,
            "body": body
        }
