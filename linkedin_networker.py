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
        "query": '"Engineering Manager" ("DevOps" OR "Cloud") India',
        "url": "https://www.linkedin.com/search/results/people/?keywords=%22Engineering%20Manager%22%20(%22DevOps%22%20OR%20%22Cloud%22)%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "recruiter",
        "query": '"Technical Recruiter" ("DevOps" OR "Cloud") India',
        "url": "https://www.linkedin.com/search/results/people/?keywords=%22Technical%20Recruiter%22%20(%22DevOps%22%20OR%20%22Cloud%22)%20India&origin=GLOBAL_SEARCH_HEADER"
    },
    {
        "role_type": "lead",
        "query": '"DevOps Lead" OR "Cloud Architect" Bangalore OR Pune OR Remote',
        "url": "https://www.linkedin.com/search/results/people/?keywords=%22DevOps%20Lead%22%20OR%20%22Cloud%20Architect%22%20India&origin=GLOBAL_SEARCH_HEADER"
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

    def generate_note(self, name: str, headline: str, role_type: str) -> str:
        first_name = name.split()[0] if name else "there"
        # Clean title / remove Dr/Mr/salutations if needed
        first_name = re.sub(r'[^a-zA-Z]', '', first_name).capitalize() or "there"

        if role_type == "manager":
            note = f"Hi {first_name} Sir, I'm a Cloud & DevOps Engineer (AWS, Docker, K8s, Terraform) and creator of InfraGenie. Would love to connect and follow your engineering work!"
        elif role_type == "recruiter":
            note = f"Hi {first_name}, I'm an Immediate Joiner Cloud & DevOps Engineer (AWS, Docker, K8s, Terraform, Python). Built InfraGenie for automated ECS deployments. Would love to connect!"
        else:
            note = f"Hi {first_name}, I'm a Cloud & DevOps Engineer passionate about AWS, K8s, and developer tooling (built InfraGenie & JobHunter). Would love to connect!"

        # Ensure strict LinkedIn 300 characters limit
        return note[:295]

    def run(self, max_connects: int = MAX_CONNECTS_PER_RUN):
        if not COOKIES_FILE.exists():
            print(f"❌ Error: LinkedIn cookies file not found at {COOKIES_FILE}")
            print("Please ensure you have authenticated your session first.")
            return

        print("=" * 65)
        print("🤝 AUTONOMOUS LINKEDIN NETWORKER (Engineering Managers & Tech Recruiters)")
        print(f"🎯 Target Max Connects This Run: {max_connects}")
        print(f"🛡️ Safety Pacing: 5-10s human delays enabled")
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

            # Load persistent cookies
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

                    # Scroll to trigger lazy loading of people cards
                    page.evaluate("window.scrollBy(0, 800)")
                    time.sleep(2.0)

                    # Locate all people result containers
                    # Search result cards typically have data-view-name="search-entity-result-universal-template" or .reusable-search__result-container
                    cards = page.query_selector_all(".reusable-search__result-container, li.artdeco-list__item, [data-view-name*='search-entity']")

                    print(f"    Found {len(cards)} profile cards on page.")

                    for card in cards:
                        if sent_connects >= max_connects:
                            break

                        # Extract name
                        name_el = card.query_selector("span[dir='ltr'] span[aria-hidden='true'], .entity-result__title-text a, a[data-field='card-headline']")
                        name = name_el.inner_text().strip() if name_el else ""

                        # Extract headline
                        headline_el = card.query_selector(".entity-result__primary-subtitle, .entity-result__summary")
                        headline = headline_el.inner_text().strip() if headline_el else ""

                        if not name or "LinkedIn Member" in name:
                            continue

                        # Check deduplication
                        if name in self.history:
                            continue

                        # Check if Connect button is present
                        connect_btn = None
                        buttons = card.query_selector_all("button")
                        for btn in buttons:
                            btn_text = btn.inner_text().strip().lower()
                            if "connect" in btn_text and "pending" not in btn_text:
                                connect_btn = btn
                                break

                        if not connect_btn:
                            continue

                        print(f"\n👉 Targeting: {name} | {headline[:45]}...")

                        # Click Connect
                        try:
                            connect_btn.scroll_into_view_if_needed()
                            time.sleep(random.uniform(1.0, 2.0))
                            connect_btn.click()
                            time.sleep(random.uniform(2.0, 3.0))

                            # Check for "Add a note" button in modal
                            add_note_btn = page.query_selector("button[aria-label='Add a note'], button:has-text('Add a note')")

                            if add_note_btn and add_note_btn.is_visible():
                                add_note_btn.click()
                                time.sleep(random.uniform(1.5, 2.5))

                                note_text = self.generate_note(name, headline, role_type)
                                textarea = page.query_selector("textarea[name='message'], textarea#custom-message")
                                if textarea:
                                    textarea.fill(note_text)
                                    time.sleep(random.uniform(1.0, 2.0))

                                # Click Send
                                send_btn = page.query_selector("button[aria-label='Send invitation'], button[aria-label='Send now'], button:has-text('Send')")
                                if send_btn and send_btn.is_visible():
                                    send_btn.click()
                                    print(f"    ✉️ Sent custom note: \"{note_text[:60]}...\"")
                            else:
                                # Send without note if modal didn't present add note
                                send_btn = page.query_selector("button[aria-label='Send without a note'], button[aria-label='Send now'], button:has-text('Send')")
                                if send_btn and send_btn.is_visible():
                                    send_btn.click()
                                    print(f"    ✉️ Sent connection invitation directly.")

                            sent_connects += 1
                            self._save_history(name)
                            print(f"    ✅ Successfully connected with {name}! (Total sent: {sent_connects}/{max_connects})")

                            # Human delay
                            sleep_time = random.uniform(6.0, 11.0)
                            print(f"    ⏳ Pacing safety delay: {sleep_time:.1f}s...")
                            time.sleep(sleep_time)

                        except Exception as e:
                            print(f"    ⚠️ Could not complete connect for {name}: {e}")
                            # Dismiss any open dialog
                            dismiss_btn = page.query_selector("button[aria-label='Dismiss']")
                            if dismiss_btn:
                                dismiss_btn.click()
                            time.sleep(1.0)

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
