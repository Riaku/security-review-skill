---
categories: [ai-llm, authorization-access-control]
domains: [backend]
---

# Sub-Agent Credential Scoping

**MUST** issue delegated sub-agents credentials and tool allowlists scoped to the sub-task, never a copy of the parent agent's full authority.

**Why:** A sub-agent inherits the parent's blast radius: a prompt-injected worker holding the orchestrator's keys can do everything the orchestrator can, and attribution collapses when both act under one identity.
**Detect:** check how sub-agents and child agent processes are launched — the same API keys, MCP server config, or profile passed through unchanged; no per-role tool allowlist and no short-lived scoped token for the delegated task.
**References:** OWASP Top 10 for LLM Applications (LLM06 excessive agency), OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
