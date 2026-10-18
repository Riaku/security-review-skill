# CSPM Continuous Cloud Posture Scanning (misconfig drift detected continuously)

**MUST** scan cloud configuration continuously for misconfigurations instead of relying on point-in-time audits.

**Why:** Public buckets, open security groups, and disabled logging appear between audits; attackers scan for them constantly.

**Detect:** grep for `prowler`, `scoutsuite`, `cloudsploit`, `checkov --framework cloud`, scheduled posture-scan jobs with alert routing.

**References:** NIST CS2 (SP 800-223), CIS Cloud Benchmarks, NIST SP 800-53 CM-6, CWE-16

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
