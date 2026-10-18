# SQL Injection

**MUST** Use parameterized queries or bound variables; never concatenate user input into SQL.

**Why:** Concatenated input lets attackers rewrite query logic to dump or destroy data.

**Detect:** `execute(` with f-strings, `%` formatting, or `+`/`||` concatenation of request values.

**References:** OWASP A03:2021, CWE-89, OWASP SQL Injection Prevention Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
