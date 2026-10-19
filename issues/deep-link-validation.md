---
categories: [mobile]
domains: [mobile]
---

# Deep Link / Universal Link Validation

**SHOULD** validate scheme, host, and parameters of every incoming deep link on the client, treating link-supplied identifiers as untrusted input, and re-check authorization server-side before acting on them.

**Why:** Unvalidated links enable phishing into authenticated flows, IDOR jumps to other users' resources, and intent hijacking on Android.

**Detect:** grep `AppDelegate continueUserActivity`, `onNewIntent`, `intent-filter`, `universalLinksOnly`; review handlers for missing authz checks on link parameters.

**References:** OWASP MASVS-PLATFORM-1, CWE-20, CWE-639, OWASP MAS Testing Guide Client-Side Attack Surface
