---
categories: [containers-k8s, sre-incidents]
domains: [infrastructure, reliability]
---

# Liveness vs Readiness Probes

**SHOULD NOT** wire dependency checks (DB, cache) into the liveness probe; reserve them for readiness only.

**Why:** Liveness failures kill pods during a downstream outage, turning a slowdown into a cluster-wide crash loop and thundering restart storm.

**Detect:** `livenessProbe` with `exec: pg_isready`/DB query, identical liveness and readiness endpoints, `initialDelaySeconds: 0`.

**References:** Kubernetes probe docs, CWE-770, Google SRE Workbook
