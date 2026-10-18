# Token Revocation & Logout Invalidation

**MAY** rely on short expiry alone for stateless tokens, but MUST provide a revocation list or denylist for high-value sessions where immediate logout is required.

**Why:** A pure stateless JWT cannot be logged out; a stolen token keeps working until expiry even after the user hits logout.

**Detect:** grep logout handler for missing token blacklist/`jti` denylist, no `/revoke` endpoint, Redis denylist absent, logout only clears client cookie.

**References:** RFC 7009, RFC 8725 §4.1, OWASP A02:2021, NIST SP 800-53 SC-23
