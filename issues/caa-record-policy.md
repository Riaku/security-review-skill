---
categories: [cloud-network]
domains: [infrastructure]
---

# CAA Record Policy

**SHOULD** publish CAA records restricting which CAs may issue certificates for the domain, with issuewild and iodef contact configured.

**Why:** Without CAA, any trusted CA can issue for your domain — a compromised or careless CA anywhere is a MITM cert waiting to happen; CAA narrows that to chosen issuers.

**Detect:** `dig CAA <domain>` and check issuewild coverage (missing issuewild = wildcards blocked for all CAs — verify intent); confirm CAA covers all public cert domains including delegated subdomains.

**References:** RFC 8659 CAA, CA/B Forum baseline requirements, letsencrypt CAA documentation

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
