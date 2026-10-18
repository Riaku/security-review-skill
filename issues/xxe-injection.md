# XML External Entity (XXE) Injection

**MUST** Disable external entities and DTD processing in every XML parser (`resolve_entities=False`, secure processing features).

**Why:** Enabled external entities let crafted XML read local files and hit internal networks.

**Detect:** `lxml.etree.parse`, `DocumentBuilderFactory`, `XmlReader` without hardening flags; `DOCTYPE` accepted in inbound XML/SOAP/SVG.

**References:** CWE-611, OWASP A03:2021, OWASP XXE Prevention Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
