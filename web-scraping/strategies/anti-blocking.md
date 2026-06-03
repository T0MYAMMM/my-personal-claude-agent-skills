# Anti-Blocking & Anti-Detection

## Overview

When websites detect automated scraping, they deploy anti-bot measures. This guide covers proxy-mcp's multi-layer anti-detection system for interactive development and Apify's fingerprint-suite for production Actors.

## When You Need Anti-Blocking

### Signs You're Being Blocked

- **403 Forbidden** errors
- **Cloudflare challenges** ("Checking your browser...")
- **Bot detection** messages ("Access Denied", "Unusual traffic")
- **CAPTCHAs** appearing unexpectedly
- **Rate limiting** (429 Too Many Requests)
- **Empty responses** or incomplete data
- **Timeouts** or connection resets
- Pages return different content than a real browser shows

---

## Layer 1: Stealth Browser (Default for All Chrome Sessions)

**Tool**: `interceptor_chrome_launch(url, stealthMode: true)`

**Always use this** when launching Chrome through proxy-mcp. Stealth mode patches browser-level detection vectors:

### What It Patches

| Detection Vector | Patch | Why |
|-----------------|-------|-----|
| `navigator.webdriver` | Set to `false` with `configurable:true` | Primary bot check; `configurable:true` matches real Chrome behavior |
| `chrome.runtime` | Exists with expected shape | Akamai's primary detection — missing `chrome.runtime` = headless Chrome |
| `Permissions.query` | Correct notification response | CDP artifacts cause wrong notification permission state |
| `Error.stack` | Cleaned of CDP traces | Removes `InjectedScript` and `evaluate` from stack traces |

### What It Deliberately Omits

| Chrome Flag | Why Omitted |
|-------------|-------------|
| `--disable-extensions` | Removes `chrome.runtime` entirely — triggers Akamai detection |
| `--mute-audio` | Detectable via AudioContext API |
| `--disable-background-networking` | Changes observable network behavior |

Injected via `Page.addScriptToEvaluateOnNewDocument` — runs before any page script, on every frame.

### When to Use

**Always** when launching Chrome on any site with bot detection. There is no downside to enabling stealth mode.

```
interceptor_chrome_launch("https://target-site.com", stealthMode: true)
```

### How to Verify

Navigate to bot detection test sites:
```
interceptor_chrome_devtools_navigate("https://bot.sannysoft.com/")
interceptor_chrome_devtools_screenshot()
```

All tests should pass with stealth mode enabled.

---

## Layer 2: Behavioral Mimicry (Humanizer)

Use humanizer tools for any interaction with page elements during reconnaissance. Each tool adds built-in anti-detection behavior.

### humanizer_move(target_id, x, y)
- **Behavior**: Cubic Bezier curves with randomized control points
- **Timing**: Fitts's law duration scaling (larger distance = proportionally faster)
- **Realism**: Overshoot + correction for distances >200px

### humanizer_click(target_id, selector)
- **Behavior**: Combines `humanizer_move` to target + click with human-like timing variance
- **Anti-detection**: Random delay before click, natural cursor path

### humanizer_type(target_id, text)
- **Behavior**: WPM-based delays (default 40 WPM)
- **Timing modifiers**: Bigram frequency (common letter pairs 0.8x speed), shift penalty +50ms
- **Realism**: Optional typo injection with QWERTY neighbor key mapping

### humanizer_scroll(target_id, direction, amount)
- **Behavior**: easeInOutQuad acceleration/deceleration curve
- **Anti-detection**: Natural scroll speed variation

### humanizer_idle(target_id, duration_ms)
- **Behavior**: Micro-jitter ±3-8px, occasional micro-scrolls
- **Anti-detection**: Defeats idle detection systems that flag motionless cursors

### When to Use

Any time you interact with page elements during reconnaissance. Use `humanizer_click` instead of direct DOM clicks, `humanizer_type` instead of direct input, etc.

---

## Layer 3: Proxy Rotation / Upstream Proxies

When IP-level blocking is detected (Cloudflare geographic restrictions, IP bans):

### Chain to Upstream Proxy

```
proxy_set_upstream("http://user:pass@proxy.apify.com:8000")
```

This routes all proxy traffic through the upstream proxy, giving you:
- **IP rotation** (different IP per request or session)
- **Geographic targeting** (residential IPs in specific countries)
- **Residential IP addresses** for strict sites

### Per-Host Upstream

Route only specific domains through proxy:

```
proxy_set_host_upstream("target-site.com", "http://user:pass@residential-proxy.com:8000")
```

### Inject Custom Headers

```
proxy_inject_headers({
    "Accept-Language": "en-US,en;q=0.9",
    "X-Forwarded-For": "removed"
})
```

### When to Use

When you're getting IP-based blocks:
- Cloudflare showing geographic challenges
- 403/429 responses that disappear with different IPs
- Site requires residential IP addresses

---

## Layer 4: TLS Fingerprint Spoofing (HTTP-Only Clients — Conditional)

**Tool**: `proxy_set_fingerprint_spoof(preset)`

Uses **impit** (Rust NAPI module) for native TLS impersonation. Spoofs:
- JA3 fingerprint
- HTTP/2 frame ordering
- Auto-normalizes User-Agent + UA Client Hints headers

### Available Presets

| Preset | Use Case |
|--------|----------|
| `chrome_131` | Match Chrome 131 TLS fingerprint |
| `chrome_136` | Match Chrome 136 TLS fingerprint |
| `chrome_136_linux` | Match Chrome 136 on Linux |
| `firefox_133` | Match Firefox 133 TLS fingerprint |
| `okhttp3` | Match OkHttp 3 (Android apps) |
| `okhttp4` | Match OkHttp 4 (Android apps) |
| `okhttp5` | Match OkHttp 5 (Android apps) |

### When to Use

**ONLY** when ALL of these conditions are met:
1. You've discovered an API via traffic interception
2. You want to switch from browser to HTTP-only client (gotScraping, curl, fetch) for faster extraction
3. The target blocks the HTTP client based on TLS fingerprint

```
proxy_set_fingerprint_spoof(preset: "chrome_136")
```

### When NOT to Use

**Do NOT use for Chrome browser sessions**. Chrome already has a legitimate TLS fingerprint — spoofing is unnecessary, incorrect, and may cause issues.

### How to Verify

```
proxy_get_tls_fingerprints()           → Check what fingerprint the server sees
proxy_list_fingerprint_presets()       → List available presets
proxy_check_fingerprint_runtime()     → Verify impit runtime is available
```

---

## Layer 5: Request Manipulation (Surgical)

For specific request-level anti-bot checks:

### Add Interception Rules

```
proxy_add_rule(
    matcher: { urlPattern: "*/bot-check/*" },
    handler: { type: "drop" }
)
```

### Rewrite URLs

```
proxy_rewrite_url("/old-endpoint/", "/new-endpoint/")
```

### Mock Responses

```
proxy_mock_response(
    matcher: { urlPattern: "*/captcha-check" },
    response: { status: 200, body: '{"success": true}' }
)
```

### When to Use

Targeted fixes for specific anti-bot checks discovered during reconnaissance:
- Blocking analytics/tracking requests that slow things down
- Bypassing specific route checks
- Testing with mocked responses

---

## Escalation Strategy

Start simple, add layers only as needed:

```
1. Stealth Browser (Layer 1) — usually sufficient
   └─ Still blocked?
2. Add Humanizer for interactions (Layer 2)
   └─ IP-blocked?
3. Add Upstream Proxies (Layer 3)
   └─ Switching to HTTP-only client and TLS-blocked?
4. Add TLS Spoofing (Layer 4)
   └─ Specific request-level issues?
5. Add Request Rules (Layer 5)
```

**Most sites only need Layers 1-2**. Layer 3 is needed for IP-based blocking. Layer 4 is only for HTTP-only clients. Layer 5 is for surgical fixes.

---

## Production Python: Anti-Detection Stack

For production Python scrapers, use these tools in order of escalation.

### playwright-stealth (Browser fingerprinting)

Install: `pip install playwright-stealth`

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context()
    await stealth_async(context)   # Patches navigator.webdriver and Chrome artifacts
    page = await context.new_page()
    await page.goto("https://target.com")
```

### curl_cffi (TLS fingerprint impersonation for httpx-style requests)

Install: `pip install curl_cffi`

```python
from curl_cffi.requests import AsyncSession

# Impersonate Chrome 131 TLS fingerprint
async with AsyncSession(impersonate="chrome131") as session:
    resp = await session.get("https://target.com/api/products/123")
    data = resp.json()
```

Available presets: `chrome99`, `chrome110`, `chrome131`, `chrome136`, `firefox133`, `safari17`

### crawlee-python session pool

```python
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(
    use_session_pool=True,
    max_concurrency=3,
    max_requests_per_minute=30,
)
```

### Proxy rotation (upstream)

```python
# httpx with proxy
async with httpx.AsyncClient(
    proxies={"http://": "http://user:pass@proxy.provider.com:8000"},
    timeout=10.0,
) as client:
    resp = await client.get(url)

# curl_cffi with proxy
async with AsyncSession(impersonate="chrome131", proxies={"https": "http://user:pass@proxy.provider.com:8000"}) as session:
    resp = await session.get(url)
```

---

## Troubleshooting

### Still Getting Blocked with Stealth Mode?

1. **Check upstream proxy** — IP might be blocked regardless of browser fingerprint
2. **Add humanizer** — site may detect automated click patterns
3. **Try residential proxies** — datacenter IPs are often blacklisted
4. **Check for JavaScript challenges** — some require specific JS execution timing

### Blocked When Switching to HTTP Client?

1. **Enable TLS spoofing** — `proxy_set_fingerprint_spoof(preset: "chrome_136")`
2. **Copy exact headers** from browser session (from `proxy_get_exchange()`)
3. **Include cookies** from browser (`interceptor_chrome_devtools_list_cookies()`)

### Detecting Fingerprint Issues

Test with bot detection sites:
```
interceptor_chrome_devtools_navigate("https://bot.sannysoft.com/")
interceptor_chrome_devtools_screenshot()
```

## Ethical Considerations

**Anti-blocking is a tool, not permission**:

- Use for public data collection
- Respect rate limits (even if you can bypass them)
- Honor robots.txt
- Don't overload servers
- Don't bypass paywalls
- Don't scrape private data
- Don't violate terms of service

## Related

- **Fingerprint patterns**: See `../reference/fingerprint-patterns.md`
- **Proxy-MCP tool reference**: See `../reference/proxy-tool-reference.md`
- **Traffic interception**: See `traffic-interception.md`
- **Session workflows**: See `session-workflows.md`

## Summary

**Multi-layer anti-detection for different contexts**:

| Context | Primary Tool | Layers |
|---------|-------------|--------|
| **Interactive development** | proxy-mcp | Stealth mode → Humanizer → Upstream proxies → TLS spoofing |
| **Production Python** | playwright-stealth + curl_cffi | Browser patch → TLS impersonation → Proxy rotation → Session pool |

**Key rules**:
1. Stealth mode for all Chrome sessions (Layer 1)
2. Humanizer for all interactions (Layer 2)
3. Upstream proxies for IP blocking (Layer 3)
4. TLS spoofing ONLY for HTTP-only clients when TLS-blocked (Layer 4)
5. **Never** use TLS spoofing for Chrome browser sessions
