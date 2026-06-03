# Hybrid Scraping Approaches

Combine multiple strategies for optimal speed, reliability, and data quality.

## Common Hybrid Patterns

### Pattern 1: Sitemap + API (Best Performance)

**Use case**: Site has sitemap + internal API (discovered via traffic capture)

**Advantages**:
- Instant URL discovery (sitemap)
- Clean structured data (API)
- 60x faster than crawling + scraping

```python
import asyncio
import re
import httpx
from bs4 import BeautifulSoup

async def main() -> None:
    # 1. Discover URLs from sitemap
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        resp = await client.get("https://shop.com/sitemap.xml")
        soup = BeautifulSoup(resp.text, "xml")
        urls = [loc.text.strip() for loc in soup.find_all("loc")]

    # 2. Extract IDs
    product_ids = [
        m.group(1) for url in urls
        if (m := re.search(r"/products/(\d+)", url))
    ]
    print(f"Found {len(product_ids)} products")

    # 3. Fetch via API (clean JSON — 100x less bandwidth)
    async with httpx.AsyncClient(headers={"Accept": "application/json"}, timeout=10.0) as client:
        for pid in product_ids:
            resp = await client.get(f"https://api.shop.com/v1/products/{pid}")
            if resp.status_code == 200:
                print(resp.json())
            await asyncio.sleep(0.05)

asyncio.run(main())
```

**Performance**: ~5 min for 1000 products

---

### Pattern 2: Sitemap + DOM Scraping (Playwright)

**Use case**: Site has sitemap but no API; content is JS-rendered

```python
import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    # Get URLs from sitemap (see sitemap-discovery.md)
    urls = await get_sitemap_urls("https://example.com")

    crawler = PlaywrightCrawler(max_concurrency=5)

    @crawler.router.default_handler
    async def handler(ctx: PlaywrightCrawlingContext) -> None:
        page = ctx.page
        data = {
            "url": ctx.request.url,
            "title": await page.text_content("h1"),
            "price": await page.text_content(".price"),
        }
        await ctx.push_data(data)

    await crawler.run(urls[:10])  # Test first

asyncio.run(main())
```

**Performance**: ~20 min for 1000 pages

---

### Pattern 3: Iterative Fallback

**Use case**: Unknown site — try fastest first, fallback automatically

**Fallback chain**: Traffic Interception → Sitemap + API → Sitemap + BS4 → Playwright

See `../examples/iterative-fallback.py` for complete implementation.

---

### Pattern 4: API + Playwright Fallback

**Use case**: API for most data, Playwright for specific complex fields

```python
import asyncio
import httpx
from playwright.async_api import async_playwright

async def scrape_product(product_id: str) -> dict:
    # 1. Core data from API (fast)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"https://api.shop.com/products/{product_id}")
        api_data = resp.json()

    # 2. Dynamic content (e.g., reviews) via Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://shop.com/products/{product_id}")
        await page.wait_for_selector(".review", timeout=5000)

        reviews = await page.evaluate("""
            () => Array.from(document.querySelectorAll(".review")).map(el => ({
                rating: el.querySelector(".rating")?.textContent,
                text: el.querySelector(".text")?.textContent,
            }))
        """)
        await browser.close()

    return {**api_data, "reviews": reviews}

asyncio.run(scrape_product("123"))
```

---

### Pattern 5: httpx + Playwright Hybrid

**Use case**: Most pages static, some JS-rendered

```python
import asyncio
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def scrape_url(url: str) -> dict | None:
    # Try httpx first (fast)
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.select_one("h1")
        if title:
            # Static page — no browser needed
            return {"url": url, "title": title.get_text(strip=True)}

    # Content missing — fall back to Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        title = await page.text_content("h1")
        await browser.close()
        return {"url": url, "title": title}
```

---

## Decision Matrix

| Scenario | Best Approach | Speed | Data Quality |
|----------|---------------|-------|--------------|
| API found via traffic capture | Traffic Interception + API (httpx) | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| Sitemap + API exist | Sitemap + API (httpx) | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| Sitemap + Static HTML | Sitemap + BeautifulSoup4 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| Sitemap + JS-rendered | Sitemap + PlaywrightCrawler | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| No sitemap + API | API Discovery (httpx) | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| Unknown site | Iterative Fallback | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| Mixed static/dynamic | httpx + Playwright | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |

---

## Best Practices

### ✅ DO:
- Start with the simplest approach (sitemap/API via httpx)
- Fall back to more complex methods only if needed
- Test small batch first (5-10 items)
- Log which method succeeded for debugging
- Use `crawlee-python` crawlers for managed crawls (retries, concurrency, storage)

### ❌ DON'T:
- Use Playwright if httpx + BeautifulSoup4 works (10x resource overhead)
- Skip API discovery — always check via traffic capture first
- Forget fallback strategies — sites change
- Mix approaches without systematic testing

---

## Related Resources

- **Traffic interception**: See `traffic-interception.md`
- **Sitemap**: See `sitemap-discovery.md`
- **API**: See `api-discovery.md`
- **DOM scraping**: See `dom-scraping.md`
- **httpx scraping**: See `httpx-scraping.md`
- **Examples**: See `../examples/hybrid-sitemap-api.py`
- **Examples**: See `../examples/iterative-fallback.py`
