---
categories: [mobile]
domains: [mobile]
---

# Screen Capture of Sensitive Views

**MUST** opt sensitive screens out of OS screenshot, screen-recording, and recents-thumbnail capture rather than assuming users will not capture them.

**Why:** The platform renders whatever the app draws, so a view showing tokens, balances, or personal data persists in the recents store and in any recorder.

**Detect:** grep for FLAG_SECURE on sensitive activities and the secure-capture equivalent on token and PII screens

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices
