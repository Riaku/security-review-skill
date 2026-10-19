---
categories: [authorization-access-control, resilience]
domains: [backend, reliability]
---

# Authorization Service Degraded Mode

**MUST** design the central authorization service for failure with replication and a documented degraded mode stating what remains allowed and for how long.

**Why:** A security component on every request path without an availability story converts its own outage into a total outage, or into an undocumented allow-all.

**Detect:** read the runbook section for the authorization service and check it states replica count, failure detection, and the exact behaviour (allow, deny, cache) during an outage.

**References:** NIST SP 800-207 §5.2, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 CP-2
