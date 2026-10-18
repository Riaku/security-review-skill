# Input Validation

**MUST** Validate all external input against type, length, range, and format allowlists at the trust boundary.

**Why:** Downstream code assumes validated data; one unchecked field becomes the injection vector.

**Detect:** Handlers reading `request.params`/body straight into logic; missing pydantic/Zod/Joi or `@Valid`.

**References:** OWASP A03:2021, CWE-20, OWASP Input Validation Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
