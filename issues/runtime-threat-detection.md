---
categories: [containers-k8s, observability]
domains: [infrastructure, reliability]
---

# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, unnoticed inside otherwise "secure" images.

**Detect:** grep `falco`, `tracee`, `tetragon`, `ebpf` in DaemonSets/deployment YAML, custom `falco_rules.yaml` files.

**References:** MITRE ATT&CK container matrix T1610, CIS Docker/K8s Benchmarks 5.x, NIST SP 800-190

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
