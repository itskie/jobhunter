import os
import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import config
from job_extractor import JobPostExtractor
from email_generator import EmailGenerator
from auto_mailer import AutoMailer

COOKIE_FILE = Path(__file__).resolve().parent / "linkedin_cookies.json"

SEARCH_URLS = [
    # Top Active Groups
    "https://www.linkedin.com/groups/9334060/",
    "https://www.linkedin.com/groups/49301/",
    "https://www.linkedin.com/groups/48613/",
    "https://www.linkedin.com/groups/1077997/",
    
    # 0-2 yrs Cloud & DevOps High-Intent Feeds
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22cloud%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22aws%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22fresher%22%20%22devops%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22intern%22%20%22devops%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22send%20resume%22%20%22devops%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22share%20resume%22%20%22devops%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22share%20cv%22%20%22cloud%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22linux%22%20%22fresher%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22kubernetes%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22terraform%22%20%22email%22&sortBy=%22date_posted%22",
    
    # AI, LLM & GenAI High-Intent Feeds
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22ai%20engineer%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22generative%20ai%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22llm%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22fastapi%22%20%22email%22&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22share%20resume%22%20%22ai%22&sortBy=%22date_posted%22",
    # Location Specific
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20bangalore%20email&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20pune%20email&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20hyderabad%20email&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20noida%20email&sortBy=%22date_posted%22",
    "https://www.linkedin.com/search/results/content/?keywords=%22hiring%22%20%22devops%22%20remote%20email&sortBy=%22date_posted%22"
]

def send_macos_notification(title: str, message: str):
    try:
        os.system(f"""osascript -e 'display notification "{message}" with title "{title}"'""")
    except Exception:
        pass

async def run_autopilot(dry_run: bool = False, max_scrolls: int = 20):
    print("=" * 65)
    print("🤖 ULTRA-ACCURATE PAN-INDIA AUTO-PILOT JOB APPLIER")
    print(f"📄 Resume Target: {config.RESUME_PATH}")
    print(f"📡 Search Queries: {len(SEARCH_URLS)} High-Intent Feeds")
    print("=" * 65)

    all_raw_posts = []
    has_cookies = COOKIE_FILE.exists()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=has_cookies,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            no_viewport=True,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        if has_cookies:
            try:
                with open(COOKIE_FILE, "r") as f:
                    cookies = json.load(f)
                    await context.add_cookies(cookies)
                print("🔑 Loaded saved LinkedIn session cookies.")
            except Exception as e:
                print(f"⚠️ Failed to load cookies: {e}")
                has_cookies = False

        page = await context.new_page()

        if not has_cookies:
            print("\n🌐 Opening LinkedIn in browser window...")
            await page.goto("https://www.linkedin.com/login", timeout=60000)
            print("👉 Boss, please log in to LinkedIn in the browser window...")
            for _ in range(150):
                await asyncio.sleep(2)
                try:
                    curr = page.url
                    if any(x in curr for x in ["/feed", "/mynetwork", "/in/", "/search", "/messaging"]):
                        print("🎉 Login detected automatically!")
                        break
                    nav = await page.query_selector(".global-nav, .feed-identity-module")
                    if nav:
                        print("🎉 Login detected via feed navigation!")
                        break
                except Exception:
                    pass
            await asyncio.sleep(3)
            cookies = await context.cookies()
            with open(COOKIE_FILE, "w") as f:
                json.dump(cookies, f)
            print("✅ Session cookies saved permanently!\n")

        for idx, target_url in enumerate(SEARCH_URLS, 1):
            print(f"\n📡 [{idx}/{len(SEARCH_URLS)}] Crawling: {target_url[:65]}...")
            try:
                await page.goto(target_url, timeout=45000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

                # Scroll and expand "...see more" buttons to uncover emails
                for s in range(max_scrolls):
                    # Click all visible "see more" buttons on the feed
                    try:
                        see_more_buttons = await page.query_selector_all(
                            "button.feed-shared-inline-show-more-text__button, [aria-label='see more'], button.see-more"
                        )
                        for btn in see_more_buttons[:10]:
                            try:
                                await btn.click(timeout=800)
                            except Exception:
                                pass
                    except Exception:
                        pass

                    await page.evaluate("window.scrollBy(0, window.innerHeight * 2.5)")
                    await page.wait_for_timeout(2000)

                # Extract from all relevant post content nodes
                elements = await page.query_selector_all(
                    ".feed-shared-update-v2, .feed-shared-text, [data-urn], .feed-shared-update-v2__description, .break-words, .update-components-text"
                )
                
                for el in elements:
                    try:
                        txt = await el.inner_text()
                        if txt and ("@" in txt or "hiring" in txt.lower() or "resume" in txt.lower() or "devops" in txt.lower()):
                            all_raw_posts.append(txt.strip())
                    except Exception:
                        pass

            except Exception as e:
                print(f"⚠️ Notice on feed #{idx}: {e}")

        await browser.close()

    print(f"\n📦 Extracted {len(all_raw_posts)} total raw feed posts.")

    unique_posts = list(dict.fromkeys(all_raw_posts))
    valid_jobs = []
    for post in unique_posts:
        parsed = JobPostExtractor.parse_post(post)
        if parsed:
            valid_jobs.append(parsed)

    print(f"🎯 Filtered: {len(valid_jobs)} matching 0-2 yrs Cloud/DevOps opportunities.")

    mailer = AutoMailer()
    applied_count = 0

    jobs_to_process = valid_jobs if config.MAX_DAILY_APPLICATIONS is None else valid_jobs[:config.MAX_DAILY_APPLICATIONS]

    for i, job in enumerate(jobs_to_process, 1):
        email_data = EmailGenerator.generate_email(job)
        to_addr = email_data["to"]
        subject = email_data["subject"]
        body = email_data["body"]

        print(f"\n[{i}/{len(jobs_to_process)}] ➔ {job['title'][:40]}... (To: {to_addr})")
        if mailer.is_already_applied(to_addr):
            print(f"    ⏭️ Already applied previously. Skipping.")
            continue

        success = mailer.send_application(to_addr, subject, body, dry_run=dry_run)
        if success:
            applied_count += 1

    print("\n" + "=" * 65)
    if dry_run:
        print(f"🏁 AUTO-PILOT DRY-RUN: {applied_count} applications ready.")
    else:
        print(f"🎉 AUTO-PILOT FINISHED: {applied_count} new applications sent to recruiters!")
        send_macos_notification(
            "JobHunter Auto-Pilot",
            f"Successfully applied to {applied_count} Cloud/DevOps jobs today!"
        )
    print("=" * 65)

def main():
    dry_run = "--dry-run" in sys.argv
    asyncio.run(run_autopilot(dry_run=dry_run))

if __name__ == "__main__":
    main()
