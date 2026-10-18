---
categories: [secrets-crypto, third-party-integrations]
domains: [backend]
---

# Integration Credential Sprawl

**SHOULD** centralize third-party SaaS credentials in a secrets manager with owner, scope, and expiry metadata — no credentials in shared docs, wikis, or personal accounts.

**Why:** SaaS credential sprawl (one per engineer, pasted in runbooks, never rotated) makes offboarding impossible to audit and breach blast radius unknowable.

**Detect:** inventory integration creds: count vs documented owners; grep wikis/runbooks/env files for SaaS API keys; check rotation history per integration; flag creds tied to individual employees.

**References:** NIST SP 800-53 IA-5, OWASP Secrets Management Cheat Sheet, vendor SSO/API-token best practices
