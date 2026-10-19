---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# Guard Condition Soundness

**MUST** review the authorization guard expression itself — always-true conditions, substring matches, falsy-through-|| fallbacks — not just the intent of the step it protects.

**Why:** A guard that evaluates true for every input is a missing control that still reads as a control in review.

**Detect:** grep authorization guards and CI `if:` conditions for always-true shapes (`contains()` on a scalar, `x == x`, a `||` fallback defaulting to true) and read each for the outcome it admits.

**References:** zizmor, https://github.com/zizmorcore/zizmor
