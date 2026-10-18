---
categories: [containers-k8s]
domains: [infrastructure]
---

# Non-Root Containers

**MUST NOT** run container processes as UID 0; every image declares a `USER` with a numeric non-zero ID.

**Why:** Root inside a container that escapes or mounts host paths becomes root on the node, bypassing most isolation assumptions.

**Detect:** `USER root`, missing `USER` directive in Dockerfile; runtime `id -u` equals 0; `runAsNonRoot: false` in pod specs.

**References:** CIS Docker 4.1, CIS K8s 5.2.6, CWE-250, OWASP K8s PSA runAsNonRoot

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
