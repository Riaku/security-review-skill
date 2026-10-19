---
categories: [authentication]
domains: [backend]
---

# Authentication Pathway Parity

**MUST** enforce the same authentication strength on every pathway, including legacy APIs, support tooling, and partner integrations.

**Why:** Support portals, legacy APIs, and partner integrations quietly carry weaker auth than the main login, so the real security level is the minimum.

**Detect:** grep route registration against the auth middleware (`app.get(`, `router.post(`, `@app.route`) for handlers with no auth dependency or factor check.

**References:** OWASP ASVS v5.0 V6.1.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B
