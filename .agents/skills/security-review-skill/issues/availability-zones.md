---
categories: [sre-incidents]
domains: [reliability]
---

# Availability Zones

**MUST** spread replicas across at least two availability zones — three for N+1 with quorum — and size each surviving zone to carry peak load, so one zone's failure cannot drop the service below minimum capacity.

**Why:** All replicas in one zone means a datacenter event takes down 100% of capacity despite looking available.

**Detect:** `topologySpreadConstraints`, `podAntiAffinity` on zone topology, ASG `VPCZoneIdentifier` with one subnet.

**References:** AWS Well-Architected reliability pillar, K8s topology docs, NIST SP 800-34
