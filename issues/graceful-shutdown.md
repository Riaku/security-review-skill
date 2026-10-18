---
categories: [sre-incidents]
domains: [reliability]
---

# Graceful Shutdown

**MUST** trap SIGTERM, stop accepting new work, finish in-flight requests, then exit before the kill deadline.

**Why:** Hard-killed workers drop committed-but-unsent transactions and half-written jobs, producing data loss users blame on the service.

**Detect:** `terminationGracePeriodSeconds`, `SIGTERM` handler absent, `preStop` hook missing, `kill -9` in stop scripts.

**References:** Kubernetes termination docs, CWE-227, Google SRE Book
