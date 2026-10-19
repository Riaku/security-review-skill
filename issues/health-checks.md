---
categories: [sre-incidents]
domains: [reliability]
---

# Health Checks

**MUST** expose an authenticated-or-network-restricted health endpoint that verifies dependencies rather than just process liveness.

**Why:** A process that answers while its database is dead passes naive checks and keeps serving broken responses to users.

**Detect:** `GET /healthz`, `/health`, `HEALTHCHECK` in Dockerfiles, `readinessProbe` hitting only static 200 or checking process liveness instead of dependencies, and the inverse error of a `livenessProbe` wired to a DB/cache check — dependency checks in liveness kill pods during a downstream outage.

**References:** Kubernetes health checks, K8s docs, CWE-770, SRE Book
