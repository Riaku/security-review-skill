---
categories: [ai-llm, compliance-privacy]
domains: [governance]
---

# Shadow AI: unsanctioned AI SaaS and embedded AI features in the stack

**MUST** inventory and govern AI features in third-party software and employee-adopted AI SaaS, since unsanctioned tools move data outside policy.

**Why:** Copilots and AI-enabled vendors quietly move code, tickets, and documents to unvetted providers.

**Detect:** network egress to openai.com/anthropic.com from unmanaged endpoints; no AI usage policy or CASB/SaaS inventory entries.

**References:** OWASP LLM09:2025, NIST AI RMF GOVERN 6, CWE-912
