---
categories: [containers-k8s, scaling-capacity]
domains: [infrastructure, reliability]
---

# Noisy-neighbor isolation between tenants/workloads

**MUST** enforce per-tenant or per-workload resource quotas (CPU, memory, I/O, connection rate) so one tenant's burst cannot degrade others sharing the host.

**Why:** Without isolation, a single abusive or misbehaving tenant saturates shared CPU, disk I/O, or network, violating SLAs for everyone co-located.

**Detect:** grep for `ResourceQuota`, `LimitRange`, `CPUShares`/`cpu_weight`, `blkio`/`IOClass`, per-tenant `rate_limit` in gateway config; flag shared pools with no per-tenant caps.

**References:** OWASP ASVS 14.2, CWE-770, NIST SP 800-184 multi-tenancy, Kubernetes QoS/ResourceQuota docs

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [scaling-capacity](../categories/scaling-capacity.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
