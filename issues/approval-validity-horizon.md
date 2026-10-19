---
categories: [ai-llm]
domains: [backend]
---

# Approval Validity Horizon

**MUST** attach an expiry to every approval or guardrail verdict and re-check it immediately before the action executes.

**Why:** State changes between check and actuation, so an approval correct at decision time can authorize an action the current state forbids.

**Detect:** grep approval objects for `expires_at` / `valid_until` and confirm the executor re-reads state or refuses stale verdicts before the side effect.

**References:** Approved-too-late guardrail staleness, https://arxiv.org/abs/2608.26306, CWE-367 (TOCTOU)
