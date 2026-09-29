import time
import config
from auto_mailer import AutoMailer

NEW_TARGETS = [
    {
        "company": "SBNA Software Solutions",
        "email": "hr@sbnasoftware.com",
        "title": "AWS Cloud Application Support Engineer",
        "role_focus": "AWS Cloud Infrastructure, Application Support, Linux administration, and system troubleshooting"
    },
    {
        "company": "Inexture Solutions",
        "email": "hr@inexture.com",
        "title": "DevOps Engineer / Junior AI Developer",
        "role_focus": "DevOps automation, Docker, Kubernetes, CI/CD pipelines, and Python AI Infrastructure"
    },
    {
        "company": "Briskminds",
        "email": "hr@briskminds.com",
        "title": "Associate Software Engineer I (Cloud & Backend)",
        "role_focus": "Cloud engineering, backend development, and scalable software systems"
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

I am writing to actively apply for the {title} position at {company}. As an Immediate Joiner (0 days notice) with hands-on expertise in {role_focus}, I am eager to contribute to your engineering and cloud operations teams.

Proven Builder & Production Track Record:
• F.R.I.D.A.Y. (Open Source): Creator of Friday (https://github.com/itskie/friday) — an autonomous memory & cognitive AI infrastructure engine with 65+ GitHub Stars, 10 forks, and 280+ PyPI package downloads. Architecture built on FastAPI, ChromaDB, and Neo4j graph topologies.
• ReelDM (Production SaaS): Architected and deployed a Meta Business Verified SaaS platform on AWS EC2, managing webhook pipelines, async Celery/Redis queues, PostgreSQL, and resilient microservices.
• InfraGenie: Built open-source cloud tooling (https://github.com/itskie/infragenie) automating zero-touch AWS ECS Fargate cluster provisioning in under 2 minutes.
• Cloud & DevSecOps: Deep hands-on proficiency with AWS (EC2, ECS, EKS, VPC, S3, IAM, CloudWatch), Linux kernel administration, automated CI/CD via GitHub Actions, and vulnerability scanning with Aqua Trivy.
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
Systems, Cloud & DevOps Engineer
itskie7910@gmail.com | +91 9122927910"""

def main():
    print("=" * 65)
    print("🚀 DISPATCHING TO NEW JOB LEADS")
    print(f"📄 Resume Target: {config.RESUME_PATH}")
    print("=" * 65)

    mailer = AutoMailer()
    sent_count = 0

    for i, target in enumerate(NEW_TARGETS, 1):
        company = target["company"]
        email = target["email"]
        title = target["title"]
        subject = f"Application for {title} — Shobhit Kumar Singh (Immediate Joiner)"
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
