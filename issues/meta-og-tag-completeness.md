---
categories: [seo-web-quality]
domains: [frontend]
---

# Meta & OG Tag Completeness

**SHOULD** emit per-page title (unique, concise), meta description, Open Graph, and Twitter Card tags — generated from content, not boilerplate.

**Why:** Missing/duplicated titles and descriptions degrade SERP click-through and make every shared link render blank in social/messaging previews.

**Detect:** crawl and flag pages with missing, duplicated, or template-identical `title`/`description`/`og:*` tags; check OG image dimensions.

**References:** Google Search Central title/description docs, Open Graph protocol, oEmbed
