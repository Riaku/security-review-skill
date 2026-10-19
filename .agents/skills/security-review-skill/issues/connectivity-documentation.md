---
categories: [cloud-network]
domains: [infrastructure]
---

# Connectivity Documentation

**MUST** document every inbound, outbound and internal connection of the system, and review that map whenever topology changes.

**Why:** An undocumented connection is an unreviewed trust path; nobody can firewall, monitor or decommission a link that is not on the map.

**Detect:** Diff the documented connectivity matrix against flow logs or egress NetworkPolicy rules; unlisted flows are gaps.

**References:** NCSC Definitive Architecture View, https://www.ncsc.gov.uk/collection/operational-technology/definitive-architecture-view
