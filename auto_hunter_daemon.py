import sys
import argparse
from job_extractor import JobPostExtractor
from email_generator import EmailGenerator
from auto_mailer import AutoMailer
import config

def run_pipeline(input_text: str, dry_run: bool = False, max_count: int = config.MAX_DAILY_APPLICATIONS):
    print("=" * 65)
    print("🤖 Autonomous Cloud/DevOps JobHunter & Auto-Apply Bot")
    print(f"📄 Resume Target: {config.RESUME_PATH}")
    print(f"🎯 Target Range: 0–{config.MAX_EXPERIENCE_YEARS} Years Experience")
    print("=" * 65)

    print("\n🔍 Parsing and filtering candidate job posts...")
    matches = JobPostExtractor.parse_multiple_posts(input_text)
    if not matches:
        single = JobPostExtractor.parse_post(input_text)
        if single:
            matches = [single]

    if not matches:
        print("⚠️ No matching 0-2 yrs Cloud/DevOps jobs found in the input.")
        return

    print(f"✅ Found {len(matches)} matching target opportunities.")
    mailer = AutoMailer()

    sent_count = 0
    for i, job in enumerate(matches[:max_count], 1):
        email_data = EmailGenerator.generate_email(job)
        recipient = email_data["to"]
        subject = email_data["subject"]
        body = email_data["body"]

        print(f"\n[{i}/{len(matches)}] Processing: {job['title'][:45]}...")
        print(f"    ➔ Recipient: {recipient}")
        print(f"    ➔ Skills: {', '.join(job['skills']) if job['skills'] else 'AWS & DevOps'}")

        if mailer.is_already_applied(recipient):
            print(f"    ⏭️ Already applied previously. Skipping.")
            continue

        success = mailer.send_application(recipient, subject, body, dry_run=dry_run)
        if success:
            sent_count += 1

    print("\n" + "=" * 65)
    if dry_run:
        print(f"🏁 DRY-RUN COMPLETE: {sent_count} applications validated and ready.")
    else:
        print(f"🏁 EXECUTION COMPLETE: {sent_count} applications sent to recruiters!")
        print(f"📊 Sent history saved in: {config.SENT_LOG_FILE}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Job Hunter & Mailer Bot")
    parser.add_argument("file", nargs="?", help="Optional file containing job posts text")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated emails without sending")
    parser.add_argument("--limit", type=int, default=config.MAX_DAILY_APPLICATIONS, help="Max emails to send")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        print("\nPaste job posts (or raw LinkedIn text) below, then press Ctrl+D:\n")
        try:
            raw_text = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nAborted.")
            return

    if not raw_text.strip():
        print("❌ No input text received.")
        return

    run_pipeline(raw_text, dry_run=args.dry_run, max_count=args.limit)

if __name__ == "__main__":
    main()
