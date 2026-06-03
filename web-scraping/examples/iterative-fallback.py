"""
Iterative Fallback Scraper

Tries strategies from fastest to slowest, falling back automatically:
  1. Sitemap + API        (fastest — traffic interception reveals API first)
  2. Sitemap + BeautifulSoup (static HTML pages)
  3. Sitemap + Playwright (JS-rendered pages)
  4. Pure Playwright crawl (no sitemap — last resort)

Use this pattern for: Unknown sites, maximum reliability.

NOTE: Phase 0 (traffic interception via proxy-mcp) is done interactively during
      reconnaissance BEFORE running this script. This handles production extraction.
"""

import asyncio
import logging
import re
from typing import Any
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_sitemap_urls(base_url: str) -> list[str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        robots_resp = await client.get(f"{base_url}/robots.txt")
        rp = RobotFileParser()
        rp.parse(robots_resp.text.splitlines())
        sitemap_url = rp.site_maps()[0] if rp.site_maps() else f"{base_url}/sitemap.xml"
        resp = await client.get(sitemap_url)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "xml")
    return [loc.text.strip() for loc in soup.find_all("loc")]


# ─── Attempt 1: Sitemap + API ────────────────────────────────────────────────

async def try_sitemap_api(base_url: str) -> dict[str, Any] | None:
    logger.info("Attempt 1: Sitemap + API")
    try:
        urls = await get_sitemap_urls(base_url)
        if not urls:
            raise ValueError("Sitemap empty")

        ids = [m.group(1) for u in urls if (m := re.search(r"/products/(\d+)", u))]
        if not ids:
            raise ValueError("No product IDs in sitemap URLs")

        test_id = ids[0]
        api_url = f"https://api.{base_url.replace('https://', '')}/products/{test_id}"

        async with httpx.AsyncClient(timeout=5.0) as client:
            probe = await client.get(api_url)
            probe.raise_for_status()

        logger.info("API accessible — using Sitemap + API")
        results = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for pid in ids[:5]:  # test batch
                r = await client.get(f"https://api.{base_url.replace('https://', '')}/products/{pid}")
                if r.status_code == 200:
                    results.append(r.json())
                await asyncio.sleep(0.1)

        return {"method": "sitemap-api", "data": results}
    except Exception as exc:
        logger.warning("Sitemap + API failed: %s", exc)
        return None


# ─── Attempt 2: Sitemap + BeautifulSoup (static HTML) ───────────────────────

async def try_sitemap_beautifulsoup(base_url: str) -> dict[str, Any] | None:
    logger.info("Attempt 2: Sitemap + BeautifulSoup")
    try:
        urls = await get_sitemap_urls(base_url)
        if not urls:
            raise ValueError("Sitemap empty")

        results: list[dict] = []
        crawler = BeautifulSoupCrawler(max_requests_per_crawl=5)

        @crawler.router.default_handler
        async def handler(ctx: BeautifulSoupCrawlingContext) -> None:
            data = {
                "url": ctx.request.url,
                "title": ctx.soup.select_one("h1").get_text(strip=True) if ctx.soup.select_one("h1") else None,
                "price": ctx.soup.select_one(".price").get_text(strip=True) if ctx.soup.select_one(".price") else None,
            }
            await ctx.push_data(data)
            results.append(data)

        await crawler.run(urls[:5])
        return {"method": "sitemap-beautifulsoup", "data": results}
    except Exception as exc:
        logger.warning("Sitemap + BeautifulSoup failed: %s", exc)
        return None


# ─── Attempt 3: Sitemap + Playwright (JS-rendered) ──────────────────────────

async def try_sitemap_playwright(base_url: str) -> dict[str, Any] | None:
    logger.info("Attempt 3: Sitemap + Playwright")
    try:
        urls = await get_sitemap_urls(base_url)
        if not urls:
            raise ValueError("Sitemap empty")

        results: list[dict] = []
        crawler = PlaywrightCrawler(max_requests_per_crawl=5, max_concurrency=2)

        @crawler.router.default_handler
        async def handler(ctx: PlaywrightCrawlingContext) -> None:
            page = ctx.page
            data = {
                "url": ctx.request.url,
                "title": await page.text_content("h1"),
                "price": await page.text_content(".price"),
            }
            await ctx.push_data(data)
            results.append(data)

        await crawler.run(urls[:5])
        return {"method": "sitemap-playwright", "data": results}
    except Exception as exc:
        logger.warning("Sitemap + Playwright failed: %s", exc)
        return None


# ─── Attempt 4: Pure Playwright crawl (last resort) ─────────────────────────

async def try_playwright_crawl(base_url: str) -> dict[str, Any]:
    logger.info("Attempt 4: Playwright crawl (fallback)")
    results: list[dict] = []
    crawler = PlaywrightCrawler(max_requests_per_crawl=10, max_concurrency=2)

    @crawler.router.default_handler
    async def handler(ctx: PlaywrightCrawlingContext) -> None:
        page = ctx.page
        data = {
            "url": ctx.request.url,
            "title": await page.text_content("h1"),
            "price": await page.text_content(".price"),
        }
        await ctx.push_data(data)
        results.append(data)
        await ctx.enqueue_links(selector="a[href*='/products/']", strategy="same-domain")

    await crawler.run([base_url])
    return {"method": "playwright-crawl", "data": results}


# ─── Orchestrator ────────────────────────────────────────────────────────────

async def scrape_with_fallback(base_url: str) -> dict[str, Any]:
    for attempt in [
        lambda: try_sitemap_api(base_url),
        lambda: try_sitemap_beautifulsoup(base_url),
        lambda: try_sitemap_playwright(base_url),
    ]:
        result = await attempt()
        if result:
            return result

    return await try_playwright_crawl(base_url)


async def main() -> None:
    result = await scrape_with_fallback("https://example.com")
    logger.info("Used method: %s — %d items", result["method"], len(result["data"]))


if __name__ == "__main__":
    asyncio.run(main())
