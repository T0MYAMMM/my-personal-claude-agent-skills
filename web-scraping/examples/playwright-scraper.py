"""
Playwright Scraper (playwright-python)

Shows how to:
1. Launch a browser with anti-detection (playwright-stealth)
2. Navigate and extract JS-rendered content
3. Intercept network requests to discover internal APIs
4. Combine browser session cookies with httpx for production API calls

Use this pattern for: JS-heavy sites, sites requiring login,
                       traffic interception to discover APIs.
"""

import asyncio
import logging

from playwright.async_api import async_playwright, Page, Route, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def intercept_requests(route: Route, request: Request) -> None:
    """Log API calls discovered during page load."""
    if "api" in request.url or request.resource_type in ("xhr", "fetch"):
        logger.info("API call: [%s] %s", request.method, request.url)
    await route.continue_()


async def scrape_with_playwright(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="America/New_York",
        )

        # playwright-stealth: patch navigator.webdriver and other detection vectors
        # Install: pip install playwright-stealth
        # from playwright_stealth import stealth_async
        # await stealth_async(context)

        page: Page = await context.new_page()

        # Intercept all requests — log API endpoints discovered during page load
        await page.route("**/*", intercept_requests)

        await page.goto(url, wait_until="networkidle", timeout=30_000)

        # Extract data from rendered DOM
        title = await page.text_content("h1")
        price = await page.text_content(".price")

        # Get cookies to reuse in httpx API calls
        cookies = await context.cookies()
        cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

        data = {
            "url": url,
            "title": title.strip() if title else None,
            "price": price.strip() if price else None,
            "cookies": cookie_header,  # Reuse in httpx for API calls
        }

        await browser.close()
        return data


async def main() -> None:
    result = await scrape_with_playwright("https://example.com/products/123")
    logger.info("Scraped: %s", result)

    # After discovering the API endpoint from logged requests above,
    # use httpx for production bulk fetching (see api-scraper.py)


if __name__ == "__main__":
    asyncio.run(main())
