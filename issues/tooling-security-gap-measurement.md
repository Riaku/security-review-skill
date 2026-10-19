---
categories: [ai-llm, testing-strategy]
domains: [backend]
---

# Tooling Security Gap Measurement

**MUST** re-measure each adopted code-generation tool's security pass rate on your own tasks, rather than inferring safety from functional gains or release notes.

**Why:** Functional improvement and security improvement diverge per model family, so yesterday's measurement is the only evidence you have about today's tool.

**Detect:** run the same security test suite per tool version and diff the pass rate across releases.

**References:** Longitudinal functionality-security gap study (arXiv 2610.08240), https://arxiv.org/abs/2610.08240
