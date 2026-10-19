---
categories: [payments-fraud]
domains: [backend]
---

# Structural Invariants Against Organized Abuse

**SHOULD** detect organized abuse through structural invariants — concentrated cash-out, shared infrastructure, synchronized timing — rather than tightening per-account thresholds.

**Why:** An attacker spread across many accounts keeps each below any fixed threshold; only the structure their economics force stays visible.

**Detect:** judgment: the fraud ruleset — whether any rule keys on cross-account structure rather than a per-entity score

**References:** Fraudster's Trilemma, https://arxiv.org/abs/2605.07383
