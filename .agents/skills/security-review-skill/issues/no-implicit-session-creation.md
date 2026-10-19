---
categories: [authentication]
domains: [backend]
---

# No Implicit Session Creation

**MUST NOT** create or refresh a session without an explicit user action, so prefetch, bots, and link scanners cannot mint sessions.

**Why:** Silent creation multiplies sessions nobody asked for, each one a credential to steal, and lets a link previewer authenticate as the recipient.

**Detect:** grep session creation inside GET handlers and middleware that issues a cookie on any request.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md
