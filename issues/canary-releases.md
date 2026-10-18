# Canary Releases

**SHOULD** gate canary traffic expansion on error-rate and latency SLOs with automatic rollback, never on a fixed timer alone.

**Why:** A timer-driven rollout spreads a defect to the whole fleet before anyone notices, turning a small blast radius into a full outage.

**Detect:** grep Argo Rollouts/Flagger configs for `canary.steps` without `analysis`/`metrics` blocks, missing `maxTraffic` error thresholds, or `abortScaleDownDelaySeconds` absent.

**References:** Google SRE Book canarying, NIST SP 800-190, AWS CodeDeploy canary guards, CWE-1095 lifecycle defect

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
