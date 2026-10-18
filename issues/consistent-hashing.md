# Consistent Hashing

**SHOULD** use virtual nodes (replicas per physical node) so key distribution stays balanced and node churn moves only a fraction of keys.

**Why:** Without virtual nodes, adding or removing a server remaps a disproportionate key share, triggering hotspots and mass cache-miss storms.

**Detect:** grep hash ring code for `vnodes`/`virtual_nodes` count near 1, plain `hash(key) % node_count` (breaks on scale), missing bounded-load or rendezvous hashing.

**References:** Karger consistent hashing paper, Cassandra vnodes docs, NIST SP 800-190 §4.5

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
