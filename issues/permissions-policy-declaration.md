---
categories: [web-client-security]
domains: [frontend]
---

# Permissions Policy Declaration

**SHOULD** send a Permissions-Policy header that disables powerful browser capabilities the application never uses.

**Why:** A compromised third-party script inherits access to camera, microphone, geolocation, and payment interfaces by default. Declaring the unused set removes the capability instead of trusting the script.

**Detect:** grep response header configuration for `Permissions-Policy` or `Feature-Policy`; compare the declared capabilities against the features the application actually calls.

**References:** OWASP Proactive Controls C8, https://github.com/OWASP/www-project-proactive-controls, W3C Permissions Policy
