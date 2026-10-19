---
categories: [api-design, third-party-integrations]
domains: [backend]
---

# Third-Party Response Validation

**MUST** validate and sanitize data returned by third-party APIs before using it in queries, rendering, or authorization decisions.

**Why:** An integration is another input channel: a compromised or misconfigured provider can return markup, a query fragment, or an unexpected type. Trusting it moves an injection sink inside your trust boundary.

**Detect:** grep integration response handling for provider fields interpolated directly into SQL, HTML, shell, or policy checks without schema validation.

**References:** OWASP API Security Top 10 (2023) API10 (unsafe consumption of APIs), https://github.com/OWASP/API-Security, CWE-20 Improper Input Validation
