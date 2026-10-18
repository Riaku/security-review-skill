---
categories: [third-party-integrations]
domains: [backend]
---

# Backing Services as Attached Resources

**SHOULD** access every backing service (database, queue, cache, SMTP) through an environment-supplied location and credential so the specific provider or instance can be swapped without code changes.

**Why:** Hardcoded provider hostnames and instance identifiers block credential rotation, block moving to a managed or failover instance, and leak internal topology into the repo. A compromise of one provider instance becomes a code-change emergency instead of a config swap.

**Detect:** grep code for hardcoded connection strings, provider URLs, and instance IDs instead of injected bindings; verify a staging deploy can point at a different provider instance with config only.

**References:** 12factor.net/backing-services, OWASP Docker Top 10 (D-04 secrets), CWE-798 hardcoded credentials
