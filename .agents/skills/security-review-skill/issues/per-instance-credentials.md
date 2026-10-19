---
categories: [secrets-crypto]
domains: [backend]
---

# Per-Instance Credentials

**MUST NOT** ship one static credential that every customer instance shares; issue per-instance or per-tenant credentials that can be revoked alone.

**Why:** A single credential extracted from one deployment then authenticates every other deployment, and revoking it breaks them all.

**Detect:** grep packaged config and installer defaults for one shared API key, service token, or database password repeated across environments and tenants.

**References:** OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
