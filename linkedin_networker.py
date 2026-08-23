import os
import json
import time
import random
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import config

BASE_DIR = Path(__file__).resolve().parent
COOKIES_FILE = BASE_DIR / "linkedin_cookies.json"
NETWORK_HISTORY_FILE = BASE_DIR / "network_history.json"

SEARCH_TARGETS = [
    {
        "role_type": "manager",
        "query": "Engineering Manager DevOps India",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Engineering%20Manager%20DevOps%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "recruiter",
        "query": "Technical Recruiter Cloud DevOps India",
        "url": "https://www.linkedin.com/search/results/people/?keywords=Technical%20Recruiter%20Cloud%20DevOps%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "lead",
        "query": "DevOps Lead Cloud Architect India",
        "url": "https://www.linkedin.com/search/results/people/?keywords=DevOps%20Lead%20Cloud%20Architect%20India&origin=GLOBAL_SEARCH_HEADER"
    }
]

MAX_CONNECTS_PER_RUN = 10

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

    def _save_history(self, profile_url_or_name: str):
        self.history.add(profile_url_or_name)
        try:
            with open(NETWORK_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump({"connected_profiles": list(self.history)}, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving network history: {e}")

    def generate_note(self, name: str, role_type: str) -> str:
        first_name = name.split()[0] if name else "there"
        first_name = re.sub(r'[^a-zA-Z]', '', first_name).capitalize() or "there"

        if role_type == "manager":
            note = f"Hi {first_name} Sir, I'm a Cloud & DevOps Engineer (AWS, Docker, K8s, Terraform) and creator of InfraGenie. Would love to connect and follow your engineering work!"
        elif role_type == "recruiter":
            note = f"Hi {first_name}, I'm an Immediate Joiner Cloud & DevOps Engineer (AWS, Docker, K8s, Terraform, Python). Built InfraGenie for automated ECS deployments. Would love to connect!"
        else:
            note = f"Hi {first_name}, I'm a Cloud & DevOps Engineer passionate about AWS, K8s, and developer tooling (built InfraGenie & JobHunter). Would love to connect!"

        return note[:295]

    def run(self, max_connects: int = MAX_CONNECTS_PER_RUN):
        if not COOKIES_FILE.exists():
            print(f"❌ Error: LinkedIn cookies file not found at {COOKIES_FILE}")
            return

        print("=" * 65)
        print("🤝 AUTONOMOUS LINKEDIN NETWORKER (Profile-Direct Mode)")
        print(f"🎯 Target Max Connects This Run: {max_connects}")
        print(f"🛡️ Safety Pacing: 6-12s human delays enabled")
        print("=" * 65)

        sent_connects = 0

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )

            with open(COOKIES_FILE, "r") as f:
                cookies = json.load(f)
            context.add_cookies(cookies)

            page = context.new_page()

            for target in SEARCH_TARGETS:
                if sent_connects >= max_connects:
                    break

                role_type = target["role_type"]
                search_url = target["url"]
                query_name = target["query"]

                print(f"\n🔍 Searching Stream: {query_name}")
                try:
                    page.goto(search_url, timeout=45000, wait_until="domcontentloaded")
                    time.sleep(random.uniform(4.0, 6.0))
                    page.evaluate("window.scrollBy(0, 1000)")
                    time.sleep(2.0)

                    # Extract all profile /in/ links
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

                    print(f"    Discovered {len(profile_links)} fresh profiles to connect with.")

                    for profile in profile_links:
                        if sent_connects >= max_connects:
                            break

                        name = profile["name"]
                        p_url = profile["url"]

                        if p_url in self.history or name in self.history:
                            continue

                        print(f"\n👉 Visiting Profile: {name} ➔ {p_url}")
                        try:
                            page.goto(p_url, timeout=30000, wait_until="domcontentloaded")
                            time.sleep(random.uniform(3.0, 5.0))

                            # Check for direct Connect button
                            connect_btn = None
                            buttons = page.query_selector_all("button")
                            for btn in buttons:
                                b_text = btn.inner_text().strip().lower()
                                if b_text == "connect" or "invite" in b_text:
                                    connect_btn = btn
                                    break

                            # If not direct, check "More" button
                            if not connect_btn:
                                more_btn = page.query_selector("button:has-text('More'), button[aria-label='More actions']")
                                if more_btn:
                                    more_btn.click()
                                    time.sleep(1.0)
                                    # Look for connect inside dropdown
                                    connect_in_dropdown = page.query_selector("div[aria-label*='Invite'], div[role='button']:has-text('Connect'), span:has-text('Connect')")
                                    if connect_in_dropdown:
                                        connect_btn = connect_in_dropdown

                            if not connect_btn:
                                print(f"    ⏭️ No Connect button found (Already connected or Following). Skipping.")
                                self._save_history(p_url)
                                continue

                            # Click Connect
                            connect_btn.click()
                            time.sleep(random.uniform(2.0, 3.0))

                            # Check for "Add a note" modal
                            add_note_btn = page.query_selector("button[aria-label='Add a note'], button:has-text('Add a note')")
                            if add_note_btn and add_note_btn.is_visible():
                                add_note_btn.click()
                                time.sleep(random.uniform(1.5, 2.5))

                                note_text = self.generate_note(name, role_type)
                                textarea = page.query_selector("textarea[name='message'], textarea#custom-message")
                                if textarea:
                                    textarea.fill(note_text)
                                    time.sleep(random.uniform(1.0, 2.0))

                                send_btn = page.query_selector("button[aria-label='Send invitation'], button[aria-label='Send now'], button:has-text('Send')")
                                if send_btn and send_btn.is_visible():
                                    send_btn.click()
                                    print(f"    ✉️ Sent custom note: \"{note_text[:60]}...\"")
                            else:
                                send_btn = page.query_selector("button[aria-label='Send without a note'], button[aria-label='Send now'], button:has-text('Send')")
                                if send_btn and send_btn.is_visible():
                                    send_btn.click()
                                    print(f"    ✉️ Sent direct invitation.")

                            sent_connects += 1
                            self._save_history(p_url)
                            self._save_history(name)
                            print(f"    ✅ Successfully sent connection request to {name}! (Total: {sent_connects}/{max_connects})")

                            sleep_time = random.uniform(7.0, 12.0)
                            print(f"    ⏳ Pacing safety delay: {sleep_time:.1f}s...")
                            time.sleep(sleep_time)

                        except Exception as e:
                            print(f"    ⚠️ Could not complete connect for {name}: {e}")
                            self._save_history(p_url)

                except Exception as e:
                    print(f"⚠️ Error scanning stream {query_name}: {e}")

            browser.close()

        print("\n" + "=" * 65)
        print(f"🎉 NETWORKING SESSION FINISHED! Sent {sent_connects} connection invitations with notes!")
        print(f"📊 History saved to: {NETWORK_HISTORY_FILE}")
        print("=" * 65)

if __name__ == "__main__":
    networker = LinkedInNetworker()
    networker.run()
