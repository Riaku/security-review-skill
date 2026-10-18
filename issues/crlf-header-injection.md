# CRLF / HTTP Header Injection & Response Splitting

**SHOULD NOT** Put user input into headers or redirect targets without rejecting CR/LF and `%0d%0a`.

**Why:** Injected line breaks forge headers or a whole second response, poisoning caches and sessions.

**Detect:** `set_header(..., user_value)`, `Location:`/`Set-Cookie` built from params without CRLF filtering.

**References:** CWE-113, CWE-93, PortSwigger HTTP Response Splitting

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
