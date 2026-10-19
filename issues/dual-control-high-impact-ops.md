---
categories: [authorization-access-control]
domains: [backend, governance]
---

# Dual Control High-Impact Ops

**MUST** require two independently authenticated approvals for high-impact operations so no single credential can complete them alone.

**Why:** One compromised or malicious credential should never be enough to delete data, move money or ship a release. Independent conditions bound what one identity can do.

**Detect:** List destructive operations (data deletion, payouts, production deploy, key rotation) and check each demands a second approver distinct from the requester.

**References:** OWASP Developer Guide: Security Principles, https://github.com/OWASP/DevGuide/blob/main/docs/en/02-foundations/03-security-principles.md
