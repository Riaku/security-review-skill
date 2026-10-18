---
categories: [authorization-access-control, cloud-network]
domains: [backend, infrastructure]
---

# Cloud Privilege-Escalation Paths (cross-role/cross-account escalation graph reviewed)

**SHOULD** periodically compute the role-to-role and cross-account escalation graph, pruning every path from low privilege to admin.

**Why:** Individually reasonable grants compose into escalation ladders (create-role, assume-role, modify-trust) no single-policy review catches.

**Detect:** run pmapper `analyze`, cloudsplaining cross-account reports; grep trust policies for `"AWS": "*"`.

**References:** AWS IAM Access Analyzer, NIST SP 800-53 AC-3/AC-6, CWE-269, Cloudsplaining, Azure AD escalation analysis

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
