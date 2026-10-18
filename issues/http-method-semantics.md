---
categories: [api-design]
domains: [backend]
---

# HTTP Method Semantics

**MUST NOT** perform state-changing operations via GET or other safe methods; mutations belong in POST/PUT/PATCH/DELETE only.

**Why:** Crawlers, prefetchers, and proxies replay safe requests, turning a link click into unintended deletes or purchases.

**Detect:** grep GET route handlers for DB writes, `session.destroy`, token revocation, or side-effect service calls.

**References:** OWASP API3:2023, CWE-650, RFC 9110 §9.2

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
