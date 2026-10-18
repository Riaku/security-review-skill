---
categories: [containers-k8s, hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# CIS Docker Benchmark

**MUST** align container host and daemon configuration with the current CIS Docker Benchmark sections 2 (daemon) and 5 (runtime), including `daemon.json` settings, before production deployment.

**Why:** Unhardened Docker defaults expose the socket, permissive logging, and root containers that turn one compromised image into full host takeover.

**Detect:** grep daemon.json for `userns-remap`, `log-driver`, `live-restore`; check `/var/run/docker.sock` permissions and `--privileged` in compose files.

**References:** CIS Docker Benchmark v1.6.0, CIS Controls v8, NIST SP 800-190

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [government-compliance](../domains/government-compliance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
