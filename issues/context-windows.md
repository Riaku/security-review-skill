# Context Windows

**SHOULD** bound and trim conversation context explicitly so sensitive earlier turns are evicted rather than silently retained or truncated unpredictably.

**Why:** Unbounded context hoards PII and secrets in every replay, and overflow truncation can drop safety instructions mid-session.

**Detect:** config keys max_tokens, context_length, truncation strategy; no retention/eviction logic in history builders.

**References:** OWASP LLM10:2025, CWE-778, NIST SP 800-53 AT-4

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
