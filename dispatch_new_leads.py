import time
import config
from auto_mailer import AutoMailer

NEW_TARGETS = [
    {
        "company": "Inexture Solutions",
        "email": "hr@inexture.com",
        "title": "DevOps Engineer / Junior AI Developer",
        "role_focus": "AI infrastructure, Python backends, Docker/Kubernetes, and DevOps automation"
    },
    {
        "company": "SBNA Software Solutions",
        "email": "hr@sbnasoftware.com",
        "title": "AWS Cloud Application Support Engineer",
        "role_focus": "AWS Cloud Infrastructure, Application Support, Linux administration, and system troubleshooting"
    },
    {
        "company": "Briskminds",
        "email": "hr@briskminds.com",
        "title": "Associate Software Engineer (Cloud & AI Backend)",
        "role_focus": "FastAPI/Python backend development, AI integrations, and cloud engineering"
    },
    {
        "company": "VTECH Integrated Solutions",
        "email": "info@vtech-edu.com",
        "title": "DevOps & Cloud Engineer",
        "role_focus": "DevOps practices, AWS Cloud management, containerization, and Linux operations"
    }
]

def build_body(target: dict) -> str:
    company = target["company"]
    title = target["title"]
    role_focus = target["role_focus"]

    return f"""Dear Hiring Team at {company},

I hope this email finds you well.

I am writing to actively apply for the {title} position at {company}. As an AI & Cloud Systems Engineer (Immediate Joiner, 0 days notice) with hands-on expertise in {role_focus}, I am eager to contribute to your engineering and product teams.

Proven Builder & Production Track Record:
• Autonomous Agentic AI & Cognitive Memory (F.R.I.D.A.Y.): Creator of Friday (https://github.com/itskie/friday) — an open-source autonomous agent and long-term memory engine with 65+ GitHub Stars, 10 forks, and 280+ PyPI package downloads. Architected dual-layer semantic memory (ChromaDB vector embeddings + Neo4j knowledge graphs) with MCP (Model Context Protocol) tool execution over FastAPI.
• Production GenAI & SaaS Infrastructure (ReelDM): Architected and deployed a Meta Business Verified platform on AWS EC2, managing webhook pipelines, asynchronous Celery/Redis background task queues, and LLM-driven autonomous customer workflows.
• Cloud & AI Infrastructure: Deep hands-on experience provisioning and scaling containerized workloads with Docker, Kubernetes, and AWS (EC2, ECS Fargate, EKS, VPC, S3, IAM, CloudWatch).
• DevSecOps & Automation: Built automated CI/CD pipelines with GitHub Actions, automated vulnerability scanning with Aqua Trivy, and built InfraGenie (https://github.com/itskie/infragenie) for zero-touch cloud provisioning.
• Education & Background: BCA in Cloud Computing from Amity University (CGPA: 8.1/10).

Availability & Preferences:
• Immediate Joiner (0 days notice period).
• Based in India; open to on-site, hybrid, or remote work arrangements.

My latest resume is attached for your review. I would greatly appreciate the opportunity to connect for a brief introductory conversation.

GitHub: https://github.com/itskie
LinkedIn: https://linkedin.com/in/itskie
Phone: +91 9122927910

Thank you for your time and consideration!

Best regards,
Shobhit Kumar Singh
AI & Cloud Systems Engineer
itskie7910@gmail.com | +91 9122927910"""

def main():
    print("=" * 65)
    print("🚀 DISPATCHING TO TARGETED LEADS")
    print(f"📄 Resume Target: {config.RESUME_PATH}")
    print("=" * 65)

    mailer = AutoMailer()
    sent_count = 0

    for i, target in enumerate(NEW_TARGETS, 1):
        company = target["company"]
        email = target["email"]
        title = target["title"]
        subject = f"Application for {title} — Shobhit Kumar Singh (AI & Cloud Systems Engineer | Immediate Joiner)"
        body = build_body(target)

        print(f"\n[{i}/{len(NEW_TARGETS)}] Target: {company} ➔ {email}")

        if mailer.is_already_applied(email):
            print(f"    ⏭️ Already applied previously. Skipping.")
            continue

        success = mailer.send_application(email, subject, body, dry_run=False)
        if success:
            sent_count += 1
            time.sleep(2)

    print("\n" + "=" * 65)
    print(f"🎉 DISPATCH COMPLETED! Sent {sent_count} applications!")
    print(f"📊 Audit history updated in: {config.SENT_LOG_FILE}")
    print("=" * 65)

if __name__ == "__main__":
    main()
