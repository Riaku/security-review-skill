---
categories: [api-design, web-api-security]
domains: [backend]
---

# Content-Type Enforcement

**MUST** reject request bodies whose declared Content-Type is not the one the endpoint expects, before parsing.

**Why:** Parsers disagree about ambiguous bodies, so a form-encoded or text payload can be read as JSON or the reverse. That disagreement turns cross-site protections and validation rules into no-ops.

**Detect:** grep route handlers and framework config for explicit content-type rejection (`415`, `UnsupportedMediaType`, `request.is_json`); flag endpoints that parse whatever arrives.

**References:** OWASP REST Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html, CWE-436 Interpretation Conflict
