---
categories: [mobile]
domains: [mobile]
---

# Keyboard Caching of Sensitive Input

**MUST** disable predictive text, autocorrect, and keyboard learning for fields that accept secrets or sensitive personal data.

**Why:** System keyboards retain and sync typed text, so a value typed once can persist in the user's dictionary and cloud backup.

**Detect:** grep for textNoSuggestions or textVisiblePassword input flags and autocorrect=false on sensitive fields

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices
