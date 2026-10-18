# GraphQL Query Depth & Complexity Limits

**MUST** Cap query depth, node count, and alias size, rejecting over-budget queries before execution.

**Why:** Unbounded nesting multiplies resolver calls into denial-of-service from one request.

**Detect:** Server config without `max_depth`/`max_complexity` validation rules; persisted-query-only mode absent; `graphiql` in prod.

**References:** OWASP A04:2021, CWE-770, OWASP GraphQL Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
