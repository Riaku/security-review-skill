---
categories: [web-api-security]
domains: [backend]
---

# IDOR

**MUST** Verify the authenticated principal may access every object referenced by a request identifier.

**Why:** Trusting client-supplied IDs lets anyone alter a number to read others' records.

**Detect:** `params['id']` in queries with no ownership filter or policy check; `get_object` without permissions.

**References:** OWASP API1:2023 Broken Object Level Authorization, OWASP A01:2021, CWE-639, OWASP Testing Guide IDOR
