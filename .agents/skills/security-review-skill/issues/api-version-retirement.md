---
categories: [api-design]
domains: [backend]
---

# API Version Retirement

**MUST** assess every older API version against the security fixes shipped in newer ones, then backport the fix or retire the version by a deadline.

**Why:** An old version left running keeps the vulnerability the new one fixed, and clients have no incentive to move. Without a retirement date the insecure surface is permanent.

**Detect:** judgment: the version support matrix and route table — each live version mapped to a security-fix status and an announced end date.

**References:** OWASP API Security Top 10 (2023) API9 (improper inventory management), https://github.com/OWASP/API-Security
