---
categories: [security-practices]
domains: [backend]
---

# Tool Evaluation on Own Corpus

**SHOULD** evaluate security-analysis tools on a hand-built corpus of known-bad and known-good cases before trusting them in the pipeline.

**Why:** Vendor benchmarks measure the vendor's test set, not your code. A fixed local corpus shows what a tool misses in your languages and frameworks.

**Detect:** Inspect the benchmark repository: versioned cases with expected findings and a recorded per-tool result.

**References:** arXiv:2503.09433, https://arxiv.org/abs/2503.09433
