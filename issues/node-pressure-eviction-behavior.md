---
categories: [containers-k8s]
domains: [infrastructure]
---

# Node Disk/Memory Pressure Eviction Behavior Understood

**SHOULD** document and test how kubelet evicts pods under DiskPressure/MemoryPressure, ordering QoS classes and PDBs correctly.

**Why:** Unexpected eviction ordering can kill stateful or critical pods first, turning a disk-full event into a data-loss outage.

**Detect:** No eviction-threshold config in kubelet; no alerts on `nodefs.available`/`memory.available`; QoS classes unset on critical workloads.

**References:** K8s docs eviction, kubelet resource-pressure evictions, CWE-770, SRE Workbook capacity practices
