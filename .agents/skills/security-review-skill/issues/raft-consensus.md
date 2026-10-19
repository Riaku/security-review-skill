---
categories: [distributed-systems]
domains: [data]
---

# Raft Consensus

**MUST** run Raft clusters with an odd number of voters (3, 5) and mutually authenticated, TLS-encrypted peer transport.

**Why:** An even voter count wastes failure budget — with 4 voters quorum is 3, so a single failure leaves no further tolerance; an odd count maximizes fault tolerance per node. Unauthenticated peers allow a rogue node to hijack the log.

**Detect:** grep raft config for voter count, missing `--listen-peer-urls=https://`/`--initial-advertise-peer-urls=https://`, missing `--peer-client-cert-auth`/`--peer-cert-file`, single-node `bootstrap` left in production manifests.

**References:** Raft paper (Ongaro), HashiCorp Raft security guide, CWE-300
