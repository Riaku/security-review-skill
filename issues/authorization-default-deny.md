---
categories: [authorization-access-control]
domains: [backend]
---

# Authorization Default Deny

**MUST** deny by default: an unmatched rule, missing role, or empty policy resolves to refusal, never to allow.

**Why:** Default-allow turns every forgotten rule into an open door, and an unloaded or empty permission set is the most common way that happens.

**Detect:** grep policy functions whose fall-through returns `True`/`allow`, `if not denied` guards, and permission lookups where `None` or `[]` is treated as unrestricted.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html, OWASP Zero Trust Architecture Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html
