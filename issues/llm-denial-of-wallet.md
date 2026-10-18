---
categories: [ai-llm, scaling-capacity]
domains: [governance, reliability]
---

# Denial-of-wallet: unbounded LLM token spend per user/tenant

**MUST** enforce per-user and per-tenant token budgets, rate limits, and alerting on LLM API spend.

**Why:** A scripted attacker or runaway agent loop can burn thousands of dollars in tokens within hours on a metered API.

**Detect:** no rate_limit, max_tokens, or budget keys on LLM gateway routes; provider usage alerts not configured.

**References:** OWASP LLM10:2025, CWE-770, CWE-400

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [scaling-capacity](../categories/scaling-capacity.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
