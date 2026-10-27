---
categories: [ai-llm, multi-tenancy]
domains: [backend]
---

# Agent Memory Isolation

**MUST** namespace agent memory per user and session so no stored context can enter another user's prompt.

**Why:** A shared store carries one user's data and instructions into another user's context: a data leak and a persistent injection channel that outlives the session that planted it.

**Detect:** grep memory and vector-store reads/writes for a user or session namespace/partition key; global collection names with no tenant field, and retrieval filtered only by similarity, are the finding.

**References:** OWASP LLM08:2025 Vector and Embedding Weaknesses, OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, OWASP Top 10 for LLM Applications (LLM01 prompt injection)
