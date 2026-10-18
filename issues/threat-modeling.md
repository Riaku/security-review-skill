---
categories: [security-practices]
domains: [backend]
---

# Threat Modeling

**MUST** produce a threat model (STRIDE or attack-tree) for every new service before its first production deploy, reviewed with the owning team.

**Why:** Unmodeled trust boundaries ship as real intrusions — attackers exploit the paths nobody drew.

**Detect:** files `docs/threat-model/`, `threat-model.md`, `stride` keywords in PR templates, `threat_model` CI gate

**References:** OWASP Threat Dragon, NIST SP 800-181, OWASP ASVS V1.2

---

**Part of:** [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
