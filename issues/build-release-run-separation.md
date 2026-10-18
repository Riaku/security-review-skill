---
categories: [deployment-release]
domains: [infrastructure]
---

# Strict Build / Release / Run Separation

**MUST NOT** rebuild per environment: build once, compose config into a versioned release, and promote the identical digest-pinned artifact from staging to production.

**Why:** A per-environment rebuild means the binary that passed staging review is not the binary running in production, silently breaking the review-to-deployment trust chain. Non-promoted builds also make rollbacks unreliable and provenance unverifiable.

**Detect:** CI jobs that build separately per environment; `:latest` tags used across environments; config compiled at build time instead of injected at release time; production digests that cannot be traced to the reviewed staging digest.

**References:** 12factor.net/build-release-run, SLSA Build L2+ provenance, OpenSSF artifact promotion guidance

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
