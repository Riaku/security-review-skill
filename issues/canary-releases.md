---
categories: [deployment-release]
domains: [infrastructure]
---

# Canary Releases

**SHOULD** gate canary traffic expansion on error-rate and latency SLOs with automatic rollback, never on a fixed timer alone.

**Why:** A timer-driven rollout spreads a defect to the whole fleet before anyone notices, turning a small blast radius into a full outage.

**Detect:** grep Argo Rollouts configs for `canary.steps` without an `analysis` step/`analysisTemplates` and for `trafficRouting` without metric-based abort; grep Flagger for `analysis.maxWeight`/`stepWeight` without `threshold` and without `metrics[].thresholdRange`.

**References:** Google SRE Book canarying, NIST SP 800-190, AWS CodeDeploy canary guards, CWE-1095 lifecycle defect
