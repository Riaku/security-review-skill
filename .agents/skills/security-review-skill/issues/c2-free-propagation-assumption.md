---
categories: [supply-chain]
domains: [backend]
---

# C2-Free Propagation Assumption

**SHOULD** design containment and detection assuming compromised code propagates without command-and-control, through local credentials and package registries.

**Why:** A worm that reads its own package and republishes it needs no egress channel, so network blocks and C2 signatures miss it entirely.

**Detect:** the containment runbook: if egress filtering is the only propagation control, the assumption is wrong

**References:** Shai-Hulud 2.0 npm worm analysis (2025)
