---
categories: [ai-llm]
domains: [governance]
---

# RAG / Knowledge-Base Poisoning

**SHOULD** validate, provenance-check, and isolate ingested documents so attacker-controlled content cannot enter the retrieval index.

**Why:** Poisoned knowledge bases make malicious instructions appear as trusted retrieved context on every query.

**Detect:** ingest pipelines without source allowlists or content scanning; vector index accepting unauthenticated uploads.

**References:** OWASP LLM04:2025, CWE-506, MITRE ATLAS
