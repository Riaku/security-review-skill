---
categories: [sre-incidents]
domains: [reliability]
---

# Single Points of Failure

**SHOULD NOT** let one component — a DNS record, a credential, one box — gate the whole service path.

**Why:** Every unreplicated dependency concentrates failure so one fault takes everything down at once.

**Detect:** one-instance StatefulSets, single `CNAME` targets, solo admin accounts, `replicas: 1`, single-node etcd/Redis without sentinel.

**References:** NIST SP 800-34, AWS Well-Architected, Google SRE Book, CWE-1049
