# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
