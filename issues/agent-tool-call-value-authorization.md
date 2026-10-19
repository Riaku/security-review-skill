---
categories: [ai-llm]
domains: [backend]
---

# Per-Call Tool Authorization

**MUST** authorize each model-initiated tool call against its concrete arguments — scope, recipient, amount, tenant — at execution time, denying by default when no rule matches.

**Why:** A capability gate only proves the agent can reach a tool, never that this recipient, amount, or record is permitted, so a steered argument turns a legitimate tool into a confused deputy.

**Detect:** grep tool dispatch that forwards model-supplied arguments straight to handlers (`tools[name](**args)`, `execute_tool(`, `function_call.arguments`) with no per-call policy check.

**References:** ScopeGate agent authorization study, https://arxiv.org/abs/2606.28679, OWASP Top 10 for LLM Applications: LLM06 Excessive Agency
