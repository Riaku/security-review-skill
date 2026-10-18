---
categories: [regulatory-frameworks]
domains: [government-compliance]
---

# CJIS (criminal justice data)

**MUST** apply CJIS Security Policy controls—advanced authentication, audit logging, and personnel screening—to every system touching Criminal Justice Information.

**Why:** Fingerprints, rap sheets, and criminal records flowing through unhardened systems expose sensitive justice data and disqualify agency access entirely.

**Detect:** grep for "CJIS", "ORI", "CHRI" markers; missing MFA, absent audit trails, unencrypted backup media in CJIS-scoped repos.

**References:** CJIS Security Policy v5.9, FBI CJIS Division, NIST SP 800-53

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
