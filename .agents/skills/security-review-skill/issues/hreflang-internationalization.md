---
categories: [seo-web-quality]
domains: [frontend]
---

# Hreflang & Internationalization Signals

**SHOULD** emit correct `hreflang` annotations for multi-language/regional sites, with reciprocal links and a self-reference on each variant.

**Why:** Missing or non-reciprocal hreflang makes Google serve the wrong language version to users and wastes crawl budget on unserved variants.

**Detect:** validate hreflang sets (HTML link tags, HTTP header, or sitemap — one mechanism), check reciprocity and x-default presence with an hreflang audit tool.

**References:** Google Search Central localized results docs, hreflang validation checklists
