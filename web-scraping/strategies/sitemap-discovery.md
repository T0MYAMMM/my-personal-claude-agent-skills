# Sitemap-Based URL Discovery

## Overview

Sitemaps are XML files that list all URLs on a website — the fastest way to discover pages.
Instead of crawling page-by-page, you get all URLs in seconds.

## When to Use Sitemaps

### ✅ USE when:
- Website has a sitemap (check `/sitemap.xml` or `robots.txt`)
- Large websites with 100+ pages
- Product catalogs, blogs, news sites
- Need complete site coverage
- E-commerce sites (products, categories)
- Time-sensitive scraping (need fast results)

### ❌ DON'T use when:
- Site has no sitemap
- Single-page applications with dynamic content
- Need to follow user flows (login, cart)
- Sitemap is outdated or incomplete

## Finding Sitemaps

```
https://example.com/sitemap.xml              ← Most common
https://example.com/robots.txt               ← Lists sitemap URLs
https://example.com/sitemap_index.xml        ← Sitemap of sitemaps
https://example.com/product-sitemap.xml      ← Product-specific
https://example.com/sitemap.xml.gz           ← Compressed
```

### Always check robots.txt first

```bash
curl https://example.com/robots.txt
```

---

## Implementation Patterns

### Pattern 1: stdlib (robots.txt → sitemap XML)

Simple, zero extra dependencies:

```python
import asyncio
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

async def get_sitemap_urls(base_url: str) -> list[str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        # 1. Parse robots.txt
        resp = await client.get(f"{base_url}/robots.txt")
        rp = RobotFileParser()
        rp.parse(resp.text.splitlines())
        sitemap_url = rp.site_maps()[0] if rp.site_maps() else f"{base_url}/sitemap.xml"

        # 2. Fetch sitemap XML
        resp = await client.get(sitemap_url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "xml")      # requires lxml
    return [loc.text.strip() for loc in soup.find_all("loc")]
```

### Pattern 2: Filter URLs with regex

```python
import re

all_urls = await get_sitemap_urls("https://shop.com")

# Only product pages
product_urls = [u for u in all_urls if re.search(r"/products/[a-z0-9-]+$", u, re.I)]

# Blog posts with date pattern
blog_urls = [u for u in all_urls if re.search(r"/blog/\d{4}/\d{2}/", u)]

# Exclude category/help pages
product_urls = [u for u in all_urls if re.search(r"/products/[^/]+$", u)]
```

See `../reference/regex-patterns.md` for more patterns.

### Pattern 3: Sitemap index (nested sitemaps)

```python
async def get_all_urls_from_index(index_url: str) -> list[str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        resp = await client.get(index_url)
        soup = BeautifulSoup(resp.text, "xml")

        # Sitemap index lists child sitemaps
        child_sitemaps = [loc.text.strip() for loc in soup.find_all("loc")]

        all_urls = []
        for sm_url in child_sitemaps:
            sm_resp = await client.get(sm_url)
            sm_soup = BeautifulSoup(sm_resp.text, "xml")
            all_urls.extend(loc.text.strip() for loc in sm_soup.find_all("loc"))

    return all_urls
```

### Pattern 4: crawlee-python (managed crawler + sitemap)

crawlee-python handles sitemaps with `enqueue_links` or by passing sitemap URLs directly:

```python
import asyncio
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

async def main() -> None:
    urls = await get_sitemap_urls("https://example.com")
    product_urls = [u for u in urls if "/products/" in u]

    crawler = BeautifulSoupCrawler(
        max_concurrency=10,
        max_requests_per_minute=60,
    )

    @crawler.router.default_handler
    async def handler(ctx: BeautifulSoupCrawlingContext) -> None:
        data = {
            "url": ctx.request.url,
            "title": ctx.soup.select_one("h1").get_text(strip=True) if ctx.soup.select_one("h1") else None,
            "price": ctx.soup.select_one(".price").get_text(strip=True) if ctx.soup.select_one(".price") else None,
        }
        await ctx.push_data(data)

    await crawler.run(product_urls[:10])  # Test with 10 first

asyncio.run(main())
```

---

## URL Filtering by lastmod Date

```python
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

async def get_recent_urls(sitemap_url: str, days: int = 30) -> list[str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        resp = await client.get(sitemap_url)
    soup = BeautifulSoup(resp.text, "xml")

    cutoff = datetime.utcnow() - timedelta(days=days)
    urls = []
    for url_el in soup.find_all("url"):
        lastmod_el = url_el.find("lastmod")
        if lastmod_el:
            lastmod = datetime.fromisoformat(lastmod_el.text[:10])
            if lastmod >= cutoff:
                urls.append(url_el.find("loc").text.strip())
    return urls
```

---

## Error Handling

```python
async def safe_get_sitemap_urls(base_url: str) -> list[str]:
    try:
        urls = await get_sitemap_urls(base_url)
        if not urls:
            print("No URLs found in sitemap — falling back to crawling")
            return []
        print(f"Found {len(urls)} URLs")
        return urls
    except Exception as exc:
        print(f"Sitemap discovery failed: {exc} — falling back to crawling")
        return []
```

---

## Best Practices

### ✅ DO:
- Check `robots.txt` first for sitemap locations
- Filter URLs with regex to get only relevant page types
- Verify sitemap is current (check `lastmod` dates)
- Test with 5-10 URLs before running full scrape
- Handle sitemap indexes (nested sitemaps)
- Log progress clearly

### ❌ DON'T:
- Assume all sites have sitemaps — always have a fallback
- Trust sitemaps to be complete — some pages may be missing
- Ignore robots.txt crawl-delay
- Skip error handling — some sitemap URLs may be broken

---

## Performance Comparison

| Metric | Sitemap | Traditional Crawling |
|--------|---------|----------------------|
| URL Discovery | 5-10 seconds | 5-10 minutes |
| Bandwidth | ~2 MB | ~200 MB |
| Coverage | 100% (if current) | 80-90% |
| Time to first data | 10-20 seconds | 5-10 minutes |

---

## Validating Sitemap with Traffic Capture

After discovering a sitemap, validate its coverage against API pagination metadata:

```
proxy_list_traffic(url_filter: "products")
proxy_get_exchange(exchange_id)   → Check "total" field in API response
```

If the API reports 5,000 products but the sitemap has 3,000, use the API for full coverage.

---

## Related Resources

- **Traffic interception**: See `traffic-interception.md`
- **Regex patterns**: See `../reference/regex-patterns.md`
- **Hybrid approaches**: See `hybrid-approaches.md`
- **API discovery**: See `api-discovery.md`
- **Example**: See `../examples/sitemap-basic.py`
