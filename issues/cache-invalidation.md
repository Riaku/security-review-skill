# Cache Invalidation

**MUST** invalidate every cached entry that holds data changed by a write, privilege change, or credential rotation before the response returns.

**Why:** Stale cached permissions or secrets let revoked users keep acting on old data long after the change.

**Detect:** grep for cache.set without paired cache.delete/evict; keys like `user_perms:`, `session:` missing invalidation hooks.

**References:** OWASP A04:2021, CWE-613, CWE-364, NIST SP 800-53 AC-2

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
