# API Discovery and Usage

## Overview

Many websites expose hidden APIs that are **10-100x faster and more reliable** than scraping HTML.
Always look for APIs via traffic capture before writing scraping code!

## Why APIs are Better Than Scraping

| Aspect | API | HTML Scraping |
|--------|-----|---------------|
| Speed | Fast (JSON responses) | Slow (render full pages) |
| Reliability | Stable structure | Breaks when HTML changes |
| Data Quality | Clean, structured JSON | Messy, requires parsing |
| Bandwidth | Low (only data) | High (images, CSS, JS) |
| Maintenance | Low (stable contracts) | High (fragile selectors) |

---

## How to Find APIs

### Via Proxy-MCP Traffic Capture (Recommended during reconnaissance)

```
proxy_start()
interceptor_chrome_launch("https://target-site.com", stealthMode: true)
interceptor_chrome_devtools_attach(target_id)

# Browse the site with humanizer
humanizer_click(target_id, ".category-link")
humanizer_idle(target_id, 2000)

# Discover APIs in captured traffic
proxy_list_traffic(url_filter: "api")
proxy_list_traffic(url_filter: "/graphql")
proxy_search_traffic(query: "application/json")

# Inspect discovered endpoints
proxy_get_exchange(exchange_id)
```

### What to Look For

Filter traffic for these common API patterns:
```
/api/...          /v1/...          /v2/...
/graphql          /_next/data/...  /wp-json/...
/rest/...         /_api/...        /internal/...
```

---

## Common API Patterns (Python / httpx)

### REST API

```python
import httpx

async with httpx.AsyncClient(
    headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    timeout=10.0,
    follow_redirects=True,
) as client:
    resp = await client.get("https://shop.com/api/products/12345")
    resp.raise_for_status()
    product = resp.json()
    print(product)
```

### GraphQL API

```python
query = """
{
    products(limit: 10) {
        id
        name
        price
        inStock
    }
}
"""

async with httpx.AsyncClient(timeout=10.0) as client:
    resp = await client.post(
        "https://example.com/graphql",
        json={"query": query},
        headers={"Content-Type": "application/json"},
    )
    products = resp.json()["data"]["products"]
```

### Paginated REST API

```python
async def fetch_all_products(client: httpx.AsyncClient, base_url: str) -> list[dict]:
    all_products = []
    page = 1

    while True:
        resp = await client.get(
            f"{base_url}/api/products",
            params={"page": page, "limit": 50},
        )
        resp.raise_for_status()
        body = resp.json()

        all_products.extend(body["products"])

        if not body.get("hasNextPage"):
            break
        page += 1
        await asyncio.sleep(0.05)  # Rate limit

    return all_products
```

---

## Authentication Handling

### Cookies from Browser Session

Extract from proxy-mcp during reconnaissance:
```
interceptor_chrome_devtools_list_cookies()
```

Use in httpx:
```python
cookies = {"session": "abc123", "cf_clearance": "xyz"}
async with httpx.AsyncClient(cookies=cookies) as client:
    resp = await client.get("https://api.example.com/data")
```

### Bearer Token

Extract from localStorage:
```
interceptor_chrome_devtools_get_storage_value("auth_token", storage_type: "local")
```

```python
headers = {"Authorization": f"Bearer {extracted_token}"}
```

### API Key (from captured traffic headers)

Use `proxy_get_exchange(exchange_id)` to inspect headers:
```python
headers = {
    "X-API-Key": "abc123…",
    "X-Client-ID": "web-app",
}
```

---

## Hybrid: Sitemap URLs + API Data

Best of both worlds — use sitemap for URL/ID discovery, API for structured data:

```python
import asyncio
import re
import httpx
from bs4 import BeautifulSoup

async def main() -> None:
    # 1. Get product URLs from sitemap
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        resp = await client.get("https://shop.com/sitemap.xml")
        soup = BeautifulSoup(resp.text, "xml")
        urls = [loc.text.strip() for loc in soup.find_all("loc")]

    # 2. Extract product IDs from URLs
    product_ids = [
        m.group(1)
        for url in urls
        if (m := re.search(r"/products/(\d+)", url))
    ]
    print(f"Found {len(product_ids)} products")

    # 3. Fetch data via API
    async with httpx.AsyncClient(headers={"Accept": "application/json"}, timeout=10.0) as client:
        for pid in product_ids[:50]:
            resp = await client.get(f"https://api.shop.com/v1/products/{pid}")
            if resp.status_code == 200:
                print(resp.json())
            await asyncio.sleep(0.05)

asyncio.run(main())
```

---

## httpx vs curl_cffi

### Use `httpx` (default)

```python
import httpx
async with httpx.AsyncClient(
    headers={"User-Agent": "Mozilla/5.0 …"},
    timeout=10.0,
    follow_redirects=True,
) as client:
    resp = await client.get(url)
```

### Use `curl_cffi` (when TLS fingerprint blocks httpx)

```python
from curl_cffi.requests import AsyncSession

async with AsyncSession(impersonate="chrome131") as session:
    resp = await session.get(url)
    data = resp.json()
```

Available presets: `chrome99`, `chrome110`, `chrome131`, `chrome136`, `firefox133`, `safari17`

---

## Rate Limiting

```python
import asyncio

for pid in product_ids:
    resp = await client.get(f"{api_url}/products/{pid}")
    # 10 req/s
    await asyncio.sleep(0.1)
```

With crawlee-python's built-in rate limiter:
```python
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler

crawler = BeautifulSoupCrawler(max_requests_per_minute=60)
```

---

## Error Handling

```python
async def safe_fetch(client: httpx.AsyncClient, url: str) -> dict | None:
    try:
        resp = await client.get(url, timeout=10.0)
        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            await asyncio.sleep(5)
            resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()

        body = resp.json()
        if body.get("error"):
            raise ValueError(f"API error: {body['error']}")
        return body

    except httpx.HTTPError as exc:
        logger.error("HTTP error %s: %s", url, exc)
        return None
```

---

## Common API Patterns to Look For

```
/_next/data/BUILD_ID/products/123.json    ← Next.js
/wp-json/wp/v2/posts                      ← WordPress
/products.json                            ← Shopify
/api/v1/products                          ← Generic REST
/graphql                                  ← GraphQL
```

---

## Best Practices

### ✅ DO:
- Always check for APIs first via traffic capture before scraping HTML
- Use `httpx` with `follow_redirects=True` and explicit `timeout`
- Copy exact headers from browser session (via `proxy_get_exchange`)
- Handle 429 with exponential backoff
- Use environment variables for credentials — never hardcode
- Type-hint API response dicts

### ❌ DON'T:
- Skip API discovery — always check via traffic capture first
- Ignore rate limits
- Hardcode API keys or credentials
- Trust API responses blindly — validate field existence
- Forget to close `httpx.AsyncClient` (use `async with`)

---

## Related Resources

- **Sitemap discovery**: See `sitemap-discovery.md`
- **Hybrid approach**: See `hybrid-approaches.md`
- **Example**: See `../examples/api-scraper.py`
- **Example**: See `../examples/hybrid-sitemap-api.py`
