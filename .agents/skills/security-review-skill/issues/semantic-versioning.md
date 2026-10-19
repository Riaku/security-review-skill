---
categories: [deployment-release]
domains: [infrastructure]
---

# Semantic Versioning

**MUST** bump major versions for breaking API changes rather than shipping them under a minor tag that consumers assume is safe to auto-upgrade.

**Why:** Dependabot and floating tags auto-adopt a "minor" release that breaks contracts, silently propagating incompatibility across every dependent service.

**Detect:** grep changelogs/tags for `MAJOR`/`MINOR` bumps against diffed public API signatures; check `package.json`/`Cargo.toml` for `^` ranges crossing breaking releases.

**References:** semver.org spec items 7-9, OWASP dependency management, CWE-1265 incorrect version semantics
