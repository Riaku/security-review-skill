---
categories: [supply-chain, web-client-security]
domains: [frontend]
---

# Subresource Integrity

**MUST** require integrity hashes on every externally hosted script or stylesheet, or record an explicit exception with its rationale.

**Why:** A third-party host or CDN that is compromised, or a package that is deleted and re-registered, serves attacker code into the page with full origin privileges.

**Detect:** grep `<script src="http` and `<link href="http` for missing `integrity=` attributes.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, W3C Subresource Integrity
