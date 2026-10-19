---
categories: [web-api-security]
domains: [backend]
---

# Parameter Source Separation

**MUST** distinguish query, body, cookie, and header parameters, and reject duplicate names where the framework merges them into one value.

**Why:** When validation reads one copy of a duplicated parameter and business logic reads another, every check can be satisfied while the action runs on different input.

**Detect:** grep for merged parameter maps (`request.values`, `request.params`, `getParameterMap`, `ctx.request.body` merged with query) and missing duplicate-parameter rejection.

**References:** OWASP ASVS v5.0 V15.3.7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md, OWASP WSTG: Testing for HTTP Parameter Pollution, CWE-235
