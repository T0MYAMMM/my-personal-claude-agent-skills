"""
Basic Sitemap-Based Scraper (crawlee-python + BeautifulSoupCrawler)

Shows how to:
1. Parse sitemap URLs with crawlee-python
2. Scrape static HTML pages with BeautifulSoupCrawler
3. Persist results via the built-in Dataset

Use this pattern for: E-commerce sites, blogs, news sites with sitemaps.
"""

import asyncio
import logging
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def discover_sitemap_urls(base_url: str) -> list[str]:
    """Parse robots.txt then the first declared sitemap."""
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        resp = await client.get(robots_url)
        resp.raise_for_status()

    rp = RobotFileParser()
    rp.parse(resp.text.splitlines())
    sitemap_url = rp.site_maps()[0] if rp.site_maps() else f"{base_url}/sitemap.xml"

    # Fetch and parse the sitemap XML
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        resp = await client.get(sitemap_url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "xml")
    urls = [loc.text.strip() for loc in soup.find_all("loc")]
    logger.info("Found %d URLs in sitemap", len(urls))
    return urls


async def main() -> None:
    base_url = "https://example.com"

    all_urls = await discover_sitemap_urls(base_url)
    # Filter: only product pages
    product_urls = [u for u in all_urls if "/products/" in u]
    logger.info("Filtered to %d product URLs", len(product_urls))

    # Test with first 10 before scaling
    test_urls = product_urls[:10]

    crawler = BeautifulSoupCrawler(
        max_requests_per_crawl=len(test_urls),
        max_request_retries=3,
        request_handler_timeout=30,
        max_crawl_depth=0,  # don't follow links — URLs already known
    )

    @crawler.router.default_handler
    async def handler(context: BeautifulSoupCrawlingContext) -> None:
        soup = context.soup
        data = {
            "url": context.request.url,
            "title": soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else None,
            "price": soup.select_one(".price").get_text(strip=True) if soup.select_one(".price") else None,
            "description": soup.select_one(".description").get_text(strip=True) if soup.select_one(".description") else None,
            "image": soup.select_one("img.main-image")["src"] if soup.select_one("img.main-image") else None,
            "in_stock": bool(soup.select_one(".in-stock")),
        }
        await context.push_data(data)
        context.log.info("Scraped: %s", context.request.url)

    await crawler.run(test_urls)
    logger.info("Scraping completed — scale by passing full product_urls list")


if __name__ == "__main__":
    asyncio.run(main())
