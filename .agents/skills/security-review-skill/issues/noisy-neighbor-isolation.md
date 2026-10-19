---
categories: [containers-k8s, multi-tenancy, scaling-capacity]
domains: [infrastructure, reliability]
---

# Noisy-neighbor isolation between tenants/workloads

**MUST** enforce per-tenant or per-workload resource quotas (CPU, memory, I/O, connection rate) so one tenant's burst cannot degrade others sharing the host.
**SHOULD** apply ResourceQuota and LimitRange to every tenant namespace so one team cannot consume the whole cluster's compute.

**Why:** Without isolation, a single abusive or misbehaving tenant saturates shared CPU, disk I/O, or network, violating SLAs for everyone co-located, and a runaway or malicious workload in an unbounded namespace exhausts shared CPU/memory, degrading every other namespace on the cluster.

**Detect:** grep for `ResourceQuota`, `LimitRange`, `CPUShares`/`cpu_weight`, `blkio`/`IOClass`, per-tenant `rate_limit` in gateway config; flag shared pools with no per-tenant caps, namespaces with no `ResourceQuota`/`LimitRange` objects, and tenant namespaces sharing unbounded node pools.

**References:** CWE-770, Kubernetes QoS/ResourceQuota docs, CIS K8s 5.2.1, K8s quotas/limitranges docs, NIST SP 800-190 5.3
