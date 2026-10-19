---
categories: [authorization-access-control]
domains: [backend]
---

# Account Graph Blast Radius

**MUST** authorize every feature that links accounts, because one compromised account inherits access through those edges.

**Why:** Family graphs, shared workspaces and org directories turn a single account takeover into access to everyone adjacent to it. The edge is an authorization decision.

**Detect:** Inspect linking features (invites, shared folders, org membership): each edge is authorized on both sides and revocable.

**References:** arXiv:2502.04303, https://arxiv.org/abs/2502.04303
