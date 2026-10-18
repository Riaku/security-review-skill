---
categories: [deployment-release, resilience]
domains: [infrastructure, reliability]
---

# Startup Dependency Ordering

**MUST** have services retry with backoff until backends (DB, cache, queues) are reachable, rather than crash-on-first-failure at boot.

**Why:** A pod that dies because the database was seconds from ready enters CrashLoopBackOff, cascading restarts across the fleet during every rolling deploy.

**Detect:** grep readiness/liveness probes and init containers for backend-wait logic; check app boot for missing retry/backoff on connection errors and `initContainers` gating startup.

**References:** Kubernetes init containers & probes docs, AWS retry/backoff patterns, CWE-756 missing custom error handling, resilience4j patterns

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [resilience](../categories/resilience.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
