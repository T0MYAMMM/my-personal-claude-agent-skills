# Phase 3: Iterative Implementation

Patterns for implementing Python scrapers incrementally — start simple, add complexity only as needed.

## Step 1: Implement Recommended Approach

### Progressive Enhancement Pattern

1. Start with minimal working code
2. Test with small sample (5-10 items)
3. Validate data quality
4. Scale to full dataset

### Reference Implementation Patterns

- **Traffic interception**: See `../strategies/traffic-interception.md`
- **Sitemap**: See `../strategies/sitemap-discovery.md`
- **API**: See `../strategies/api-discovery.md`
- **DOM scraping**: See `../strategies/dom-scraping.md`
- **Examples**: See `../examples/` directory

---

## Step 2: Test Small Batch First

```python
import asyncio
from my_scraper import get_sitemap_urls, scrape_products

async def main() -> None:
    urls = await get_sitemap_urls("https://example.com")
    test_urls = urls[:10]

    print(f"Testing with {len(test_urls)} URLs first …")
    results = await scrape_products(test_urls)

    # Validate output quality
    assert all("title" in r for r in results), "Missing title field"
    assert all("price" in r for r in results), "Missing price field"
    print(f"✓ {len(results)} items scraped, data looks good")

asyncio.run(main())
```

### Validation Checklist

- ✓ Data structure correct?
- ✓ All fields populated (no None where values expected)?
- ✓ Encoding correct (no garbled UTF-8)?
- ✓ Performance acceptable (time per page)?

---

## Step 3: Scale or Fallback

### If Test Succeeds

```python
# Scale to full dataset — pass all URLs
results = await scrape_products(all_urls)
print(f"✓ Completed: {len(results)} products")
```

### If Test Fails

```python
# Diagnose before scaling
# → Check if content is JS-rendered (upgrade to Playwright)
# → Check if selector changed (re-validate)
# → Check if rate-limited (add delay)
print("Issues detected — inspect first 3 failures before scaling")
```

---

## Step 4: Handle Blocking (If Encountered)

### Identify Blocking Type

- **Rate limiting** → Slow down requests (`asyncio.sleep()`, `max_requests_per_minute`)
- **IP blocking** → Use a proxy
- **Bot detection** → Add stealth browser (`playwright-stealth`), randomise headers
- **Cloudflare/CAPTCHA** → Stealth + residential proxy (see `../strategies/anti-blocking.md`)

### Apply Anti-Blocking (Python)

```python
# Slow down with httpx
await asyncio.sleep(0.1)   # 10 req/s max

# Randomise User-Agent
import random
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0.0.0",
]
headers["User-Agent"] = random.choice(user_agents)

# TLS fingerprint spoofing with curl_cffi (when httpx is blocked)
from curl_cffi.requests import AsyncSession
async with AsyncSession(impersonate="chrome131") as session:
    resp = await session.get(url)

# crawlee-python — built-in rate limiting and session pool
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(
    max_concurrency=3,
    max_requests_per_minute=30,
    use_session_pool=True,
)
```

**During reconnaissance** (proxy-mcp):
```
# Stealth mode handles most browser-level detection
interceptor_chrome_launch(url, stealthMode: true)

# Add humanizer for behavioral anti-detection
humanizer_click(target_id, selector)
humanizer_idle(target_id, duration_ms)
```

### Escalation Order

1. Add `asyncio.sleep` delays
2. Randomise User-Agent + Accept headers
3. Add `playwright-stealth` for browser sessions
4. Switch from `httpx` to `curl_cffi` for TLS impersonation
5. Add upstream proxy (datacenter → residential)

---

## Step 5: Add Robustness

### Error Handling with httpx

```python
import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)

async def fetch_with_retry(
    client: httpx.AsyncClient, url: str, retries: int = 3
) -> dict | None:
    for attempt in range(retries):
        try:
            resp = await client.get(url)
            if resp.status_code == 429:
                wait = 5 * (attempt + 1)
                logger.warning("Rate limited on %s — waiting %ds", url, wait)
                await asyncio.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            logger.error("Request failed [%d/%d] %s: %s", attempt + 1, retries, url, exc)
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)
    return None
```

### Error Handling with crawlee-python

```python
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

crawler = BeautifulSoupCrawler(
    max_request_retries=3,
    request_handler_timeout=60,
)

@crawler.router.default_handler
async def handler(context: BeautifulSoupCrawlingContext) -> None:
    try:
        title = context.soup.select_one("h1").get_text(strip=True)
        await context.push_data({"url": context.request.url, "title": title})
    except Exception as exc:
        context.log.error("Failed %s: %s", context.request.url, exc)
        raise  # Triggers built-in retry
```

### Enhancements Checklist

- [ ] Retries with exponential backoff
- [ ] Progress logging (`logging`, not `print`)
- [ ] Data validation (assert expected fields exist)
- [ ] Rate limiting (delays or `max_requests_per_minute`)
- [ ] Graceful handling of 404/429/503 status codes
- [ ] Output persistence (GCS, local file, database)

---

Back to main workflow: `../SKILL.md`
