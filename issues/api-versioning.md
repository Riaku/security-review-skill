---
categories: [api-design]
domains: [backend]
---

# API Versioning

**SHOULD** version APIs explicitly via URL path or header from day one, keeping the breaking-change policy documented per version.

**Why:** Unversioned APIs force simultaneous upgrades of every consumer, turning one breaking change into a coordinated outage.

**Detect:** routes lacking `/v1/` prefix, absent `Accept-Version`/`Api-Version` header handling, no deprecation policy doc.

**References:** OWASP API 2023, Microsoft REST API Guidelines §10, Google AIP-180

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
