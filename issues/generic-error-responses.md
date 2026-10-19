---
categories: [web-api-security]
domains: [backend]
---

# Generic Error Responses

**MUST** return a generic, user-safe error body to clients and keep stack traces, paths, and query fragments in server-side logs only.

**Why:** Stack traces, internal hostnames, and SQL fragments in a response hand an attacker the map of the system for free.

**Detect:** grep response builders for `str(e)`, `traceback.format_exc`, `err.Error()`, `e.getMessage()` serialized into the body, and default framework debug pages reachable in production.

**References:** OWASP Error Handling Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
