---
categories: [secrets-crypto]
domains: [backend]
---

# Resumption Key Rotation

**MUST** rotate session-ticket and resumption keys on a short schedule and destroy retired keys, so a stolen key exposes only sessions since the last rotation.

**Why:** A long-lived ticket key silently voids forward secrecy: one key compromise decrypts every session it ever wrapped.

**Detect:** grep for ticket key material and rotation (`SessionTicketKey`, `ticket_keys`, `ssl_session_timeout`, `session_ticket` rotation job) and for a retention window on retired keys.

**References:** RFC 9325 §3.4, https://www.rfc-editor.org/rfc/rfc9325.html, NIST SP 800-57 Part 1
