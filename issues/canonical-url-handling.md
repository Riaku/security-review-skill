---
categories: [seo-web-quality]
domains: [frontend]
---

# Canonical URL Handling

**SHOULD** emit a self-referencing canonical link on every indexable page and canonicalize http→https, www→apex, trailing-slash, and param variants to one URL per resource.

**Why:** Without canonicals, the same content competes with itself across variants, splitting ranking signals and creating duplicate-content indexing chaos.

**Detect:** grep templates for `<link rel="canonical">`; crawl and flag pages whose canonical points to non-200 or non-canonical variants; check 301 rules for scheme/host/slash.

**References:** Google Search Central canonicalization docs, SEO canonical best practices

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
