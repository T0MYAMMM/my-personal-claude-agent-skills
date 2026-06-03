"""
API-Based Scraper (httpx)

Shows how to:
1. Fetch structured data via a discovered API
2. Handle authentication (cookies, tokens, headers)
3. Retry on rate-limiting and transient errors

Use this pattern for: Any site with a discoverable REST/GraphQL API.
"""

import asyncio
import logging
from typing import Any

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_API_URL = "https://api.example.com/v1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    # Add auth when needed:
    # "Authorization": "Bearer YOUR_TOKEN",
    # "X-API-Key": "YOUR_KEY",
}


async def fetch_product(
    client: httpx.AsyncClient, product_id: int, retries: int = 3
) -> dict[str, Any] | None:
    url = f"{BASE_API_URL}/products/{product_id}"
    for attempt in range(retries):
        try:
            response = await client.get(url)
            if response.status_code == 404:
                logger.warning("Product %d not found", product_id)
                return None
            if response.status_code == 429:
                wait = 5 * (attempt + 1)
                logger.warning("Rate limited — waiting %ds", wait)
                await asyncio.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            logger.error("HTTP error on product %d (attempt %d): %s", product_id, attempt + 1, exc)
            if attempt == retries - 1:
                return None
            await asyncio.sleep(1)
    return None


async def main() -> None:
    product_ids = [123, 456, 789]  # Obtain from sitemap or prior reconnaissance
    results: list[dict] = []

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=10.0,
        follow_redirects=True,
    ) as client:
        for pid in product_ids:
            logger.info("Fetching product %d …", pid)
            data = await fetch_product(client, pid)
            if data:
                results.append(
                    {
                        "id": data.get("id"),
                        "name": data.get("name"),
                        "price": data.get("price"),
                        "in_stock": data.get("in_stock"),
                    }
                )
                logger.info("  ✓ %s", data.get("name"))
            await asyncio.sleep(0.1)  # 10 req/s max

    logger.info("Fetched %d / %d products", len(results), len(product_ids))
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())
