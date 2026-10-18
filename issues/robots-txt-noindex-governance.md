---
categories: [seo-web-quality]
domains: [frontend]
---

# Robots.txt & noindex Governance

**MUST** treat robots.txt as a crawl-traffic control, never a security control, and keep `noindex` meta/X-Robots-Tag policy deliberate per environment (staging MUST be noindex).

**Why:** robots.txt does not hide URLs (crawlers still see linked URLs), and a missing staging `noindex` leaks pre-release content into the index.

**Detect:** fetch `/robots.txt` on every environment; grep responses for `X-Robots-Tag`; check staging for `noindex, nofollow`; verify admin/internal paths are noindex not just disallowed.

**References:** Google Search Central robots.txt docs, robots.txt Exclusion Standard RFC 9309, CWE-538

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
