# HTTP-Only Scraping with httpx + BeautifulSoup4

## Overview

HTTP-only scraping avoids launching a browser by fetching raw HTML with `httpx` and parsing it with `BeautifulSoup4`. **crawlee-python's `BeautifulSoupCrawler`** wraps this into a managed crawler with retries, concurrency, and storage built in.

## When to Use HTTP-Only (No Browser)

### ✅ USE when:
- Website serves static HTML (server-side rendered)
- No JavaScript execution needed
- High-volume scraping (5-10x faster than Playwright)
- Low memory requirements
- API doesn't exist but HTML is simple enough to parse

### ❌ DON'T use when:
- Site requires JavaScript (React, Vue, Angular SPA)
- Content loads dynamically via AJAX after page load
- Need to interact with the page (clicks, forms, scroll)
- `__NEXT_DATA__` or similar inline JSON contains the data — use JSON extraction instead (see `api-discovery.md`)

---

## Option A: crawlee-python BeautifulSoupCrawler (Recommended)

Best for managed crawls — handles retries, concurrency, queue, and storage.

```python
import asyncio
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

async def main() -> None:
    crawler = BeautifulSoupCrawler(
        max_concurrency=10,
        max_requests_per_minute=60,
        max_request_retries=3,
    )

    @crawler.router.default_handler
    async def handler(context: BeautifulSoupCrawlingContext) -> None:
        soup = context.soup
        data = {
            "url": context.request.url,
            "title": soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else None,
            "price": soup.select_one(".price").get_text(strip=True) if soup.select_one(".price") else None,
        }
        await context.push_data(data)
        context.log.info("Scraped: %s", context.request.url)

    await crawler.run(["https://example.com"])

asyncio.run(main())
```

### Enqueue links (crawling)

```python
@crawler.router.default_handler
async def handler(context: BeautifulSoupCrawlingContext) -> None:
    # Scrape current page
    await context.push_data({"title": context.soup.select_one("h1").get_text(strip=True)})
    # Follow product links on the same domain
    await context.enqueue_links(selector="a.product-link", strategy="same-domain")
```

---

## Option B: httpx + BeautifulSoup4 (Simple / Custom)

Best for simple scripts, API pipelines, or when you want full control.

```python
import asyncio
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

async def scrape_page(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    return {
        "url": url,
        "title": soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else None,
        "price": soup.select_one(".price").get_text(strip=True) if soup.select_one(".price") else None,
        "description": soup.select_one(".description").get_text(strip=True) if soup.select_one(".description") else None,
    }

async def main() -> None:
    urls = ["https://example.com/products/1", "https://example.com/products/2"]
    async with httpx.AsyncClient(headers=HEADERS, timeout=10.0, follow_redirects=True) as client:
        for url in urls:
            data = await scrape_page(client, url)
            print(data)
            await asyncio.sleep(0.1)  # Rate limiting

asyncio.run(main())
```

---

## CSS Selector Patterns (BeautifulSoup4)

```python
# Basic selectors
soup.select_one("h1")                          # Tag
soup.select_one(".price")                      # Class
soup.select_one("#product-id")                 # ID
soup.select_one("div.product")                 # Tag + class
soup.select_one("a[href]")                     # Attribute exists
soup.select_one('[data-testid="price"]')        # data-* attribute

# Hierarchy
soup.select("div > p")                         # Direct children
soup.select("div .price")                      # Descendants

# Multiple elements
for el in soup.select(".product-item"):
    name = el.select_one(".name").get_text(strip=True)
    price = el.select_one(".price").get_text(strip=True)

# Extraction
el.get_text(strip=True)                        # Text content
el.get("src")                                  # Attribute value
el.decode_contents()                           # Inner HTML
```

---

## Common Patterns

### Extract a list of items

```python
@crawler.router.default_handler
async def handler(context: BeautifulSoupCrawlingContext) -> None:
    products = []
    for el in context.soup.select(".product-item"):
        products.append({
            "name": el.select_one(".name").get_text(strip=True),
            "price": el.select_one(".price").get_text(strip=True),
            "url": el.select_one("a").get("href"),
            "image": el.select_one("img").get("src"),
        })
    await context.push_data(products)
```

### Extract inline JSON (`__NEXT_DATA__`, `__INITIAL_STATE__`)

```python
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
script = soup.select_one("script#__NEXT_DATA__")
if script:
    data = json.loads(script.string)
    product = data["props"]["pageProps"]["product"]
```

---

## Performance vs Playwright

| Metric | httpx + BS4 | Playwright |
|--------|-------------|------------|
| Speed (1000 pages) | 5-10 min | 30-60 min |
| Memory | ~50 MB | ~500 MB |
| CPU | Low | High |
| Concurrency | 30-50 parallel | 5-10 |

---

## When to Upgrade to Playwright

Switch if you observe:
- Empty elements (content loads via JavaScript)
- Infinite scroll / "Load More" buttons
- React/Vue/Angular indicators (`__NEXT_DATA__`, `ng-app`)
- Content appears after a delay

## TLS Fingerprint Issues (curl_cffi)

If the server rejects httpx based on TLS fingerprint, swap to `curl_cffi`:

```python
from curl_cffi.requests import AsyncSession

async with AsyncSession(impersonate="chrome131") as session:
    resp = await session.get("https://target.com/api/products/123")
    data = resp.json()
```

See `anti-blocking.md` for full TLS escalation guide.

## Related

- **Decision guide**: `httpx-vs-browser-test.md`
- **When API is better**: `api-discovery.md`
- **Playwright (JS sites)**: `dom-scraping.md`
- **Example**: `../examples/sitemap-basic.py`
