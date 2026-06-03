# httpx vs Browser Decision Test

Determine whether a site needs a full browser (Playwright) or can be scraped with
HTTP-only tools (`httpx` + `BeautifulSoup4` / `crawlee-python BeautifulSoupCrawler`).

## Quick Decision

**Use httpx (HTTP-only)** when raw HTML contains all target data points.  
**Use Browser** when data is rendered by JavaScript after page load.

---

## Early Exit: Raw HTML Assessment

Before launching a browser, check if raw HTML is sufficient.

### Phase 0 Check (curl-based)

```bash
curl -s -L "https://target.com/page" | head -500
```

Search the raw HTML for each data point the user wants:

| Data Point | Search Method | Found? |
|-----------|---------------|--------|
| Product name | Search for known product name text | YES/NO |
| Price | Search for price pattern (`Rp`, `$XX`, etc.) | YES/NO |
| Description | Search for first 20 chars of description | YES/NO |

**Early exit rule**: If **all** data points are found in raw HTML → **skip browser entirely**.  
Proceed to selector validation (below), then go to Phase 3.

**Continue to browser** if raw HTML finds **less than 50%** of data points, or critical ones are missing.

**Edge case**: If raw HTML has *some* data points (50-99%), note which are missing and launch browser only to find those.

---

## Three-Way Test (when browser is needed)

Compare data availability across three sources:

### Source 1: Raw HTML (curl / httpx)
```bash
curl -s "https://target.com/page" > raw.html
```
- Parse with text search or regex
- Fastest, lowest resource usage
- What `httpx + BeautifulSoup4` will see

### Source 2: Rendered DOM (browser)
```
interceptor_chrome_devtools_snapshot()
```
- Accessibility tree after JavaScript execution
- What `playwright-python` will see

### Source 3: Network Traffic (API)
```
proxy_list_traffic(url_filter: "api")
proxy_search_traffic(query: "application/json")
```
- JSON data from API calls
- Often the cleanest source
- May contain data not visible in DOM

### Comparison Matrix

| Data Point | Raw HTML | Rendered DOM | API Response | Best Source |
|-----------|----------|-------------|--------------|-------------|
| Title | YES | YES | YES | Raw HTML (simplest) |
| Price | NO | YES | NO | Rendered DOM |
| Reviews | NO | NO | YES | API |

**Decision**: Use the simplest source that covers each data point.

---

## Post-Decision Validation

**Critical rule**: Finding text in HTML is NOT enough. A data point is only "found" when the extraction path is specified AND tested.

### For httpx + BeautifulSoup4 (CSS selectors):

1. **Identify selector**: Find the CSS selector that targets the data
2. **Verify uniqueness**: Confirm it matches exactly one element (or expected count)
3. **Test extraction**: Confirm it returns the correct text/attribute value

```
Data point: Product name
Selector: h1.product-title
Verified: YES — soup.select_one("h1.product-title").get_text() = expected name

Data point: Price
Selector: span.price
Verified: PARTIAL — found in rendered DOM only, not raw HTML
Action: Requires Playwright, not httpx
```

### For inline JSON (`__NEXT_DATA__`, `__NUXT__`):

```python
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
script = soup.select_one("script#__NEXT_DATA__")
data = json.loads(script.string)

# Verify path resolves:
product = data["props"]["pageProps"]["product"]
assert product["name"] == "Expected Product Name"
```

### For API endpoints:

1. **Replay request**: Make the same call with `httpx`
2. **Verify response**: Confirm expected data structure
3. **Test pagination**: At least page 1 and page 2

---

## Decision Output

After testing, produce a clear recommendation:

```
HTTPX VIABLE: YES / NO / PARTIAL

Data points via httpx + BS4 (raw HTML):
  - Product name: h1.product-title ✓ validated
  - Description: .product-desc ✓ validated

Data points requiring Playwright:
  - Price: .price-box (JS-rendered)
  - Stock: .availability (JS-rendered)

Data points via API:
  - Reviews: GET /api/reviews?product_id={id} ✓ validated

RECOMMENDATION: Hybrid — httpx for name/description, API for reviews,
Playwright only if price/stock needed from rendered DOM.
```

---

## Common Pitfalls

### "Found in HTML" doesn't mean "extractable with httpx"
- Text may be inside a `<script>` tag (JSON, not a DOM element) → use JSON extraction
- Text may be in an HTML comment
- Text may be split across multiple elements
- Always verify with an actual CSS selector

### Generated class names (React/Vue/Angular)
- Class names like `.css-1a2b3c` change on every build
- Prefer `data-*` attributes: `[data-testid="price"]`
- Prefer structural selectors over generated class names

### Partial SSR
- Some sites render a skeleton in SSR, hydrate with JS on load
- Price might show as `Rp 0` or `--` in raw HTML but correct after hydration
- Always compare raw HTML values against rendered DOM values
