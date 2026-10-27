---
categories: [security-practices]
domains: [backend]
---

# Threat Modeling

**MUST** produce a threat model (STRIDE or attack-tree) for every new service before its first production deploy, reviewed with the owning team.

**Why:** Unmodeled trust boundaries ship as real intrusions — attackers exploit the paths nobody drew.

**Detect:** files `docs/threat-model/`, `threat-model.md`, `stride` keywords in PR templates, `threat_model` CI gate

**References:** OWASP A04:2021 Insecure Design, OWASP Threat Dragon, NIST SP 800-154, OWASP ASVS V1.2
