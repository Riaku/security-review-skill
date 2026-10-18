---
categories: [cloud-network, web-api-security]
domains: [backend, infrastructure]
---

# Open Directory Listing

**SHOULD NOT** enable directory indexes on web servers or object storage where file enumeration reveals backups, configs, or internal artifacts.

**Why:** `Autoindex on` / bucket list permission turns one known filename pattern into a full inventory of everything ever placed there.

**Detect:** grep server configs for `autoindex on`, `Options +Indexes`, bucket `ListBucket` grants; probe for `Index of /` responses.

**References:** OWASP WSTG-CONF-01, CWE-548, AWS S3 ACL best practices

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
