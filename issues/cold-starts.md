---
categories: [scaling-capacity]
domains: [reliability]
---

# Cold Starts

**MUST** bound cold-start latency (provision plus warm-up) below the client timeout for every scale-from-zero or lazily-loaded path.

**Why:** A cold instance that initializes slower than the caller's timeout drops the very requests that triggered the scale-up, amplifying the surge.

**Detect:** grep for `minReplicas: 0`, `scaleDownDelaySecondsAfterFinish`, initContainer warm-up steps, `timeoutSeconds` in client config; compare recorded cold-start timings against those timeouts.

**References:** AWS Well-Architected REL11-BP03, CWE-400, Google SRE scaling practices

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
