---
categories: [cloud-network, security-practices]
domains: [backend, infrastructure]
---

# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, cutting shortest chains first.

**Why:** Findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep `cartography`, `bloodhound`, `attack_path` reports, reachability graph exports.

**References:** MITRE ATT&CK, NIST SP 800-30, BloodHound docs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
