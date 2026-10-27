---
categories: [ai-llm, authorization-access-control]
domains: [backend]
---

# Vector Retrieval Authorization

**MUST** filter vector-store queries by the caller's entitlements — tenant, namespace, document ACL — before retrieved chunks enter a prompt, and never let similarity search alone decide what the model may read.

**Why:** An index shared across tenants turns retrieval into a confused deputy: the query is authorized but the documents are not, so `top_k` returns the nearest chunks whether or not the caller could open them. Embeddings carry source text closely enough that an unentitled hit is a disclosure, not a ranking artifact.

**Detect:** similarity queries with no ACL predicate (`collection.query(embedding, n_results=5)`); a single collection or namespace for every tenant; ACL checks applied after the prompt is assembled; retrieved source links that 403 for the requesting user; per-user filtering implemented in application code only, so an alternate retrieval path bypasses it.

**References:** OWASP LLM08:2025, CWE-639, OWASP ASVS v5.0 V8 Authorization
