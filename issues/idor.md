# IDOR

**MUST** Verify the authenticated principal may access every object referenced by a request identifier.

**Why:** Trusting client-supplied IDs lets anyone alter a number to read others' records.

**Detect:** `params['id']` in queries with no ownership filter or policy check; `get_object` without permissions.

**References:** OWASP A01:2021, CWE-639, OWASP Testing Guide IDOR

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
