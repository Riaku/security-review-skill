---
categories: [containers-k8s]
domains: [infrastructure]
---

# Multi-Stage Builds

**MUST** build images with multi-stage Dockerfiles so compilers, headers, and build caches never ship in the final stage.

**Why:** Single-stage images carry toolchains that widen the attack surface and make CVE triage impossible against runtime-only needs.

**Detect:** Dockerfile lacking a second `FROM` line; `gcc`, `make`, `-dev` packages or `/root/.cache` present in final image layers.

**References:** CIS Docker Benchmark (image build), NIST SP 800-190 4.2

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
