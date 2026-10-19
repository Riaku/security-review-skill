---
categories: [security-practices]
domains: [governance]
---

# Threat Model From Code

**MUST** derive the threat model from the code and architecture definition and regenerate it in CI so the document cannot drift from the system.

**Why:** Hand-maintained models and annotation-based mitigation labels decay silently, so the document keeps claiming controls the code no longer implements.

**Detect:** git log -1 --format=%cd -- threatmodel/ compared with the last commit touching the described components; a stale regeneration date fails

**References:** OWASP pytm, https://github.com/OWASP/pytm
