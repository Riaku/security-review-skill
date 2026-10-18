# Lighthouse CI Performance Budgets

**SHOULD** run Lighthouse (or Lighthouse CI) on every PR with asserted budgets for performance, accessibility, best-practices, and SEO scores; fail the build on regression.

**Why:** Untracked Lighthouse scores decay one merge at a time; a CI gate makes regression visible at the commit that caused it.

**Detect:** check for `lighthouse-ci` config (`lighthouserc.json`), `lhci autorun` in workflows, asserted `assert` thresholds per category/metric.

**References:** Lighthouse CI docs (github.com/GoogleChrome/LighthouseCI), web.dev performance budgets
