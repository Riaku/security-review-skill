# Index Bloat & Faceted-URL Control

**SHOULD NOT** allow faceted navigation, session IDs, sort/filter params, and internal search results to be indexed at scale.

**Why:** Millions of low-value param URLs explode the index, bury the pages that matter, and crater crawl efficiency on large sites.

**Detect:** `site:domain` count vs actual page count; crawl for `?sort=`, `?filter=`, `?session=` variants returning 200 indexable; check robots/canonical/noindex on facet routes.

**References:** Google Search Central faceted-navigation guidance, crawl-budget optimization docs

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
