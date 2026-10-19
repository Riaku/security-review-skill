---
categories: [web-api-security]
domains: [backend]
---

# Abstraction Escape Hatches

**MUST** review the raw and escape-hatch APIs of every ORM, query builder, and template engine for untrusted input, since the abstraction does not sanitize them.

**Why:** Injection reappears wherever input reaches concatenated raw SQL, literal fragments, or template escape-hatch calls, and the layer itself ships its own vulnerabilities.

**Detect:** grep for `raw(`, `Raw(`, `.literal(`, `createQuery(`, `execute(`, `|safe`, `Markup(` receiving request data.

**References:** OWASP WSTG: ORM injection, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/, CWE-89 (SQL Injection)
