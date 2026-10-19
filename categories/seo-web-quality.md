# seo-web-quality

Search visibility, crawl/index hygiene, and page experience (Google Search Central, CWV, Lighthouse).

## What this category covers

This category covers whether a site can be discovered, crawled, and indexed correctly, and whether its pages meet the rendering and performance expectations search engines measure. Its member items span crawl directives and sitemaps, canonical and redirect handling, index-bloat control, hreflang and structured data, meta/OG tag completeness, Core Web Vitals and Lighthouse budgets, image serving, crawler-renderable content, and Google Search Central policy compliance. A reviewer here should check the site as both a crawler and a real user see it, and confirm that indexability, canonicalization, and page-experience budgets are deliberate rather than accidental. Findings are usually a page that should not be indexed but is, or one that is indexable but crawls badly: a canonical pointing elsewhere, a redirect chain, or a client-rendered page Googlebot cannot see.

- Crawl and index governance: robots.txt, noindex/X-Robots-Tag, sitemaps, faceted-URL control.
- Canonicalization and redirect/status hygiene.
- Rendering for crawlers: SSR/prerender equivalence with the user-facing DOM.
- Page experience: Core Web Vitals budgets and Lighthouse CI assertions.
- Structured data, meta/OG tags, hreflang, and image serving.

## What it does not cover

- [web-client-security](../categories/web-client-security.md) — access control, header security, and cache directives belong there; robots.txt is crawl-traffic control and never a substitute for them.
- [observability](../categories/observability.md) — runtime SLOs, metrics, and alerting belong there; build-time page-quality budgets belong here.
- [deployment-release](../categories/deployment-release.md) — which gates a release must pass belongs there; what the page-quality budget asserts belongs here.

## What a finding here looks like

- a staging site reachable without `noindex`, so staging pages rank in production results.
- an indexable URL that 301s through a second hop before resolving.
- a client-rendered page whose HTML arrives empty, so Googlebot indexes a blank shell.
- LCP at the 75th percentile well above the 2.5s budget with no gate to catch it.
- a faceted filter combination generating thousands of indexable near-duplicate URLs.
