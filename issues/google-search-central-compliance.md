---
categories: [seo-web-quality]
domains: [frontend]
---

# Google Search Central Compliance

**SHOULD** follow Google Search Central spam-and-quality policies: no cloaking, doorway pages, keyword stuffing, or hidden text; crawlable without login walls where indexability is intended.

**Why:** Violations trigger manual actions or algorithmic demotion — traffic loss that looks like a "technical" problem but is a policy problem.

**Detect:** diff HTML served to Googlebot UA vs normal UA (cloaking check); review Search Console coverage + manual-action reports; audit templated landing-page generation.

**References:** Google Search Essentials (spam policies), Google Search Central docs, Schema.org
