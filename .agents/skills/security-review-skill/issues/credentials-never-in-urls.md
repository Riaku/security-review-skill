---
categories: [secrets-crypto]
domains: [backend, frontend]
---

# Credentials Never in URLs

**MUST NOT** place credentials, API keys, reset tokens, or session identifiers in URL paths, query strings, or fragments.

**Why:** URLs are copied into access logs, browser history, Referer headers, proxy caches and shell history, so a URL-borne secret spreads to systems you never authorized.

**Detect:** grep for `?token=`, `?api_key=`, `?access_token=`, `?password=`, and route definitions that take a secret in a path segment

**References:** OWASP Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html, CWE-598 Use of GET Request Method With Sensitive Query Strings
