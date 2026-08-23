import os
import sys
import urllib.parse
from job_extractor import JobPostExtractor
from email_generator import EmailGenerator

def main():
    print("=" * 60)
    print("🤖 LinkedIn Group JobHunter & Auto-Apply Bot (v1.0)")
    print("=" * 60)

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        print("\nPaste your LinkedIn group posts below (Press Ctrl+D or Ctrl+Z when done):\n")
        try:
            content = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nExiting...")
            return

    if not content.strip():
        print("❌ No text provided. Exiting.")
        return

    print("\n🔍 Parsing and filtering jobs (Criteria: 0-2 yrs / Fresher & Cloud/DevOps/AI)...")
    matches = JobPostExtractor.parse_multiple_posts(content)

    if not matches:
        # Try parsing single post if splitting produced nothing
        single = JobPostExtractor.parse_post(content)
        if single:
            matches = [single]

    if not matches:
        print("⚠️ No matching 0-2 yrs Cloud/DevOps job posts with emails found.")
        return

    print(f"\n✅ Found {len(matches)} matching opportunities!\n")

    html_cards = []

    for i, job in enumerate(matches, 1):
        email_data = EmailGenerator.generate_email(job)
        print(f"[{i}] {job['title'][:40]}... ➔ {email_data['to']}")
        print(f"    Subject: {email_data['subject']}")
        print(f"    Detected Skills: {', '.join(job['skills']) if job['skills'] else 'General Cloud'}")
        print("-" * 50)

        # Generate mailto link
        subject_enc = urllib.parse.quote(email_data["subject"])
        body_enc = urllib.parse.quote(email_data["body"])
        mailto_url = f"mailto:{email_data['to']}?subject={subject_enc}&body={body_enc}"

        html_cards.append(f"""
        <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:18px; margin-bottom:12px; color:#f8fafc;">
          <h3 style="color:#38bdf8; margin-bottom:4px;">{i}. {job['title']}</h3>
          <p style="color:#94a3b8; font-size:13px; margin-bottom:10px;"><b>To:</b> {email_data['to']} | <b>Skills:</b> {', '.join(job['skills'])}</p>
          <a href="{mailto_url}" style="background:#2563eb; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:13px; display:inline-block;">🚀 Open in Mail & Send</a>
        </div>
        """)

    # Export an updated 1-click sender page
    output_html = f"""<!DOCTYPE html>
    <html>
    <head><title>Auto-Generated Job Applications</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family:'Inter',sans-serif; background:#0f172a; padding:30px; max-width:750px; margin:auto; }}</style>
    </head>
    <body>
      <h1 style="color:#38bdf8; text-align:center;">⚡ Auto-Generated Job Applications ({len(matches)} Found)</h1>
      <p style="color:#94a3b8; text-align:center; margin-bottom:25px;">Click any button to open your email client with 100% pre-filled application details!</p>
      {''.join(html_cards)}
      <p style="color:#cbd5e1; text-align:center; margin-top:20px; font-size:12px;">📎 Remember to attach <code>Shobhit_Singh_Resume.pdf</code> before sending!</p>
    </body>
    </html>
    """

    out_path = "/Users/kie/Desktop/Latest_Job_Applications.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"\n🎉 1-Click Application Launcher generated on your Desktop:")
    print(f"👉 {out_path}")

if __name__ == "__main__":
    main()
