---
categories: [ai-llm, scaling-capacity]
domains: [backend]
---

# Model Extraction Throttling

**SHOULD** cap and detect systematic harvesting — per-key request rate, input diversity, output volume — that would let a competitor clone the served model through the API alone.

**Why:** Extraction needs many well-chosen queries, not a breach: a few thousand input/output pairs reproduce behaviour closely enough to compete with the provider who paid to train it. A per-request rate limit does not stop this, because the attack is patient, spread across keys, and looks like ordinary product usage until output volume is measured.

**Detect:** no per-key daily quota or unique-input-diversity metric on a public inference endpoint; no alarm when one key's prompt diversity or output-token volume exceeds the fleet baseline; logprobs or full distributions returned where a label would do; bulk-capture prohibition in the terms with no technical control behind it.

**References:** OWASP LLM10:2025, MITRE ATLAS AML.T0024, NIST AI 100-2
