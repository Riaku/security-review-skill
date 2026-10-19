---
categories: [mobile]
domains: [mobile]
---

# Immutable Deferred Actions

**MUST** make deferred actions handed to the platform immutable and explicitly targeted, with a frozen payload and a fixed component.

**Why:** A mutable or implicitly routed pending action can be intercepted, redirected, or have its extras rewritten before the system delivers it.

**Detect:** grep for PendingIntent built without FLAG_IMMUTABLE, or with an implicit intent instead of an explicit component

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices
