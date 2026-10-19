---
categories: [ai-llm]
domains: [backend]
---

# Provenance Trust Lattice

**SHOULD** attach provenance labels to model inputs and enforce that lower-trust content cannot influence higher-trust decisions.

**Why:** Heuristic filters are bypassed routinely; a structural non-interference rule makes provenance a checkable property instead of a judgment call.

**Detect:** grep the pipeline for trust labels (`trust_level`, `source_trust`, `provenance`) and for a policy check that blocks rather than logs cross-level influence.

**References:** Cryptographic input provenance for LLM pipelines, https://arxiv.org/abs/2508.09288
