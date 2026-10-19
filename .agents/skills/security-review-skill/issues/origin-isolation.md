---
categories: [web-client-security]
domains: [frontend]
---

# Origin Isolation

**MUST** host separate applications on separate hostnames so the same-origin policy keeps one from scripting or reading the other.

**Why:** Two apps on one origin share cookies, storage, and script context, so a flaw in the weaker one is an authenticated foothold in the stronger.

**Detect:** grep ingress and router config for several apps mounted under one host or path prefix, and list the cookies and storage keys they share.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, CWE-346
