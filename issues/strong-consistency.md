# Strong Consistency

**MUST** route linearizable reads and writes through the consensus quorum, never bypassing it with direct node access for critical paths.

**Why:** A client reading a non-quorum node sees stale committed state, breaking invariants that strong consistency was purchased to guarantee.

**Detect:** grep for direct `:2379`/`:8500` single-node endpoints, `consistency=eventual` on critical reads, admin ports exposed without auth in ingress.

**References:** etcd consistency docs, Jepsen test reports, NIST SP 800-53 SC-8

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
