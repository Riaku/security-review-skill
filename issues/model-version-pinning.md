---
categories: [ai-llm, supply-chain]
domains: [governance]
---

# Model Version Pinning

**MUST** pin exact model versions or digests rather than floating aliases like gpt-4 or latest in production configs.

**Why:** Silent upstream model swaps change safety behavior and data-handling guarantees without any code review.

**Detect:** grep model: "latest", model: gpt-4 without dated suffix; missing digest/revision fields in inference config.

**References:** OWASP LLM03:2025, CWE-1104, NIST AI RMF MANAGE
