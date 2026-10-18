---
categories: [scaling-capacity]
domains: [reliability]
---

# OOM Killer

**SHOULD** set explicit memory requests/limits and OOM-score priorities so the kernel evicts disposable workers before critical stateful processes.

**Why:** With unbounded memory, the OOM killer picks by size, not importance — it will happily terminate the database while the leaking cache survives.

**Detect:** grep manifests for `resources.limits.memory`, `oom_score_adj`, and dmesg/journal for `Out of memory: Killed process`; flag containers with no limit or critical services at default scores.

**References:** CWE-400, Kubernetes QoS docs, NIST SP 800-184, kernel OOM protection (oom_score_adj)
