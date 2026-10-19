---
categories: [authentication]
domains: [backend]
---

# Session Visibility

**MUST** give users a list of their active sessions with per-session termination, and administrators the same per-user and global view.

**Why:** A session the user cannot see is one they cannot revoke, so a stolen cookie stays live until expiry with no visible trace.

**Detect:** open the account security page and the admin session table and check both list device, time, and a revoke action.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md
