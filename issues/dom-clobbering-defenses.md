---
categories: [web-client-security]
domains: [frontend]
---

# DOM Clobbering Defenses

**MUST NOT** depend on global names, implicit element identifiers, or untyped DOM property access; declare variables explicitly and read values through typed accessors.

**Why:** Markup injection can shadow a global the script trusts, so a config object becomes an attacker-chosen element and a check silently reads the wrong value.

**Detect:** grep for bare global reads (`if (config)`, `window.<id>`), `document.forms[name]` lookups, and `id`/`name` attributes that collide with script globals.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, OWASP WSTG: Testing for DOM Clobbering
