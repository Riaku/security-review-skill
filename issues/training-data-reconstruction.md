---
categories: [ai-llm]
domains: [backend, data]
---

# Training Data Reconstruction

**SHOULD** keep records under restricted access out of training sets for any model that callers outside that restriction can query.

**Why:** Model access alone supports reconstruction of training records, so serving a model trained on sensitive data hands over a sampling oracle for it.

**Detect:** Inspect each deployed model's training-data manifest against its exposure tier, and flag models trained on identifiable records that untrusted callers can query.

**References:** OWASP LLM02:2025 Sensitive Information Disclosure, SoK on data reconstruction (arXiv 2506.07888), https://arxiv.org/abs/2506.07888
