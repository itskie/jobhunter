import asyncio
import re
from playwright.async_api import async_playwright
from typing import List

GROUP_URL = "https://www.linkedin.com/groups/9334060/"
SEARCH_URL = "https://www.linkedin.com/search/results/content/?keywords=hiring%20devops%20fresher%20email&sortBy=%22date_posted%22"

async def scrape_linkedin_posts(use_headful: bool = False, max_scrolls: int = 4) -> List[str]:
    posts_text = []
    print("🌐 Launching automated browser crawler...")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=not use_headful)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"📡 Navigating to LinkedIn World IT Jobs Group: {GROUP_URL}...")
        try:
            await page.goto(GROUP_URL, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Auto-scroll to load posts dynamically
            for s in range(max_scrolls):
                print(f"    ⬇️ Scrolling feed ({s+1}/{max_scrolls})...")
                await page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
                await page.wait_for_timeout(2000)

            # Extract post content containers
            elements = await page.query_selector_all(".feed-shared-update-v2, .feed-shared-text, [data-urn], article")
            print(f"📦 Found {len(elements)} raw feed post blocks.")

            for el in elements:
                text = await el.inner_text()
                if text and ("@" in text or "hiring" in text.lower() or "devops" in text.lower()):
                    posts_text.append(text.strip())

        except Exception as e:
            print(f"⚠️ Crawler notice: {e}")
        finally:
            await browser.close()

    return list(dict.fromkeys(posts_text))

if __name__ == "__main__":
    results = asyncio.run(scrape_linkedin_posts(use_headful=False))
    print(f"🎯 Total unique hiring posts extracted: {len(results)}")
