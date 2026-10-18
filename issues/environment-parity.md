# Environment Parity

**SHOULD** keep dev, staging, and production identical in runtime versions, TLS termination, and network policy so defects surface before prod.

**Why:** Bugs that only exist under production's real configuration — stricter TLS, real auth, actual latency — ship invisible and get discovered by customers.

**Detect:** diff `helm values-*.yaml` across environments for divergent image tags, ingress TLS settings, networkPolicy presence, and connection-pool sizes.

**References:** 12-Factor process parity, NIST SP 800-53 CM-6 configuration settings, Etsy continuous deployment lessons

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
