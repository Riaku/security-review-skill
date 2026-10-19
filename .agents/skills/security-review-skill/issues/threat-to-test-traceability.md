---
categories: [security-practices]
domains: [governance]
---

# Threat-to-Test Traceability

**MUST** map each identified threat to an attack-pattern identifier and to the requirement or test that would catch it.

**Why:** A threat list that stops at description produces no evidence anything was addressed. Linking each threat to a test closes the loop and exposes unmitigated rows.

**Detect:** Inspect the threat-model table: every row has a threat, an attack-pattern ID, a mitigation requirement and a verification artifact.

**References:** OWASP Cornucopia, https://cornucopia.owasp.org/about/
