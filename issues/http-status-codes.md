---
categories: [api-design]
domains: [backend]
---

# HTTP Status Codes

**MUST** return accurate status codes: 401 for unauthenticated, 403 for unauthorized, 404 for missing resources, never 200 with an error body.

**Why:** Masking failures as 200 breaks client retry logic and lets attackers probe auth boundaries without signal.

**Detect:** grep handlers for `return 200` alongside error payloads; missing `401`/`403`/`404` in route error paths.

**References:** OWASP API2:2023, CWE-390, RFC 9110 §15

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
