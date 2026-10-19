---
categories: [authorization-access-control]
domains: [backend]
---

# Subject Authority Propagation

**MUST** carry the originating subject's authority through service chains, so downstream decisions use that subject's permissions rather than the intermediary's.

**Why:** When a middle service calls downstream with its own machine credentials, every downstream check authorizes the service and the user's limits vanish.

**Detect:** grep downstream clients for machine-credential auth (`client_credentials`, `service_account`, `AssumeRole`) on calls that act for an end user.

**References:** OWASP ASVS v5.0 V8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md, CWE-441
