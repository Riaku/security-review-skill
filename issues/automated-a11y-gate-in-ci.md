---
categories: [testing-strategy]
domains: [backend]
---

# Automated A11y Gate in CI

**SHOULD** run automated accessibility checks (axe-core/pa11y) in CI on UI changes, failing on new violations of the target WCAG level.

**Why:** One-line accessibility checklist items change nothing; a CI gate on actual scans makes regressions visible at the PR and compounds into real WCAG compliance over time.

**Detect:** check CI for `@axe-core/playwright`, `jest-axe`, pa11y-ci configs with violation thresholds; verify scans cover key routes, not just the homepage; check manual a11y review for what automation misses (keyboard flows, screen-reader semantics).

**References:** axe-core docs, WCAG 2.2, WAI-ARIA authoring practices, EAA/Section 508 compliance guidance

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
