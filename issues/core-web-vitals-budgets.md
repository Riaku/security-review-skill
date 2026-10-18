# Core Web Vitals Budgets

**MUST** define and enforce Core Web Vitals budgets — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 at the 75th percentile of real users.

**Why:** CWV is Google's published ranking and UX signal; unmeasured pages drift past thresholds silently and lose both search visibility and conversions.

**Detect:** check for CrUX/RUM data, `web-vitals` library instrumentation, Lighthouse CI assertions on `largest-contentful-paint`, `interaction-to-next-paint`, `cumulative-layout-shift`.

**References:** web.dev/vitals, Google Search Central CWV docs, Lighthouse performance category
