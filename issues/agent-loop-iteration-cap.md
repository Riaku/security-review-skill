---
categories: [ai-llm, resilience]
domains: [backend, reliability]
---

# Agent Loop Iteration Cap

**MUST** bound autonomous agent loops with a hard iteration or turn limit and a wall-clock deadline, terminating in a declared degraded outcome when the budget is exhausted.

**Why:** A self-correcting agent with no external cap can retry the same failing tool call indefinitely, burning metered spend, holding rate-limit quota and locks, and delaying the human who would otherwise notice.
**Detect:** grep agent loop code for `while True` or recursion with no max-iterations counter or deadline; confirm budget exhaustion returns an explicit failure or degraded path rather than silently re-entering the loop.
**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, CWE-835 Loop with Unreachable Exit Condition
