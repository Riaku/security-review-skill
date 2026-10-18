# Redirect Chain & Status Hygiene

**MUST NOT** chain redirects (>1 hop) on indexable URLs, and MUST serve 410/404 (not soft-404) for removed content.

**Why:** Chains waste crawl budget, slow users, and break link equity; soft-404s (200 on missing pages) pollute the index and mask real removals.

**Detect:** crawl and flag redirect_count > 1; check removed-content routes return 200 with "not found" body (soft-404) via Search Console coverage report.

**References:** Google Search Central redirect docs, RFC 7231 status semantics, soft-404 guidance

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
