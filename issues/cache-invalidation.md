---
categories: [caching]
domains: [reliability]
---

# Cache Invalidation

**MUST** invalidate every cached entry that holds data changed by a write, privilege change, or credential rotation before the response returns, and for security-relevant keys (permissions, sessions) invalidate by versioned/generation key or tombstone with a bounded TTL, so a reader that loaded the old value cannot repopulate the entry after the invalidation.

**Why:** Stale cached permissions or secrets let revoked users keep acting on old data long after the change.

**Detect:** grep for cache.set without paired cache.delete/evict; keys like `user_perms:`, `session:` missing invalidation hooks.

**References:** OWASP A04:2021, CWE-613, NIST SP 800-53 AC-2
