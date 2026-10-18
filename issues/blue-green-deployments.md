# Blue-Green Deployments

**SHOULD** keep the idle environment patched and drained of live secrets, with automated cutover health gates before traffic shifts.

**Why:** A stale standby environment becomes an unmonitored foothold, and a premature cutover routes users onto unverified code mid-incident.

**Detect:** grep switch scripts for missing health-check gates before service/ingress selector flips; compare standby image tags against the live CVE-patched baseline.

**References:** NIST SP 800-190, AWS Blue/Green deployment guidance, CWE-1188 insecure default initialization

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
