---
categories: [observability]
domains: [infrastructure]
---

# Security Telemetry Access Control

**MUST** restrict security telemetry, network maps, and policy exports to dedicated administrator accounts, since they describe where the valuable assets are.

**Why:** The map of the defences is reconnaissance: policy stores reveal which accounts are worth compromising and monitoring data reveals what is watched.

**Detect:** kubectl auth can-i --list -n monitoring --as=<subject>; compare with the admin-only group that should be the sole reader.

**References:** NIST SP 800-207 §5.5, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 AC-6
