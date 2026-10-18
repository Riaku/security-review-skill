# Human-in-the-loop approval for destructive agent tool calls

**MUST** require explicit human confirmation before an autonomous agent executes destructive actions (deletes, payments, sends, deploys).

**Why:** A hijacked or hallucinating agent with unguarded write access can cause irreversible damage in a single automated chain.

**Detect:** agent tool registry lacks confirm/approval flags on destructive verbs; auto-execute=true on write-capable tools.

**References:** OWASP LLM06:2025, NIST AI RMF GOVERN 3, CWE-807

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
