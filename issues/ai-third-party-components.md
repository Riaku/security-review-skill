---
categories: [ai-llm, supply-chain]
domains: [backend, data]
---

# AI Third-Party Components

**MUST** inventory third-party datasets, pre-trained models, plugins, and hosted model APIs, recording their downstream impact and a contingency plan for failure.

**Why:** Errors and compromises in procured models or data propagate silently into every downstream output, and an uninventoried component cannot be rotated or recalled.

**Detect:** grep for unpinned model and dataset loads (`from_pretrained(`, `hf_hub_download`, dataset URLs, plugin registries) and check each appears in the component inventory with a digest.

**References:** NIST AI 600-1 GOVERN 6.1, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
