# FedRAMP (Low/Moderate/High)

**MUST** map every cloud service consumed by the system to a FedRAMP authorization boundary at the impact level matching the data it processes, with inherited controls documented in the System Security Plan.

**Why:** Operating unauthorized cloud services inside a federal boundary voids the ATO and exposes agency data with no oversight.

**Detect:** grep IaC for AWS/Azure/GCP regions outside FedRAMP-authorized partitions; missing "fedramp", "boundary", "inherit" in compliance docs.

**References:** FedRAMP Rev5, NIST SP 800-53, FedRAMP Marketplace

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
