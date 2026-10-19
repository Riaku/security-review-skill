---
categories: [security-practices]
domains: [backend]
---

# Complementary SAST Engines

**SHOULD** run more than one static-analysis engine and use their combined findings to direct human security review.

**Why:** A single engine misses whole bug classes, and its clean result is read as proof of safety. Different engines fail on different patterns.

**Detect:** CI runs at least two independent analyzers (for example semgrep plus CodeQL) and routes both SARIF outputs into one triage queue.

**References:** arXiv:2407.12241, https://arxiv.org/abs/2407.12241
