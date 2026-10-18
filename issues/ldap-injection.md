# LDAP Injection

**MUST** Escape `* ( ) \` and NUL in values interpolated into LDAP filters; prefer parameterized libraries or strict allowlists.

**Why:** Unescaped input rewrites filter logic, bypassing authentication or dumping directory entries.

**Detect:** String-built `(&(uid=%s)...)` filters; `search(` with concatenated user values; missing `ldap_escape`.

**References:** CWE-90, OWASP A03:2021, OWASP LDAP Injection Prevention Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
