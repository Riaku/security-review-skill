---
categories: [ai-llm]
domains: [governance]
---

# Prompt Injection

**MUST** treat all untrusted content (user input, retrieved documents, tool output) as data, never as instructions that override system policy.

**Why:** Injected text can hijack model behavior, leaking secrets or triggering actions the operator never authorized.

**Detect:** raw user/RAG strings interpolated into f-string prompts; missing delimiters or injection test cases.

**References:** OWASP LLM01:2025, CWE-74, NIST AI 100-2

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
