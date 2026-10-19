---
categories: [authentication]
domains: [backend]
---

# Revocation as Best Effort

**MUST NOT** depend on revocation lookups as the primary control for a credential; cap lifetimes, reissue automatically, and treat revocation as a supplement.

**Why:** Revocation infrastructure fails open in practice — offline nodes, soft-fail responders, stale CRLs — so lifetime caps carry the real risk reduction.

**Detect:** grep credential lifetime settings (`expires_in`, `max_age`, `--ttl`) and every `ocsp`/`crl` reference; long lifetimes with only a revocation lookup is the finding.

**References:** RFC 9325 §7.5, https://www.rfc-editor.org/rfc/rfc9325.html, NIST SP 800-57 Part 1
