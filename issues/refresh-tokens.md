---
categories: [authentication]
domains: [backend]
---

# Refresh Tokens

**SHOULD** store refresh tokens server-side with rotation on every use, invalidating the previous token after exchange.

**Why:** A static, non-rotating refresh token lets an attacker who steals one mint fresh access tokens forever, even after the user logs in again.

**Detect:** grep refresh endpoints for missing rotation (`old token reused`), refresh tokens kept in localStorage, no `revoked`/`rotated_at` column in token store.

**References:** OWASP A02:2021, CWE-523, RFC 6749 §6, OAuth Security BCP §4.13

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
