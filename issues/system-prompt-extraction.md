---
categories: [ai-llm]
domains: [governance]
---

# System prompt extraction and sensitive config embedded in prompts

**SHOULD NOT** embed secrets, credentials, or proprietary logic in system prompts, since extraction via jailbreak or logging is always possible.

**Why:** Prompt contents can be coaxed out verbatim by an attacker or leaked through provider logs.

**Detect:** API keys, connection strings, or business rules literal in system prompt templates; prompt text in logs/tracing exporters.

**References:** OWASP LLM07:2025, CWE-522, CWE-200

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
