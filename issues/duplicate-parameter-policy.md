---
categories: [web-api-security]
domains: [backend]
---

# Duplicate Parameter Policy

**MUST** define one duplicate-parameter policy — reject, first-wins, or last-wins — and apply it identically in the validator, the filter, and the handler.

**Why:** Standards leave repeated-field semantics undefined, so a filter and the application can read different values from the same request, and the filter approves what the handler never sees.

**Detect:** grep parameter accessors that silently collapse duplicates (`req.query.x`, `request.args.get`, `getParameter`) and confirm the framework rejects repeated keys.

**References:** OWASP WSTG: HTTP parameter pollution, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/, CWE-235 (Parameter Pollution)
