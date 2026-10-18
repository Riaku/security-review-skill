# Crawler-Renderable Content (SSR/Prerender for JS Apps)

**SHOULD** server-render or prerender content that must rank when the site is a client-side JS app; verify Googlebot sees the same DOM as users.

**Why:** Google renders JS but late, expensively, and imperfectly — CSR-only content risks partial indexing, missing meta tags, and slow first-index times.

**Detect:** fetch pages with JS disabled (or `site:` cache vs live DOM diff); check for SSR/prerender layer (Next SSR, prerender.io, static gen); verify meta/OG present in raw HTML.

**References:** Google Search Central JS SEO guidance, web.dev rendering docs

---

**Part of:** [seo-web-quality](../categories/seo-web-quality.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
