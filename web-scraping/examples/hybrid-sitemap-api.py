"""
Hybrid: Sitemap + API Scraper

Shows how to:
1. Discover all product URLs instantly from sitemap
2. Extract IDs from URL patterns
3. Fetch structured data from the site's internal API (discovered via traffic capture)

Use this pattern for: Best performance + data quality.
Performance: 60x faster than crawling + cleaner than HTML parsing.
"""

import asyncio
import logging
import re
from typing import Any
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://shop.example.com"
API_URL = "https://api.example.com/v1"  # Discovered via traffic interception
RATE_LIMIT_DELAY = 0.05  # 20 req/s


async def discover_product_ids(base_url: str) -> list[str]:
    """Parse sitemap and extract product IDs from URL paths."""
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        robots_resp = await client.get(robots_url)
        rp = RobotFileParser()
        rp.parse(robots_resp.text.splitlines())
        sitemap_url = rp.site_maps()[0] if rp.site_maps() else f"{base_url}/sitemap.xml"

        sitemap_resp = await client.get(sitemap_url)
        sitemap_resp.raise_for_status()

    soup = BeautifulSoup(sitemap_resp.text, "xml")
    urls = [loc.text.strip() for loc in soup.find_all("loc")]

    ids = []
    for url in urls:
        match = re.search(r"/products/(\d+)", url)
        if match:
            ids.append(match.group(1))

    logger.info("Extracted %d product IDs from %d sitemap URLs", len(ids), len(urls))
    return ids


async def fetch_product(
    client: httpx.AsyncClient, product_id: str
) -> dict[str, Any] | None:
    try:
        resp = await client.get(f"{API_URL}/products/{product_id}")
        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            await asyncio.sleep(5)
            resp = await client.get(f"{API_URL}/products/{product_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        logger.error("Failed product %s: %s", product_id, exc)
        return None


async def main() -> None:
    logger.info("Phase 1: Sitemap discovery")
    product_ids = await discover_product_ids(BASE_URL)

    # Test with first 50 before scaling to full dataset
    test_ids = product_ids[:50]
    logger.info("Phase 2: API data fetching (%d products)", len(test_ids))

    results: list[dict] = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
        for i, pid in enumerate(test_ids, 1):
            data = await fetch_product(client, pid)
            if data:
                results.append(
                    {
                        "id": data.get("id"),
                        "name": data.get("name"),
                        "price": data.get("price"),
                        "url": f"{BASE_URL}/products/{pid}",
                    }
                )
            if i % 10 == 0:
                logger.info("Progress: %d/%d", i, len(test_ids))
            await asyncio.sleep(RATE_LIMIT_DELAY)

    logger.info("Completed: %d products fetched", len(results))
    if results:
        logger.info("Sample: %s", results[0])


if __name__ == "__main__":
    asyncio.run(main())
