# XML Sitemap Maintenance

**SHOULD** auto-generate sitemap.xml containing only canonical, indexable, non-noindex URLs, with accurate lastmod, and ping/submit on deploy.

**Why:** A stale sitemap (listing removed, noindex, or redirected URLs) wastes crawl budget and delays discovery of real content.

**Detect:** validate sitemap against URL statuses (all 200 + indexable); check lastmod reflects real changes; confirm robots.txt references the sitemap.

**References:** Google Search Central sitemap docs, sitemap.org protocol

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
