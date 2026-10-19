---
categories: [ai-llm]
domains: [data]
---

# Training Data Trust Boundary

**MUST** treat corpora that train, tune, or configure a decision component as untrusted input with their own provenance, validation, and write access control.

**Why:** Whoever can write the corpus shapes the component's behavior without touching code, and the effect survives review because the model carries the payload.

**Detect:** grep the training and tuning pipeline for dataset reads without a pinned digest or source provenance (`read_csv("http`, `load_dataset(`, `s3://` paths without version IDs).

**References:** OWASP ML Top 10: ML02 Data Poisoning, https://github.com/OWASP/www-project-machine-learning-security-top-10/tree/master/docs
