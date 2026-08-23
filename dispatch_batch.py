import time
from pathlib import Path
import config
from auto_mailer import AutoMailer

# Sample recruiter targets template (Add your custom recruiter leads here)
RECRUITER_TARGETS = [
    {"name": "Hiring Lead", "company": "Cloud Systems", "email": "recruiter@example.com"},
    {"name": "Talent Partner", "company": "Tech Innovators", "email": "careers@example.com"}
]

def build_body(recruiter_name: str, company: str) -> str:
    first_name = recruiter_name.split()[0] if recruiter_name else "Hiring Team"
    return f"""Dear {first_name},

I hope this email finds you well.

I am reaching out to explore early-career or junior Cloud & DevOps Engineer opportunities at {company}. As an Immediate Joiner with hands-on experience in AWS cloud infrastructure, container orchestration (Docker/Kubernetes), and Infrastructure as Code (Terraform), I would love to contribute to your engineering and cloud operations teams.

Key Highlights of My Experience:
• Cloud Infrastructure: Proficient with AWS core services (EC2, ECS Fargate, EKS, VPC, S3, IAM, CloudWatch) and Linux system administration.
• Containerization & DevSecOps: Dockerized microservices, configured GitHub Actions CI/CD pipelines, and implemented automated security vulnerability scanning with Aqua Trivy.
• Project & Builder Proof: Built InfraGenie ({config.CANDIDATE_GITHUB}/infragenie), an open-source tool that provisions zero-touch AWS ECS clusters in <2 minutes.
• Work Experience: DevOps Engineer Intern | Strong foundation in Cloud Computing.

I am an Immediate Joiner (0 days notice) and open to working on-site, hybrid, or remote across any {company} location.

I have attached my latest resume for your review. Would greatly appreciate the opportunity to connect for a quick introductory conversation.

GitHub: {config.CANDIDATE_GITHUB}
LinkedIn: {config.CANDIDATE_LINKEDIN}
Phone: {config.CANDIDATE_PHONE}

Thank you for your time and consideration!

Best regards,
{config.CANDIDATE_NAME}
Cloud & DevOps Engineer
{config.CANDIDATE_EMAIL} | {config.CANDIDATE_PHONE}"""

def main():
    print("=" * 65)
    print("🚀 BATCH RECRUITER DISPATCHER TEMPLATE")
    print(f"📄 Resume Target: {config.RESUME_PATH}")
    print(f"🎯 Total Targets: {len(RECRUITER_TARGETS)} Target Recruiters")
    print("=" * 65)

    mailer = AutoMailer()
    sent_count = 0

    for i, target in enumerate(RECRUITER_TARGETS, 1):
        name = target["name"]
        company = target["company"]
        email = target["email"]
        subject = f"Application for Cloud & DevOps Engineer — {config.CANDIDATE_NAME} (Immediate Joiner)"
        body = build_body(name, company)

        print(f"\n[{i}/{len(RECRUITER_TARGETS)}] Dispatching to: {name} ({company}) ➔ {email}")

        if mailer.is_already_applied(email):
            print(f"    ⏭️ Already applied previously. Skipping.")
            continue

        success = mailer.send_application(email, subject, body, dry_run=False)
        if success:
            sent_count += 1
            time.sleep(1.5)

    print("\n" + "=" * 65)
    print(f"🎉 BATCH DISPATCH COMPLETED! Sent {sent_count} applications!")
    print("=" * 65)

if __name__ == "__main__":
    main()
