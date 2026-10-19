---
categories: [ai-llm, authorization-access-control]
domains: [backend]
---

# Agent Tool Authorization

**MUST** enforce authorization for agent tool execution outside the agent's own decision context, never from a flag the agent sets for itself.

**Why:** Anything inside the model's context is attacker-influenceable through prompt injection, including an 'approved' flag. Enforcement must live in the component that actually executes the call.

**Detect:** grep tool-execution code for approval checks that read agent-supplied arguments, prompt state, or model output instead of a server-side authorization decision.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, OWASP Top 10 for LLM Applications (LLM06 excessive agency)
