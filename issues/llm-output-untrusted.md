---
categories: [ai-llm, security-practices]
domains: [backend, governance]
---

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM01:2025, CWE-79, CWE-89, CWE-78

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
