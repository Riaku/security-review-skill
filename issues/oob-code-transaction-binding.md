---
categories: [authentication]
domains: [backend]
---

# OOB Code Transaction Binding

**MUST** bind every out-of-band code or approval request to the authentication transaction that created it, so it cannot satisfy another one.

**Why:** Unbound codes let an attacker trigger many flows, collect delivered codes, and apply any of them to the session being attacked.

**Detect:** grep OTP verification for lookup by code alone rather than by `(code, transaction_id)` or an equivalent server-side binding.

**References:** OWASP ASVS v5.0 V6.6.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md
