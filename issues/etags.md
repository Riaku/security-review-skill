# ETags

**SHOULD NOT** generate ETags from data that leaks across users or tenants, and strong validators must change whenever the underlying resource changes.

**Why:** Weak or shared ETags cause stale conditional responses; content-derived tags can expose other tenants' data via cache reuse.

**Detect:** `ETag` built from user-independent hashes; `If-None-Match` handlers ignoring tenant ID; weak `W/` validators on auth-sensitive resources.

**References:** OWASP A04:2021, CWE-916, RFC 7232 section 2.3, RFC 9110 8.8.3

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
