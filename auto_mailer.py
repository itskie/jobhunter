import os
import json
import csv
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import config

class AutoMailer:
    def __init__(self):
        self.history_file = Path(config.HISTORY_FILE)
        self.sent_log_file = Path(config.SENT_LOG_FILE)
        self.applied_emails = self._load_history()

    def _load_history(self) -> set:
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception:
                return set()
        return set()

    def _save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(list(self.applied_emails), f, indent=2)

    def is_already_applied(self, email: str) -> bool:
        return email.lower().strip() in self.applied_emails

    def send_application(self, to_email: str, subject: str, body: str, dry_run: bool = False) -> bool:
        to_email = to_email.strip().lower()
        if self.is_already_applied(to_email):
            print(f"⏭️ Skipping {to_email} (Already applied earlier)")
            return False

        if dry_run:
            print(f"🔍 [DRY RUN] Would send to: {to_email}")
            print(f"   Subject: {subject}")
            print(f"   Attachment: {config.RESUME_PATH}")
            return True

        if not config.GMAIL_APP_PASSWORD:
            print(f"❌ Cannot send to {to_email}: GMAIL_APP_PASSWORD not set in environment.")
            return False

        msg = MIMEMultipart()
        msg["From"] = f"{config.CANDIDATE_NAME} <{config.CANDIDATE_EMAIL}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach text body
        msg.attach(MIMEText(body, "plain"))

        # Attach PDF Resume
        resume_file = Path(config.RESUME_PATH)
        if resume_file.exists():
            with open(resume_file, "rb") as f:
                pdf_part = MIMEApplication(f.read(), _subtype="pdf")
                pdf_part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename="Shobhit_Kumar_Singh_Resume.pdf"
                )
                msg.attach(pdf_part)
        else:
            print(f"⚠️ Warning: Resume not found at {config.RESUME_PATH}")

        try:
            with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.login(config.CANDIDATE_EMAIL, config.GMAIL_APP_PASSWORD)
                server.sendmail(config.CANDIDATE_EMAIL, to_email, msg.as_string())

            # Update history and CSV log
            self.applied_emails.add(to_email)
            self._save_history()

            # Append to CSV log
            file_exists = self.sent_log_file.exists()
            with open(self.sent_log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Recipient_Email", "Subject", "Status"])
                writer.writerow([datetime.now().isoformat(), to_email, subject, "SENT"])

            print(f"✅ Application successfully sent to: {to_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False
