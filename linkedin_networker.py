import os
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
COOKIES_FILE = BASE_DIR / "linkedin_cookies.json"
NETWORK_HISTORY_FILE = BASE_DIR / "network_history.json"

SEARCH_TARGETS = [
    {
        "role_type": "grow",
        "query": "People You May Know in AI & Cloud",
        "url": "https://www.linkedin.com/mynetwork/grow/"
    },
    {
        "role_type": "ai_manager",
        "query": "Engineering Manager AI Bangalore",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Engineering%20Manager%20AI%20Bangalore&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "ai_recruiter",
        "query": "Technical Recruiter AI India",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Technical%20Recruiter%20AI%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "cto_founder",
        "query": "Founder CTO AI Bangalore",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Founder%20CTO%20AI%20Bangalore&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "devops_manager",
        "query": "Engineering Manager DevOps India",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Engineering%20Manager%20DevOps%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "backend_manager",
        "query": "Engineering Manager Backend Bangalore",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Engineering%20Manager%20Backend%20Bangalore&origin=GLOBAL_SEARCH_HEADER"
    }
]

MAX_CONNECTS_PER_RUN = 12

class LinkedInNetworker:
    def __init__(self):
        self.history = self._load_history()

    def _load_history(self) -> set:
        if NETWORK_HISTORY_FILE.exists():
            try:
                with open(NETWORK_HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data.get("connected_profiles", []))
            except Exception as e:
                print(f"⚠️ Error loading network history: {e}")
        return set()

    def _save_history(self, identifier: str):
        self.history.add(identifier)
        try:
            with open(NETWORK_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump({"connected_profiles": list(self.history)}, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving network history: {e}")

    def run(self, max_connects: int = MAX_CONNECTS_PER_RUN):
        has_cookies = COOKIES_FILE.exists()

        print("=" * 65)
        print("🤝 AUTONOMOUS LINKEDIN NETWORKER (AI & Systems Edition)")
        print(f"🎯 Target Max Connects This Run: {max_connects}")
        print(f"🛡️ Safety Pacing: 6-10s human delays enabled")
        print("=" * 65)

        sent_connects = 0

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=has_cookies,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )

            if has_cookies:
                try:
                    with open(COOKIES_FILE, "r") as f:
                        cookies = json.load(f)
                    context.add_cookies(cookies)
                    print("🔑 Loaded saved LinkedIn session cookies.")
                except Exception as e:
                    print(f"⚠️ Failed to load cookies: {e}")
                    has_cookies = False

            page = context.new_page()

            if not has_cookies:
                print("\n🌐 Opening LinkedIn in browser window...")
                page.goto("https://www.linkedin.com/login", timeout=45000)
                input("\n👉 Press [ENTER] once you are logged in: ")
                cookies = context.cookies()
                with open(COOKIES_FILE, "w") as f:
                    json.dump(cookies, f)
                print("✅ Session cookies saved permanently.\n")

            # Stream 1: Grow Network Page (1-Click Instant Connects)
            print("\n🔍 Scanning Stream 1: Grow Network (AI & Cloud Sphere)...")
            try:
                page.goto("https://www.linkedin.com/mynetwork/grow/", timeout=45000, wait_until="domcontentloaded")
                time.sleep(3.5)
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(2.0)

                connect_btns = page.query_selector_all("button[aria-label*='Invite'], button:has-text('Connect')")
                print(f"    Found {len(connect_btns)} direct connect opportunities.")

                for btn in connect_btns:
                    if sent_connects >= max_connects:
                        break

                    aria = btn.get_attribute("aria-label") or ""
                    name = aria.replace("Invite", "").replace("to connect", "").strip() or "Tech Professional"

                    if name in self.history:
                        continue

                    try:
                        btn.scroll_into_view_if_needed()
                        time.sleep(1.0)
                        btn.click()
                        time.sleep(2.0)

                        # Handle possible modal if it pops up
                        send_without_note = page.query_selector("button[aria-label='Send without a note'], button:has-text('Send without a note')")
                        if send_without_note and send_without_note.is_visible():
                            send_without_note.click()
                            time.sleep(1.0)

                        sent_connects += 1
                        self._save_history(name)
                        print(f"    ✅ [1-Click Connect Sent] ➔ {name} (Total: {sent_connects}/{max_connects})")

                        delay = random.uniform(6.0, 9.0)
                        print(f"    ⏳ Pacing safety delay: {delay:.1f}s...")
                        time.sleep(delay)

                    except Exception as e:
                        print(f"    ⚠️ Could not click connect for {name}: {e}")

            except Exception as e:
                print(f"⚠️ Error scanning Grow Network: {e}")

            # Stream 2: People Search Streams
            if sent_connects < max_connects:
                for target in SEARCH_TARGETS[1:]:
                    if sent_connects >= max_connects:
                        break

                    search_url = target["url"]
                    query_name = target["query"]

                    print(f"\n🔍 Scanning Stream: {query_name}")
                    try:
                        page.goto(search_url, timeout=45000, wait_until="domcontentloaded")
                        time.sleep(4.0)
                        page.evaluate("window.scrollBy(0, 1000)")
                        time.sleep(2.0)

                        profile_links = []
                        links = page.query_selector_all('a[href*="/in/"]')
                        for l in links:
                            href = l.get_attribute("href")
                            if href and "/in/" in href:
                                clean_href = href.split("?")[0].rstrip("/")
                                raw_text = l.inner_text().strip()
                                name = raw_text.split("\n")[0].strip()
                                if name and "LinkedIn Member" not in name and len(name) > 2:
                                    if clean_href not in [p["url"] for p in profile_links] and clean_href not in self.history:
                                        profile_links.append({"name": name, "url": clean_href})

                        print(f"    Found {len(profile_links)} candidate profile links.")

                        for profile in profile_links:
                            if sent_connects >= max_connects:
                                break

                            name = profile["name"]
                            p_url = profile["url"]

                            if p_url in self.history or name in self.history:
                                continue

                            print(f"\n👉 Visiting Profile: {name}")
                            try:
                                page.goto(p_url, timeout=30000, wait_until="domcontentloaded")
                                time.sleep(3.5)

                                # Check direct connect button
                                connect_btn = page.query_selector("button:has-text('Connect'), button[aria-label*='Invite']")
                                if connect_btn and connect_btn.is_visible():
                                    connect_btn.click()
                                    time.sleep(2.0)

                                    send_without_note = page.query_selector("button[aria-label='Send without a note'], button:has-text('Send without a note')")
                                    if send_without_note and send_without_note.is_visible():
                                        send_without_note.click()
                                    else:
                                        send_btn = page.query_selector("button[aria-label='Send now'], button[aria-label='Send invitation'], button:has-text('Send')")
                                        if send_btn and send_btn.is_visible():
                                            send_btn.click()

                                    sent_connects += 1
                                    self._save_history(p_url)
                                    self._save_history(name)
                                    print(f"    ✅ [Direct Connect Sent] ➔ {name} (Total: {sent_connects}/{max_connects})")

                                    delay = random.uniform(7.0, 11.0)
                                    print(f"    ⏳ Pacing safety delay: {delay:.1f}s...")
                                    time.sleep(delay)
                                else:
                                    print(f"    ⏭️ Direct connect not visible on profile. Skipping to next.")
                                    self._save_history(p_url)

                            except Exception as e:
                                print(f"    ⚠️ Error connecting with {name}: {e}")
                                self._save_history(p_url)

                    except Exception as e:
                        print(f"⚠️ Error scanning search stream: {e}")

            browser.close()

        print("\n" + "=" * 65)
        print(f"🎉 NETWORKING SESSION COMPLETED! Dispatched {sent_connects} connection requests!")
        print(f"📊 History saved to: {NETWORK_HISTORY_FILE}")
        print("=" * 65)

if __name__ == "__main__":
    networker = LinkedInNetworker()
    networker.run()
