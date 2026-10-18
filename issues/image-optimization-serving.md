---
categories: [seo-web-quality]
domains: [frontend]
---

# Image Optimization & Modern Serving

**MUST** serve images in modern formats (WebP/AVIF) with explicit dimensions, responsive `srcset`, and lazy-loading below the fold.

**Why:** Unoptimized images are the single largest CWV regression source — LCP killer, bandwidth waste, and layout shift (CLS) when dimensions are missing.

**Detect:** grep templates for `<img>` without `width`/`height`/`srcset`/`loading="lazy"`; audit page weight by type (Lighthouse "reduce initial server response"/image reports).

**References:** web.dev fast images, Google image optimization guidance, Lighthouse image audits

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
