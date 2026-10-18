# Raft Consensus

**MUST** run Raft clusters with an odd number of voters (3, 5) and mutually authenticated, TLS-encrypted peer transport.

**Why:** An even voter count cannot form a quorum after one failure; unauthenticated peers allow a rogue node to hijack the log.

**Detect:** grep raft config for `peers=` count, `raft.enable-tls=false`, missing `--peer-urls=https`, single-node `bootstrap` left in production manifests.

**References:** Raft paper (Ongaro), HashiCorp Raft security guide, CWE-300 Channel Endpoint Verify

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
