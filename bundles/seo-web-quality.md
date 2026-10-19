# seo-web-quality — full checklist (13 items)

Search visibility, crawl/index hygiene, and page experience (Google Search Central, CWV, Lighthouse).

> Generated artifact — edit the issue files, not this one. Manifest: [categories/seo-web-quality.md](../categories/seo-web-quality.md) · Index: [SKILL.md](../SKILL.md)

# Canonical URL Handling

**SHOULD** emit a self-referencing canonical link on every indexable page and canonicalize http→https, www→apex, trailing-slash, and param variants to one URL per resource.

**Why:** Without canonicals, the same content competes with itself across variants, splitting ranking signals and creating duplicate-content indexing chaos.

**Detect:** grep templates for `<link rel="canonical">`; crawl and flag pages whose canonical points to non-200 or non-canonical variants; check 301 rules for scheme/host/slash.

**References:** Google Search Central canonicalization docs, SEO canonical best practices

# Core Web Vitals Budgets

**MUST** define and enforce Core Web Vitals budgets — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 at the 75th percentile of real users.

**Why:** CWV is Google's published ranking and UX signal; unmeasured pages drift past thresholds silently and lose both search visibility and conversions.

**Detect:** check for CrUX/RUM data, `web-vitals` library instrumentation, Lighthouse CI assertions on `largest-contentful-paint`, `interaction-to-next-paint`, `cumulative-layout-shift`.

**References:** web.dev/vitals, Google Search Central CWV docs, Lighthouse performance category

# Crawler-Renderable Content (SSR/Prerender for JS Apps)

**SHOULD** server-render or prerender content that must rank when the site is a client-side JS app; verify Googlebot sees the same DOM as users.

**Why:** Google renders JS but late, expensively, and imperfectly — CSR-only content risks partial indexing, missing meta tags, and slow first-index times.

**Detect:** fetch pages with JS disabled (or `site:` cache vs live DOM diff); check for SSR/prerender layer (Next SSR, prerender.io, static gen); verify meta/OG present in raw HTML.

**References:** Google Search Central JS SEO guidance, web.dev rendering docs

# Google Search Central Compliance

**SHOULD** follow Google Search Central spam-and-quality policies: no cloaking, doorway pages, keyword stuffing, or hidden text; crawlable without login walls where indexability is intended.

**Why:** Violations trigger manual actions or algorithmic demotion — traffic loss that looks like a "technical" problem but is a policy problem.

**Detect:** diff HTML served to Googlebot UA vs normal UA (cloaking check); review Search Console coverage + manual-action reports; audit templated landing-page generation.

**References:** Google Search Essentials (spam policies), Google Search Central docs, Schema.org

# Hreflang & Internationalization Signals

**SHOULD** emit correct `hreflang` annotations for multi-language/regional sites, with reciprocal links and a self-reference on each variant.

**Why:** Missing or non-reciprocal hreflang makes Google serve the wrong language version to users and wastes crawl budget on unserved variants.

**Detect:** validate hreflang sets (HTML link tags, HTTP header, or sitemap — one mechanism), check reciprocity and x-default presence with an hreflang audit tool.

**References:** Google Search Central localized results docs, hreflang validation checklists

# Image Optimization & Modern Serving

**MUST** serve images in modern formats (WebP/AVIF) with explicit dimensions, responsive `srcset`, and lazy-loading below the fold.

**Why:** Unoptimized images are the single largest CWV regression source — LCP killer, bandwidth waste, and layout shift (CLS) when dimensions are missing.

**Detect:** grep templates for `<img>` without `width`/`height`/`srcset`/`loading="lazy"`; audit page weight by type (Lighthouse "reduce initial server response"/image reports).

**References:** web.dev fast images, Google image optimization guidance, Lighthouse image audits

# Index Bloat & Faceted-URL Control

**SHOULD NOT** allow faceted navigation, session IDs, sort/filter params, and internal search results to be indexed at scale.

**Why:** Millions of low-value param URLs explode the index, bury the pages that matter, and crater crawl efficiency on large sites.

**Detect:** `site:domain` count vs actual page count; crawl for `?sort=`, `?filter=`, `?session=` variants returning 200 indexable; check robots/canonical/noindex on facet routes.

**References:** Google Search Central faceted-navigation guidance, crawl-budget optimization docs

# Lighthouse CI Performance Budgets

**SHOULD** run Lighthouse (or Lighthouse CI) on every PR with asserted budgets for performance, accessibility, best-practices, and SEO scores; fail the build on regression.

**Why:** Untracked Lighthouse scores decay one merge at a time; a CI gate makes regression visible at the commit that caused it.

**Detect:** check for `lighthouse-ci` config (`lighthouserc.json`), `lhci autorun` in workflows, asserted `assert` thresholds per category/metric.

**References:** Lighthouse CI docs (github.com/GoogleChrome/LighthouseCI), web.dev performance budgets

# Meta & OG Tag Completeness

**SHOULD** emit per-page title (unique, concise), meta description, Open Graph, and Twitter Card tags — generated from content, not boilerplate.

**Why:** Missing/duplicated titles and descriptions degrade SERP click-through and make every shared link render blank in social/messaging previews.

**Detect:** crawl and flag pages with missing, duplicated, or template-identical `title`/`description`/`og:*` tags; check OG image dimensions.

**References:** Google Search Central title/description docs, Open Graph protocol, oEmbed

# Redirect Chain & Status Hygiene

**MUST NOT** chain redirects (>1 hop) on indexable URLs, and MUST serve 410/404 (not soft-404) for removed content.

**Why:** Chains waste crawl budget, slow users, and break link equity; soft-404s (200 on missing pages) pollute the index and mask real removals.

**Detect:** crawl and flag redirect_count > 1; check removed-content routes return 200 with "not found" body (soft-404) via Search Console coverage report.

**References:** Google Search Central redirect docs, RFC 9110 §15.4/§15.5 (redirection and client-error status codes), soft-404 guidance

# Robots.txt & noindex Governance

**MUST** treat robots.txt as a crawl-traffic control, never a security control, and keep `noindex` meta/X-Robots-Tag policy deliberate per environment (staging MUST be noindex).

**Why:** robots.txt does not hide URLs (crawlers still see linked URLs), and a missing staging `noindex` leaks pre-release content into the index.

**Detect:** fetch `/robots.txt` on every environment; grep responses for `X-Robots-Tag`; check staging for `noindex, nofollow`; verify admin/internal paths are noindex not just disallowed.

**References:** Google Search Central robots.txt docs, robots.txt Exclusion Standard RFC 9309, CWE-538

# Structured Data (Schema.org) Validation

**SHOULD** emit valid JSON-LD structured data (Organization, Product, Article, FAQ, BreadcrumbList) and validate it before deploy.

**Why:** Invalid or misleading structured data forfeits rich results and can trigger a structured-data manual action; valid markup is free SERP real estate.

**Detect:** grep templates for `application/ld+json`; run Rich Results Test / Schema validator in CI; diff required vs emitted properties per type.

**References:** Google Search Central structured data docs, schema.org validators, Rich Results Test

# XML Sitemap Maintenance

**SHOULD** auto-generate sitemap.xml containing only canonical, indexable, non-noindex URLs, with accurate lastmod, and reference it from robots.txt and submit it through Search Console (Google retired the sitemaps ping endpoint in 2023).

**Why:** A stale sitemap (listing removed, noindex, or redirected URLs) wastes crawl budget and delays discovery of real content.

**Detect:** validate sitemap against URL statuses (all 200 + indexable); check lastmod reflects real changes; confirm robots.txt references the sitemap.

**References:** Google Search Central sitemap docs, sitemap.org protocol

