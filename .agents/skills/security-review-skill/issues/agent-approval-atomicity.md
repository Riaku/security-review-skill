---
categories: [ai-llm]
domains: [backend]
---

# Agent Approval Atomicity

**MUST** check and consume an approval atomically immediately before execution, requiring fresh approval when the target or parameters change.

**Why:** Approval followed by substitution is a time-of-check/time-of-use hole: the human approves one action and the agent executes another. Single-use approval bound to the exact arguments closes it.

**Detect:** grep approval stores for `get` then `execute` without an atomic consume, and for approvals keyed on tool name rather than a hash of the exact arguments.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, CWE-367 Time-of-check Time-of-use Race Condition
