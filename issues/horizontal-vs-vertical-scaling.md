---
categories: [scaling-capacity]
domains: [reliability]
---

# Horizontal vs Vertical Scaling

**SHOULD** prefer horizontal scaling for stateless tiers and reserve vertical scaling for stateful components, documenting each datastore's single-node ceiling.

**Why:** Vertical-only growth creates a single point of failure and a hard wall that arrives mid-incident with no headroom to add replicas.

**Detect:** grep manifests for `replicas: 1`, `resources.limits` near node capacity, `nodeSelector` pinning; check stateful services for a documented max-node-size plan.

**References:** NIST SP 800-184, AWS Well-Architected REL05-BP02, CWE-400

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
