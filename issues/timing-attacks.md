---
categories: [authentication]
domains: [backend]
---

# Timing Attacks

**MUST** compare secrets (password hashes, tokens, API keys) using constant-time comparison functions.

**Why:** Early-exit string comparison leaks byte-by-byte match timing, letting a remote attacker reconstruct valid secrets through repeated requests.

**Detect:** grep for `==` or `===` comparing hashes/tokens instead of `hmac.compare_digest`, `crypto.timingSafeEqual`, or `MessageDigest.isEqual`.

**References:** CWE-208, CWE-203, OWASP A02:2021, NIST SP 800-53 SC-8
