# Web Scraping Skill

Intelligent web scraping with automatic strategy selection and Python-first production deployment.

## Overview

This skill provides:
- **Adaptive reconnaissance** — Phases 0-5 with quality gates (curl first, browser only if needed)
- **Framework-aware detection** — Identifies site framework before searching, skips irrelevant patterns
- **Validated findings** — Every claimed selector/path/API is tested before reporting
- **Self-critiquing reports** — Intelligence reports include gap analysis and staleness warnings
- **Iterative implementation** — Starts simple, adds complexity only if needed
- **Production-ready guidance** — Python packaging, Docker, GCP Cloud Run / Google Batch

## Stack

| Layer | Tool |
|---|---|
| HTTP scraping | `httpx` (async); `curl_cffi` for TLS impersonation |
| HTML parsing | `BeautifulSoup4` |
| Managed crawler | `crawlee-python` (`BeautifulSoupCrawler` / `PlaywrightCrawler`) |
| Browser automation | `playwright-python` |
| Anti-detection | `playwright-stealth`, `curl_cffi` presets |
| Traffic interception | proxy-mcp MITM tools (reconnaissance only) |
| Deployment | Docker + GCP Cloud Run / Google Batch |
| Language | Python 3.11+ |

**Crawlee**: Both `crawlee-python` (production) and Crawlee JS/TS (learning reference) are valid.
The Python port is recommended for new production code; JS Crawlee is mature and well-documented for learning patterns.

## Quick Start

### Scenario 1: Scrape a Website

```
User: "Scrape https://example.com"

Claude will automatically:
1. Phase 0: curl raw HTML — detect framework, search for data points, check sitemaps
2. QUALITY GATE: All data in HTML? → Skip browser, go to validation
3. Phase 1: Stealth browser loads page, traffic reveals API endpoint (only if needed)
4. Phase 2: Deep scan for missing data — targeted interactions, API sniffing
5. Phase 3: Validate every finding — test selectors, replay APIs, confirm JSON paths
6. Phase 4: Protection testing (only if 403/bot signals detected)
7. Phase 5: Intelligence report with self-critique
8. Implement in Python iteratively (httpx → crawlee-python → playwright-python)
9. Test with small batch, then scale
```

### Scenario 2: Productionize

```
User: "Productionize this scraper" / "Deploy to Cloud Run"

Claude will:
1. Package as Dockerfile (Python 3.11 slim + Playwright Chromium)
2. Guide Click CLI entry point
3. Choose: Cloud Run (HTTP/cron) vs Google Batch (parallel jobs)
4. Wire GCS output and Secret Manager credentials
5. Write cloudbuild.yaml
6. Test locally via Docker
```

## Directory Structure

```
web-scraping/
├── SKILL.md                    # Main entry point (proactive workflow)
├── workflows/
│   ├── reconnaissance.md       # Phase 1 interactive reconnaissance (CRITICAL)
│   ├── implementation.md       # Iterative Python implementation patterns
│   └── productionization.md    # GCP Cloud Run / Google Batch workflow
├── strategies/
│   ├── framework-signatures.md # Framework detection lookup tables
│   ├── httpx-vs-browser-test.md # httpx vs Browser decision + early exit
│   ├── proxy-escalation.md    # Protection testing skip/run conditions
│   ├── traffic-interception.md # MITM proxy traffic capture
│   ├── sitemap-discovery.md   # Sitemap patterns (Python)
│   ├── api-discovery.md       # Finding and using APIs (httpx)
│   ├── dom-scraping.md        # playwright-python + DevTools bridge
│   ├── httpx-scraping.md      # HTTP-only scraping (httpx + BS4 / crawlee-python)
│   ├── hybrid-approaches.md   # Combining strategies
│   ├── anti-blocking.md       # playwright-stealth + curl_cffi + proxies
│   └── session-workflows.md   # Session recording, HAR, replay
├── examples/
│   ├── playwright-scraper.py  # Browser + traffic interception
│   ├── sitemap-basic.py       # Sitemap scraper (crawlee-python)
│   ├── api-scraper.py         # Pure API approach (httpx)
│   ├── hybrid-sitemap-api.py  # Combined approach
│   └── iterative-fallback.py  # Tries API → BS4 → Playwright → crawl
└── reference/
    ├── report-schema.md       # Intelligence report format (Sections 1-7)
    ├── proxy-tool-reference.md # Proxy-MCP tools (80+)
    ├── regex-patterns.md
    ├── fingerprint-patterns.md
    └── anti-patterns.md
```

## Performance Reference

| Approach | Time (1000 pages) | vs Crawling |
|----------|-------------------|-------------|
| Sitemap + API (httpx) | 5 minutes | 60x faster |
| Sitemap + BeautifulSoup4 | 10 minutes | 30x faster |
| Sitemap + PlaywrightCrawler | 20 minutes | 15x faster |
| Playwright crawl (fallback) | 45 minutes | Baseline |

## Core Philosophy

**Intelligence first, implementation second.**

Priority order:
1. **Traffic interception** — find the API before writing any code
2. **Sitemaps** — instant URL discovery (60x faster than crawling)
3. **API** — structured data (10-100x less bandwidth)
4. **httpx + BeautifulSoup4** — fast HTTP-only scraping for static HTML
5. **Playwright** — full browser only when JavaScript rendering is required

## Version

**6.0.0** — Python-first rewrite:
- **CHANGED**: Stack migrated from TypeScript/Apify to Python (`httpx`, `playwright-python`, `crawlee-python`)
- **CHANGED**: Productionization targets GCP Cloud Run / Google Batch (was Apify)
- **CHANGED**: Anti-detection uses `playwright-stealth` + `curl_cffi` (was Apify fingerprint-suite)
- **KEPT**: All reconnaissance phases (0-5), proxy-mcp tools, adaptive quality gates
- **KEPT**: Crawlee patterns — now via `crawlee-python` with JS Crawlee as learning reference
